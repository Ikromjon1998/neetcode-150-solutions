# 05 — PHP & Laravel

## The library: `packages/core-php`

Zero runtime dependencies beyond `ext-json`. No Laravel, no `Illuminate\*`, no HTTP.

```
src/
  Contracts/
    ProblemDefinition.php   the interface a problem class implements
    ContractRepository.php  loads packages/contracts/problems/*.json
  Exceptions/               NoSolutionException and friends
  Support/
    Difficulty.php  Topic.php     backed enums
    Approach.php    ProblemMeta.php  readonly classes
  Registry/
    DefaultProblems.php     the explicit class list
    ProblemRegistry.php     built from an injectable list
  ArraysAndHashing/
    TwoSum.php  ValidAnagram.php
```

### Registration is an interface plus a list

```php
final class TwoSum implements ProblemDefinition
{
    public const SLUG = 'two-sum';

    public static function slug(): string { return self::SLUG; }

    /** @return array<string, callable> */
    public static function solutions(): array
    {
        return [
            'brute-force' => self::bruteForce(...),
            'hash-map'    => self::hashMap(...),
        ];
    }
}
```

`self::bruteForce(...)` is PHP 8.1 **first-class callable syntax** — a `Closure` over the
method, not a `[self::class, 'method']` array. It is type-checked at compile time, and a
renamed method becomes an error instead of a runtime "method not found".

PHP has had attributes since 8.0 and they could have played the decorator's role. They were
not used, because reading them means reflecting over every candidate class — and
reflection-based discovery is precisely what `php artisan config:cache` exists to avoid. An
explicit interface plus an explicit list is faster *and* easier to follow.

### `readonly class`

```php
final readonly class Approach
{
    public function __construct(
        public string $key,
        public string $name,
        public string $time,
        public string $space,
        public ?string $note = null,
        public bool $isDefault = false,
    ) {}
}
```

Constructor property promotion plus `readonly` (8.2) is Python's `@dataclass(frozen=True)` in
one line — and unlike TypeScript's `readonly`, PHP enforces it at runtime.

### Backed enums

```php
enum Topic: string
{
    case ArraysAndHashing = 'arrays-and-hashing';
    ...
}
```

`Topic::from('arrays-and-hashing')` validates and throws on an unknown value; `->value` gets
the string back. Closest to Python's `StrEnum`, except PHP will not compare an enum to a bare
string — you must write `->value`, which catches a class of bug the Python version does not.

---

## The app: `apps/api-php`

A real `composer create-project laravel/laravel` install, not a hand-rolled skeleton.

```
app/
  Http/Controllers/
    HealthController.php  CatalogController.php
  Problems/                       ← feature modules, see below
    TwoSum/
      TwoSumController.php  TwoSumRequest.php
  Providers/NeetCodeServiceProvider.php
  Support/
    ApiError.php  SolveResponse.php  Timing.php
bootstrap/app.php                 routing + middleware + exception rendering
config/neetcode.php               the registered problem list
routes/api.php
tests/
  Feature/  Support/ContractCases.php
```

### `app/Problems/` instead of `app/Http/Controllers/`

PSR-4 maps `App\` to `app/`, so this needs no configuration. It keeps a feature's controller
and its FormRequest in one folder, which is the same shape as the NestJS module and the
FastAPI package — and this repo exists to compare like with like.

This is a mild deviation from the default Laravel layout and a common one in real codebases
once they outgrow a single `Controllers` directory.

### The service provider is the whole integration surface

```php
final class NeetCodeServiceProvider extends ServiceProvider
{
    public function register(): void
    {
        $this->app->singleton(ContractRepository::class, fn () =>
            new ContractRepository(config('neetcode.contracts_dir')));

        $this->app->singleton(ProblemRegistry::class, fn ($app) =>
            new ProblemRegistry(config('neetcode.problems', []),
                                $app->make(ContractRepository::class)));
    }

