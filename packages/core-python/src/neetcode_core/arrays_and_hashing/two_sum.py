"""1. Two Sum

Return the indices of the two numbers in `nums` that add up to `target`. Exactly one solution
exists and the same element may not be used twice.

    https://leetcode.com/problems/two-sum/

Each function below is an exercise. Replace the `raise` with your implementation, then:

    make test-python

Stuck? `make show SLUG=two-sum` prints a worked answer.
"""

from __future__ import annotations

from neetcode_core.errors import UnsolvedError
from neetcode_core.registry import solution

SLUG = "two-sum"
PATH = "packages/core-python/src/neetcode_core/arrays_and_hashing/two_sum.py"


@solution(SLUG, approach="brute-force")
def two_sum_brute_force(nums: list[int], target: int) -> list[int]:
    """Nested loops — target: O(n^2) time, O(1) space.

    Check every pair. Kept on purpose as the baseline the optimal approach is measured against.
    """
    raise UnsolvedError(SLUG, "brute-force", PATH)


@solution(SLUG, approach="hash-map")
def two_sum_hash_map(nums: list[int], target: int) -> list[int]:
    """One-pass hash map — target: O(n) time, O(n) space.

    Trade space for time: remember every value seen so far and look up the complement in O(1).
    """
    raise UnsolvedError(SLUG, "hash-map", PATH)
