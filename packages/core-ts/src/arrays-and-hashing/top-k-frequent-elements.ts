/**
 * 347. Top K Frequent Elements
 *
 * Return the `k` most frequent values in `nums`. LeetCode accepts any order; this repo pins a
 * canonical one — descending by frequency, then ascending by value — so the three implementations
 * can be compared byte for byte.
 *
 * https://leetcode.com/problems/top-k-frequent-elements/
 *
 * Each function below is an exercise. Replace the `throw` with your implementation,
 * then run `make test-node`.
 *
 * Stuck? `make show SLUG=top-k-frequent-elements` prints a worked answer.
 */

import { defineProblem } from "../define-problem";
import { UnsolvedError } from "../errors";

export const SLUG = "top-k-frequent-elements";
const PATH = "packages/core-ts/src/arrays-and-hashing/top-k-frequent-elements.ts";

/**
 * Count, then sort by frequency — target: O(n log n) time, O(n) space.
 *
 * Tally, then sort the distinct values. The sort dominates, but on the small inputs this problem
 * usually sees it is the fastest of the two.
 */
export function topKFrequentElementsSorting(nums: readonly number[], k: number): number[] {
  throw new UnsolvedError(SLUG, "sorting", PATH);
}

/**
 * Bucket by frequency — target: O(n) time, O(n) space.
 *
 * A count can never exceed n, so an array of n+1 buckets indexed by frequency replaces the sort
 * entirely. Walking it from the back yields values in descending frequency for free.
 */
export function topKFrequentElementsBucketSort(nums: readonly number[], k: number): number[] {
  throw new UnsolvedError(SLUG, "bucket-sort", PATH);
}

export const topKFrequentElements = defineProblem(SLUG, {
  sorting: topKFrequentElementsSorting,
  "bucket-sort": topKFrequentElementsBucketSort,
});
