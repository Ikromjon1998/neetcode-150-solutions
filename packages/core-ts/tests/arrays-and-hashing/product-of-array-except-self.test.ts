/**
 * 238. Product of Array Except Self — driven by packages/contracts/problems/0238-product-of-array-except-self.json.
 *
 * No hand-written fixtures: add a case to the JSON and it lands here, in the Python suite and
 * in the PHP suite at the same time.
 */

import { describe, expect, it } from "vitest";
import { contractCases } from "../../src/index";
import { productOfArrayExceptSelfBruteForce, productOfArrayExceptSelfPrefixSuffix } from "../../src/arrays-and-hashing/product-of-array-except-self";

interface Input {
  nums: number[];
}

const SLUG = "product-of-array-except-self";
const CASES = contractCases<Input, number[]>(SLUG);
const IMPLEMENTATIONS = [
  ["brute-force", productOfArrayExceptSelfBruteForce],
  ["prefix-suffix", productOfArrayExceptSelfPrefixSuffix],
] as const;

describe.each(IMPLEMENTATIONS)("product-of-array-except-self (%s)", (_key, solve) => {
  it.each(CASES)("$name", ({ input, expected }) => {
    expect(solve(input.nums)).toEqual(expected);
  });
});

describe("product-of-array-except-self differential", () => {
  it.each(CASES)("all approaches agree: $name", ({ input }) => {
    const results = IMPLEMENTATIONS.map(([, solve]) => solve(input.nums));
    for (const result of results) expect(result).toEqual(results[0]);
  });
});
