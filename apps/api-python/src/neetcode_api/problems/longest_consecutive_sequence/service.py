"""Application service for Longest Consecutive Sequence.

The seam between HTTP and the algorithm: plain values in, plain values out.
"""

from __future__ import annotations

from neetcode_core import get_solution

from neetcode_api.timing import timed

SLUG = "longest-consecutive-sequence"


class LongestConsecutiveSequenceService:
    def solve(self, nums: list[int], approach: str) -> tuple[int, int]:
        """Return `(result, elapsed_microseconds)`."""
        algorithm = get_solution(SLUG, approach=approach)
        return timed(algorithm, nums)
