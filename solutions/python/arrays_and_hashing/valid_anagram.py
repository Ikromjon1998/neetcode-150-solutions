"""242. Valid Anagram — https://leetcode.com/problems/valid-anagram/

`t` is an anagram of `s` when both hold exactly the same characters with exactly the same
multiplicities. Order is irrelevant; counts are everything.

Both approaches below are registered and reachable from the API via `?approach=`.
"""

from __future__ import annotations

from collections import Counter

from neetcode_core.registry import solution

SLUG = "valid-anagram"


@solution(SLUG, approach="sorting")
def valid_anagram_sorting(s: str, t: str) -> bool:
    """Two anagrams have the same sorted form.

    Time O(n log n), space O(n) — `sorted()` returns a new list, it does not sort in place.

    Obviously correct, and on short strings the C-level sort beats a Python-level count loop
    despite the worse asymptotics. Measure before assuming the O(n) version is faster.
    """
    return sorted(s) == sorted(t)


@solution(SLUG, approach="hash-map")
def valid_anagram_hash_map(s: str, t: str) -> bool:
    """Count characters in one string, decrement for the other.

    Time O(n), space O(k) in the alphabet size.

    The length check first is not an optimisation — it is what makes the rest correct. Without
    it, `Counter("a") == Counter("aa")` would already be False, but the early exit documents
    the reasoning and skips the allocation entirely for the common mismatch.

    `Counter` is the idiomatic answer here and it is implemented in C. The TypeScript and PHP
    versions have to build the tally by hand, which is the clearest single example in this
    repo of Python's standard library doing more of the work for you.
    """
    if len(s) != len(t):
        return False
    return Counter(s) == Counter(t)
