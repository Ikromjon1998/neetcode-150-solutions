/** Application service for Top K Frequent Elements: the seam between HTTP and the algorithm. */

import { Injectable } from "@nestjs/common";
import { getSolution } from "@neetcode/core";
import { timed } from "../../common/timing";

export const SLUG = "top-k-frequent-elements";

type SolveFn = (nums: number[], k: number) => number[];

@Injectable()
export class TopKFrequentElementsService {
  solve(nums: number[], k: number, approach: string): { result: number[]; elapsedMicros: number } {
    const algorithm = getSolution(SLUG, approach) as SolveFn;
    return timed(() => algorithm(nums, k));
  }
}
