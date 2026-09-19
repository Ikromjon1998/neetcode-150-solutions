/**
 * 238. Product of Array Except Self — https://leetcode.com/problems/product-of-array-except-self/
 *
 * Each output position holds the product of every input element except the one beneath it.
 *
 * Division is forbidden, and that restriction is doing real work: "total ÷ nums[i]" breaks the
 * moment a zero appears, and breaks differently for one zero than for two.
 */

import { defineProblem } from "../define-problem";

export const SLUG = "product-of-array-except-self";

/**
 * Collapse `-0` to `0`.
 *
 * IEEE 754 has a signed zero and JavaScript exposes it. For `[-1, 1, 0, -3, 3]` the product for
 * index 0 is `1 * 0 * -3 * 3`, which evaluates left to right as `0 → -0 → -0`. Python's and
 * PHP's integers have no signed zero at all, so both produce a plain `0` and this
 * implementation was the odd one out — caught by the shared contract's "contains one zero"
 * case, which is exactly what it is there for.
 *
 * Worth knowing how narrowly this escapes notice: `-0 === 0` is `true`, so no ordinary
 * comparison sees it, and `JSON.stringify(-0)` is `"0"`, so the HTTP response would have agreed
 * with the other two apps regardless. Only a structural deep-equal — which is what the test
 * does, and what `Object.is` does — can tell them apart.
 *
 * `value === 0` matches both zeros, so returning the literal normalises either to `+0`.
 */
function normalizeZero(value: number): number {
  return value === 0 ? 0 : value;
}

/**
 * Recompute each product from scratch. Time O(n^2), space O(1) beyond the output.
 *
 * The empty product is 1, which is why a single-element input returns `[1]`.
 */
export function productOfArrayExceptSelfBruteForce(nums: readonly number[]): number[] {
  const result: number[] = [];
  for (let i = 0; i < nums.length; i++) {
    let product = 1;
    for (let j = 0; j < nums.length; j++) {
      if (i !== j) product *= nums[j]!;
    }
    result.push(normalizeZero(product));
  }
  return result;
}

/**
 * Left products, then fold the right products in. Time O(n), space O(1) beyond the output.
 *
 * The answer at `i` factorises into everything left of `i` times everything right of `i`. The
 * first pass writes the left half into the output array; the second walks backwards carrying
 * the right half in a single variable, so no second array is ever allocated.
 *
 * `new Array(n).fill(1)` rather than `new Array(n)`: the latter creates a *sparse* array whose
 * holes are `undefined`, and `undefined *= x` yields `NaN`. Python's `[1] * n` and PHP's
 * `array_fill` have no equivalent hazard.
 */
export function productOfArrayExceptSelfPrefixSuffix(nums: readonly number[]): number[] {
  const result = new Array<number>(nums.length).fill(1);

  let prefix = 1;
  for (let i = 0; i < nums.length; i++) {
    result[i] = prefix;
    prefix *= nums[i]!;
  }

  let suffix = 1;
  for (let i = nums.length - 1; i >= 0; i--) {
    result[i] = normalizeZero(result[i]! * suffix);
    suffix *= nums[i]!;
  }

  return result;
}

export const productOfArrayExceptSelf = defineProblem(SLUG, {
  "brute-force": productOfArrayExceptSelfBruteForce,
  "prefix-suffix": productOfArrayExceptSelfPrefixSuffix,
});
