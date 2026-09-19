<?php

declare(strict_types=1);

namespace NeetCode\Core\ArraysAndHashing;

use NeetCode\Core\Contracts\ProblemDefinition;
use NeetCode\Core\Exceptions\UnsolvedException;

/**
 * 347. Top K Frequent Elements
 *
 * Return the `k` most frequent values in `nums`. LeetCode accepts any order; this repo pins a
 * canonical one — descending by frequency, then ascending by value — so the three implementations
 * can be compared byte for byte.
 *
 * https://leetcode.com/problems/top-k-frequent-elements/
 *
 * Each method below is an exercise. Replace the `throw` with your implementation, then
 * run `make test-php`.
 *
 * Stuck? `make show SLUG=top-k-frequent-elements` prints a worked answer.
 */
final class TopKFrequentElements implements ProblemDefinition
{
    public const SLUG = 'top-k-frequent-elements';

    private const PATH = 'packages/core-php/src/ArraysAndHashing/TopKFrequentElements.php';

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
     * Count, then sort by frequency — target: O(n log n) time, O(n) space.
     *
     * Tally, then sort the distinct values. The sort dominates, but on the small inputs this
     * problem usually sees it is the fastest of the two.
     */
    public static function sorting(array $nums, int $k): array
    {
        throw new UnsolvedException(self::SLUG, 'sorting', self::PATH);
    }

    /**
     * Bucket by frequency — target: O(n) time, O(n) space.
     *
     * A count can never exceed n, so an array of n+1 buckets indexed by frequency replaces the
     * sort entirely. Walking it from the back yields values in descending frequency for free.
     */
    public static function bucketSort(array $nums, int $k): array
    {
        throw new UnsolvedException(self::SLUG, 'bucket-sort', self::PATH);
    }
}
