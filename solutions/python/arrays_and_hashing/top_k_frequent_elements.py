"""347. Top K Frequent Elements — https://leetcode.com/problems/top-k-frequent-elements/

The `k` most frequent values in `nums`.

LeetCode accepts any order. This repo pins a canonical one — **descending by frequency, then
ascending by value** — because three implementations that return the same set in three
different orders cannot be compared byte for byte, and comparing them is the point here.
"""

from __future__ import annotations

from collections import Counter

from neetcode_core.registry import solution

SLUG = "top-k-frequent-elements"


@solution(SLUG, approach="sorting")
def top_k_frequent_sorting(nums: list[int], k: int) -> list[int]:
    """Tally, then sort the distinct values. Time O(n log n), space O(n).

    `key=lambda item: (-item[1], item[0])` is the canonical order in one expression: negate the
    count to sort it descending while leaving the value ascending. Python's sort is stable, so
    the tuple key expresses both directions without a custom comparator — the TypeScript and
    PHP versions both need an explicit two-term comparison function.
    """
    counts = Counter(nums)
    ordered = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    return [value for value, _ in ordered[:k]]


@solution(SLUG, approach="bucket-sort")
def top_k_frequent_bucket_sort(nums: list[int], k: int) -> list[int]:
    """Bucket the values by frequency. Time O(n), space O(n).

    No value can occur more than `len(nums)` times, so an array of `n + 1` buckets indexed by
    frequency has somewhere to put everything. Walking it from the back yields descending
    frequency without ever sorting.

    Each bucket is sorted internally only to honour the ascending-value tie-break this repo
    pins. That sort is over values sharing one frequency, so it does not change the linear
    bound in any realistic input — but it is a real cost, and it exists because of the
    canonical ordering rather than because of the algorithm.
    """
    if k <= 0:
        return []

    counts = Counter(nums)
    buckets: list[list[int]] = [[] for _ in range(len(nums) + 1)]
    for value, count in counts.items():
        buckets[count].append(value)

    result: list[int] = []
    for count in range(len(buckets) - 1, 0, -1):
        for value in sorted(buckets[count]):
            result.append(value)
            if len(result) == k:
                return result

    return result
