# 06 — Language & framework comparison

The side-by-side. Everything here was observed while building this repo, not copied from a
blog post — each row has code in the tree you can go and read.

---

## Part 1 — the languages

### Hash maps

| | Python | TypeScript | PHP |
|---|---|---|---|
| Type | `dict` | `Map` | `array` |
| Keys | any hashable | any value (SameValueZero) | `int` \| `string` only |
| Numeric keys | stay numbers | stay numbers *in a `Map`* | stay integers |
| Missing key | `KeyError` / `.get(k, d)` | `undefined` / `.get(k) ?? d` | notice / `$a[$k] ?? $d` |
| Ordered | yes (3.7+) | yes | yes |
| Counting helper | `collections.Counter` | — (write the loop) | `array_count_values` (scalars only) |

**The JavaScript trap.** An object literal is not a hash map. Its keys are coerced to strings,
so `0` and `"0"` and `-0` collide, and `"constructor"` hits `Object.prototype`. Use `Map`.
`packages/core-ts/src/arrays-and-hashing/two-sum.ts` has the comment.

**Composite keys** split the three differently again — and the two that cannot use one directly
are blocked for opposite reasons:

| | A 26-element tally as a map key | Why |
|---|---|---|
| Python | `tuple(counts)` — **used directly** | tuples are hashable and hash *by value* |
| TypeScript | must serialise (`counts.join(",")`) | `Map` keys are too permissive — any object, compared by *reference* |
| PHP | must serialise (`implode(',', $counts)`) | array keys are too restrictive — `int\|string` only |

Getting it wrong in TypeScript is silent: `new Map().set([1,2], "a").get([1,2])` is `undefined`.
See [Group Anagrams](problems/0049-group-anagrams.md).

### Strings

| | Python | TypeScript | PHP |
|---|---|---|---|
| Unit | code point | UTF-16 code unit | **byte** |
| Length | `len(s)` ✓ | `s.length` ⚠️ surrogate pairs count as 2 | `strlen` ✗ / `mb_strlen` ✓ |
| Iterate | `for c in s` ✓ | `for (const c of s)` ✓ / `s.split("")` ✗ | `mb_str_split` ✓ / `str_split` ✗ |
| Sort characters | `sorted(s)` | `[...s].sort()` | `mb_str_split` then `sort` |

This is the biggest practical difference of the three and it bites on every string problem.
The Valid Anagram contract carries the case `{"s": "héllo", "t": "olléh"}` specifically to
catch it — a naive `strlen`/`str_split` PHP implementation fails it, and the other two pass.

### Numbers

| | Python | TypeScript | PHP |
|---|---|---|---|
| Integers | arbitrary precision | IEEE 754 double; safe to 2⁵³−1 | 64-bit; **silently becomes float on overflow** |
| Integer division | `//` | `Math.floor(a / b)` | `intdiv()` |
| A float used as an index | `TypeError` | silently `undefined` | truncated + deprecation notice |
| Signed zero | none — `0` is `0` | **`-0` exists**; `-0 === 0` but `Object.is` differs | none |
| Default sort | numeric | **lexicographic** — `[10,9].sort()` → `[10,9]` | numeric |
| Big values | native | `BigInt` | `bcmath` / `gmp` |

Negative zero is the one people have not usually met. `1 * 0 * -3` is `-0`, `-0 === 0` is
`true`, and `JSON.stringify(-0)` is `"0"` — so it is invisible over the wire and invisible to
every ordinary comparison, but a structural deep-equal sees it. It broke exactly one of the
three implementations of [Product of Array Except Self](problems/0238-product-of-array-except-self.md).

`[10, 9, 1].sort()` returning `[1, 10, 9]` is the JavaScript bug everyone writes once. Always
`sort((a, b) => a - b)`.

### Immutability

| | Python | TypeScript | PHP |
|---|---|---|---|
| Frozen value object | `@dataclass(frozen=True, slots=True)` | `interface` with `readonly` | `final readonly class` |
| Enforced | runtime | **compile time only** | runtime |
| Immutable sequence | `tuple` | `readonly T[]` (compile time) | — |

TypeScript's `readonly` disappears at runtime. A cast, a JSON round-trip, or any untyped
boundary and it is gone. Python and PHP actually enforce theirs.

### "Not found"

| | Python | TypeScript | PHP |
|---|---|---|---|
| Absent value | `None` | `undefined` *and* `null` | `null` |
| Falsy trap | `0`, `""`, `[]` are falsy | `0`, `""`, `NaN` are falsy | `0`, `""`, `"0"`, `[]` are falsy |
| Safe default | `d.get(k, 0)` | `m.get(k) ?? 0` | `$a[$k] ?? 0` |

