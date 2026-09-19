<?php

declare(strict_types=1);

namespace NeetCode\Core\ArraysAndHashing;

use NeetCode\Core\Contracts\ProblemDefinition;
use NeetCode\Core\Exceptions\UnsolvedException;

/**
 * 49. Group Anagrams
 *
 * Group the strings so that every group holds exactly the mutual anagrams. LeetCode accepts any
 * order; this repo pins a canonical one — each group sorted ascending, and the groups themselves
 * sorted by their first member — so the three implementations can be compared byte for byte.
 *
 * https://leetcode.com/problems/group-anagrams/
 *
 * Each method below is an exercise. Replace the `throw` with your implementation, then
 * run `make test-php`.
 *
 * Stuck? `make show SLUG=group-anagrams` prints a worked answer.
 */
final class GroupAnagrams implements ProblemDefinition
{
    public const SLUG = 'group-anagrams';

    private const PATH = 'packages/core-php/src/ArraysAndHashing/GroupAnagrams.php';

    public static function slug(): string
    {
        return self::SLUG;
    }

    /** @return array<string, callable> */
    public static function solutions(): array
    {
        return [
            'sorted-key' => self::sortedKey(...),
            'count-key' => self::countKey(...),
        ];
    }

    /**
     * Sorted string as the key — target: O(n k log k) time, O(n k) space.
     *
     * Two words are anagrams exactly when their sorted forms match, so the sorted string is a
     * ready-made group key. k is the word length; the log k is the per-word sort.
     */
    public static function sortedKey(array $strs): array
    {
        throw new UnsolvedException(self::SLUG, 'sorted-key', self::PATH);
    }

    /**
     * Character-count tuple as the key — target: O(n k) time, O(n k) space.
     *
     * Replace the per-word sort with a 26-slot tally rendered as a key. Linear in the word length,
     * and the clearest place in this repo where the three languages disagree about what may be
     * used as a map key.
     */
    public static function countKey(array $strs): array
    {
        throw new UnsolvedException(self::SLUG, 'count-key', self::PATH);
    }
}
