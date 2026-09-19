<?php

declare(strict_types=1);

namespace NeetCode\Core\ArraysAndHashing;

use NeetCode\Core\Contracts\ProblemDefinition;

/**
 * 217. Contains Duplicate — https://leetcode.com/problems/contains-duplicate/
 *
 * Return true when any value appears in `$nums` more than once.
 */
final class ContainsDuplicate implements ProblemDefinition
{
    public const SLUG = 'contains-duplicate';

    public static function slug(): string
    {
        return self::SLUG;
    }

    /** @return array<string, callable> */
    public static function solutions(): array
    {
        return [
            'brute-force' => self::bruteForce(...),
            'sorting' => self::sorting(...),
            'hash-set' => self::hashSet(...),
        ];
    }

    /**
     * Compare every pair. Time O(n^2), space O(1).
     *
     * @param  list<int>  $nums
     */
    public static function bruteForce(array $nums): bool
    {
        $length = count($nums);

        for ($i = 0; $i < $length; $i++) {
            for ($j = $i + 1; $j < $length; $j++) {
                if ($nums[$i] === $nums[$j]) {
                    return true;
                }
            }
        }

        return false;
    }

    /**
     * Sort, then check adjacent pairs. Time O(n log n), space O(n).
     *
     * `sort()` takes its argument by reference and mutates it — but `$nums` is already a copy,
     * because PHP arrays are value types with copy-on-write. That is the opposite of
     * JavaScript, where the array is a reference and `[...nums]` is required to avoid
     * mutating the caller's data.
     *
     * @param  list<int>  $nums
     */
    public static function sorting(array $nums): bool
    {
        sort($nums);

        for ($i = 1, $length = count($nums); $i < $length; $i++) {
            if ($nums[$i] === $nums[$i - 1]) {
                return true;
            }
        }

        return false;
    }

    /**
     * Set membership; return on the first repeat. Time O(n), space O(n).
     *
     * PHP has no Set type, so an array's keys stand in for one — which works precisely because
     * array keys are unique and integer keys stay integers. `isset()` on a key is the
     * membership test.
     *
     * `count(array_unique($nums)) !== count($nums)` is the popular one-liner and is strictly
     * worse: it always consumes the whole input, and `array_unique` compares as *strings* by
     * default, so `[1, "1"]` would count as a duplicate.
     *
     * @param  list<int>  $nums
     */
    public static function hashSet(array $nums): bool
    {
        /** @var array<int, true> $seen */
        $seen = [];

        foreach ($nums as $value) {
            if (isset($seen[$value])) {
                return true;
            }

            $seen[$value] = true;
        }

        return false;
    }
}