Use `??` in TypeScript, never `||` — `||` swallows a legitimate `0`. PHP's `"0"` being falsy is
its own special hazard.

### Error handling

| | Python | TypeScript | PHP |
|---|---|---|---|
| Base | `Exception` | `Error` | `Exception` / `RuntimeException` |
| Custom class | trivial | needs `Object.setPrototypeOf` | trivial |
| Checked | no | no | no |

Extending `Error` in TypeScript breaks `instanceof` under downlevelling unless you restore the
prototype in the constructor. Every core error class here does. `packages/core-ts/src/errors.ts`.

### Standard library reach

| Task | Python | TypeScript | PHP |
|------|--------|------------|-----|
| Count | `Counter` | hand-rolled | `array_count_values` |
| Heap | `heapq` | hand-rolled | `SplMinHeap` |
| Deque | `collections.deque` | hand-rolled | `SplQueue` |
| Binary search | `bisect` | hand-rolled | hand-rolled |
| Combinatorics | `itertools` | hand-rolled | hand-rolled |

Python wins this comfortably. In an algorithms repo it is the difference between a three-line
solution and a twenty-line one, and it is the reason the three implementations of the same
problem often look least alike here.

---

## Part 2 — the frameworks

### Registration / discovery

| | FastAPI | NestJS | Laravel |
|---|---|---|---|
| Mechanism | `pkgutil.walk_packages` at import | explicit barrel array | class-string array in config |
| Cost per problem | nothing | one import line | one array entry |
| Verified at compile time | no | **yes** | no |
| Freezable at deploy | no | bundler tree-shakes | **`config:cache`** |
| Fails how | silently, on a typo | compile error | container error at boot |

### Dependency injection

| | FastAPI | NestJS | Laravel |
|---|---|---|---|
| Mechanism | `Depends(callable)` per parameter | constructor injection from decorator metadata | container autowiring from type hints |
| Registration needed | none | provider listed in a module | none (or a `singleton` binding) |
| Resolved | per request | at boot (graph), per scope | per resolution |
| Parameterised deps | factory returning a closure | pipe/provider constructed per route | explicit call |
| Wiring mistakes surface | first request | **boot** | first resolution |

NestJS is the most ceremonious and catches the most at boot. Laravel is the most automatic —
type-hint and it appears — which is lovely until you need to know *where* something came from.
FastAPI sits between: explicit at the call site, no registry anywhere.

### Request validation

| | FastAPI | NestJS | Laravel |
|---|---|---|---|
| Tool | Pydantic model | `class-validator` DTO | FormRequest |
| Declared as | type annotations | decorators | rule strings |
| Parses or checks? | **parses** | checks an already-parsed object | checks raw input |
| Coerces `"7"` → `7` | yes, unless `StrictInt` | no | **yes**, under `integer` |
| Rejects unknown fields | `extra="forbid"` | `forbidNonWhitelisted` | ✗ — silently dropped |
| Empty string is valid | yes | yes | ✗ under `required` — use `present` |
| Default failure status | **422** | **400** | 422 (JSON) / 302 (HTML) |
| Editor autocompletion | full | full | none (rules are strings) |

Three genuinely different philosophies. Pydantic *parses* — it turns unknown input into a
typed object. `class-validator` *checks* — the object already exists. Laravel *inspects raw
input with a string DSL*, which buys enormous flexibility (cross-field rules, conditional
rules, database-aware rules) and costs all compile-time safety.

Every one of the three was adjusted to make them agree. See the table in [AGENTS.md](../AGENTS.md).

### Errors → status codes

| | FastAPI | NestJS | Laravel |
|---|---|---|---|
| Where | `@app.exception_handler` | `@Catch()` filter | `withExceptions` in `bootstrap/app.php` |
| Default POST success | **200** | **201** | 200 |
| Default validation failure | 422 | 400 | 422 JSON / 302 HTML |
| JSON by default | yes | yes | **only if the client asks** |

The NestJS `201` and the Laravel HTML-by-default are both one-line fixes, and both are the
kind of thing you only discover by running the same request against all three.

### API documentation

| | FastAPI | NestJS | Laravel |
|---|---|---|---|
| OpenAPI | **free** | `@nestjs/swagger` + `@ApiProperty` on every field | third-party package |
| Swagger UI | `/docs` | `/docs` after setup | — |
| Source of truth | the Pydantic model | duplicated decorators | — |

FastAPI's strongest single argument. The model *is* the schema; there is nothing to keep in
sync. NestJS needs a parallel set of decorators that can silently drift from the validation
decorators beside them.

### Testing

