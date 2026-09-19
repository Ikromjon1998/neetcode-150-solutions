/**
 * 242. Valid Anagram — driven by packages/contracts/problems/0242-valid-anagram.json.
 *
 * No hand-written fixtures: add a case to the JSON and it lands here, in the Python suite and
 * in the PHP suite at the same time.
 */

import { describe, expect, it } from "vitest";
import { contractCases } from "../../src/index";
import { validAnagramSorting, validAnagramHashMap } from "../../src/arrays-and-hashing/valid-anagram";

interface Input {
  s: string;
  t: string;
}

const SLUG = "valid-anagram";
const CASES = contractCases<Input, boolean>(SLUG);
const IMPLEMENTATIONS = [
  ["sorting", validAnagramSorting],
  ["hash-map", validAnagramHashMap],
] as const;

describe.each(IMPLEMENTATIONS)("valid-anagram (%s)", (_key, solve) => {
  it.each(CASES)("$name", ({ input, expected }) => {
    expect(solve(input.s, input.t)).toEqual(expected);
  });
});

describe("valid-anagram differential", () => {
  it.each(CASES)("all approaches agree: $name", ({ input }) => {
    const results = IMPLEMENTATIONS.map(([, solve]) => solve(input.s, input.t));
    for (const result of results) expect(result).toEqual(results[0]);
  });
});
