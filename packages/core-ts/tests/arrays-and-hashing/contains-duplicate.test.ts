/**
 * 217. Contains Duplicate — driven by packages/contracts/problems/0217-contains-duplicate.json.
 *
 * No hand-written fixtures: add a case to the JSON and it lands here, in the Python suite and
 * in the PHP suite at the same time.
 */

import { describe, expect, it } from "vitest";
import { contractCases } from "../../src/index";
import { containsDuplicateBruteForce, containsDuplicateSorting, containsDuplicateHashSet } from "../../src/arrays-and-hashing/contains-duplicate";

interface Input {
  nums: number[];
}

const SLUG = "contains-duplicate";
const CASES = contractCases<Input, boolean>(SLUG);
const IMPLEMENTATIONS = [
  ["brute-force", containsDuplicateBruteForce],
  ["sorting", containsDuplicateSorting],
  ["hash-set", containsDuplicateHashSet],
] as const;

describe.each(IMPLEMENTATIONS)("contains-duplicate (%s)", (_key, solve) => {
  it.each(CASES)("$name", ({ input, expected }) => {
    expect(solve(input.nums)).toEqual(expected);
  });
});

describe("contains-duplicate differential", () => {
  it.each(CASES)("all approaches agree: $name", ({ input }) => {
    const results = IMPLEMENTATIONS.map(([, solve]) => solve(input.nums));
    for (const result of results) expect(result).toEqual(results[0]);
  });
});