| | FastAPI | NestJS | Laravel |
|---|---|---|---|
| Runner | pytest | Jest (Vitest for the lib) | PHPUnit |
| In-process HTTP | `TestClient(app)` | `supertest(app.getHttpServer())` | `$this->postJson()` |
| Data-driven cases | `@pytest.mark.parametrize` | `it.each` | `#[DataProvider]` |
| Named cases | ✅ ids | ✅ `$name` interpolation | ✅ yielded keys |
| Boots the real app | ✅ via the factory | ✅ via the factory | ✅ always |

All three can drive the real application in-process with no network. The ergonomics of
data-driven tests are closest between pytest and Jest; PHPUnit's provider must be `static` and
runs **before** the framework boots, which is exactly why `ContractRepository` being
framework-free matters — `tests/Support/ContractCases.php` cannot use the container.

---

## Part 2.5 — what the benchmarks actually showed

Every solve response carries `elapsedMicros` — time inside the algorithm only. Nine problems
in, three results were worth more than the theory that predicted them.

### A JIT beats an interpreter at tight loops, by a lot

Contains Duplicate and Product of Array Except Self, both brute force, n = 3000 (µs):

| | Python | TypeScript | PHP |
|---|---|---|---|
| contains-duplicate O(n²) | 69,810 | **1,312** | 29,438 |
| product-except-self O(n²) | 114,482 | **5,825** | 61,020 |

TypeScript is 20–53× faster than Python on a tight nested numeric loop, and ~5× faster than
PHP. The gap narrows to roughly 8× on the linear versions, where there is far less loop body to
optimise. If your hot path is a hand-written loop over numbers, this is the single largest
performance difference in the repo.

### The better complexity does not always win

Two cases where the O(n) approach **lost** to the O(n log n) one on a realistic input:

| Problem | n | O(n log n) | O(n) | Why |
|---|---|---|---|---|
| Longest Consecutive (Python) | 3000 | **124** | 129 | `sorted()` runs in C; the set walk runs in the interpreter |
| Top K Frequent (all three) | 3000 | **44 / 59 / 60** | 260 / 137 / 77 | 3001 buckets allocated for 200 distinct values |

Neither is a rounding error — Top K's bucket sort is 6× slower in Python. Both are the same
lesson from opposite directions: asymptotics describe growth, not cost, and the constant factor
is where the language shows up.

### Same complexity, different constant

Valid Sudoku is O(1) either way — the board is always 81 cells:

| | Python | TypeScript | PHP |
|---|---|---|---|
| three-pass | 17 | 11 | 16 |
| single-pass | **7** | **8** | **7** |

A consistent 2×, purely from reading each cell once instead of three times. "Same complexity"
and "same speed" are different claims.

---

## Part 3 — the scoreboard

Opinionated, and only about this repo's use case.

| | Python / FastAPI | TypeScript / NestJS | PHP / Laravel |
|---|---|---|---|
| Expressing an algorithm | **★★★** stdlib does the work | ★★ | ★★ |
| Type safety at the boundary | ★★★ Pydantic parses | ★★★ compile + runtime | ★ rule strings |
| Type safety inside | ★★ mypy is opt-in | **★★★** | ★★ |
| Lines of ceremony per endpoint | **★★★** fewest | ★ most | ★★ |
| API docs | **★★★** free | ★★ decorators | ★ none |
| Catching wiring mistakes early | ★ first request | **★★★** boot | ★★ |
| Batteries included | ★★ | ★★ | **★★★** |
| Surprising defaults | ★★★ few | ★★ 201, 400 | ★ four separate ones |

**If you want one takeaway:** FastAPI gets an endpoint right with the least code and gives you
documentation for nothing. NestJS makes structural mistakes impossible to ship but charges you
four files per feature. Laravel has the most built in and the most defaults that are wrong for
a JSON API — every one fixable in a line, but you have to know.

---

## Where to look in the code

| Concept | Python | TypeScript | PHP |
|---|---|---|---|
| Registry | `core-python/src/neetcode_core/registry.py` | `core-ts/src/registry.ts` | `core-php/src/Registry/ProblemRegistry.php` |
| Contract loader | `contracts.py` | `contracts.ts` | `Contracts/ContractRepository.php` |
| Domain errors | `errors.py` | `errors.ts` | `Exceptions/` |
| Error → status | `exception_handlers.py` | `common/filters/domain-exception.filter.ts` | `bootstrap/app.php` |
| Request validation | `problems/two_sum/schemas.py` | `problems/two-sum/dto/` | `Problems/TwoSum/TwoSumRequest.php` |
| DI | `dependencies.py` | `*.module.ts` | `Providers/NeetCodeServiceProvider.php` |
| Timing | `timing.py` | `common/timing.ts` | `Support/Timing.php` |
