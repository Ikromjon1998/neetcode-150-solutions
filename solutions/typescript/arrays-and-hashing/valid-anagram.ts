/**
 * 242. Valid Anagram — https://leetcode.com/problems/valid-anagram/
 *
 * `t` is an anagram of `s` when both hold exactly the same characters with exactly the same
 * multiplicities. Order is irrelevant; counts are everything.
 */

import { defineProblem } from "../define-problem";

export const SLUG = "valid-anagram";

/**
 * Two anagrams have the same sorted form. Time O(n log n), space O(n).
 *
 * `[...s]` rather than `s.split("")`. Spreading a string iterates it by code *point*, so a
 * character outside the Basic Multilingual Plane stays one element; `split("")` cuts it into
 * two lone surrogates and would compare garbage. Python and PHP have no equivalent trap —
 * Python iterates code points natively, and PHP treats the string as bytes either way.
 */
export function validAnagramSorting(s: string, t: string): boolean {
  if (s.length !== t.length) return false;
  return [...s].sort().join("") === [...t].sort().join("");
}

/**
 * Count characters in one string, decrement for the other. Time O(n), space O(k).
 *
 * A `Map`, not an object literal: object keys are coerced to strings, and a key like
 * `"constructor"` would collide with `Object.prototype`. `Map` has no prototype chain to
 * collide with. Python's `Counter` does this in one call; here it is worth seeing the loop.
 */
export function validAnagramHashMap(s: string, t: string): boolean {
  if (s.length !== t.length) return false;

  const counts = new Map<string, number>();
  for (const char of s) counts.set(char, (counts.get(char) ?? 0) + 1);

  for (const char of t) {
    const remaining = counts.get(char);
    if (remaining === undefined || remaining === 0) return false;
    counts.set(char, remaining - 1);
  }

  return true;
}

export const validAnagram = defineProblem(SLUG, {
  sorting: validAnagramSorting,
  "hash-map": validAnagramHashMap,
});
