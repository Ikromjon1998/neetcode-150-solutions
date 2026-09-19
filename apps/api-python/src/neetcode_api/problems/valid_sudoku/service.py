"""Application service for Valid Sudoku.

The seam between HTTP and the algorithm: plain values in, plain values out.
"""

from __future__ import annotations

from neetcode_core import get_solution

from neetcode_api.timing import timed

SLUG = "valid-sudoku"


class ValidSudokuService:
    def solve(self, board: list[list[str]], approach: str) -> tuple[bool, int]:
        """Return `(result, elapsed_microseconds)`."""
        algorithm = get_solution(SLUG, approach=approach)
        return timed(algorithm, board)
