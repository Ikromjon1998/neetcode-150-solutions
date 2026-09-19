"""36. Valid Sudoku

Decide whether a partially filled 9x9 board breaks any Sudoku rule. Only the filled cells are
checked, and the board need not be solvable — a board with no contradictions among its current
entries is valid. Empty cells are the string `"."`.

    https://leetcode.com/problems/valid-sudoku/

Each function below is an exercise. Replace the `raise` with your implementation, then:

    make test-python

Stuck? `make show SLUG=valid-sudoku` prints a worked answer.
"""

from __future__ import annotations

from neetcode_core.errors import UnsolvedError
from neetcode_core.registry import solution

SLUG = "valid-sudoku"
PATH = "packages/core-python/src/neetcode_core/arrays_and_hashing/valid_sudoku.py"


@solution(SLUG, approach="three-pass")
def valid_sudoku_three_pass(board: list[list[str]]) -> bool:
    """Rows, then columns, then boxes — target: O(1) time, O(1) space.

    Three independent sweeps, each building a fresh set per unit. The most readable version, and
    the board is a fixed 81 cells so the constant factor is the only thing that varies.
    """
    raise UnsolvedError(SLUG, "three-pass", PATH)


@solution(SLUG, approach="single-pass")
def valid_sudoku_single_pass(board: list[list[str]]) -> bool:
    """One pass, nine of each tracker — target: O(1) time, O(1) space.

    Visit each cell once, updating its row, column and box tracker together. The box index is `(r
    // 3) * 3 + c // 3` — the one line in this problem worth deriving rather than memorising.
    """
    raise UnsolvedError(SLUG, "single-pass", PATH)
