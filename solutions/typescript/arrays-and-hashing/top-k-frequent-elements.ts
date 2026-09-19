/**
 * 347. Top K Frequent Elements — https://leetcode.com/problems/top-k-frequent-elements/
 *
 * The `k` most frequent values in `nums`.
 *
 * LeetCode accepts any order; this repo pins descending-by-frequency then ascending-by-value so
 * the three implementations can be compared byte for byte.
 */

import { defineProblem } from "../define-problem";

export const SLUG = "top-k-frequent-elements";

function tally(nums: readonly number[]): Map<number, number> {
  const counts = new Map<number, number>();
  for (const value of nums) counts.set(value, (counts.get(value) ?? 0) + 1);
  return counts;
}

/**
 * Tally, then sort the distinct values. Time O(n log n), space O(n).
 *
 * Python expresses the canonical order as a single tuple key, `(-count, value)`. JavaScript has
 * no tuple comparison, so the two terms have to be spelled out: compare counts descending, and
 * fall through to values ascending only on a tie.
 */
export function topKFrequentElementsSorting(nums: readonly number[], k: number): number[] {
  return [...tally(nums).entries()]
    .sort(([valueA, countA], [valueB, countB]) => countB - countA || valueA - valueB)
    .slice(0, Math.max(0, k))
    .map(([value]) => value);
}

/**
 * Bucket the values by frequency. Time O(n), space O(n).
 *
 * No value can occur more than `nums.length` times, so an array of `n + 1` buckets indexed by
 * frequency has somewhere to put everything. Walking it from the back yields descending
 * frequency without ever sorting.
 *
 * Each bucket is sorted internally only to honour this repo's ascending-value tie-break.
 */
export function topKFrequentElementsBucketSort(nums: readonly number[], k: number): number[] {
  if (k <= 0) return [];

  const buckets: number[][] = Array.from({ length: nums.length + 1 }, () => []);
  for (const [value, count] of tally(nums)) buckets[count]!.push(value);

  const result: number[] = [];
  for (let count = buckets.length - 1; count > 0; count--) {
    for (const value of buckets[count]!.sort((a, b) => a - b)) {
      result.push(value);
      if (result.length === k) return result;
    }
  }

  return result;
}

export const topKFrequentElements = defineProblem(SLUG, {
  sorting: topKFrequentElementsSorting,
  "bucket-sort": topKFrequentElementsBucketSort,
});
