"""347. Top K Frequent Elements

Return the `k` most frequent values in `nums`. LeetCode accepts any order; this repo pins a
canonical one — descending by frequency, then ascending by value — so the three implementations
can be compared byte for byte.

    https://leetcode.com/problems/top-k-frequent-elements/

Each function below is an exercise. Replace the `raise` with your implementation, then:

    make test-python

Stuck? `make show SLUG=top-k-frequent-elements` prints a worked answer.
"""

from __future__ import annotations

from neetcode_core.errors import UnsolvedError
from neetcode_core.registry import solution

SLUG = "top-k-frequent-elements"
PATH = "packages/core-python/src/neetcode_core/arrays_and_hashing/top_k_frequent_elements.py"


@solution(SLUG, approach="sorting")
def top_k_frequent_sorting(nums: list[int], k: int) -> list[int]:
    """Count, then sort by frequency — target: O(n log n) time, O(n) space.

    Tally, then sort the distinct values. The sort dominates, but on the small inputs this problem
    usually sees it is the fastest of the two.
    """
    raise UnsolvedError(SLUG, "sorting", PATH)


@solution(SLUG, approach="bucket-sort")
def top_k_frequent_bucket_sort(nums: list[int], k: int) -> list[int]:
    """Bucket by frequency — target: O(n) time, O(n) space.

    A count can never exceed n, so an array of n+1 buckets indexed by frequency replaces the sort
    entirely. Walking it from the back yields values in descending frequency for free.
    """
    raise UnsolvedError(SLUG, "bucket-sort", PATH)
