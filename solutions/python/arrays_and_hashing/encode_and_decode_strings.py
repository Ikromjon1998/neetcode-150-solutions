"""271. Encode and Decode Strings — https://leetcode.com/problems/encode-and-decode-strings/

Flatten a list of arbitrary strings into one string, and recover the list exactly.

Unlike every other problem here this is a design exercise with two halves, so the registered
function runs the **full round trip**: it encodes the input and returns what decoding produces.
A correct implementation therefore returns its input unchanged — and any encoding that cannot
survive delimiters, empty strings or leading digits will not.
"""

from __future__ import annotations

from neetcode_core.registry import solution

SLUG = "encode-and-decode-strings"

SENTINEL = "#"
DELIMITER = ":"
ESCAPE = "\\"


def encode_length_prefixed(strs: list[str]) -> str:
    """`<length>#<payload>` for each string, concatenated."""
    return "".join(f"{len(word)}{SENTINEL}{word}" for word in strs)


def decode_length_prefixed(encoded: str) -> list[str]:
    """Read a length, skip the sentinel, take exactly that many characters, repeat."""
    result: list[str] = []
    cursor = 0

    while cursor < len(encoded):
        sentinel = encoded.index(SENTINEL, cursor)
        length = int(encoded[cursor:sentinel])
        start = sentinel + 1
        result.append(encoded[start : start + length])
        cursor = start + length

    return result


@solution(SLUG, approach="length-prefixed")
def encode_decode_length_prefixed(strs: list[str]) -> list[str]:
    """Round trip through the length-prefixed encoding. Time O(n), space O(n).

    The length is read *before* the payload, so the payload is never scanned and may contain
    absolutely anything — `#`, digits, newlines, `4#test`. That is the whole reason this is the
    standard answer: it makes the payload opaque rather than trying to escape it.

    Note that `len()` counts **code points** in Python, and the slice that reads the payload
    back also works in code points, so the two agree. That symmetry is not free in every
    language — see the PHP version, where the obvious `strlen` counts bytes.
    """
    return decode_length_prefixed(encode_length_prefixed(strs))


def encode_delimiter_escaped(strs: list[str]) -> str:
    r"""Join on `:`, escaping `\` first and then `:` inside each payload.

    Order matters: escape the escape character before the delimiter, or decoding cannot tell
    `\:` (an escaped delimiter) from `\` followed by a real delimiter.
    """
    escaped = [
        word.replace(ESCAPE, ESCAPE * 2).replace(DELIMITER, ESCAPE + DELIMITER)
        for word in strs
    ]
    return DELIMITER.join(escaped)


def decode_delimiter_escaped(encoded: str) -> list[str]:
    """Scan character by character, honouring the escape."""
    result: list[str] = []
    current: list[str] = []
    index = 0

    while index < len(encoded):
        char = encoded[index]
        if char == ESCAPE and index + 1 < len(encoded):
            current.append(encoded[index + 1])
            index += 2
        elif char == DELIMITER:
            result.append("".join(current))
            current = []
            index += 1
        else:
            current.append(char)
            index += 1

    result.append("".join(current))
    return result


@solution(SLUG, approach="delimiter-escaped")
def encode_decode_delimiter_escaped(strs: list[str]) -> list[str]:
    """Round trip through the escaped-delimiter encoding. Time O(n), space O(n).

    Correct, but strictly more work than the length prefix: every character of every payload is
    examined twice — once to escape it and once to unescape it — and the decoder cannot skip
    ahead. It is here to make the length prefix's advantage concrete rather than asserted.

    The empty list is the one case the delimiter approach cannot represent: joining nothing
    produces `""`, and splitting `""` produces `[""]`, not `[]`. Handled explicitly below,
    which is itself the lesson — a delimiter-based format needs a special case that a
    length-prefixed one does not.
    """
    if not strs:
        return []
    return decode_delimiter_escaped(encode_delimiter_escaped(strs))
