"""1. Two Sum

Return the indices of the two numbers in `nums` that add up to `target`. Exactly one solution
exists and the same element may not be used twice.

    https://leetcode.com/problems/two-sum/

Each function below is an exercise. Replace the `raise` with your implementation, then:

    make test-python

Stuck? `make show SLUG=two-sum` prints a worked answer.
"""

from __future__ import annotations

from neetcode_core.errors import NoSolutionError
from neetcode_core.registry import solution

SLUG = "two-sum"


@solution(SLUG, approach="brute-force")
def two_sum_brute_force(nums: list[int], target: int) -> list[int]:
    """Nested loops — target: O(n^2) time, O(1) space.

    Check every pair. Kept on purpose as the baseline the optimal approach is measured against.
    """
    length = len(nums)
    for i in range(length):
        for j in range(i + 1, length):
            if nums[i] + nums[j] == target:
                return [i, j]

    raise NoSolutionError(SLUG, f"No two entries of nums sum to {target}.")


@solution(SLUG, approach="hash-map")
def two_sum_hash_map(nums: list[int], target: int) -> list[int]:
    """One-pass hash map — target: O(n) time, O(n) space.

    Trade space for time: remember every value seen so far and look up the complement in O(1).
    """
    seen: dict[int, int] = {}

    for idx, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], idx]
        seen[num] = idx

    raise NoSolutionError(SLUG, f"No two entries of nums sum to {target}.")
