# 04 — TypeScript & NestJS

## The library: `packages/core-ts`

Zero runtime dependencies. CommonJS output, because its consumer is NestJS — an ESM-only core
would be unrequirable from the app.

```
src/
  index.ts           public surface — the barrel
  types.ts           ProblemMeta, Approach, Difficulty, Topic, SolutionFn
  errors.ts          NoSolutionError and friends
  contracts.ts       loads packages/contracts/problems/*.json
  define-problem.ts  the `defineProblem` helper — and why it lives alone
  registry.ts        the explicit module list
  arrays-and-hashing/
    two-sum.ts
    valid-anagram.ts
```

### Registration is explicit, and that is the point

```typescript
// registry.ts
import { twoSum } from "./arrays-and-hashing/two-sum";
import { validAnagram } from "./arrays-and-hashing/valid-anagram";

const PROBLEM_MODULES: readonly ProblemModule[] = [twoSum, validAnagram];
```

One import line per problem — which the generator writes for you. In exchange:

- the bundler can tree-shake, so a consumer importing one algorithm does not pull in 150
- the type-checker verifies every entry really is a `ProblemModule`
- there is no filesystem access at import time, so this works in a browser bundle or a Lambda

Python's `pkgutil` discovery could do none of those things. Neither approach is better; they
are optimised for different deployment targets.

### `defineProblem` lives in its own file — here is the bug that put it there

The natural home for `defineProblem` is `registry.ts`. That creates a cycle: `registry.ts`
imports every problem module, and every problem module imports `defineProblem` from
`registry.ts`. At runtime it surfaces as:

```
TypeError: defineProblem is not a function
```

Node starts evaluating `registry.ts`, immediately hits `import ... from "./two-sum"`,
evaluates *that* file to completion — and at that moment `registry.ts` has not yet reached its
own `export function defineProblem`, so the binding is still in its temporal dead zone.

A leaf module with no imports of its own cannot participate in a cycle. That is the fix, and
`define-problem.ts` exists for no other reason.

Python tolerates the same pattern (it binds names lazily at attribute access) and PHP's
autoloader never sees it (classes load on first use). This is a JavaScript-shaped problem with
a JavaScript-shaped answer.

### `const` type parameters

```typescript
export function defineProblem<const T extends Readonly<Record<string, SolutionFn>>>(
  slug: string,
  solutions: T,
): { slug: string; solutions: T }
```

The `const` modifier (TS 5.0+) preserves the literal keys, so `twoSum.solutions["hash-map"]`
type-checks and `twoSum.solutions["hashmap"]` is a compile error. Without it the parameter
widens to `Record<string, SolutionFn>` and every typo compiles.

### Custom errors need `Object.setPrototypeOf`

```typescript
export class NeetCodeError extends Error {
  constructor(message: string) {
    super(message);
    this.name = new.target.name;
    Object.setPrototypeOf(this, new.target.prototype);
  }
}
```

Extending a built-in like `Error` from TypeScript breaks the prototype chain under ES5/ES2015
downlevelling, so `instanceof` silently returns false and the NestJS exception filter stops
matching — the error falls through to a 500. This is the single most common footgun in custom
TypeScript errors, and Python and PHP have no equivalent.

### `noUncheckedIndexedAccess`

Enabled in `tsconfig.base.json`, which is why the algorithms are full of `nums[i]!`. It makes
`nums[i]` have type `number | undefined`, forcing you to acknowledge that an array index can
miss. Verbose in tight loops, and worth it everywhere else.

---

## The app: `apps/api-node`

```
src/
  main.ts                 entrypoint
  app.factory.ts          builds the configured app — used by main AND by the tests
  app.module.ts           root module
  common/
    dto/solve-response.dto.ts   shared envelope (classes, not interfaces — see below)
    filters/domain-exception.filter.ts
    pipes/approach.pipe.ts
    timing.ts
  health/   catalog/
  problems/
    problems.module.ts    the explicit list of feature modules
    two-sum/
      two-sum.module.ts  two-sum.controller.ts  two-sum.service.ts
      dto/two-sum-request.dto.ts
test/
  setup.ts  *.e2e.spec.ts
```

### One factory, used by `main.ts` *and* the tests

```typescript
// app.factory.ts
export async function createApp(options: CreateAppOptions = {}): Promise<INestApplication> {
  verifyRegistry();
  const app = await NestFactory.create(AppModule, { logger: options.logger ?? [...] });
  app.useGlobalPipes(new ValidationPipe({ ... }));
  app.useGlobalFilters(new DomainExceptionFilter());
  SwaggerModule.setup("docs", app, ...);
  return app;
}
```

The e2e tests call the same function. A test that configures its own pipeline is a test that
can pass while production is broken.

### The `ValidationPipe`, and why every option is there

```typescript
new ValidationPipe({
  whitelist: true,                    // strip properties with no decorator
  forbidNonWhitelisted: true,         // ...and 422 if there were any
  transform: true,
  errorHttpStatusCode: 422,           // Nest defaults to 400; FastAPI uses 422
})
```

