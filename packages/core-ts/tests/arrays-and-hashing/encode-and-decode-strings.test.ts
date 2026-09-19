/**
 * 271. Encode and Decode Strings — driven by packages/contracts/problems/0271-encode-and-decode-strings.json.
 *
 * No hand-written fixtures: add a case to the JSON and it lands here, in the Python suite and
 * in the PHP suite at the same time.
 */

import { describe, expect, it } from "vitest";
import { contractCases } from "../../src/index";
import { encodeAndDecodeStringsLengthPrefixed, encodeAndDecodeStringsDelimiterEscaped } from "../../src/arrays-and-hashing/encode-and-decode-strings";

interface Input {
  strs: string[];
}

const SLUG = "encode-and-decode-strings";
const CASES = contractCases<Input, string[]>(SLUG);
const IMPLEMENTATIONS = [
  ["length-prefixed", encodeAndDecodeStringsLengthPrefixed],
  ["delimiter-escaped", encodeAndDecodeStringsDelimiterEscaped],
] as const;

describe.each(IMPLEMENTATIONS)("encode-and-decode-strings (%s)", (_key, solve) => {
  it.each(CASES)("$name", ({ input, expected }) => {
    expect(solve(input.strs)).toEqual(expected);
  });
});

describe("encode-and-decode-strings differential", () => {
  it.each(CASES)("all approaches agree: $name", ({ input }) => {
    const results = IMPLEMENTATIONS.map(([, solve]) => solve(input.strs));
    for (const result of results) expect(result).toEqual(results[0]);
  });
});
