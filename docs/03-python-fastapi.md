# 03 — Python & FastAPI

## The library: `packages/core-python`

Zero runtime dependencies. Not "few" — zero. The whole package is stdlib.

```
src/neetcode_core/
  __init__.py       public surface; apps import from here, never from submodules
  types.py          ProblemMeta, Approach, Difficulty, Topic
  errors.py         NoSolutionError and friends
  contracts.py      loads packages/contracts/problems/*.json
  registry.py       @solution decorator + pkgutil auto-discovery
  arrays_and_hashing/
    two_sum.py
    valid_anagram.py
```

### Registration by decorator

```python
from neetcode_core.registry import solution

SLUG = "two-sum"

@solution(SLUG, approach="hash-map")
def two_sum_hash_map(nums: list[int], target: int) -> list[int]:
    ...
```

The decorator registers the function as a **side effect of importing the module**, then
returns it unchanged — so it is still an ordinary callable you can import and test directly.

`discover()` walks the package with `pkgutil.walk_packages` and imports every submodule, which
is what makes the decorator fire. Net effect: **drop a file into a topic folder and it appears
in the API.** No registration step at all.

The cost is real and worth naming: a typo in a filename registers nothing and fails silently,
and the import-time scan touches the filesystem. `verify_registry()` catches the first problem
by cross-checking against the contracts, and the app calls it at startup.

### `StrEnum` for the vocabularies

```python
class Difficulty(StrEnum):
    EASY = "easy"
```

`StrEnum` (3.11+) members *are* strings, so `Difficulty.EASY == "easy"` is True and JSON
serialisation needs no encoder. The PHP backed enum is the closest equivalent; TypeScript's
string-literal union is the same idea but vanishes at runtime.

### `@dataclass(frozen=True, slots=True)`

`frozen` gives immutability; `slots` drops the per-instance `__dict__`, which matters once
there are 150 of these in memory. PHP's `readonly class` is the direct analogue. TypeScript's
`readonly` is compile-time only — nothing stops a cast.

---

## The app: `apps/api-python`

```
src/neetcode_api/
  main.py                application factory + lifespan
  config.py              pydantic-settings
  dependencies.py        Depends() providers
  timing.py              perf_counter_ns around the algorithm only
  http_status.py         the one status code we pin by hand
  exception_handlers.py  domain errors → HTTP statuses
  schemas/common.py      the shared response envelope
  routers/
    health.py
    catalog.py
  problems/
    __init__.py          pkgutil auto-registration of routers
    two_sum/
      router.py  schemas.py  service.py
```

### The application factory

```python
def create_app(settings: Settings | None = None) -> FastAPI:
    app = FastAPI(..., lifespan=lifespan)
    register_exception_handlers(app)
    app.include_router(health.router)
    app.include_router(catalog.router)
    for router in all_routers():          # discovered, not listed
        app.include_router(router)
    return app
```

A factory rather than a module-level `app = FastAPI()` so tests can build an isolated instance
with overridden settings. `TestClient(create_app())` then exercises the real routing, the real
validation and the real exception handlers.

### Lifespan: fail the boot, not the request

```python
@asynccontextmanager
async def lifespan(_: FastAPI):
    discover()
    verify_registry()      # raises if a contract declares an unimplemented approach
    yield
```

A container that cannot serve correct answers should never pass its readiness check. The
NestJS and Laravel apps do the same thing at their own boot points.

### `Depends` is not a container

This is the biggest conceptual difference from the other two frameworks. FastAPI resolves
dependencies by **call signature**, not from a type registry:

```python
async def solve_two_sum(
    payload: TwoSumRequest,
    approach: Annotated[str, Depends(approach_provider(SLUG))],
    service: Annotated[TwoSumService, Depends(TwoSumService)],
) -> SolveResponse[list[int]]:
```

There is no module graph and nothing to register. A dependency is just a callable; passing the
class `TwoSumService` means "call it with no arguments per request".

Because dependencies are ordinary callables, a *factory returning a closure* is the natural
way to parameterise one per route — `approach_provider(SLUG)` bakes in the slug and validates
the query parameter against that problem's keys only.

### The trap: `from __future__ import annotations`

`apps/api-python/src/neetcode_api/dependencies.py` deliberately does **not** have that import,
and there is a comment saying so. Here is why.

That import makes every annotation a string, evaluated lazily. FastAPI must evaluate the
`Annotated[str, Query(...)]` inside `approach_provider` to build the OpenAPI schema — and by
then, `Query` and `available` are locals of a function that has already returned. Pydantic
raises:

```
PydanticUserError: `TypeAdapter[...]` is not fully defined
```

**Deferred annotations and dependency factories do not mix.** Every other file in the app has
the import; that one must not.

### `StrictInt`, not `int`

```python
nums: list[StrictInt] = Field(min_length=2)
target: StrictInt
```

In its default lax mode Pydantic coerces the JSON string `"7"` to `7`. `class-validator`'s
`@IsInt()` in the NestJS app rejects it. Being strict at the API boundary is both better
practice and what keeps the three apps agreeing. Same reasoning for `extra="forbid"`, which
makes a typo'd field name a 422 rather than a silent no-op.

### What FastAPI gives you for free

`/docs` and `/openapi.json`, generated from the Pydantic models. No decorators, no
configuration. The NestJS app needs `@nestjs/swagger` plus an `@ApiProperty` on every DTO
field to reach the same place; the Laravel app has no equivalent without a third-party
package. If API documentation matters to you, this is FastAPI's single strongest argument.

---

## Commands

```bash
make run-python                      # uvicorn --reload on :8000
make test-python                     # core + api
cd packages/core-python && pytest -k two_sum -v
cd packages/core-python && mypy      # strict mode
ruff check packages/core-python apps/api-python
```

## Idioms worth copying

| Want | Use |
|------|-----|
| Count elements | `collections.Counter` |
| Default-valued dict | `collections.defaultdict(list)` |
| Deque / sliding window | `collections.deque` |
| Heap | `heapq` (min-heap; negate for a max-heap) |
| Binary search | `bisect.bisect_left` / `insort` |
| Pairwise iteration | `itertools.pairwise` |
| Cached pure function | `functools.cache` |
| Index while looping | `enumerate(xs)` — never `range(len(xs))` |
| Two sequences together | `zip(xs, ys, strict=True)` |

`strict=True` on `zip` is a 3.10+ addition worth the habit: without it, `zip` silently stops at
the shorter input, which is a class of bug neither TypeScript nor PHP will let you write as
easily.
