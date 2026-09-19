"""Application service for Product of Array Except Self.

The seam between HTTP and the algorithm: plain values in, plain values out.
"""

from __future__ import annotations

from neetcode_core import get_solution

from neetcode_api.timing import timed

SLUG = "product-of-array-except-self"


class ProductOfArrayExceptSelfService:
    def solve(self, nums: list[int], approach: str) -> tuple[list[int], int]:
        """Return `(result, elapsed_microseconds)`."""
        algorithm = get_solution(SLUG, approach=approach)
        return timed(algorithm, nums)