    public function boot(): void
    {
        $this->app->make(ProblemRegistry::class)->verify();   // fail the boot, not the request
    }
}
```

Singletons, so the contract JSON is parsed once per process rather than once per request.

After that, **every controller just type-hints `ProblemRegistry`** and the container resolves
it. No decorator, no module declaration, no `Depends()`. Of the three frameworks, Laravel's
injection is the most automatic — and correspondingly the least visible, which cuts both ways.

### `config/neetcode.php` and `config:cache`

```php
return [
    'problems'        => DefaultProblems::all(),
    'contracts_dir'   => env('NEETCODE_CONTRACTS_DIR'),
    'verify_on_boot'  => (bool) env('NEETCODE_VERIFY_ON_BOOT', true),
];
```

A plain array on purpose. `php artisan config:cache` compiles every config file into one
cached PHP array at deploy time, so a production request never scans a directory or reflects
over a class. FastAPI's `pkgutil` discovery is cheaper to write and cannot be frozen this way.

---

## The four Laravel defaults that fight a JSON API

Every one of these was hit while building this repo. All four are worked around in the code
with a comment at the site.

### 1. `required` rejects the empty string

```php
'nums' => ['required', 'array'],      // ✗ rejects []
's'    => ['required', 'string'],     // ✗ rejects ""
's'    => ['present', 'string'],      // ✓
```

`required` fails for `null`, `""`, `[]`, and empty Countables. Pydantic and `class-validator`
accept all of those for a declared field. The Valid Anagram case `{"s": "", "t": ""}` 422'd
here while returning 200 in the other two apps.

**Use `present`. Never `required`.** `present` means what you actually want: the key must be
in the payload.

### 2. `ConvertEmptyStringsToNull` mangles the body before validation

Laravel applies `TrimStrings` and `ConvertEmptyStringsToNull` to every request by default.
Both were designed for HTML form posts, where a blank text input and an absent one mean the
same thing. In a JSON API they do not — `{"s": ""}` arrives at your validator as
`{"s": null}`.

```php
// bootstrap/app.php
$middleware->remove([
    \Illuminate\Foundation\Http\Middleware\ConvertEmptyStringsToNull::class,
    \Illuminate\Foundation\Http\Middleware\TrimStrings::class,
]);
```

Neither Pydantic nor `class-validator` has any equivalent behaviour.

### 3. `$request->all()` merges the query string into the body

The unexpected-field check originally read `array_keys($this->all())` — and every request with
`?approach=hash-map` 422'd, because `approach` looked like an unexpected body field.

```php
$unexpected = array_diff(array_keys($this->json()->all()), ['nums', 'target']);
```

`json()` is the decoded body and nothing else.

### 4. `integer` accepts the numeric string `"7"`

Pydantic's `StrictInt` and `class-validator`'s `@IsInt()` both refuse it. Laravel's `integer`
rule does not, so the FormRequests do the check by hand:

```php
private function strictInteger(string $label): callable
{
    return static function (string $attribute, mixed $value, callable $fail) use ($label): void {
        if (! is_int($value)) {
            $fail("{$label} must be an integer.");
        }
    };
}
```

### Bonus: `validated()` key order follows rule evaluation

Not a bug, but it made the e2e tests fail on an exact-array comparison. The controllers rebuild
the echoed input explicitly (`['nums' => ..., 'target' => ...]`) rather than passing
`validated()` through — an API's key order should not depend on a validator's internals.

---

## Exception rendering

Laravel 11+ moved exception handling out of `app/Exceptions/Handler.php` and into
`bootstrap/app.php`:

```php
->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->shouldRenderJsonWhen(static fn (): bool => true);   // API-only app

    $exceptions->render(static fn (NoSolutionException $e) =>
        ApiError::make(404, 'no_solution', $e->detail, problem: $e->slug));
    ...
})
```

`shouldRenderJsonWhen(fn () => true)` matters: the default only renders JSON for `api/*` paths
or when the client sends `Accept: application/json`. Since the routes are mounted at the root
(`apiPrefix: ''`, so paths match the other two apps), a plain `curl` would otherwise get an
HTML error page.

The default `ValidationException` body is `{"message": ..., "errors": {...}}`; a render hook
flattens it into the shared `{"error": {"type", "message", "details"}}` envelope.

---

## Strings are byte arrays

The single largest difference between the PHP algorithms and their Python and TypeScript
siblings:

```php
strlen("héllo")        // 6  — bytes
mb_strlen("héllo")     // 5  — characters
str_split("héllo")     // splits the é in half
mb_str_split("héllo")  // correct
```

**Every string problem in this repo uses the `mb_*` family.** Python iterates code points
natively; JavaScript does too, provided you spread rather than `split("")`. PHP is the only
one of the three where the default is wrong, and the contract for Valid Anagram carries a
non-ASCII case specifically to catch it.

---

## Commands

```bash
make run-php                                  # php artisan serve on :8080
make test-php                                 # core + api
cd packages/core-php && ./vendor/bin/phpunit
cd apps/api-php && php artisan test
cd apps/api-php && php artisan route:list
cd apps/api-php && ./vendor/bin/pint          # style
```

## Idioms worth copying

| Want | Use |
|------|-----|
| Hash map | a plain `array` — integer keys stay integers |
| Default value | `$a[$k] ?? 0` — reads the key once, no notice |
| Count elements | `array_count_values()` for scalars |
| Stack / queue | `array_push`/`array_pop`; `SplQueue` for a real queue |
| Heap | `SplMinHeap` / `SplMaxHeap` / `SplPriorityQueue` |
| Fixed-size array | `SplFixedArray` when memory matters |
| Sort preserving keys | `asort` / `uasort` — `sort()` reindexes |
| Strict comparison | `===` always; `==` does type juggling |
| Iterate with index | `foreach ($xs as $i => $x)` |
| Callable from a method | `self::method(...)` (first-class callable, 8.1+) |
