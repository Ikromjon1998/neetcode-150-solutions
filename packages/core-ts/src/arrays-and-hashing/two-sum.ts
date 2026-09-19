/**
 * 1. Two Sum
 *
 * Return the indices of the two numbers in `nums` that add up to `target`. Exactly one solution
 * exists and the same element may not be used twice.
 *
 * https://leetcode.com/problems/two-sum/
 *
 * Each function below is an exercise. Replace the `throw` with your implementation,
 * then run `make test-node`.
 *
 * Stuck? `make show SLUG=two-sum` prints a worked answer.
 */

import { defineProblem } from "../define-problem";
import { UnsolvedError } from "../errors";

export const SLUG = "two-sum";
const PATH = "packages/core-ts/src/arrays-and-hashing/two-sum.ts";

/**
 * Nested loops — target: O(n^2) time, O(1) space.
 *
 * Check every pair. Kept on purpose as the baseline the optimal approach is measured against.
 */
export function twoSumBruteForce(nums: readonly number[], target: number): number[] {
  throw new UnsolvedError(SLUG, "brute-force", PATH);
}

/**
 * One-pass hash map — target: O(n) time, O(n) space.
 *
 * Trade space for time: remember every value seen so far and look up the complement in O(1).
 */
export function twoSumHashMap(nums: readonly number[], target: number): number[] {
  throw new UnsolvedError(SLUG, "hash-map", PATH);
}

export const twoSum = defineProblem(SLUG, {
  "brute-force": twoSumBruteForce,
  "hash-map": twoSumHashMap,
});
