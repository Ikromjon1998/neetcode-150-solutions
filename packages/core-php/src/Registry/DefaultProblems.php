<?php

declare(strict_types=1);

namespace NeetCode\Core\Registry;

use NeetCode\Core\ArraysAndHashing\TwoSum;
use NeetCode\Core\ArraysAndHashing\EncodeAndDecodeStrings;
use NeetCode\Core\ArraysAndHashing\ValidSudoku;
use NeetCode\Core\ArraysAndHashing\GroupAnagrams;
use NeetCode\Core\ArraysAndHashing\TopKFrequentElements;
use NeetCode\Core\ArraysAndHashing\LongestConsecutiveSequence;
use NeetCode\Core\ArraysAndHashing\ProductOfArrayExceptSelf;
use NeetCode\Core\ArraysAndHashing\ContainsDuplicate;
use NeetCode\Core\ArraysAndHashing\ValidAnagram;

/**
 * The explicit list of problem classes.
 *
 * The Laravel app publishes this as `config/neetcode.php`, which is what lets
 * `php artisan config:cache` freeze the whole registry into a single compiled PHP array at
 * deploy time — no directory scan, no reflection, no autoloader misses on a cold request.
 *
 * ADD NEW PROBLEM CLASSES HERE. `make new-problem` inserts the import and the entry.
 */
final class DefaultProblems
{
    /** @return list<class-string<\NeetCode\Core\Contracts\ProblemDefinition>> */
    public static function all(): array
    {
        return [
            TwoSum::class,
            EncodeAndDecodeStrings::class,
            ValidSudoku::class,
            GroupAnagrams::class,
            TopKFrequentElements::class,
            LongestConsecutiveSequence::class,
            ProductOfArrayExceptSelf::class,
            ContainsDuplicate::class,
            ValidAnagram::class,
        ];
    }
}
