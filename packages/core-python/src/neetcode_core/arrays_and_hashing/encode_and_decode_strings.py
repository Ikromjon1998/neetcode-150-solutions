"""271. Encode and Decode Strings

Design an encoding that flattens a list of arbitrary strings into one string, and a decoding that
recovers the list exactly. Unlike the other problems here this is a design exercise with two
halves, so the endpoint runs the full round trip: it encodes the input and returns what decoding
produces. A correct implementation therefore returns its input unchanged — and any encoding that
cannot survive delimiters, empty strings or digits will not.

    https://leetcode.com/problems/encode-and-decode-strings/

Each function below is an exercise. Replace the `raise` with your implementation, then:

    make test-python

Stuck? `make show SLUG=encode-and-decode-strings` prints a worked answer.
"""

from __future__ import annotations

from neetcode_core.errors import UnsolvedError
from neetcode_core.registry import solution

SLUG = "encode-and-decode-strings"
PATH = "packages/core-python/src/neetcode_core/arrays_and_hashing/encode_and_decode_strings.py"


@solution(SLUG, approach="length-prefixed")
def encode_decode_length_prefixed(strs: list[str]) -> list[str]:
    """Length prefix and sentinel — target: O(n) time, O(n) space.

    Write each string as `<length>#<string>`. The length is read before the payload, so the
    payload is never scanned for a delimiter and may contain anything at all — including `#` and
    digits. The standard answer, and the only one here that is unconditionally safe.
    """
    raise UnsolvedError(SLUG, "length-prefixed", PATH)


@solution(SLUG, approach="delimiter-escaped")
def encode_decode_delimiter_escaped(strs: list[str]) -> list[str]:
    """Escaped delimiter — target: O(n) time, O(n) space.

    Join on a delimiter, escaping any occurrence of it (and of the escape character) inside the
    payloads. Correct, but every decode has to scan character by character — it exists here to
    show what the length prefix buys you.
    """
    raise UnsolvedError(SLUG, "delimiter-escaped", PATH)
