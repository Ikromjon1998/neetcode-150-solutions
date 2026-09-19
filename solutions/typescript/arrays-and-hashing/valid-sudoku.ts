/**
 * 36. Valid Sudoku — https://leetcode.com/problems/valid-sudoku/
 *
 * Decide whether a partially filled 9x9 board breaks any Sudoku rule. Only the filled cells are
 * checked, and the board need not be solvable. Empty cells are the string `"."`.
 */

import { defineProblem } from "../define-problem";

export const SLUG = "valid-sudoku";

const EMPTY = ".";
const SIZE = 9;
const BOX = 3;

/** True when the filled cells hold no repeat. Empty cells are ignored entirely. */
function allDistinct(cells: readonly string[]): boolean {
  const filled = cells.filter((cell) => cell !== EMPTY);
  return new Set(filled).size === filled.length;
}

/**
 * Rows, then columns, then boxes. Time O(1), space O(1).
 *
 * The board is a fixed 81 cells, so every approach is O(1) and only the constant factor varies.
 * This one reads the board three times and each sweep checks exactly one rule.
 */
export function validSudokuThreePass(board: readonly (readonly string[])[]): boolean {
  for (const row of board) {
    if (!allDistinct(row)) return false;
  }

  for (let column = 0; column < SIZE; column++) {
    const cells = Array.from({ length: SIZE }, (_, row) => board[row]![column]!);
    if (!allDistinct(cells)) return false;
  }

  for (let boxRow = 0; boxRow < SIZE; boxRow += BOX) {
    for (let boxCol = 0; boxCol < SIZE; boxCol += BOX) {
      const cells: string[] = [];
      for (let r = 0; r < BOX; r++) {
        for (let c = 0; c < BOX; c++) cells.push(board[boxRow + r]![boxCol + c]!);
      }
      if (!allDistinct(cells)) return false;
    }
  }

  return true;
}

/**
 * One visit per cell, updating three trackers at once. Time O(1), space O(1).
 *
 * The box index is `Math.floor(row / BOX) * BOX + Math.floor(column / BOX)`. Note the two
 * explicit `Math.floor` calls — JavaScript's `/` is floating-point division, so unlike Python's
 * `//` and PHP's `intdiv`, truncation has to be asked for. `7 / 3` is `2.333…`, and using it as
 * an array index would silently return `undefined`.
 */
export function validSudokuSinglePass(board: readonly (readonly string[])[]): boolean {
  const rows = Array.from({ length: SIZE }, () => new Set<string>());
  const columns = Array.from({ length: SIZE }, () => new Set<string>());
  const boxes = Array.from({ length: SIZE }, () => new Set<string>());

  for (let row = 0; row < board.length; row++) {
    const cells = board[row]!;
    for (let column = 0; column < cells.length; column++) {
      const cell = cells[column]!;
      if (cell === EMPTY) continue;

      const box = Math.floor(row / BOX) * BOX + Math.floor(column / BOX);
      if (rows[row]!.has(cell) || columns[column]!.has(cell) || boxes[box]!.has(cell)) {
        return false;
      }

      rows[row]!.add(cell);
      columns[column]!.add(cell);
      boxes[box]!.add(cell);
    }
  }

  return true;
}

export const validSudoku = defineProblem(SLUG, {
  "three-pass": validSudokuThreePass,
  "single-pass": validSudokuSinglePass,
});
