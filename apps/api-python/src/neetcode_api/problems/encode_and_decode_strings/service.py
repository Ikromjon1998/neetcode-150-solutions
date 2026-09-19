"""Application service for Encode and Decode Strings.

The seam between HTTP and the algorithm: plain values in, plain values out.
"""

from __future__ import annotations

from neetcode_core import get_solution

from neetcode_api.timing import timed

SLUG = "encode-and-decode-strings"


class EncodeAndDecodeStringsService:
    def solve(self, strs: list[str], approach: str) -> tuple[list[str], int]:
        """Return `(result, elapsed_microseconds)`."""
        algorithm = get_solution(SLUG, approach=approach)
        return timed(algorithm, strs)
