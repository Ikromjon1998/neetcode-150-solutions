<?php

declare(strict_types=1);

namespace NeetCode\Core\ArraysAndHashing;

use NeetCode\Core\Contracts\ProblemDefinition;
use NeetCode\Core\Exceptions\UnsolvedException;

/**
 * 36. Valid Sudoku
 *
 * Decide whether a partially filled 9x9 board breaks any Sudoku rule. Only the filled cells are
 * checked, and the board need not be solvable — a board with no contradictions among its current
 * entries is valid. Empty cells are the string `"."`.
 *
 * https://leetcode.com/problems/valid-sudoku/
 *
 * Each method below is an exercise. Replace the `throw` with your implementation, then
 * run `make test-php`.
 *
 * Stuck? `make show SLUG=valid-sudoku` prints a worked answer.
 */
final class ValidSudoku implements ProblemDefinition
{
    public const SLUG = 'valid-sudoku';

    private const PATH = 'packages/core-php/src/ArraysAndHashing/ValidSudoku.php';

    public static function slug(): string
    {
        return self::SLUG;
    }

    /** @return array<string, callable> */
    public static function solutions(): array
    {
        return [
            'three-pass' => self::threePass(...),
            'single-pass' => self::singlePass(...),
        ];
    }

    /**
     * Rows, then columns, then boxes — target: O(1) time, O(1) space.
     *
     * Three independent sweeps, each building a fresh set per unit. The most readable version, and
     * the board is a fixed 81 cells so the constant factor is the only thing that varies.
     */
    public static function threePass(array $board): bool
    {
        throw new UnsolvedException(self::SLUG, 'three-pass', self::PATH);
    }

    /**
     * One pass, nine of each tracker — target: O(1) time, O(1) space.
     *
     * Visit each cell once, updating its row, column and box tracker together. The box index is
     * `(r // 3) * 3 + c // 3` — the one line in this problem worth deriving rather than
     * memorising.
     */
    public static function singlePass(array $board): bool
    {
        throw new UnsolvedException(self::SLUG, 'single-pass', self::PATH);
    }
}
