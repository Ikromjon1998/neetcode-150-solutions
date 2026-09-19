# `neetcode/core` (PHP)

The algorithms, and nothing else. **No Laravel, no `Illuminate\*`, no HTTP** — the only
dependency is `ext-json`.

## Use

```php
use NeetCode\Core\Registry\ProblemRegistry;
use NeetCode\Core\ArraysAndHashing\TwoSum;

$registry = ProblemRegistry::default();

$solve = $registry->solution('two-sum', 'hash-map');
$solve([2, 7, 11, 15], 9);                  // [0, 1]

$registry->solution('two-sum');              // the contract's default approach
TwoSum::hashMap([2, 7, 11, 15], 9);          // or call the method directly
```

Inside the Laravel app, type-hint `ProblemRegistry` and the container resolves the singleton
bound by `NeetCodeServiceProvider`.

## Layout

```
src/
  Contracts/
    ProblemDefinition.php    the interface a problem class implements
    ContractRepository.php   loads packages/contracts/problems/*.json
  Exceptions/                NoSolutionException & friends
  Support/
    Difficulty.php Topic.php        backed enums
    Approach.php   ProblemMeta.php  readonly classes
  Registry/
    DefaultProblems.php      the explicit class list
    ProblemRegistry.php      built from an injectable list
  ArraysAndHashing/
    TwoSum.php  ValidAnagram.php
tests/                       contract-driven, no hand-written fixtures
```

## How registration works

A problem class implements `ProblemDefinition` and returns its approaches as first-class
callables:

```php
public static function solutions(): array
{
    return [
        'brute-force' => self::bruteForce(...),
        'hash-map'    => self::hashMap(...),
    ];
}
```

`DefaultProblems::all()` is the explicit list; the Laravel app publishes it as
`config/neetcode.php`, which is what lets `php artisan config:cache` freeze the whole registry
into one compiled array at deploy time. Attributes plus reflection would have been the
"clever" answer and would have given exactly that up.

## Strings are byte arrays

`strlen("héllo")` is 6, not 5. `str_split` cuts multi-byte characters in half. **Every string
problem in this package uses `mb_strlen` / `mb_str_split`.** It is the single biggest
difference between this code and its Python and TypeScript siblings.

## Test

```bash
composer install
./vendor/bin/phpunit
./vendor/bin/phpunit --filter=TwoSum
```
