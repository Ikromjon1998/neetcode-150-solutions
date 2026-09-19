/**
 * 36. Valid Sudoku
 *
 * Decide whether a partially filled 9x9 board breaks any Sudoku rule. Only the filled cells are
 * checked, and the board need not be solvable — a board with no contradictions among its current
 * entries is valid. Empty cells are the string `"."`.
 *
 * https://leetcode.com/problems/valid-sudoku/
 *
 * Each function below is an exercise. Replace the `throw` with your implementation,
 * then run `make test-node`.
 *
 * Stuck? `make show SLUG=valid-sudoku` prints a worked answer.
 */

import { defineProblem } from "../define-problem";
import { UnsolvedError } from "../errors";

export const SLUG = "valid-sudoku";
const PATH = "packages/core-ts/src/arrays-and-hashing/valid-sudoku.ts";

/**
 * Rows, then columns, then boxes — target: O(1) time, O(1) space.
 *
 * Three independent sweeps, each building a fresh set per unit. The most readable version, and the
 * board is a fixed 81 cells so the constant factor is the only thing that varies.
 */
export function validSudokuThreePass(board: readonly (readonly string[])[]): boolean {
  throw new UnsolvedError(SLUG, "three-pass", PATH);
}

/**
 * One pass, nine of each tracker — target: O(1) time, O(1) space.
 *
 * Visit each cell once, updating its row, column and box tracker together. The box index is `(r //
 * 3) * 3 + c // 3` — the one line in this problem worth deriving rather than memorising.
 */
export function validSudokuSinglePass(board: readonly (readonly string[])[]): boolean {
  throw new UnsolvedError(SLUG, "single-pass", PATH);
}

export const validSudoku = defineProblem(SLUG, {
  "three-pass": validSudokuThreePass,
  "single-pass": validSudokuSinglePass,
});
