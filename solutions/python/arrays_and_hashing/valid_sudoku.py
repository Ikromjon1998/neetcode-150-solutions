"""36. Valid Sudoku — https://leetcode.com/problems/valid-sudoku/

Decide whether a partially filled 9x9 board breaks any Sudoku rule.

Only the filled cells are checked, and the board need not be solvable: a board with no
contradiction among its current entries is valid. Empty cells are the string `"."`.
"""

from __future__ import annotations

from collections.abc import Iterable

from neetcode_core.registry import solution

SLUG = "valid-sudoku"

EMPTY = "."
SIZE = 9
BOX = 3


def _all_distinct(cells: Iterable[str]) -> bool:
    """True when the filled cells hold no repeat. Empty cells are ignored entirely."""
    filled = [cell for cell in cells if cell != EMPTY]
    return len(filled) == len(set(filled))


@solution(SLUG, approach="three-pass")
def valid_sudoku_three_pass(board: list[list[str]]) -> bool:
    """Rows, then columns, then boxes. Time O(1), space O(1).

    The board is a fixed 81 cells, so every approach here is O(1) and the only thing that
    varies is the constant factor. This one reads the board three times and is by far the
    easiest version to convince yourself is correct — each sweep checks exactly one rule.
    """
    if any(not _all_distinct(row) for row in board):
        return False

    for column in range(SIZE):
        if not _all_distinct(board[row][column] for row in range(SIZE)):
            return False

    for box_row in range(0, SIZE, BOX):
        for box_col in range(0, SIZE, BOX):
            cells = (
                board[box_row + r][box_col + c]
                for r in range(BOX)
                for c in range(BOX)
            )
            if not _all_distinct(cells):
                return False

    return True


@solution(SLUG, approach="single-pass")
def valid_sudoku_single_pass(board: list[list[str]]) -> bool:
    """One visit per cell, updating three trackers at once. Time O(1), space O(1).

    The box index is `(row // BOX) * BOX + column // BOX`. Worth deriving rather than
    memorising: integer-dividing a coordinate by 3 collapses it to which band of three it falls
    in, and the row band is then scaled by 3 to leave room for the column band.

    27 sets — nine rows, nine columns, nine boxes — each holding at most nine entries. That
    fixed bound is the O(1) space.
    """
    rows: list[set[str]] = [set() for _ in range(SIZE)]
    columns: list[set[str]] = [set() for _ in range(SIZE)]
    boxes: list[set[str]] = [set() for _ in range(SIZE)]

    for row, cells in enumerate(board):
        for column, cell in enumerate(cells):
            if cell == EMPTY:
                continue

            box = (row // BOX) * BOX + column // BOX
            if cell in rows[row] or cell in columns[column] or cell in boxes[box]:
                return False

            rows[row].add(cell)
            columns[column].add(cell)
            boxes[box].add(cell)

    return True
