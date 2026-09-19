/** Application service for Valid Anagram: the seam between HTTP and the algorithm. */

import { Injectable } from "@nestjs/common";
import { getSolution } from "@neetcode/core";
import { timed } from "../../common/timing";

export const SLUG = "valid-anagram";

type SolveFn = (s: string, t: string) => boolean;

@Injectable()
export class ValidAnagramService {
  solve(s: string, t: string, approach: string): { result: boolean; elapsedMicros: number } {
    const algorithm = getSolution(SLUG, approach) as SolveFn;
    return timed(() => algorithm(s, t));
  }
}
