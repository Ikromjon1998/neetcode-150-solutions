"""Application service for Top K Frequent Elements.

The seam between HTTP and the algorithm: plain values in, plain values out.
"""

from __future__ import annotations

from neetcode_core import get_solution

from neetcode_api.timing import timed

SLUG = "top-k-frequent-elements"


class TopKFrequentElementsService:
    def solve(self, nums: list[int], k: int, approach: str) -> tuple[list[int], int]:
        """Return `(result, elapsed_microseconds)`."""
        algorithm = get_solution(SLUG, approach=approach)
        return timed(algorithm, nums, k)
