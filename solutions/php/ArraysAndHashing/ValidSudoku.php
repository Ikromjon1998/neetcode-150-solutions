<?php

declare(strict_types=1);

namespace NeetCode\Core\ArraysAndHashing;

use NeetCode\Core\Contracts\ProblemDefinition;

/**
 * 36. Valid Sudoku — https://leetcode.com/problems/valid-sudoku/
 *
 * Decide whether a partially filled 9x9 board breaks any Sudoku rule. Only the filled cells are
 * checked, and the board need not be solvable. Empty cells are the string `"."`.
 */
final class ValidSudoku implements ProblemDefinition
{
    public const SLUG = 'valid-sudoku';

    private const EMPTY_CELL = '.';

    private const SIZE = 9;

    private const BOX = 3;

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
     * True when the filled cells hold no repeat. Empty cells are ignored entirely.
     *
     * @param  list<string>  $cells
     */
    private static function allDistinct(array $cells): bool
    {
        $filled = array_filter($cells, static fn (string $cell): bool => $cell !== self::EMPTY_CELL);

        return count(array_unique($filled)) === count($filled);
    }

    /**
     * Rows, then columns, then boxes. Time O(1), space O(1).
     *
     * The board is a fixed 81 cells, so every approach is O(1) and only the constant factor
     * varies. This one reads the board three times and each sweep checks exactly one rule.
     *
     * @param  list<list<string>>  $board
     */
    public static function threePass(array $board): bool
    {
        foreach ($board as $row) {
            if (! self::allDistinct($row)) {
                return false;
            }
        }

        for ($column = 0; $column < self::SIZE; $column++) {
            if (! self::allDistinct(array_column($board, $column))) {
                return false;
            }
        }

        for ($boxRow = 0; $boxRow < self::SIZE; $boxRow += self::BOX) {
            for ($boxCol = 0; $boxCol < self::SIZE; $boxCol += self::BOX) {
                $cells = [];

                for ($r = 0; $r < self::BOX; $r++) {
                    for ($c = 0; $c < self::BOX; $c++) {
                        $cells[] = $board[$boxRow + $r][$boxCol + $c];
                    }
                }

                if (! self::allDistinct($cells)) {
                    return false;
                }
            }
        }

        return true;
    }

    /**
     * One visit per cell, updating three trackers at once. Time O(1), space O(1).
     *
     * The box index is `intdiv($row, self::BOX) * self::BOX + intdiv($column, self::BOX)`.
     * `intdiv` rather than `/`: PHP's division operator returns a float, and a float array index
     * is silently truncated with a deprecation notice in 8.1+. Python's `//` is the direct
     * equivalent; JavaScript needs `Math.floor`.
     *
     * 27 trackers, each an array used as a set. That fixed bound is the O(1) space.
     *
     * @param  list<list<string>>  $board
     */
    public static function singlePass(array $board): bool
    {
        /** @var list<array<string, true>> $rows */
        $rows = array_fill(0, self::SIZE, []);
        /** @var list<array<string, true>> $columns */
        $columns = array_fill(0, self::SIZE, []);
        /** @var list<array<string, true>> $boxes */
        $boxes = array_fill(0, self::SIZE, []);

        foreach ($board as $row => $cells) {
            foreach ($cells as $column => $cell) {
                if ($cell === self::EMPTY_CELL) {
                    continue;
                }

                $box = intdiv($row, self::BOX) * self::BOX + intdiv($column, self::BOX);

                // One `isset()` per tracker, OR-ed. Note that `isset($a, $b)` is AND, not
                // OR — a genuinely easy way to write a check that silently never fires.
                if (isset($rows[$row][$cell])
                    || isset($columns[$column][$cell])
                    || isset($boxes[$box][$cell])) {
                    return false;
                }

                $rows[$row][$cell] = true;
                $columns[$column][$cell] = true;
                $boxes[$box][$cell] = true;
            }
        }

        return true;
    }
}
