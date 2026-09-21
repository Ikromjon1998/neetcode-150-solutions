"""242. Valid Anagram

Return true when `t` is an anagram of `s` — that is, when both strings contain exactly the same
characters with exactly the same multiplicities.

    https://leetcode.com/problems/valid-anagram/

Each function below is an exercise. Replace the `raise` with your implementation, then:

    make test-python

Stuck? `make show SLUG=valid-anagram` prints a worked answer.
"""

from __future__ import annotations

from neetcode_core.registry import solution

SLUG = "valid-anagram"
PATH = "packages/core-python/src/neetcode_core/arrays_and_hashing/valid_anagram.py"


@solution(SLUG, approach="sorting")
def valid_anagram_sorting(s: str, t: str) -> bool:
    """Sort both strings — target: O(n log n) time, O(n) space.

    Two anagrams have the same sorted form. Three lines and obviously correct, which is worth
    something — but the sort dominates, and all three languages must copy the string to sort it.
    """
    return sorted(s) == sorted(t)

@solution(SLUG, approach="hash-map")
def valid_anagram_hash_map(s: str, t: str) -> bool:
    """Character frequency count — target: O(n) time, O(k) space.

    Count each character in `s`, decrement for each in `t`, and a single pass over the counts
    decides it. O(k) in the alphabet size, not the input length.
    """
    hash_map = {}
    for char in s:
        hash_map[char] = hash_map.get(char, 0) + 1
    for char in t:
        hash_map[char] = hash_map.get(char, 0) - 1
    return all(num == 0 for num in hash_map.values())
