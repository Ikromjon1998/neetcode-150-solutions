"""1. Two Sum — https://leetcode.com/problems/two-sum/

Given `nums` and `target`, return the indices of the two numbers adding up to `target`.

Both approaches below are registered and reachable from the API via `?approach=`, so you can
benchmark them against each other over the same input without changing any code.
"""

from __future__ import annotations

from neetcode_core.errors import NoSolutionError
from neetcode_core.registry import solution

SLUG = "two-sum"


@solution(SLUG, approach="brute-force")
def two_sum_brute_force(nums: list[int], target: int) -> list[int]:
    """Check every pair.

    Time O(n^2), space O(1). Worth keeping: it is the baseline that makes the hash-map
    version's space cost look like a bargain, and on tiny inputs it is genuinely faster
    because it never allocates.
    """
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]
    raise NoSolutionError(SLUG, f"No two entries of nums sum to {target}.")


@solution(SLUG, approach="hash-map")
def two_sum_hash_map(nums: list[int], target: int) -> list[int]:
    """One pass, remembering every value already seen.

    Time O(n), space O(n). The trick is to look *backwards* for the complement instead of
    forwards for the partner: by the time the second number of the pair is the current
    element, the first one is guaranteed to already be in `seen`.
    """
    seen: dict[int, int] = {}
    for index, value in enumerate(nums):
        complement = target - value
        if complement in seen:
            return [seen[complement], index]
        seen[value] = index
    raise NoSolutionError(SLUG, f"No two entries of nums sum to {target}.")
