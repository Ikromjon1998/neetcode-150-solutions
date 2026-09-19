# 07 — Testing strategy

## Red by default

`make test` fails on a fresh clone. Every algorithm is an unsolved stub raising `UnsolvedError`,
and the six suites are the specification you implement against.

Two consequences worth stating:

- **You never write a test.** The cases live in the contracts; solving a problem means making
  existing tests pass.
- **CI cannot just run `make test`.** It runs two jobs instead: one asserting every live file is
  still a stub (`solutions.py status --assert-stubs`), and one applying the reference answers
  and requiring all six suites green (`make verify-solutions`).

## The problem this solves

Three implementations of the same algorithm drift. Not dramatically — one of them quietly
handles the empty input differently, or returns `[1, 0]` where the others return `[0, 1]`, and
nothing notices because each has its own hand-written test file.

So the test cases do not live in the test files. They live in one JSON file per problem, and
six suites read it.

```
packages/contracts/problems/0001-two-sum.json
        │
        ├──► packages/core-python/tests/…        pytest            ┐
        ├──► packages/core-ts/tests/…            vitest            │ the algorithm
        ├──► packages/core-php/tests/…           phpunit           ┘
        │
        ├──► apps/api-python/tests/…             pytest + TestClient   ┐
        ├──► apps/api-node/test/…                jest + supertest      │ the HTTP layer
        └──► apps/api-php/tests/Feature/…        phpunit + Laravel     ┘
```

Add a case to the JSON and six suites tighten at once. There is no way to make a Python test
pass by weakening it, because the case is in a file the other five also read.

## The contract's three sections

```jsonc
{
  "cases":           [{ "name": "...", "input": {...}, "expected": [0, 1] }],
  "validationCases": [{ "name": "...", "input": {...}, "status": 422 }],
  "notFoundCases":   [{ "name": "...", "input": {...} }]
}
```

| Section | What it asserts | Core suites | App suites |
|---------|-----------------|-------------|------------|
| `cases` | correct answer | ✅ every approach | ✅ every approach, over HTTP |
| `validationCases` | malformed input is rejected | ✖ | ✅ status + `error.type` |
| `notFoundCases` | valid input with no answer | ✅ raises | ✅ 404 |

`validationCases` are deliberately absent from the core suites. Validation belongs to the
framework; the algorithm is entitled to assume it was called correctly.

## Four kinds of test, and what each one is for

### 1. Correctness — every case × every approach

```python
@pytest.mark.parametrize("approach", APPROACHES)
@pytest.mark.parametrize("case", contract_cases(SLUG))
def test_solves_every_contract_case(approach: str, case: dict) -> None:
    solve = get_solution(SLUG, approach=approach)
    assert solve(case["input"]["nums"], case["input"]["target"]) == case["expected"]
```

Two approaches × six cases is twelve individually-named tests, from four lines.

### 2. Differential — the approaches must agree

```python
def test_all_approaches_agree(case: dict) -> None:
    results = {a: get_solution(SLUG, approach=a)(...) for a in APPROACHES}
    assert len(set(map(tuple, results.values()))) == 1, results
```

This is what makes adding an approach cheap. A new implementation is automatically compared
against the ones you already trust, on every case — you get a regression suite for free.

### 3. Registry guards — they scale with the repo

`test_registry.py`, `registry.test.ts` and `ProblemRegistryTest.php` run against **every**
problem in the package:

- contracts and implementations agree (`verify_registry()`)
- exactly one default approach per problem
- the default resolves without an explicit key
- unknown slugs and unknown approach keys raise the right error, with the available keys
  listed

Problem 150 is checked by exactly the same tests as problem 1, and you write none of them.

### 4. Cross-language coverage — `make test-contracts`

The one thing no single test suite can catch: an approach declared in the contract and
implemented in only one language. `tools/validate_contracts.py` reads each core package's
source and checks the registered approach keys against the contract, in all three.

It also enforces the housekeeping: filename matches `{id:04d}-{slug}`, ids and slugs are
unique, kebab-case everywhere, exactly one default, and no `TODO` or `O(?)` left behind.

## App-level tests boot the real application

Not a mock. Not a partially-configured test harness. The real thing, in-process:

| App | How |
|-----|-----|
| FastAPI | `TestClient(create_app())` — the same factory `main.py` uses |
| NestJS | `createApp({ logger: false })` — the same factory `main.ts` uses |
| Laravel | `Tests\TestCase` boots the framework as configured |

That means the real validation pipe, the real exception filter, the real middleware. A test
that configures its own pipeline is a test that can pass while production is broken — and the
`ConvertEmptyStringsToNull` bug documented in [05](05-php-laravel.md) would have slipped
through exactly that gap.

## The PHPUnit wrinkle worth knowing

PHPUnit calls data providers **before** the Laravel application boots, so
`app(ContractRepository::class)` is not available in one. `tests/Support/ContractCases.php`
instantiates `ContractRepository` directly — which is only possible because the core package
is framework-free.

A small thing, but it is the clearest demonstration of why the layering earns its keep.

## Where the contracts get found

All three loaders resolve the directory the same way:

1. `$NEETCODE_CONTRACTS_DIR` if set
2. otherwise walk up the tree looking for `packages/contracts/problems`

The starting point differs by language for reasons worth knowing:

| | Starts from | Why |
|---|---|---|
| Python | `__file__` | reliable |
| TypeScript | `process.cwd()` | `import.meta.url` is ESM-only and this compiles to CJS for NestJS |
| PHP | `__DIR__`, then `getcwd()` | Composer installs the package as a symlink into `vendor/` |

## Running things

```bash
make test               # all six suites (red until you solve things)
make test-python        # or -node / -php
make test-contracts     # validity + cross-language coverage
make verify-solutions   # apply every reference answer, run everything, restore

cd packages/core-python && pytest -k two_sum -v
npx vitest --root packages/core-ts                     # watch mode
cd apps/api-php && php artisan test --filter=TwoSum
```

## What is deliberately not tested

- **`elapsedMicros` values.** Asserted to be an integer, never compared. Timing assertions are
  the classic flaky test.
- **Generated OpenAPI schema contents.** One test asserts the path exists; pinning the whole
  document would break on every framework upgrade for no benefit.
- **The algorithms' internals.** Only inputs and outputs. That is what lets you rewrite an
  approach without touching a test.

## Current state

With the reference answers applied (`make verify-solutions`):

```
python: core  249    python: api  199
node:   core  250    node:   api  199
php:    core  250    php:    api  198
                                 ─────
                                 1,345
```

Without them — the state of a fresh clone — essentially all of those fail, which is the
exercise.

From nine problems, and you hand-write none of it. The count grows with
`cases × approaches × 6 suites`, so one problem with three approaches and nine cases adds over
200 assertions on its own.
