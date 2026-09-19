<?php

declare(strict_types=1);

namespace NeetCode\Core\ArraysAndHashing;

use NeetCode\Core\Contracts\ProblemDefinition;

/**
 * 238. Product of Array Except Self — https://leetcode.com/problems/product-of-array-except-self/
 *
 * Each output position holds the product of every input element except the one beneath it.
 *
 * Division is forbidden, and that restriction is doing real work: "total / $nums[$i]" breaks
 * the moment a zero appears, and breaks differently for one zero than for two.
 */
final class ProductOfArrayExceptSelf implements ProblemDefinition
{
    public const SLUG = 'product-of-array-except-self';

    public static function slug(): string
    {
        return self::SLUG;
    }

    /** @return array<string, callable> */
    public static function solutions(): array
    {
        return [
            'brute-force' => self::bruteForce(...),
            'prefix-suffix' => self::prefixSuffix(...),
        ];
    }

    /**
     * Recompute each product from scratch. Time O(n^2), space O(1) beyond the output.
     *
     * The empty product is 1, which is why a single-element input returns `[1]`.
     *
     * @param  list<int>  $nums
     * @return list<int>
     */
    public static function bruteForce(array $nums): array
    {
        $result = [];

        foreach (array_keys($nums) as $i) {
            $product = 1;

            foreach ($nums as $j => $value) {
                if ($i !== $j) {
                    $product *= $value;
                }
            }

            $result[] = $product;
        }

        return $result;
    }

    /**
     * Left products, then fold the right products in. Time O(n), space O(1) beyond the output.
     *
     * The answer at `$i` factorises into everything left of `$i` times everything right of
     * `$i`. The first pass writes the left half into the output; the second walks backwards
     * carrying the right half in a single variable, so no second array is allocated.
     *
     * `array_fill(0, count($nums), 1)` rather than assigning into an empty array by index:
     * PHP would happily create a sparse array with string-ordered keys, and the result would no
     * longer be a `list`. JSON-encoding a non-list array produces an object, not an array — a
     * silent and very confusing way for this endpoint to disagree with the other two.
     *
     * @param  list<int>  $nums
     * @return list<int>
     */
    public static function prefixSuffix(array $nums): array
    {
        $length = count($nums);
        $result = array_fill(0, $length, 1);

        $prefix = 1;
        for ($i = 0; $i < $length; $i++) {
            $result[$i] = $prefix;
            $prefix *= $nums[$i];
        }

        $suffix = 1;
        for ($i = $length - 1; $i >= 0; $i--) {
            $result[$i] *= $suffix;
            $suffix *= $nums[$i];
        }

        return $result;
    }
}
