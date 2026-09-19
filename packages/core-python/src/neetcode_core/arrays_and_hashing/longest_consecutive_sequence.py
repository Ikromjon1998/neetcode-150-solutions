"""128. Longest Consecutive Sequence

Return the length of the longest run of consecutive integers present in `nums`. The elements need
not be adjacent in the array, and duplicates do not extend a run.

    https://leetcode.com/problems/longest-consecutive-sequence/

Each function below is an exercise. Replace the `raise` with your implementation, then:

    make test-python

Stuck? `make show SLUG=longest-consecutive-sequence` prints a worked answer.
"""

from __future__ import annotations

from neetcode_core.errors import UnsolvedError
from neetcode_core.registry import solution

SLUG = "longest-consecutive-sequence"
PATH = "packages/core-python/src/neetcode_core/arrays_and_hashing/longest_consecutive_sequence.py"


@solution(SLUG, approach="sorting")
def longest_consecutive_sorting(nums: list[int]) -> int:
    """Sort, then walk — target: O(n log n) time, O(n) space.

    Once sorted, a run is a stretch of neighbours differing by exactly one. Duplicates must be
    skipped rather than counted, which is the detail this approach gets wrong first.
    """
    raise UnsolvedError(SLUG, "sorting", PATH)


@solution(SLUG, approach="hash-set")
def longest_consecutive_hash_set(nums: list[int]) -> int:
    """Start only at run beginnings — target: O(n) time, O(n) space.

    Put everything in a set, then walk a run only from a value whose predecessor is absent. That
    guard is what keeps it O(n) — without it the inner loop re-walks every run from every member
    and it degrades to O(n^2).
    """
    raise UnsolvedError(SLUG, "hash-set", PATH)
