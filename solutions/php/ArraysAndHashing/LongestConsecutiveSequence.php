<?php

declare(strict_types=1);

namespace NeetCode\Core\ArraysAndHashing;

use NeetCode\Core\Contracts\ProblemDefinition;

/**
 * 128. Longest Consecutive Sequence — https://leetcode.com/problems/longest-consecutive-sequence/
 *
 * The length of the longest run of consecutive integers present in `$nums`. Position in the
 * array is irrelevant, and duplicates do not lengthen a run.
 */
final class LongestConsecutiveSequence implements ProblemDefinition
{
    public const SLUG = 'longest-consecutive-sequence';

    public static function slug(): string
    {
        return self::SLUG;
    }

    /** @return array<string, callable> */
    public static function solutions(): array
    {
        return [
            'sorting' => self::sorting(...),
            'hash-set' => self::hashSet(...),
        ];
    }

    /**
     * Sort, then walk. Time O(n log n), space O(n).
     *
     * `array_values(array_unique($nums))` deduplicates and re-indexes. The re-index matters:
     * `array_unique` preserves the original keys, leaving gaps, and the `for` loop below indexes
     * positionally. Python's `sorted(set(...))` and JavaScript's `[...new Set(...)]` both return
     * a densely indexed sequence for free.
     *
     * @param  list<int>  $nums
     */
    public static function sorting(array $nums): int
    {
        if ($nums === []) {
            return 0;
        }

        $ordered = array_values(array_unique($nums));
        sort($ordered);

        $longest = 1;
        $current = 1;

        for ($i = 1, $length = count($ordered); $i < $length; $i++) {
            $current = $ordered[$i] - $ordered[$i - 1] === 1 ? $current + 1 : 1;
            $longest = max($longest, $current);
        }

        return $longest;
    }

    /**
     * Walk each run exactly once, from its start. Time O(n), space O(n).
     *
     * The `isset($seen[$value - 1])` guard is the entire algorithm. Without it the inner loop
     * re-walks every run from every one of its members and the whole thing degrades to O(n^2).
     *
     * `array_flip` turns the values into keys in one C-level call, which is PHP's idiomatic way
     * to build a set from a list — and it deduplicates as a side effect, since keys are unique.
     *
     * @param  list<int>  $nums
     */
    public static function hashSet(array $nums): int
    {
        /** @var array<int, int> $seen */
        $seen = array_flip($nums);
        $longest = 0;

        foreach (array_keys($seen) as $value) {
            if (isset($seen[$value - 1])) {
                continue; // not the start of a run
            }

            $length = 1;
            while (isset($seen[$value + $length])) {
                $length++;
            }

            $longest = max($longest, $length);
        }

        return $longest;
    }
}
