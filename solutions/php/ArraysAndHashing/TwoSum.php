<?php

declare(strict_types=1);

namespace NeetCode\Core\ArraysAndHashing;

use NeetCode\Core\Contracts\ProblemDefinition;
use NeetCode\Core\Exceptions\NoSolutionException;

/**
 * 1. Two Sum — https://leetcode.com/problems/two-sum/
 *
 * Given `$nums` and `$target`, return the indices of the two numbers adding up to `$target`.
 *
 * Both approaches below are registered and reachable from the API via `?approach=`, so you
 * can benchmark them against each other over the same input without changing any code.
 */
final class TwoSum implements ProblemDefinition
{
    public const SLUG = 'two-sum';

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
     * Check every pair. Time O(n^2), space O(1).
     *
     * Worth keeping: it is the baseline that makes the hash-map version's space cost look
     * like a bargain, and on tiny inputs it is genuinely faster because it never allocates.
     *
     * @param  list<int>  $nums
     * @return list<int>
     */
    public static function bruteForce(array $nums, int $target): array
    {
        $length = count($nums);

        for ($i = 0; $i < $length; $i++) {
            for ($j = $i + 1; $j < $length; $j++) {
                if ($nums[$i] + $nums[$j] === $target) {
                    return [$i, $j];
                }
            }
        }

        throw new NoSolutionException(self::SLUG, "No two entries of nums sum to {$target}.");
    }

    /**
     * One pass, remembering every value already seen. Time O(n), space O(n).
     *
     * PHP's array doubles as its hash map, and integer keys stay integers — no stringification
     * and no collision between `0` and `-0` the way a plain JavaScript object would have.
     * `isset()` rather than `array_key_exists()` because the stored values are indices and are
     * never null, so the faster check is also the correct one.
     *
     * @param  list<int>  $nums
     * @return list<int>
     */
    public static function hashMap(array $nums, int $target): array
    {
        /** @var array<int, int> $seen */
        $seen = [];

        foreach ($nums as $index => $value) {
            $complement = $target - $value;

            if (isset($seen[$complement])) {
                return [$seen[$complement], $index];
            }

            $seen[$value] = $index;
        }

        throw new NoSolutionException(self::SLUG, "No two entries of nums sum to {$target}.");
    }
}
