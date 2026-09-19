"""238. Product of Array Except Self — https://leetcode.com/problems/product-of-array-except-self/

Each output position holds the product of every input element *except* the one beneath it.

Division is forbidden by the problem, and that restriction is doing real work: the obvious
"total product ÷ nums[i]" breaks the moment a zero appears, and breaks differently for one zero
than for two.
"""

from __future__ import annotations

from neetcode_core.registry import solution

SLUG = "product-of-array-except-self"


@solution(SLUG, approach="brute-force")
def product_except_self_brute_force(nums: list[int]) -> list[int]:
    """Recompute each product from scratch. Time O(n^2), space O(1) beyond the output.

    The empty product is 1, which is why a single-element input returns `[1]` rather than
    `[0]` or an error. Worth stating out loud — it is the case every rewrite gets wrong.
    """
    result = []
    for i in range(len(nums)):
        product = 1
        for j, value in enumerate(nums):
            if i != j:
                product *= value
        result.append(product)
    return result


@solution(SLUG, approach="prefix-suffix")
def product_except_self_prefix_suffix(nums: list[int]) -> list[int]:
    """Left products, then fold the right products in. Time O(n), space O(1) beyond the output.

    The insight is that the answer at `i` factorises into everything left of `i` times
    everything right of `i`. The first pass writes the left half into the output array; the
    second walks backwards carrying the right half in a single variable, so no second array is
    ever allocated.

    The output array does not count toward the space bound — that is the problem's own
    convention, and it is the only reason this counts as O(1).
    """
    result = [1] * len(nums)

    prefix = 1
    for i, value in enumerate(nums):
        result[i] = prefix
        prefix *= value

    suffix = 1
    for i in range(len(nums) - 1, -1, -1):
        result[i] *= suffix
        suffix *= nums[i]

    return result
