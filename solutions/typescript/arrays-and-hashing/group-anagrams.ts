/**
 * 49. Group Anagrams — https://leetcode.com/problems/group-anagrams/
 *
 * Group the input strings so that each group holds exactly the mutual anagrams.
 *
 * LeetCode accepts any order; this repo pins each group sorted ascending and the groups sorted
 * by their first member, so the three implementations can be compared byte for byte.
 */

import { defineProblem } from "../define-problem";

export const SLUG = "group-anagrams";

const ALPHABET = 26;
const CODE_A = "a".charCodeAt(0);

/** Impose this repo's ordering. Not part of the algorithm; part of the comparison. */
function canonical(groups: Iterable<string[]>): string[][] {
  return [...groups]
    .map((group) => [...group].sort())
    .sort((a, b) => (a[0]! < b[0]! ? -1 : a[0]! > b[0]! ? 1 : 0));
}

/**
 * Key each word by its sorted form. Time O(n·k log k), space O(n·k).
 *
 * `[...word].sort().join("")` rather than `word.split("").sort().join("")` — spreading iterates
 * code points, `split("")` iterates UTF-16 code units and would cut a surrogate pair in half.
 */
export function groupAnagramsSortedKey(strs: readonly string[]): string[][] {
  const groups = new Map<string, string[]>();
  for (const word of strs) {
    const key = [...word].sort().join("");
    const bucket = groups.get(key);
    if (bucket) bucket.push(word);
    else groups.set(key, [word]);
  }
  return canonical(groups.values());
}

/**
 * Key each word by its character tally. Time O(n·k), space O(n·k).
 *
 * Replaces the per-word sort with a single pass building a 26-slot tally.
 *
 * The tally then has to become a key, and this is where JavaScript is most awkward of the
 * three. `Map` compares object keys by **reference**, so a `number[]` key never matches a
 * second array with identical contents — every word would land in its own group. The counts
 * must be serialised to a primitive. Python can use a `tuple` directly, because tuples hash by
 * value; PHP has no choice either, since array keys are `int|string`.
 */
export function groupAnagramsCountKey(strs: readonly string[]): string[][] {
  const groups = new Map<string, string[]>();

  for (const word of strs) {
    const counts = new Array<number>(ALPHABET).fill(0);
    for (const char of word) counts[char.charCodeAt(0) - CODE_A]!++;
    const key = counts.join(",");

    const bucket = groups.get(key);
    if (bucket) bucket.push(word);
    else groups.set(key, [word]);
  }

  return canonical(groups.values());
}

export const groupAnagrams = defineProblem(SLUG, {
  "sorted-key": groupAnagramsSortedKey,
  "count-key": groupAnagramsCountKey,
});
