# 01 — Architecture

## Exercises, not answers

Every algorithm in `packages/core-*` ships as a stub:

```python
@solution(SLUG, approach="hash-map")
def two_sum_hash_map(nums: list[int], target: int) -> list[int]:
    """One-pass hash map — target: O(n) time, O(n) space.

    Trade space for time: remember every value seen so far and look up the complement in O(1).
    """
    raise UnsolvedError(SLUG, "hash-map", PATH)
```

The registration, the signature and the docstring are fixed; the body is yours. The docstring
is generated from the contract's approach entry, so it states what to build and what it must
cost, never how.

Everything downstream still works while it is a stub — the problem appears in `GET /problems`,
the request DTO still validates, the route still exists. Only the call into the algorithm
fails, and it fails as a **501** carrying the path of the file to edit. Reference answers live
under `solutions/` and reach the tree only via `make solution`.

## The one decision everything else follows from

**Algorithms are a library. Frameworks are delivery.**

```
                  packages/contracts/problems/*.json
                   metadata + test cases, one file per problem
                                    │
        ┌───────────────────────────┼───────────────────────────┐
        │                           │                           │
  core-python                    core-ts                    core-php
  neetcode_core                @neetcode/core              neetcode/core
  ── zero runtime deps ──   ── zero runtime deps ──   ── zero runtime deps ──
        │                           │                           │
        ▼                           ▼                           ▼
   api-python                   api-node                    api-php
    FastAPI                      NestJS                      Laravel
   :8000                        :3000                       :8080
```

A core package may not import a framework. Not FastAPI, not `@nestjs/common`, not
`Illuminate\*`. It has no notion of a request, a response, or a status code.

Three things fall out of that:

1. **The algorithms are testable in isolation.** `pytest packages/core-python` needs no server
   and no fixtures. A failure is a failure in the algorithm, full stop.
2. **The frameworks are swappable.** Replacing FastAPI with Litestar would not touch a single
   line of algorithm code.
3. **The comparison is honest.** When the three apps differ, the difference is genuinely the
   framework's — the algorithm underneath is the same shape in all three.

## Layers

### Layer 1 — contracts (`packages/contracts`)

JSON. No code. One file per problem, holding both the metadata (title, difficulty, topic,
approaches and their complexities) and the test cases.

Six test suites read it. That is what keeps three languages honest: you cannot fix a Python
bug by weakening a Python test, because the case lives in a file the other five suites also
read. See [07 — Testing strategy](07-testing-strategy.md).

### Layer 2 — core packages

Each is a real, installable package — not a folder of loose files:

| | Package name | Import as | Installed by |
|---|---|---|---|
| Python | `neetcode-core` | `neetcode_core` | `pip install -e` (hatchling) |
| TypeScript | `@neetcode/core` | `@neetcode/core` | npm workspace |
| PHP | `neetcode/core` | `NeetCode\Core\` | Composer path repository |

Each contains: typed value objects (`ProblemMeta`, `Approach`, `Difficulty`, `Topic`), domain
exceptions, a contract loader, a registry, and one module per problem.

### Layer 3 — applications

Each app owns exactly what a framework is for:

- routing
- request validation and deserialisation
- dependency injection
- mapping domain errors onto HTTP status codes
- serialisation and API documentation

And nothing else. The controller for Two Sum is about forty lines, of which the algorithm is
one: `getSolution(SLUG, approach)`.

## The three registries — deliberately different

Every app has to answer "how do I find the solutions?". Each language answers it the way its
ecosystem actually would, and comparing them is half the point of this repo.

| | Mechanism | Adding a problem costs | What it buys | What it costs |
|---|---|---|---|---|
| **Python** | `@solution` decorator + `pkgutil.walk_packages` | nothing | drop a file in, it appears | import-time filesystem scan; a typo'd filename silently registers nothing |
| **TypeScript** | explicit barrel in `registry.ts` | one import line | tree-shaking, compile-time verification, works in a browser bundle | you must remember the line (the generator writes it) |
| **PHP** | class-string array in `config/neetcode.php` | one array entry | `php artisan config:cache` freezes it at deploy; nothing is instantiated until used | same manual step, plus a layer of indirection |

None is best. Python's is the least ceremony and the most magic; TypeScript's is the most
statically verifiable; PHP's is the most deployment-friendly. They are three reasonable
answers to identical requirements, which is exactly why having all three side by side is
worth more than picking one.

## Request flow

The same request through all three, at the same level of detail:

```
POST /problems/two-sum?approach=hash-map
{"nums":[2,7,11,15],"target":9}
```

### FastAPI

```
Starlette router
  → TwoSumRequest              Pydantic model, StrictInt, extra="forbid"
  → Depends(approach_provider) closure validating ?approach=
  → Depends(TwoSumService)     per-request instance
  → get_solution(...)          registry lookup
  → timed(...)                 perf_counter_ns around the algorithm only
  → SolveResponse              Pydantic model, serialised by alias
