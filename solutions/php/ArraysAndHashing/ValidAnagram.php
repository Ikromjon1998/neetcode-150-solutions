<?php

declare(strict_types=1);

namespace NeetCode\Core\ArraysAndHashing;

use NeetCode\Core\Contracts\ProblemDefinition;

/**
 * 242. Valid Anagram — https://leetcode.com/problems/valid-anagram/
 *
 * `$t` is an anagram of `$s` when both hold exactly the same characters with exactly the same
 * multiplicities. Order is irrelevant; counts are everything.
 *
 * PHP strings are byte arrays, not sequences of characters. `strlen()` counts bytes and
 * `str_split()` splits bytes, so "héllo" would be cut mid-character and two different
 * multi-byte strings could compare equal by accident. Both implementations below use the
 * `mb_*` family, which is the single biggest difference between this file and its Python and
 * TypeScript siblings — both of those iterate characters correctly by default.
 */
final class ValidAnagram implements ProblemDefinition
{
    public const SLUG = 'valid-anagram';

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
     * Two anagrams have the same sorted form. Time O(n log n), space O(n).
     */
    public static function sorting(string $s, string $t): bool
    {
        if (mb_strlen($s) !== mb_strlen($t)) {
            return false;
        }

        $left = mb_str_split($s);
        $right = mb_str_split($t);
        sort($left);
        sort($right);

        return $left === $right;
    }

    /**
     * Count characters in one string, decrement for the other. Time O(n), space O(k).
     *
     * `$counts[$char] ?? 0` rather than `isset()` plus a branch: the null-coalescing operator
     * reads the key once and does not emit a notice for a missing one. Python's `Counter` and
     * `dict.get` cover the same ground; JavaScript needs `Map.get() ?? 0`.
     */
    public static function hashMap(string $s, string $t): bool
    {
        if (mb_strlen($s) !== mb_strlen($t)) {
            return false;
        }

        /** @var array<string, int> $counts */
        $counts = [];

        foreach (mb_str_split($s) as $char) {
            $counts[$char] = ($counts[$char] ?? 0) + 1;
        }

        foreach (mb_str_split($t) as $char) {
            if (($counts[$char] ?? 0) === 0) {
                return false;
            }

            $counts[$char]--;
        }

        return true;
    }
}
