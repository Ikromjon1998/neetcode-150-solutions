/**
 * 271. Encode and Decode Strings
 *
 * Design an encoding that flattens a list of arbitrary strings into one string, and a decoding
 * that recovers the list exactly. Unlike the other problems here this is a design exercise with
 * two halves, so the endpoint runs the full round trip: it encodes the input and returns what
 * decoding produces. A correct implementation therefore returns its input unchanged — and any
 * encoding that cannot survive delimiters, empty strings or digits will not.
 *
 * https://leetcode.com/problems/encode-and-decode-strings/
 *
 * Each function below is an exercise. Replace the `throw` with your implementation,
 * then run `make test-node`.
 *
 * Stuck? `make show SLUG=encode-and-decode-strings` prints a worked answer.
 */

import { defineProblem } from "../define-problem";
import { UnsolvedError } from "../errors";

export const SLUG = "encode-and-decode-strings";
const PATH = "packages/core-ts/src/arrays-and-hashing/encode-and-decode-strings.ts";

/**
 * Length prefix and sentinel — target: O(n) time, O(n) space.
 *
 * Write each string as `<length>#<string>`. The length is read before the payload, so the payload
 * is never scanned for a delimiter and may contain anything at all — including `#` and digits. The
 * standard answer, and the only one here that is unconditionally safe.
 */
export function encodeAndDecodeStringsLengthPrefixed(strs: readonly string[]): string[] {
  throw new UnsolvedError(SLUG, "length-prefixed", PATH);
}

/**
 * Escaped delimiter — target: O(n) time, O(n) space.
 *
 * Join on a delimiter, escaping any occurrence of it (and of the escape character) inside the
 * payloads. Correct, but every decode has to scan character by character — it exists here to show
 * what the length prefix buys you.
 */
export function encodeAndDecodeStringsDelimiterEscaped(strs: readonly string[]): string[] {
  throw new UnsolvedError(SLUG, "delimiter-escaped", PATH);
}

export const encodeAndDecodeStrings = defineProblem(SLUG, {
  "length-prefixed": encodeAndDecodeStringsLengthPrefixed,
  "delimiter-escaped": encodeAndDecodeStringsDelimiterEscaped,
});
