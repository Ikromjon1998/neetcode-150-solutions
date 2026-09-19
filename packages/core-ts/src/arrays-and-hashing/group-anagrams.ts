/**
 * 49. Group Anagrams
 *
 * Group the strings so that every group holds exactly the mutual anagrams. LeetCode accepts any
 * order; this repo pins a canonical one — each group sorted ascending, and the groups themselves
 * sorted by their first member — so the three implementations can be compared byte for byte.
 *
 * https://leetcode.com/problems/group-anagrams/
 *
 * Each function below is an exercise. Replace the `throw` with your implementation,
 * then run `make test-node`.
 *
 * Stuck? `make show SLUG=group-anagrams` prints a worked answer.
 */

import { defineProblem } from "../define-problem";
import { UnsolvedError } from "../errors";

export const SLUG = "group-anagrams";
const PATH = "packages/core-ts/src/arrays-and-hashing/group-anagrams.ts";

/**
 * Sorted string as the key — target: O(n k log k) time, O(n k) space.
 *
 * Two words are anagrams exactly when their sorted forms match, so the sorted string is a
 * ready-made group key. k is the word length; the log k is the per-word sort.
 */
export function groupAnagramsSortedKey(strs: readonly string[]): string[][] {
  throw new UnsolvedError(SLUG, "sorted-key", PATH);
}

/**
 * Character-count tuple as the key — target: O(n k) time, O(n k) space.
 *
 * Replace the per-word sort with a 26-slot tally rendered as a key. Linear in the word length, and
 * the clearest place in this repo where the three languages disagree about what may be used as a
 * map key.
 */
export function groupAnagramsCountKey(strs: readonly string[]): string[][] {
  throw new UnsolvedError(SLUG, "count-key", PATH);
}

export const groupAnagrams = defineProblem(SLUG, {
  "sorted-key": groupAnagramsSortedKey,
  "count-key": groupAnagramsCountKey,
});
