/**
 * 128. Longest Consecutive Sequence — driven by packages/contracts/problems/0128-longest-consecutive-sequence.json.
 *
 * No hand-written fixtures: add a case to the JSON and it lands here, in the Python suite and
 * in the PHP suite at the same time.
 */

import { describe, expect, it } from "vitest";
import { contractCases } from "../../src/index";
import { longestConsecutiveSequenceSorting, longestConsecutiveSequenceHashSet } from "../../src/arrays-and-hashing/longest-consecutive-sequence";

interface Input {
  nums: number[];
}

const SLUG = "longest-consecutive-sequence";
const CASES = contractCases<Input, number>(SLUG);
const IMPLEMENTATIONS = [
  ["sorting", longestConsecutiveSequenceSorting],
  ["hash-set", longestConsecutiveSequenceHashSet],
] as const;

describe.each(IMPLEMENTATIONS)("longest-consecutive-sequence (%s)", (_key, solve) => {
  it.each(CASES)("$name", ({ input, expected }) => {
    expect(solve(input.nums)).toEqual(expected);
  });
});

describe("longest-consecutive-sequence differential", () => {
  it.each(CASES)("all approaches agree: $name", ({ input }) => {
    const results = IMPLEMENTATIONS.map(([, solve]) => solve(input.nums));
    for (const result of results) expect(result).toEqual(results[0]);
  });
});
