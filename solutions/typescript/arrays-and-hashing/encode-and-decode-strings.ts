/**
 * 271. Encode and Decode Strings — https://leetcode.com/problems/encode-and-decode-strings/
 *
 * Flatten a list of arbitrary strings into one string, and recover the list exactly.
 *
 * A design exercise with two halves, so the registered function runs the full round trip: it
 * encodes the input and returns what decoding produces. A correct implementation therefore
 * returns its input unchanged — and any encoding that cannot survive delimiters, empty strings
 * or leading digits will not.
 */

import { defineProblem } from "../define-problem";

export const SLUG = "encode-and-decode-strings";

const SENTINEL = "#";
const DELIMITER = ":";
const ESCAPE = "\\";

/** `<length>#<payload>` for each string, concatenated. */
export function encodeLengthPrefixed(strs: readonly string[]): string {
  return strs.map((word) => `${[...word].length}${SENTINEL}${word}`).join("");
}

/**
 * Read a length, skip the sentinel, take exactly that many characters, repeat.
 *
 * The slicing is done over an array of code points rather than the raw string. `String.slice`
 * counts UTF-16 code units, so a length measured in code points and a slice measured in code
 * units disagree the moment an emoji appears — and the decoder silently returns garbage rather
 * than throwing. Python and PHP each have their own version of this mismatch; none of the three
 * gets it for free.
 */
export function decodeLengthPrefixed(encoded: string): string[] {
  const chars = [...encoded];
  const result: string[] = [];
  let cursor = 0;

  while (cursor < chars.length) {
    let sentinel = cursor;
    while (chars[sentinel] !== SENTINEL) sentinel++;

    const length = Number(chars.slice(cursor, sentinel).join(""));
    const start = sentinel + 1;
    result.push(chars.slice(start, start + length).join(""));
    cursor = start + length;
  }

  return result;
}

/**
 * Round trip through the length-prefixed encoding. Time O(n), space O(n).
 *
 * The length is read before the payload, so the payload is never scanned and may contain
 * anything at all — `#`, digits, `4#test`. That is why this is the standard answer: it makes
 * the payload opaque instead of trying to escape it.
 */
export function encodeAndDecodeStringsLengthPrefixed(strs: readonly string[]): string[] {
  return decodeLengthPrefixed(encodeLengthPrefixed(strs));
}

/**
 * Join on `:`, escaping `\` first and then `:` inside each payload.
 *
 * Order matters: escape the escape character before the delimiter, or decoding cannot tell an
 * escaped delimiter from a backslash followed by a real one.
 */
export function encodeDelimiterEscaped(strs: readonly string[]): string {
  return strs
    .map((word) => word.split(ESCAPE).join(ESCAPE + ESCAPE).split(DELIMITER).join(ESCAPE + DELIMITER))
    .join(DELIMITER);
}

/** Scan code point by code point, honouring the escape. */
export function decodeDelimiterEscaped(encoded: string): string[] {
  const chars = [...encoded];
  const result: string[] = [];
  let current = "";

  for (let index = 0; index < chars.length; index++) {
    const char = chars[index]!;
    if (char === ESCAPE && index + 1 < chars.length) {
      current += chars[++index]!;
    } else if (char === DELIMITER) {
      result.push(current);
      current = "";
    } else {
      current += char;
    }
  }

  result.push(current);
  return result;
}

/**
 * Round trip through the escaped-delimiter encoding. Time O(n), space O(n).
 *
 * Correct, but strictly more work: every character is examined twice and the decoder cannot
 * skip ahead. It exists to make the length prefix's advantage concrete rather than asserted.
 *
 * The empty list is the one case a delimiter format cannot represent — joining nothing produces
 * `""`, and splitting `""` produces `[""]`, not `[]`. The special case below is itself the
 * lesson.
 */
export function encodeAndDecodeStringsDelimiterEscaped(strs: readonly string[]): string[] {
  if (strs.length === 0) return [];
  return decodeDelimiterEscaped(encodeDelimiterEscaped(strs));
}

export const encodeAndDecodeStrings = defineProblem(SLUG, {
  "length-prefixed": encodeAndDecodeStringsLengthPrefixed,
  "delimiter-escaped": encodeAndDecodeStringsDelimiterEscaped,
});
