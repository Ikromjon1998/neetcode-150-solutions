<?php

declare(strict_types=1);

namespace NeetCode\Core\ArraysAndHashing;

use NeetCode\Core\Contracts\ProblemDefinition;
use NeetCode\Core\Exceptions\NoSolutionException;

/**
 * 1. Two Sum
 *
 * Return the indices of the two numbers in `nums` that add up to `target`. Exactly one solution
 * exists and the same element may not be used twice.
 *
 * https://leetcode.com/problems/two-sum/
 *
 * Each method below is an exercise. Replace the `throw` with your implementation, then
 * run `make test-php`.
 *
 * Stuck? `make show SLUG=two-sum` prints a worked answer.
 */
final class TwoSum implements ProblemDefinition
{
    public const SLUG = 'two-sum';

    private const PATH = 'packages/core-php/src/ArraysAndHashing/TwoSum.php';

    public static function slug(): string
    {
        return self::SLUG;
    }

    /** @return array<string, callable> */
    public static function solutions(): array
    {
        return [
            'brute-force' => self::bruteForce(...),
            'hash-map' => self::hashMap(...),
        ];
    }

    /**
     * Nested loops — target: O(n^2) time, O(1) space.
     *
     * Check every pair. Kept on purpose as the baseline the optimal approach is measured against.
     */
    public static function bruteForce(array $nums, int $target): array
    {
        $lengthOfArray = count($nums);

        for($i = 0; $i < $lengthOfArray; ++$i) {
            for ($j = $i + 1; $j < $lengthOfArray; ++$j) {
                if ($nums[$i] + $nums[$j] === $target) {
                    return [$i, $j];
                }
            }
        }

        throw new NoSolutionException(self::SLUG, 'No two numbers sum to the target.');
    }

    /**
     * One-pass hash map — target: O(n) time, O(n) space.
     *
     * Trade space for time: remember every value seen so far and look up the complement in O(1).
     */
    public static function hashMap(array $nums, int $target): array
    {
        $seen = [];

        foreach($nums as $i => $num) {
            $complement = $target - $num;

            if(isset($seen[$complement])) {
                return [$seen[$complement], $i];
            }

            $seen[$num] = $i;
        }

        throw new NoSolutionException(self::SLUG, 'No two numbers sum to the target.');
    }
}
