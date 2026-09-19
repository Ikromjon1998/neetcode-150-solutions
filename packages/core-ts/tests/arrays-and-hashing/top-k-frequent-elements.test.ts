/**
 * 347. Top K Frequent Elements — driven by packages/contracts/problems/0347-top-k-frequent-elements.json.
 *
 * No hand-written fixtures: add a case to the JSON and it lands here, in the Python suite and
 * in the PHP suite at the same time.
 */

import { describe, expect, it } from "vitest";
import { contractCases } from "../../src/index";
import { topKFrequentElementsSorting, topKFrequentElementsBucketSort } from "../../src/arrays-and-hashing/top-k-frequent-elements";

interface Input {
  nums: number[];
  k: number;
}

const SLUG = "top-k-frequent-elements";
const CASES = contractCases<Input, number[]>(SLUG);
const IMPLEMENTATIONS = [
  ["sorting", topKFrequentElementsSorting],
  ["bucket-sort", topKFrequentElementsBucketSort],
] as const;

describe.each(IMPLEMENTATIONS)("top-k-frequent-elements (%s)", (_key, solve) => {
  it.each(CASES)("$name", ({ input, expected }) => {
    expect(solve(input.nums, input.k)).toEqual(expected);
  });
});

describe("top-k-frequent-elements differential", () => {
  it.each(CASES)("all approaches agree: $name", ({ input }) => {
    const results = IMPLEMENTATIONS.map(([, solve]) => solve(input.nums, input.k));
    for (const result of results) expect(result).toEqual(results[0]);
  });
});
