/**
 * 217. Contains Duplicate
 *
 * Return true when any value appears in `nums` more than once, and false when every element is
 * distinct.
 *
 * https://leetcode.com/problems/contains-duplicate/
 *
 * Each function below is an exercise. Replace the `throw` with your implementation,
 * then run `make test-node`.
 *
 * Stuck? `make show SLUG=contains-duplicate` prints a worked answer.
 */

import { defineProblem } from "../define-problem";
import { UnsolvedError } from "../errors";

export const SLUG = "contains-duplicate";
const PATH = "packages/core-ts/src/arrays-and-hashing/contains-duplicate.ts";

/**
 * Compare every pair — target: O(n^2) time, O(1) space.
 *
 * The only approach that allocates nothing. On inputs of a handful of elements it wins outright,
 * which is worth seeing before dismissing it.
 */
export function containsDuplicateBruteForce(nums: readonly number[]): boolean {
  for(let i = 0; i< nums.length; i++) {
    for(let j = i +1; j < nums.length; j ++) {
      if (nums[i] === nums[j]) {
        return true;
      }
    }
  }
  return false;
}

/**
 * Sort, then scan neighbours — target: O(n log n) time, O(n) space.
 *
 * Duplicates become adjacent once sorted. Not O(1) space in any of these three languages, since
 * none can sort the caller's array in place without mutating it.
 */
export function containsDuplicateSorting(nums: readonly number[]): boolean {
  let new_array = [...nums].sort((a, b) => a - b);
  for (let i = 1; i < new_array.length; i ++) {
    if (new_array[i - 1] === new_array[i]){
      return true;
    }
  }
  return false;
}

/**
 * Set membership — target: O(n) time, O(n) space.
 *
 * Return on the first repeat, so the early-exit case is far better than O(n) in practice — a
 * duplicate at index 1 costs two operations regardless of input size.
 */
export function containsDuplicateHashSet(nums: readonly number[]): boolean {
  let hashValue =  new Set<number>();
  for (const num of nums) {
    if (hashValue.has(num)) {
      return true;
    }
    hashValue.add(num);
  }
  return false;
}

export const containsDuplicate = defineProblem(SLUG, {
  "brute-force": containsDuplicateBruteForce,
  sorting: containsDuplicateSorting,
  "hash-set": containsDuplicateHashSet,
});
