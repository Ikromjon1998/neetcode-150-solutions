/**
 * 1. Two Sum — driven entirely by packages/contracts/problems/0001-two-sum.json.
 *
 * Note what is *not* here: no hand-written input/expected pairs. Add a case to the JSON and
 * it lands in this file, in the Python suite and in the PHP suite at the same time.
 */

import { describe, expect, it } from "vitest";
import {
  contractCases,
  NoSolutionError,
  notFoundCases,
  twoSumBruteForce,
  twoSumHashMap,
} from "../../src/index";

interface TwoSumInput {
  nums: number[];
  target: number;
}

const SLUG = "two-sum";
const CASES = contractCases<TwoSumInput, number[]>(SLUG);
const IMPLEMENTATIONS = [
  ["brute-force", twoSumBruteForce],
  ["hash-map", twoSumHashMap],
] as const;

describe.each(IMPLEMENTATIONS)("two-sum (%s)", (_key, solve) => {
  it.each(CASES)("$name", ({ input, expected }) => {
    expect(solve(input.nums, input.target)).toEqual(expected);
  });

  it.each(notFoundCases<TwoSumInput>(SLUG))("throws NoSolutionError: $name", ({ input }) => {
    expect(() => solve(input.nums, input.target)).toThrow(NoSolutionError);
  });
});

describe("two-sum differential", () => {
  /**
   * Every approach must return the identical answer. This is the test that makes adding a
   * new approach cheap and safe — it is automatically compared against the trusted ones.
   */
  it.each(CASES)("all approaches agree: $name", ({ input }) => {
    const results = IMPLEMENTATIONS.map(([, solve]) => solve(input.nums, input.target));
    for (const result of results) expect(result).toEqual(results[0]);
  });
});
