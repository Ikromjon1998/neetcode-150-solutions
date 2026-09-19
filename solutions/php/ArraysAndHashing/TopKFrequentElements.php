<?php

declare(strict_types=1);

namespace NeetCode\Core\ArraysAndHashing;

use NeetCode\Core\Contracts\ProblemDefinition;

/**
 * 347. Top K Frequent Elements — https://leetcode.com/problems/top-k-frequent-elements/
 *
 * The `$k` most frequent values in `$nums`.
 *
 * LeetCode accepts any order; this repo pins descending-by-frequency then ascending-by-value so
 * the three implementations can be compared byte for byte.
 */
final class TopKFrequentElements implements ProblemDefinition
{
    public const SLUG = 'top-k-frequent-elements';

    public static function slug(): string
    {
        return self::SLUG;
    }

    /** @return array<string, callable> */
    public static function solutions(): array
    {
        return [
            'sorting' => self::sorting(...),
            'bucket-sort' => self::bucketSort(...),
        ];
    }

    /**
     * Tally, then sort the distinct values. Time O(n log n), space O(n).
     *
     * `array_count_values` builds the tally in one C-level call — PHP's nearest equivalent to
     * Python's `Counter`. It only accepts int and string values, which is fine here and is the
     * reason it does not appear in problems whose elements are arrays.
     *
     * The canonical order needs a two-term comparison. PHP's spaceship operator on arrays
     * compares element by element, so `[-$countA, $valueA] <=> [-$countB, $valueB]` expresses
     * both directions in one line — closer to Python's tuple key than to JavaScript, which has
     * no array comparison at all.
     *
     * @param  list<int>  $nums
     * @return list<int>
     */
    public static function sorting(array $nums, int $k): array
    {
        if ($k <= 0) {
            return [];
        }

        $counts = array_count_values($nums);
        $values = array_keys($counts);

        usort($values, static fn (int $a, int $b): int => [-$counts[$a], $a] <=> [-$counts[$b], $b]);

        return array_slice($values, 0, $k);
    }

    /**
     * Bucket the values by frequency. Time O(n), space O(n).
     *
     * No value can occur more than `count($nums)` times, so an array of `n + 1` buckets indexed
     * by frequency has somewhere to put everything. Walking it from the back yields descending
     * frequency without ever sorting.
     *
     * Each bucket is sorted internally only to honour this repo's ascending-value tie-break.
     *
     * @param  list<int>  $nums
     * @return list<int>
     */
    public static function bucketSort(array $nums, int $k): array
    {
        if ($k <= 0) {
            return [];
        }

        $counts = array_count_values($nums);
        $buckets = array_fill(0, count($nums) + 1, []);

        foreach ($counts as $value => $count) {
            $buckets[$count][] = $value;
        }

        $result = [];

        for ($count = count($buckets) - 1; $count > 0; $count--) {
            $bucket = $buckets[$count];
            sort($bucket);

            foreach ($bucket as $value) {
                $result[] = $value;

                if (count($result) === $k) {
                    return $result;
                }
            }
        }

        return $result;
    }
}
