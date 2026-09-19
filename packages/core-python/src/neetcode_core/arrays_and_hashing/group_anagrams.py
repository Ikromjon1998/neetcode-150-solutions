"""49. Group Anagrams

Group the strings so that every group holds exactly the mutual anagrams. LeetCode accepts any
order; this repo pins a canonical one — each group sorted ascending, and the groups themselves
sorted by their first member — so the three implementations can be compared byte for byte.

    https://leetcode.com/problems/group-anagrams/

Each function below is an exercise. Replace the `raise` with your implementation, then:

    make test-python

Stuck? `make show SLUG=group-anagrams` prints a worked answer.
"""

from __future__ import annotations

from neetcode_core.errors import UnsolvedError
from neetcode_core.registry import solution

SLUG = "group-anagrams"
PATH = "packages/core-python/src/neetcode_core/arrays_and_hashing/group_anagrams.py"


@solution(SLUG, approach="sorted-key")
def group_anagrams_sorted_key(strs: list[str]) -> list[list[str]]:
    """Sorted string as the key — target: O(n k log k) time, O(n k) space.

    Two words are anagrams exactly when their sorted forms match, so the sorted string is a
    ready-made group key. k is the word length; the log k is the per-word sort.
    """
    raise UnsolvedError(SLUG, "sorted-key", PATH)


@solution(SLUG, approach="count-key")
def group_anagrams_count_key(strs: list[str]) -> list[list[str]]:
    """Character-count tuple as the key — target: O(n k) time, O(n k) space.

    Replace the per-word sort with a 26-slot tally rendered as a key. Linear in the word length,
    and the clearest place in this repo where the three languages disagree about what may be used
    as a map key.
    """
    raise UnsolvedError(SLUG, "count-key", PATH)
