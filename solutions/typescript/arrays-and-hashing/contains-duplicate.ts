/**
 * 217. Contains Duplicate — https://leetcode.com/problems/contains-duplicate/
 *
 * Return true when any value appears in `nums` more than once.
 */

import { defineProblem } from "../define-problem";

export const SLUG = "contains-duplicate";

/**
 * Compare every pair. Time O(n^2), space O(1).
 *
 * The only approach here that allocates nothing, which is why it is kept: below roughly twenty
 * elements it beats both of the others.
 */
export function containsDuplicateBruteForce(nums: readonly number[]): boolean {
  for (let i = 0; i < nums.length; i++) {
    for (let j = i + 1; j < nums.length; j++) {
      if (nums[i] === nums[j]) return true;
    }
  }
  return false;
}

/**
 * Sort, then check adjacent pairs. Time O(n log n), space O(n).
 *
 * Two JavaScript-specific notes. `[...nums]` because `Array.prototype.sort` sorts **in place**
 * and would mutate the caller's array — Python's `sorted()` and PHP's need for an explicit
 * copy both make this harder to get wrong. And `(a, b) => a - b`, because the default
 * comparator converts elements to strings: `[10, 9].sort()` returns `[10, 9]`.
 */
export function containsDuplicateSorting(nums: readonly number[]): boolean {
  const sorted = [...nums].sort((a, b) => a - b);
  for (let i = 1; i < sorted.length; i++) {
    if (sorted[i] === sorted[i - 1]) return true;
  }
  return false;
}

/**
 * Set membership; return on the first repeat. Time O(n), space O(n).
 *
 * `new Set(nums).size !== nums.length` is the popular one-liner and is strictly worse: it
 * always consumes the whole input, while this returns after two operations when the duplicate
 * is at index 1.
 */
export function containsDuplicateHashSet(nums: readonly number[]): boolean {
  const seen = new Set<number>();
  for (const value of nums) {
    if (seen.has(value)) return true;
    seen.add(value);
  }
  return false;
}

export const containsDuplicate = defineProblem(SLUG, {
  "brute-force": containsDuplicateBruteForce,
  sorting: containsDuplicateSorting,
  "hash-set": containsDuplicateHashSet,
});
