"""217. Contains Duplicate — https://leetcode.com/problems/contains-duplicate/

Return True when any value appears in `nums` more than once.

Three approaches are registered, which makes this the best problem in the repo for watching
the `?approach=` comparison actually mean something: the asymptotics genuinely diverge once
the input is large.
"""

from __future__ import annotations

from neetcode_core.registry import solution

SLUG = "contains-duplicate"


@solution(SLUG, approach="brute-force")
def contains_duplicate_brute_force(nums: list[int]) -> bool:
    """Compare every pair. Time O(n^2), space O(1).

    The only approach here that allocates nothing. Worth keeping for exactly that reason —
    for n below roughly twenty it beats both of the others in every one of the three
    languages, because building a set or a sorted copy costs more than the comparisons do.
    """
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] == nums[j]:
                return True
    return False


@solution(SLUG, approach="sorting")
def contains_duplicate_sorting(nums: list[int]) -> bool:
    """Sort, then check adjacent pairs. Time O(n log n), space O(n).

    `sorted()` returns a new list rather than sorting in place, which is the right call in a
    library: mutating the caller's argument would be a surprise. That is also why this is O(n)
    space and not O(1).

    `itertools.pairwise` (3.10+) expresses "every adjacent pair" directly. The TypeScript and
    PHP versions both index into the array manually.
    """
    from itertools import pairwise

    return any(a == b for a, b in pairwise(sorted(nums)))


@solution(SLUG, approach="hash-set")
def contains_duplicate_hash_set(nums: list[int]) -> bool:
    """Remember what has been seen; return on the first repeat. Time O(n), space O(n).

    The one-liner `len(set(nums)) != len(nums)` is shorter and is what most people write. It is
    also strictly worse: it always consumes the entire input, while this version returns after
    two operations when the duplicate sits at index 1. Big-O hides that difference; the
    `elapsedMicros` field in the API response does not.
    """
    seen: set[int] = set()
    for value in nums:
        if value in seen:
            return True
        seen.add(value)
    return False
