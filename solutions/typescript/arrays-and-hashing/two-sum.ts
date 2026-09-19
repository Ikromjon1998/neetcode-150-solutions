/**
 * 1. Two Sum — https://leetcode.com/problems/two-sum/
 *
 * Given `nums` and `target`, return the indices of the two numbers adding up to `target`.
 *
 * Both approaches below are registered and reachable from the API via `?approach=`, so you
 * can benchmark them against each other over the same input without changing any code.
 */

import { NoSolutionError } from "../errors";
import { defineProblem } from "../define-problem";

export const SLUG = "two-sum";

/**
 * Check every pair. Time O(n^2), space O(1).
 *
 * Worth keeping: it is the baseline that makes the hash-map version's space cost look like a
 * bargain, and on tiny inputs it is genuinely faster because it never allocates.
 */
export function twoSumBruteForce(nums: readonly number[], target: number): number[] {
  for (let i = 0; i < nums.length; i++) {
    for (let j = i + 1; j < nums.length; j++) {
      if (nums[i]! + nums[j]! === target) return [i, j];
    }
  }
  throw new NoSolutionError(SLUG, `No two entries of nums sum to ${target}.`);
}

/**
 * One pass, remembering every value already seen. Time O(n), space O(n).
 *
 * `Map`, not a plain object: object keys are coerced to strings, so `-0` and `0` would
 * collide and numeric keys would be re-parsed on every lookup. `Map` keeps real number keys
 * with SameValueZero semantics. Python's `dict` and PHP's array both sidestep this — it is a
 * genuinely JavaScript-only trap.
 */
export function twoSumHashMap(nums: readonly number[], target: number): number[] {
  const seen = new Map<number, number>();
  for (let index = 0; index < nums.length; index++) {
    const value = nums[index]!;
    const complement = seen.get(target - value);
    if (complement !== undefined) return [complement, index];
    seen.set(value, index);
  }
  throw new NoSolutionError(SLUG, `No two entries of nums sum to ${target}.`);
}

export const twoSum = defineProblem(SLUG, {
  "brute-force": twoSumBruteForce,
  "hash-map": twoSumHashMap,
});
