<?php

declare(strict_types=1);

namespace NeetCode\Core\ArraysAndHashing;

use NeetCode\Core\Contracts\ProblemDefinition;
use NeetCode\Core\Exceptions\UnsolvedException;

/**
 * 128. Longest Consecutive Sequence
 *
 * Return the length of the longest run of consecutive integers present in `nums`. The elements
 * need not be adjacent in the array, and duplicates do not extend a run.
 *
 * https://leetcode.com/problems/longest-consecutive-sequence/
 *
 * Each method below is an exercise. Replace the `throw` with your implementation, then
 * run `make test-php`.
 *
 * Stuck? `make show SLUG=longest-consecutive-sequence` prints a worked answer.
 */
final class LongestConsecutiveSequence implements ProblemDefinition
{
    public const SLUG = 'longest-consecutive-sequence';

    private const PATH = 'packages/core-php/src/ArraysAndHashing/LongestConsecutiveSequence.php';

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
     * Sort, then walk — target: O(n log n) time, O(n) space.
     *
     * Once sorted, a run is a stretch of neighbours differing by exactly one. Duplicates must be
     * skipped rather than counted, which is the detail this approach gets wrong first.
     */
    public static function sorting(array $nums): int
    {
        throw new UnsolvedException(self::SLUG, 'sorting', self::PATH);
    }

    /**
     * Start only at run beginnings — target: O(n) time, O(n) space.
     *
     * Put everything in a set, then walk a run only from a value whose predecessor is absent. That
     * guard is what keeps it O(n) — without it the inner loop re-walks every run from every member
     * and it degrades to O(n^2).
     */
    public static function hashSet(array $nums): int
    {
        throw new UnsolvedException(self::SLUG, 'hash-set', self::PATH);
    }
}
