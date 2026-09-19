/**
 * 128. Longest Consecutive Sequence — https://leetcode.com/problems/longest-consecutive-sequence/
 *
 * The length of the longest run of consecutive integers present in `nums`. Position in the
 * array is irrelevant, and duplicates do not lengthen a run.
 */

import { defineProblem } from "../define-problem";

export const SLUG = "longest-consecutive-sequence";

/**
 * Sort, then walk. Time O(n log n), space O(n).
 *
 * `[...new Set(nums)].sort((a, b) => a - b)` does three jobs at once: copy (so the caller's
 * array is not reordered), deduplicate, and sort numerically. The explicit comparator is not
 * optional — the default sort compares elements as strings.
 */
export function longestConsecutiveSequenceSorting(nums: readonly number[]): number {
  if (nums.length === 0) return 0;

  const ordered = [...new Set(nums)].sort((a, b) => a - b);
  let longest = 1;
  let current = 1;

  for (let i = 1; i < ordered.length; i++) {
    current = ordered[i]! - ordered[i - 1]! === 1 ? current + 1 : 1;
    longest = Math.max(longest, current);
  }

  return longest;
}

/**
 * Walk each run exactly once, from its start. Time O(n), space O(n).
 *
 * The `!seen.has(value - 1)` guard is the entire algorithm. Without it the inner loop re-walks
 * every run from every one of its members and the whole thing degrades to O(n^2) — the version
 * people write first and then wonder why it is not faster than sorting.
 */
export function longestConsecutiveSequenceHashSet(nums: readonly number[]): number {
  const seen = new Set(nums);
  let longest = 0;

  for (const value of seen) {
    if (seen.has(value - 1)) continue; // not the start of a run

    let length = 1;
    while (seen.has(value + length)) length++;
    longest = Math.max(longest, length);
  }

  return longest;
}

export const longestConsecutiveSequence = defineProblem(SLUG, {
  sorting: longestConsecutiveSequenceSorting,
  "hash-set": longestConsecutiveSequenceHashSet,
});
