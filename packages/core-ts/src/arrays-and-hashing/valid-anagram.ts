/**
 * 242. Valid Anagram
 *
 * Return true when `t` is an anagram of `s` — that is, when both strings contain exactly the same
 * characters with exactly the same multiplicities.
 *
 * https://leetcode.com/problems/valid-anagram/
 *
 * Each function below is an exercise. Replace the `throw` with your implementation,
 * then run `make test-node`.
 *
 * Stuck? `make show SLUG=valid-anagram` prints a worked answer.
 */

import { defineProblem } from "../define-problem";
import { UnsolvedError } from "../errors";

export const SLUG = "valid-anagram";
const PATH = "packages/core-ts/src/arrays-and-hashing/valid-anagram.ts";

/**
 * Sort both strings — target: O(n log n) time, O(n) space.
 *
 * Two anagrams have the same sorted form. Three lines and obviously correct, which is worth
 * something — but the sort dominates, and all three languages must copy the string to sort it.
 */
export function validAnagramSorting(s: string, t: string): boolean {
  throw new UnsolvedError(SLUG, "sorting", PATH);
}

/**
 * Character frequency count — target: O(n) time, O(k) space.
 *
 * Count each character in `s`, decrement for each in `t`, and a single pass over the counts
 * decides it. O(k) in the alphabet size, not the input length.
 */
export function validAnagramHashMap(s: string, t: string): boolean {
  throw new UnsolvedError(SLUG, "hash-map", PATH);
}

export const validAnagram = defineProblem(SLUG, {
  sorting: validAnagramSorting,
  "hash-map": validAnagramHashMap,
});
