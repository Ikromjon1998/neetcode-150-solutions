<?php

declare(strict_types=1);

namespace NeetCode\Core\ArraysAndHashing;

use NeetCode\Core\Contracts\ProblemDefinition;
use NeetCode\Core\Exceptions\UnsolvedException;

/**
 * 217. Contains Duplicate
 *
 * Return true when any value appears in `nums` more than once, and false when every element is
 * distinct.
 *
 * https://leetcode.com/problems/contains-duplicate/
 *
 * Each method below is an exercise. Replace the `throw` with your implementation, then
 * run `make test-php`.
 *
 * Stuck? `make show SLUG=contains-duplicate` prints a worked answer.
 */
final class ContainsDuplicate implements ProblemDefinition
{
    public const SLUG = 'contains-duplicate';

    private const PATH = 'packages/core-php/src/ArraysAndHashing/ContainsDuplicate.php';

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
     * Compare every pair — target: O(n^2) time, O(1) space.
     *
     * The only approach that allocates nothing. On inputs of a handful of elements it wins
     * outright, which is worth seeing before dismissing it.
     */
    public static function bruteForce(array $nums): bool
    {
        for($i = 0; $i < count($nums); $i++) {
            for($j = $i + 1; $j < count($nums); $j++) {
                if ($nums[$i] === $nums[$j]) {
                    return true;
                }
            }
        }
        return false;
    }

    /**
     * Sort, then scan neighbours — target: O(n log n) time, O(n) space.
     *
     * Duplicates become adjacent once sorted. Not O(1) space in any of these three languages,
     * since none can sort the caller's array in place without mutating it.
     */
    public static function sorting(array $nums): bool
    {
        sort($nums);
        for($i = 0; $i < count($nums); $i++) {
            if (count($nums) === $i + 1) {
                return false;
            }
            if($nums[$i] === $nums[$i + 1]) {
                return true;
            }
        }
        return false;
    }

    /**
     * Set membership — target: O(n) time, O(n) space.
     *
     * Return on the first repeat, so the early-exit case is far better than O(n) in practice — a
     * duplicate at index 1 costs two operations regardless of input size.
     */
    public static function hashSet(array $nums): bool
    {
        $hashSet = [];
        for($i = 0; $i < count($nums); $i++) {
           $hashSet[$nums[$i]] += 1;
           if ($hashSet[$nums[$i]] > 1) {
               return true;
           }
        }
        return false;
    }
}
