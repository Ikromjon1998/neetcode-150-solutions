/**
 * `defineProblem` lives in its own module to break an import cycle.
 *
 * The natural home for it is `registry.ts`, but `registry.ts` imports every problem module in
 * order to build its map, and every problem module needs this helper. That cycle resolves at
 * runtime as `defineProblem is not a function`: Node starts evaluating `registry.ts`, hits
 * the import of `two-sum.ts`, evaluates that file to completion — and at that moment
 * `registry.ts` has not yet reached its own `export function defineProblem`, so the binding is
 * still in its temporal dead zone.
 *
 * A leaf module with no imports of its own cannot participate in a cycle, which is the fix.
 * Python's import system tolerates this pattern (it binds names lazily at attribute access),
 * and PHP's autoloader never sees it at all because classes load on first use. This is a
 * JavaScript-shaped problem with a JavaScript-shaped answer.
 */

import type { SolutionFn } from "./types";

/**
 * Declare a problem's implementations.
 *
 * `const T` keeps the approach keys as a literal union, so `twoSum.solutions["hash-map"]`
 * type-checks and `twoSum.solutions["hashmap"]` does not.
 */
export function defineProblem<const T extends Readonly<Record<string, SolutionFn>>>(
  slug: string,
  solutions: T,
): { slug: string; solutions: T } {
  return { slug, solutions };
}
