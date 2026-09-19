/** Application service for Contains Duplicate: the seam between HTTP and the algorithm. */

import { Injectable } from "@nestjs/common";
import { getSolution } from "@neetcode/core";
import { timed } from "../../common/timing";

export const SLUG = "contains-duplicate";

type SolveFn = (nums: number[]) => boolean;

@Injectable()
export class ContainsDuplicateService {
  solve(nums: number[], approach: string): { result: boolean; elapsedMicros: number } {
    const algorithm = getSolution(SLUG, approach) as SolveFn;
    return timed(() => algorithm(nums));
  }
}
