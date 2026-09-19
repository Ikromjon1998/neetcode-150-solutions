/**
 * 49. Group Anagrams — driven by packages/contracts/problems/0049-group-anagrams.json.
 *
 * No hand-written fixtures: add a case to the JSON and it lands here, in the Python suite and
 * in the PHP suite at the same time.
 */

import { describe, expect, it } from "vitest";
import { contractCases } from "../../src/index";
import { groupAnagramsSortedKey, groupAnagramsCountKey } from "../../src/arrays-and-hashing/group-anagrams";

interface Input {
  strs: string[];
}

const SLUG = "group-anagrams";
const CASES = contractCases<Input, string[][]>(SLUG);
const IMPLEMENTATIONS = [
  ["sorted-key", groupAnagramsSortedKey],
  ["count-key", groupAnagramsCountKey],
] as const;

describe.each(IMPLEMENTATIONS)("group-anagrams (%s)", (_key, solve) => {
  it.each(CASES)("$name", ({ input, expected }) => {
    expect(solve(input.strs)).toEqual(expected);
  });
});

describe("group-anagrams differential", () => {
  it.each(CASES)("all approaches agree: $name", ({ input }) => {
    const results = IMPLEMENTATIONS.map(([, solve]) => solve(input.strs));
    for (const result of results) expect(result).toEqual(results[0]);
  });
});
