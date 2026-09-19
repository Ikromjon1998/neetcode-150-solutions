# `neetcode/api-php` — PHP / Laravel

The Laravel application. It owns HTTP, validation and serialisation; it owns **no algorithms** —
those come from [`packages/core-php`](../../packages/core-php), wired in through a Composer
path repository.

## Run

```bash
make run-php         # from the repo root, http://localhost:8080
```

## Endpoints

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/health` | Liveness + how many problems are registered |
| GET | `/problems` | Catalog of every solved problem |
| GET | `/problems/{slug}` | Metadata for one problem |
| POST | `/problems/two-sum` | `?approach=brute-force\|hash-map` |
| POST | `/problems/valid-anagram` | `?approach=sorting\|hash-map` |
| POST | `/problems/contains-duplicate` | `?approach=brute-force\|sorting\|hash-set` |
| POST | `/problems/valid-sudoku` | `?approach=three-pass\|single-pass` |
| POST | `/problems/group-anagrams` | `?approach=sorted-key\|count-key` |
| POST | `/problems/longest-consecutive-sequence` | `?approach=sorting\|hash-set` |
| POST | `/problems/product-of-array-except-self` | `?approach=brute-force\|prefix-suffix` |
| POST | `/problems/encode-and-decode-strings` | `?approach=length-prefixed\|delimiter-escaped` |
| POST | `/problems/top-k-frequent-elements` | `?approach=sorting\|bucket-sort` |

Routes are mounted with an **empty API prefix** (`apiPrefix: ''` in `bootstrap/app.php`) so the
paths match the FastAPI and NestJS apps byte for byte.

## Layout

```
app/
  Http/Controllers/     HealthController, CatalogController
  Problems/TwoSum/      TwoSumController, TwoSumRequest    ← feature modules
  Providers/NeetCodeServiceProvider.php   the whole integration surface
  Support/              ApiError, SolveResponse, Timing
bootstrap/app.php       routing + middleware + exception rendering
config/neetcode.php     the registered problem list
routes/api.php          concrete problem routes BEFORE /problems/{slug}
tests/
  Feature/              contract-driven HTTP tests
  Support/ContractCases.php   PHPUnit data providers
```

`app/Problems/` rather than `app/Http/Controllers/` keeps a feature's controller and request
object together — the same shape as the NestJS module and the FastAPI package. PSR-4 maps
`App\` to `app/`, so it needs no configuration.

## Adding a problem

```bash
make new-problem ARGS="--id 242 --slug valid-anagram ..."
```

The generator writes the controller and FormRequest, and inserts the route in `routes/api.php`
before the `{slug}` catch-all.

## Test

```bash
make test-php                 # core + api
php artisan test
php artisan test --filter=TwoSum
php artisan route:list
```

## The four Laravel defaults that fight a JSON API

All four are already worked around; each has a comment at the site. Full write-up in
[`docs/05-php-laravel.md`](../../docs/05-php-laravel.md).

1. **`required` rejects `""`, `[]` and `"0"`.** Use `present` in every FormRequest.
2. **`ConvertEmptyStringsToNull` rewrites the body before validation.** Removed, along with
   `TrimStrings`, in `bootstrap/app.php`.
3. **`$request->all()` merges the query string into the body.** Inspect `$request->json()->all()`.
4. **The `integer` rule accepts the string `"7"`.** Explicit `is_int` closures instead.

Plus: `validated()` key order follows rule evaluation, not declaration — the controllers
rebuild the echoed input explicitly.
