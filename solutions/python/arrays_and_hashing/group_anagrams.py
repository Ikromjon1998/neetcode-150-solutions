"""49. Group Anagrams — https://leetcode.com/problems/group-anagrams/

Group the input strings so that each group holds exactly the mutual anagrams.

LeetCode accepts any order. This repo pins a canonical one — each group sorted ascending, and
the groups sorted by their first member — so the three implementations can be compared byte
for byte.
"""

from __future__ import annotations

from collections import defaultdict

from neetcode_core.registry import solution

SLUG = "group-anagrams"


def _canonical(groups: list[list[str]]) -> list[list[str]]:
    """Impose this repo's ordering. Not part of the algorithm; part of the comparison."""
    ordered = [sorted(group) for group in groups]
    ordered.sort()
    return ordered


@solution(SLUG, approach="sorted-key")
def group_anagrams_sorted_key(strs: list[str]) -> list[list[str]]:
    """Key each word by its sorted form. Time O(n·k log k), space O(n·k).

    Two words are anagrams exactly when their sorted forms are equal, so the sorted string is a
    ready-made group key. `k` is the word length; the `log k` is the per-word sort.
    """
    groups: dict[str, list[str]] = defaultdict(list)
    for word in strs:
        groups["".join(sorted(word))].append(word)
    return _canonical(list(groups.values()))


@solution(SLUG, approach="count-key")
def group_anagrams_count_key(strs: list[str]) -> list[list[str]]:
    """Key each word by its character tally. Time O(n·k), space O(n·k).

    Replaces the per-word sort with a single pass that builds a 26-slot tally, then uses that
    tally as the key — linear in the word length.

    The key must be hashable, which is where the three languages part company most sharply.
    Python can use a `tuple` directly. TypeScript has to serialise the counts into a string
    because `Map` compares array keys by reference. PHP has no choice at all: array keys are
    `int|string`, so a string it is.
    """
    groups: dict[tuple[int, ...], list[str]] = defaultdict(list)
    for word in strs:
        counts = [0] * 26
        for char in word:
            counts[ord(char) - ord("a")] += 1
        groups[tuple(counts)].append(word)
    return _canonical(list(groups.values()))
