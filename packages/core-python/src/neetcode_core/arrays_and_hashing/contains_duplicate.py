"""217. Contains Duplicate

Return true when any value appears in `nums` more than once, and false when every element is
distinct.

    https://leetcode.com/problems/contains-duplicate/

Each function below is an exercise. Replace the `raise` with your implementation, then:

    make test-python

Stuck? `make show SLUG=contains-duplicate` prints a worked answer.
"""

from __future__ import annotations

from neetcode_core.registry import solution

SLUG = "contains-duplicate"
PATH = "packages/core-python/src/neetcode_core/arrays_and_hashing/contains_duplicate.py"


@solution(SLUG, approach="brute-force")
def contains_duplicate_brute_force(nums: list[int]) -> bool:
    """Compare every pair — target: O(n^2) time, O(1) space.

    The only approach that allocates nothing. On inputs of a handful of elements it wins outright,
    which is worth seeing before dismissing it.
    """
    for index1 in range(len(nums)):
        for index2 in range(index1 + 1, len(nums)):
            if nums[index1] == nums[index2]:
                return True
    return False


@solution(SLUG, approach="sorting")
def contains_duplicate_sorting(nums: list[int]) -> bool:
    """Sort, then scan neighbours — target: O(n log n) time, O(n) space.

    Duplicates become adjacent once sorted. Not O(1) space in any of these three languages, since
    none can sort the caller's array in place without mutating it.
    """
    new_nums = sorted(nums)
    return any(new_nums[index - 1] == new_nums[index] for index in range(1, len(new_nums)))


@solution(SLUG, approach="hash-set")
def contains_duplicate_hash_set(nums: list[int]) -> bool:
    """Set membership — target: O(n) time, O(n) space.

    Return on the first repeat, so the early-exit case is far better than O(n) in practice — a
    duplicate at index 1 costs two operations regardless of input size.
    """
    hash_map = {}
    for num in nums:
        if num in hash_map:
            return True
        hash_map[num] = True
    return False
