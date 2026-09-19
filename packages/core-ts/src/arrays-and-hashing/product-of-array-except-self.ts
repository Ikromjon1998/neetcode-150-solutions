/**
 * 238. Product of Array Except Self
 *
 * Return an array where each position holds the product of every element of `nums` except the one
 * at that position. Division is not allowed, which is what makes the problem interesting — the
 * obvious total-product-divided-by-self approach breaks on zeros anyway.
 *
 * https://leetcode.com/problems/product-of-array-except-self/
 *
 * Each function below is an exercise. Replace the `throw` with your implementation,
 * then run `make test-node`.
 *
 * Stuck? `make show SLUG=product-of-array-except-self` prints a worked answer.
 */

import { defineProblem } from "../define-problem";
import { UnsolvedError } from "../errors";

export const SLUG = "product-of-array-except-self";
const PATH = "packages/core-ts/src/arrays-and-hashing/product-of-array-except-self.ts";

/**
 * Recompute each product — target: O(n^2) time, O(1) space.
 *
 * For every index, multiply everything else. The baseline, and the only one that needs no
 * auxiliary reasoning.
 */
export function productOfArrayExceptSelfBruteForce(nums: readonly number[]): number[] {
  throw new UnsolvedError(SLUG, "brute-force", PATH);
}

/**
 * Prefix and suffix products — target: O(n) time, O(1) space.
 *
 * Each answer is (product of everything to the left) x (product of everything to the right). Two
 * passes, reusing the output array as the accumulator, so the extra space is a single running
 * variable.
 */
export function productOfArrayExceptSelfPrefixSuffix(nums: readonly number[]): number[] {
  throw new UnsolvedError(SLUG, "prefix-suffix", PATH);
}

export const productOfArrayExceptSelf = defineProblem(SLUG, {
  "brute-force": productOfArrayExceptSelfBruteForce,
  "prefix-suffix": productOfArrayExceptSelfPrefixSuffix,
});
