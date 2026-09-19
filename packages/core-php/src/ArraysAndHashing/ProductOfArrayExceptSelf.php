<?php

declare(strict_types=1);

namespace NeetCode\Core\ArraysAndHashing;

use NeetCode\Core\Contracts\ProblemDefinition;
use NeetCode\Core\Exceptions\UnsolvedException;

/**
 * 238. Product of Array Except Self
 *
 * Return an array where each position holds the product of every element of `nums` except the one
 * at that position. Division is not allowed, which is what makes the problem interesting — the
 * obvious total-product-divided-by-self approach breaks on zeros anyway.
 *
 * https://leetcode.com/problems/product-of-array-except-self/
 *
 * Each method below is an exercise. Replace the `throw` with your implementation, then
 * run `make test-php`.
 *
 * Stuck? `make show SLUG=product-of-array-except-self` prints a worked answer.
 */
final class ProductOfArrayExceptSelf implements ProblemDefinition
{
    public const SLUG = 'product-of-array-except-self';

    private const PATH = 'packages/core-php/src/ArraysAndHashing/ProductOfArrayExceptSelf.php';

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
     * Recompute each product — target: O(n^2) time, O(1) space.
     *
     * For every index, multiply everything else. The baseline, and the only one that needs no
     * auxiliary reasoning.
     */
    public static function bruteForce(array $nums): array
    {
        throw new UnsolvedException(self::SLUG, 'brute-force', self::PATH);
    }

    /**
     * Prefix and suffix products — target: O(n) time, O(1) space.
     *
     * Each answer is (product of everything to the left) x (product of everything to the right).
     * Two passes, reusing the output array as the accumulator, so the extra space is a single
     * running variable.
     */
    public static function prefixSuffix(array $nums): array
    {
        throw new UnsolvedException(self::SLUG, 'prefix-suffix', self::PATH);
    }
}