```

### NestJS

```
Express router
  → ValidationPipe             global; whitelist + forbidNonWhitelisted + 422
  → TwoSumRequestDto           class-validator decorators
  → ApproachPipe(SLUG)         per-route pipe instance
  → TwoSumService              constructor-injected singleton
  → getSolution(...)
  → timed(...)                 process.hrtime.bigint()
  → SolveResponseDto           plain object; Swagger schema from decorators
```

### Laravel

```
Illuminate router
  → TwoSumRequest              FormRequest; resolved and validated before the controller runs
  → resolveApproach()          explicit check against the registry
  → ProblemRegistry            container-autowired singleton
  → ->solution(...)
  → Timing::measure()          hrtime(true)
  → SolveResponse::make()      JsonResponse factory
```

Same five steps every time. The differences are in *where the framework puts the seam*, and
that is what [06 — Comparison](06-language-comparison.md) is about.

## Error handling — one translation site per app

Core packages throw `NoSolutionError` / `NoSolutionException`. They do not know 404 exists.
Each app maps domain errors to statuses in exactly one file:

| App | File |
|-----|------|
| FastAPI | `src/neetcode_api/exception_handlers.py` |
| NestJS | `src/common/filters/domain-exception.filter.ts` |
| Laravel | `bootstrap/app.php` → `withExceptions(...)` |

| Situation | Status | `error.type` |
|-----------|--------|--------------|
| Body fails validation | 422 | `validation_error` |
| Unknown `?approach=` | 422 | `unknown_approach` |
| Unknown problem slug | 404 | `unknown_problem` |
| Valid input, no answer exists | 404 | `no_solution` |
| Approach is still an unsolved stub | 501 | `not_implemented` |

The ordering matters and is worth checking after any change: a malformed body must 422 *before*
the stub is ever called, so an unsolved exercise never masks a validation bug. All three apps
were verified to agree on this — `invalid=422, unknown-approach=422, unsolved=501`.

Two of those three frameworks had to be reconfigured to agree. NestJS returns 400 for
validation by default; Laravel returns HTML unless the client asks for JSON, converts empty
strings to null before validation, and rejects `""` under `required`. Each workaround is
commented at the site where it lives.

## Why `elapsedMicros` is in the response

Every solve response carries the wall-clock time spent *inside the algorithm* — not routing,
not validation, not serialisation. It makes two comparisons possible without any tooling:

- **Approach vs. approach** within one language. Run `?approach=brute-force` against
  `?approach=hash-map` on a large input and watch the asymptotics show up.
- **Language vs. language** on the same input. Treat the absolute numbers with suspicion
  (JIT warm-up, GC timing, interpreter startup) but the ratios are informative.

Each app measures with a monotonic, nanosecond-resolution clock —
`time.perf_counter_ns()`, `process.hrtime.bigint()`, `hrtime(true)` — because the alternatives
(`time()`, `Date.now()`, `microtime()`) do not have the resolution to see an O(n) pass over a
six-element list.
