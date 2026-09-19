# `@neetcode/core` (TypeScript)

The algorithms, and nothing else. **Zero runtime dependencies** — no NestJS, no HTTP. Every
solution is a plain exported function you can import anywhere.

CommonJS output on purpose: the consumer is NestJS, which is CJS. An ESM-only core would be
unrequirable from the app.

## Use

```typescript
import { getSolution, allMeta, NoSolutionError, twoSumHashMap } from "@neetcode/core";

twoSumHashMap([2, 7, 11, 15], 9);        // [0, 1] — direct import keeps the exact signature
getSolution("two-sum", "hash-map");       // via the registry
getSolution("two-sum");                   // the contract's default approach
allMeta().map((m) => m.slug);             // ['two-sum', 'valid-anagram']
```

## Layout

```
src/
  index.ts           public surface — the barrel
  types.ts           ProblemMeta, Approach, Difficulty, Topic, SolutionFn
  errors.ts          NoSolutionError & friends (no HTTP status codes in sight)
  contracts.ts       loads packages/contracts/problems/*.json
  define-problem.ts  the defineProblem helper — in its own file to break an import cycle
  registry.ts        the explicit module list
  arrays-and-hashing/
    two-sum.ts  valid-anagram.ts
tests/               contract-driven, no hand-written fixtures
```

## How registration works

```typescript
// registry.ts
import { twoSum } from "./arrays-and-hashing/two-sum";
const PROBLEM_MODULES: readonly ProblemModule[] = [twoSum, validAnagram];
```

Explicit, one import line per problem. In exchange the bundler can tree-shake, the type-checker
verifies every entry, and there is no filesystem access at import time — so this works in a
browser bundle or a Lambda. Python's `pkgutil` auto-discovery can do none of those; PHP's
config array trades differently again. See
[`docs/06-language-comparison.md`](../../docs/06-language-comparison.md).

`defineProblem` lives in `define-problem.ts` rather than `registry.ts` because the natural
placement creates a cycle that fails at runtime with `defineProblem is not a function`. The
file explains it in full.

## Build and test

```bash
npm run build --workspace @neetcode/core    # required before the NestJS app builds
npm run test  --workspace @neetcode/core    # vitest
npx vitest --root packages/core-ts          # watch mode
npx tsc --noEmit -p packages/core-ts/tsconfig.json
```
