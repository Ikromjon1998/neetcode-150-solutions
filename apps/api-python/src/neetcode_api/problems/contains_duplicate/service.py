"""Application service for Contains Duplicate.

The seam between HTTP and the algorithm: plain values in, plain values out.
"""

from __future__ import annotations

from neetcode_core import get_solution

from neetcode_api.timing import timed

SLUG = "contains-duplicate"


class ContainsDuplicateService:
    def solve(self, nums: list[int], approach: str) -> tuple[bool, int]:
        """Return `(result, elapsed_microseconds)`."""
        algorithm = get_solution(SLUG, approach=approach)
        return timed(algorithm, nums)
