"""128. Longest Consecutive Sequence — https://leetcode.com/problems/longest-consecutive-sequence/

The length of the longest run of consecutive integers present in `nums`. Position in the array
is irrelevant, and duplicates do not lengthen a run.
"""

from __future__ import annotations

from itertools import pairwise

from neetcode_core.registry import solution

SLUG = "longest-consecutive-sequence"


@solution(SLUG, approach="sorting")
def longest_consecutive_sorting(nums: list[int]) -> int:
    """Sort, then walk. Time O(n log n), space O(n).

    The trap is duplicates: `[1, 2, 2, 3]` is a run of three, not four. Deduplicating through
    a `set` before sorting removes the problem entirely, which is cheaper to reason about than
    teaching the walk to skip zero-differences.

    `itertools.pairwise` (3.10+) says "every adjacent pair" directly. The TypeScript and PHP
    versions both index manually with `ordered[i] - ordered[i - 1]`.
    """
    if not nums:
        return 0

    ordered = sorted(set(nums))
    longest = current = 1

    for previous, value in pairwise(ordered):
        current = current + 1 if value - previous == 1 else 1
        longest = max(longest, current)

    return longest


@solution(SLUG, approach="hash-set")
def longest_consecutive_hash_set(nums: list[int]) -> int:
    """Walk each run exactly once, from its start. Time O(n), space O(n).

    The `value - 1 not in seen` guard is the entire algorithm. Without it the inner loop
    re-walks every run from every one of its members and the whole thing degrades to O(n^2) —
    which is the version people write first and then wonder why it is not faster than sorting.

    With the guard, each run is walked from its smallest member and from nowhere else, so
    across the whole input the inner loop takes O(n) steps in total.
    """
    seen = set(nums)
    longest = 0

    for value in seen:
        if value - 1 in seen:
            continue  # not the start of a run — it will be counted from further down

        length = 1
        while value + length in seen:
            length += 1
        longest = max(longest, length)

    return longest
