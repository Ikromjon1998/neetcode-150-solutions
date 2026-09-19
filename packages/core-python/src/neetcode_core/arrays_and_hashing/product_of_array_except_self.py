"""238. Product of Array Except Self

Return an array where each position holds the product of every element of `nums` except the one at
that position. Division is not allowed, which is what makes the problem interesting — the obvious
total-product-divided-by-self approach breaks on zeros anyway.

    https://leetcode.com/problems/product-of-array-except-self/

Each function below is an exercise. Replace the `raise` with your implementation, then:

    make test-python

Stuck? `make show SLUG=product-of-array-except-self` prints a worked answer.
"""

from __future__ import annotations

from neetcode_core.errors import UnsolvedError
from neetcode_core.registry import solution

SLUG = "product-of-array-except-self"
PATH = "packages/core-python/src/neetcode_core/arrays_and_hashing/product_of_array_except_self.py"


@solution(SLUG, approach="brute-force")
def product_except_self_brute_force(nums: list[int]) -> list[int]:
    """Recompute each product — target: O(n^2) time, O(1) space.

    For every index, multiply everything else. The baseline, and the only one that needs no
    auxiliary reasoning.
    """
    raise UnsolvedError(SLUG, "brute-force", PATH)


@solution(SLUG, approach="prefix-suffix")
def product_except_self_prefix_suffix(nums: list[int]) -> list[int]:
    """Prefix and suffix products — target: O(n) time, O(1) space.

    Each answer is (product of everything to the left) x (product of everything to the right). Two
    passes, reusing the output array as the accumulator, so the extra space is a single running
    variable.
    """
    raise UnsolvedError(SLUG, "prefix-suffix", PATH)