`forbidNonWhitelisted` is the counterpart of Pydantic's `extra="forbid"`. `errorHttpStatusCode`
is a deliberate divergence from the Nest default so all three apps agree.

### DTOs must be classes

```typescript
export class TwoSumRequestDto {
  @ApiProperty({ type: [Number], minItems: 2, example: [2, 7, 11, 15] })
  @IsArray() @ArrayMinSize(2) @IsInt({ each: true })
  nums!: number[];
}
```

Not a style preference. Both `class-validator` and `@nestjs/swagger` read **runtime** metadata
emitted by the decorators, and an interface leaves nothing behind at runtime. FastAPI gets the
same result for free because Pydantic models already are runtime objects.

Note also that `class-validator` validates an *already-parsed* object — it does not parse. That
is why `@IsInt()` rejects the string `"7"` outright rather than coercing it, and why the
Pydantic model in the FastAPI app uses `StrictInt` to match.

### `@HttpCode(HttpStatus.OK)` — do not forget this

```typescript
@Post(SLUG)
@HttpCode(HttpStatus.OK)
```

NestJS answers a `POST` with **201 Created** by default. Solving a problem creates nothing, and
FastAPI and Laravel both answer 200. Forgetting this line is the single most common reason a
Nest endpoint disagrees with its Python twin — it is exactly how the Two Sum e2e suite first
failed while building this repo.

### Pipes carry configuration through their constructor

```typescript
@Query("approach", new ApproachPipe(SLUG)) approach: string
```

`ApproachPipe` is instantiated per route with the slug baked in, so each endpoint validates
`?approach=` against *its own* registered keys. The FastAPI equivalent is a dependency factory
returning a closure; Laravel does it with an explicit check in the controller.

### The exception filter is `@Catch()` with no arguments

It catches everything, then translates:

| Thrown | Status | `error.type` |
|--------|--------|--------------|
| `NoSolutionError` | 404 | `no_solution` |
| `UnknownProblemError` | 404 | `unknown_problem` |
| `UnknownApproachError` | 422 | `unknown_approach` |
| `HttpException` (422) | 422 | `validation_error` |
| anything else | 500 | `internal_error` |

`ValidationPipe` throws with `{ statusCode, message: string[], error }` — `message` is
`class-validator`'s array of human-readable constraint failures. The filter lifts it into
`error.details` to match FastAPI's `{ field, message }` shape as closely as the two libraries
allow. They are not identical: `class-validator` does not report the field separately, so the
filter takes the first word of the message as a hint.

### Two test runners on purpose

| Package | Runner | Why |
|---------|--------|-----|
| `packages/core-ts` | **Vitest** | plain TS library, no decorators, fastest option |
| `apps/api-node` | **Jest + supertest** | canonical for NestJS; `ts-jest` handles `emitDecoratorMetadata` natively |

Vitest can run NestJS, but it needs `@swc/core` plus `unplugin-swc` to emit decorator metadata
— an extra moving part with a well-known failure mode. Each package uses the idiomatic choice
for what it is, which is also a small lesson in itself.

Note `vitest.config.mts`, not `.ts`: the package is CommonJS, so a `.ts` config loads through
Vite's deprecated CJS API and warns on every run.

---

## Build wiring, briefly

`apps/api-node/tsconfig.json` has **no `paths` mapping** to the core source, and that is
deliberate. With one, `tsc` pulls `packages/core-ts/src` into the build tree and output lands
at `dist/apps/api-node/src/main.js` instead of `dist/main.js`, breaking `start:prod`.

Instead the app resolves `@neetcode/core` through the npm workspace symlink to the built
`dist/`. Which means **core-ts must be built before api-node** — `make setup-node` and the
root `build` script both do it in that order.

Jest is the exception: its `moduleNameMapper` points at `packages/core-ts/src/index.ts` so
tests run without a build step.

---

## Commands

```bash
make run-node                                   # nest start --watch on :3000
make test-node                                  # core + api
npm run test --workspace @neetcode/core
npm run build --workspace @neetcode/core        # required before nest build
npx tsc --noEmit -p apps/api-node/tsconfig.json
```

## Idioms worth copying

| Want | Use |
|------|-----|
| Hash map with real keys | `new Map()` — never `{}`, whose keys coerce to strings |
| Set semantics | `new Set()` |
| Default value | `map.get(k) ?? 0` — `??`, not `\|\|`, which swallows `0` and `""` |
| Iterate a string safely | `for (const ch of s)` or `[...s]` — never `s.split("")` |
| Fixed-size numeric array | `new Array(n).fill(0)` or a `TypedArray` |
| Sort numbers | `xs.sort((a, b) => a - b)` — the default sort is **lexicographic** |
| Integer division | `Math.trunc(a / b)` or `(a / b) \| 0` |
| Big integers | `BigInt` past `Number.MAX_SAFE_INTEGER` (2⁵³−1) |
