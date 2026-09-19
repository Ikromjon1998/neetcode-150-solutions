/**
 * 36. Valid Sudoku — driven by packages/contracts/problems/0036-valid-sudoku.json.
 *
 * No hand-written fixtures: add a case to the JSON and it lands here, in the Python suite and
 * in the PHP suite at the same time.
 */

import { describe, expect, it } from "vitest";
import { contractCases } from "../../src/index";
import { validSudokuThreePass, validSudokuSinglePass } from "../../src/arrays-and-hashing/valid-sudoku";

interface Input {
  board: string[][];
}

const SLUG = "valid-sudoku";
const CASES = contractCases<Input, boolean>(SLUG);
const IMPLEMENTATIONS = [
  ["three-pass", validSudokuThreePass],
  ["single-pass", validSudokuSinglePass],
] as const;

describe.each(IMPLEMENTATIONS)("valid-sudoku (%s)", (_key, solve) => {
  it.each(CASES)("$name", ({ input, expected }) => {
    expect(solve(input.board)).toEqual(expected);
  });
});

describe("valid-sudoku differential", () => {
  it.each(CASES)("all approaches agree: $name", ({ input }) => {
    const results = IMPLEMENTATIONS.map(([, solve]) => solve(input.board));
    for (const result of results) expect(result).toEqual(results[0]);
  });
});
