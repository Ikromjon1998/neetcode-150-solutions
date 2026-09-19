<?php

declare(strict_types=1);

namespace NeetCode\Core\ArraysAndHashing;

use NeetCode\Core\Contracts\ProblemDefinition;
use NeetCode\Core\Exceptions\UnsolvedException;

/**
 * 242. Valid Anagram
 *
 * Return true when `t` is an anagram of `s` — that is, when both strings contain exactly the same
 * characters with exactly the same multiplicities.
 *
 * https://leetcode.com/problems/valid-anagram/
 *
 * Each method below is an exercise. Replace the `throw` with your implementation, then
 * run `make test-php`.
 *
 * Stuck? `make show SLUG=valid-anagram` prints a worked answer.
 */
final class ValidAnagram implements ProblemDefinition
{
    public const SLUG = 'valid-anagram';

    private const PATH = 'packages/core-php/src/ArraysAndHashing/ValidAnagram.php';

    public static function slug(): string
    {
        return self::SLUG;
    }

    /** @return array<string, callable> */
    public static function solutions(): array
    {
        return [
            'sorting' => self::sorting(...),
            'hash-map' => self::hashMap(...),
        ];
    }

    /**
     * Sort both strings — target: O(n log n) time, O(n) space.
     *
     * Two anagrams have the same sorted form. Three lines and obviously correct, which is worth
     * something — but the sort dominates, and all three languages must copy the string to sort it.
     */
    public static function sorting(string $s, string $t): bool
    {
        throw new UnsolvedException(self::SLUG, 'sorting', self::PATH);
    }

    /**
     * Character frequency count — target: O(n) time, O(k) space.
     *
     * Count each character in `s`, decrement for each in `t`, and a single pass over the counts
     * decides it. O(k) in the alphabet size, not the input length.
     */
    public static function hashMap(string $s, string $t): bool
    {
        throw new UnsolvedException(self::SLUG, 'hash-map', self::PATH);
    }
}
