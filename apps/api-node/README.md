# `@neetcode/api-node` — TypeScript / NestJS

The NestJS application. It owns HTTP, validation and serialisation; it owns **no algorithms** —
those come from [`packages/core-ts`](../../packages/core-ts).

## Run

```bash
make run-node        # from the repo root, http://localhost:3000
```

Swagger UI at <http://localhost:3000/docs>, schema at `/openapi.json`.

## Endpoints

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/health` | Liveness + how many problems are registered |
| GET | `/problems` | Catalog of every solved problem |
| GET | `/problems/:slug` | Metadata for one problem |
| POST | `/problems/two-sum` | `?approach=brute-force\|hash-map` |
| POST | `/problems/valid-anagram` | `?approach=sorting\|hash-map` |
| POST | `/problems/contains-duplicate` | `?approach=brute-force\|sorting\|hash-set` |
| POST | `/problems/valid-sudoku` | `?approach=three-pass\|single-pass` |
| POST | `/problems/group-anagrams` | `?approach=sorted-key\|count-key` |
| POST | `/problems/longest-consecutive-sequence` | `?approach=sorting\|hash-set` |
| POST | `/problems/product-of-array-except-self` | `?approach=brute-force\|prefix-suffix` |
| POST | `/problems/encode-and-decode-strings` | `?approach=length-prefixed\|delimiter-escaped` |
| POST | `/problems/top-k-frequent-elements` | `?approach=sorting\|bucket-sort` |

## Layout

```
src/
  main.ts                      entrypoint
  app.factory.ts               builds the configured app — used by main AND the tests
  app.module.ts                root module (order matters: problems before catalog)
  common/
    dto/solve-response.dto.ts  the envelope shared with the FastAPI and Laravel apps
    filters/domain-exception.filter.ts   the ONE place errors become status codes
    pipes/approach.pipe.ts     validates ?approach= per route
    timing.ts                  hrtime around the algorithm only
  health/  catalog/
  problems/
    problems.module.ts         the explicit list of feature modules
    two-sum/
      two-sum.module.ts  two-sum.controller.ts  two-sum.service.ts
      dto/two-sum-request.dto.ts
test/
  setup.ts  *.e2e.spec.ts      boots the real app via createApp()
```

## Adding a problem

Don't do it by hand:

```bash
make new-problem ARGS="--id 242 --slug valid-anagram ..."
```

The generator writes the module, controller, service and DTO, and inserts the entry in
`problems.module.ts`.

## Test

```bash
make test-node                              # core + api
npm run test --workspace @neetcode/api-node # jest + supertest
```

## Notes specific to this stack

- **`@HttpCode(HttpStatus.OK)` on every solve endpoint.** Nest answers `POST` with 201 by
  default; FastAPI and Laravel answer 200.
- **`errorHttpStatusCode: 422`** on the global `ValidationPipe`. Nest defaults to 400.
- **DTOs are classes, not interfaces.** Both `class-validator` and `@nestjs/swagger` read
  runtime decorator metadata, and an interface leaves nothing behind.
- **`forbidNonWhitelisted: true`** — an unrecognised field is a 422, matching Pydantic's
  `extra="forbid"`.
- **No `paths` mapping to the core source.** It breaks `nest build`'s output layout. The app
  resolves `@neetcode/core` through the workspace symlink to `dist/`, so **build the core
  first**. Jest is the exception and maps to source for speed.
