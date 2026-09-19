# `neetcode-api` — Python / FastAPI

The Python application. It owns HTTP, validation and serialisation; it owns **no algorithms**
— those come from [`packages/core-python`](../../packages/core-python).

## Run

```bash
make run-python                 # from the repo root, http://localhost:8000
```

Then open <http://localhost:8000/docs> for the generated Swagger UI.

## Endpoints

| Method | Path                   | Purpose                                      |
|--------|------------------------|----------------------------------------------|
| GET    | `/health`              | Liveness + how many problems are registered  |
| GET    | `/problems`            | Catalog of every solved problem              |
| GET    | `/problems/{slug}`     | Metadata for one problem                     |
| POST   | `/problems/two-sum` | `?approach=brute-force\|hash-map` |
| POST   | `/problems/valid-anagram` | `?approach=sorting\|hash-map` |
| POST   | `/problems/contains-duplicate` | `?approach=brute-force\|sorting\|hash-set` |
| POST   | `/problems/valid-sudoku` | `?approach=three-pass\|single-pass` |
| POST   | `/problems/group-anagrams` | `?approach=sorted-key\|count-key` |
| POST   | `/problems/longest-consecutive-sequence` | `?approach=sorting\|hash-set` |
| POST   | `/problems/product-of-array-except-self` | `?approach=brute-force\|prefix-suffix` |
| POST   | `/problems/encode-and-decode-strings` | `?approach=length-prefixed\|delimiter-escaped` |
| POST   | `/problems/top-k-frequent-elements` | `?approach=sorting\|bucket-sort` |
| GET    | `/docs`, `/openapi.json` | Swagger UI and the OpenAPI schema          |

```bash
curl -s localhost:8000/problems/two-sum \
  -H 'content-type: application/json' \
  -d '{"nums":[2,7,11,15],"target":9}' | jq
```

## Layout

```
src/neetcode_api/
  main.py                application factory + lifespan (fails boot on registry drift)
  config.py              pydantic-settings, env-driven
  dependencies.py        Depends() providers, incl. ?approach= validation
  timing.py              stopwatch around the algorithm call only
  exception_handlers.py  the ONE place domain errors become status codes
  schemas/common.py      the response envelope shared with the NestJS and Laravel apps
  routers/
    health.py
    catalog.py           derived from the registry — never edited when adding a problem
  problems/
    __init__.py          pkgutil auto-registration of problem routers
    two_sum/
      router.py          HTTP surface
      schemas.py         request DTO (StrictInt — see the file for why)
      service.py         the seam between HTTP and the algorithm
tests/
  test_health_and_catalog.py
  test_two_sum.py        contract-driven; mirrors the NestJS and Laravel suites exactly
```

## Adding a problem

Don't do it by hand:

```bash
make new-problem SLUG=valid-anagram
```

The generator writes `problems/<slug>/{router,schemas,service}.py` plus the test file. Because
`problems/__init__.py` discovers routers with `pkgutil`, **you never edit `main.py`**.

## Test

```bash
make test-python        # from the repo root (core + api)
pytest                  # from this directory
pytest -k two_sum -v
```

## Notes specific to this stack

- **OpenAPI is free.** The Pydantic models *are* the schema. NestJS needs `@nestjs/swagger`
  decorators to match; Laravel needs a third-party package.
- **422, not 400.** FastAPI's default for a body validation failure. The other two apps were
  reconfigured to match — see [`docs/06-language-comparison.md`](../../docs/06-language-comparison.md).
- **`Depends` injects by call signature**, not by a type registry. There is no container and
  no module graph; a dependency is just a callable. Compare with NestJS constructor injection
  and Laravel's autowiring container.
- **`extra="forbid"`** on request models: an unrecognised field is a 422, not a shrug.
