<?php

declare(strict_types=1);

namespace NeetCode\Core\ArraysAndHashing;

use NeetCode\Core\Contracts\ProblemDefinition;

/**
 * 49. Group Anagrams — https://leetcode.com/problems/group-anagrams/
 *
 * Group the input strings so that each group holds exactly the mutual anagrams.
 *
 * LeetCode accepts any order; this repo pins each group sorted ascending and the groups sorted
 * by their first member, so the three implementations can be compared byte for byte.
 */
final class GroupAnagrams implements ProblemDefinition
{
    public const SLUG = 'group-anagrams';

    private const ALPHABET = 26;

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
     * Impose this repo's ordering. Not part of the algorithm; part of the comparison.
     *
     * `array_values` at both levels is not decoration. `sort()` re-indexes, but the outer array
     * still carries whatever keys the grouping produced, and a PHP array with non-sequential
     * keys JSON-encodes as an **object**, not an array — which would make this endpoint's
     * response structurally different from the Python and TypeScript ones while looking
     * identical in a `var_dump`.
     *
     * @param  array<array-key, list<string>>  $groups
     * @return list<list<string>>
     */
    private static function canonical(array $groups): array
    {
        $ordered = [];

        foreach ($groups as $group) {
            sort($group);
            $ordered[] = $group;
        }

        usort($ordered, static fn (array $a, array $b): int => $a[0] <=> $b[0]);

        return array_values($ordered);
    }

    /**
     * Key each word by its sorted form. Time O(n*k log k), space O(n*k).
     *
     * Two words are anagrams exactly when their sorted forms are equal, so the sorted string is
     * a ready-made group key. `mb_str_split` rather than `str_split`, as everywhere in this
     * repo that touches a string.
     *
     * @param  list<string>  $strs
     * @return list<list<string>>
     */
    public static function sortedKey(array $strs): array
    {
        /** @var array<string, list<string>> $groups */
        $groups = [];

        foreach ($strs as $word) {
            $chars = mb_str_split($word);
            sort($chars);
            $groups[implode('', $chars)][] = $word;
        }

        return self::canonical($groups);
    }

    /**
     * Key each word by its character tally. Time O(n*k), space O(n*k).
     *
     * Replaces the per-word sort with a single pass building a 26-slot tally.
     *
     * The tally then has to become a key, and PHP has the least choice of the three languages:
     * array keys are `int|string` only, so the counts must be serialised. Python can use a
     * `tuple` directly because tuples hash by value; JavaScript must serialise too, but for the
     * opposite reason — `Map` compares array keys by reference.
     *
     * @param  list<string>  $strs
     * @return list<list<string>>
     */
    public static function countKey(array $strs): array
    {
        /** @var array<string, list<string>> $groups */
        $groups = [];

        foreach ($strs as $word) {
            $counts = array_fill(0, self::ALPHABET, 0);

            foreach (mb_str_split($word) as $char) {
                $counts[ord($char) - ord('a')]++;
            }

            $groups[implode(',', $counts)][] = $word;
        }

        return self::canonical($groups);
    }
}
