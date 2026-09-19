/** Application service for Valid Sudoku: the seam between HTTP and the algorithm. */

import { Injectable } from "@nestjs/common";
import { getSolution } from "@neetcode/core";
import { timed } from "../../common/timing";

export const SLUG = "valid-sudoku";

type SolveFn = (board: string[][]) => boolean;

@Injectable()
export class ValidSudokuService {
  solve(board: string[][], approach: string): { result: boolean; elapsedMicros: number } {
    const algorithm = getSolution(SLUG, approach) as SolveFn;
    return timed(() => algorithm(board));
  }
}
