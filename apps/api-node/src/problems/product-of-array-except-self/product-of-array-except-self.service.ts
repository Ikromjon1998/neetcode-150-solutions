/** Application service for Product of Array Except Self: the seam between HTTP and the algorithm. */

import { Injectable } from "@nestjs/common";
import { getSolution } from "@neetcode/core";
import { timed } from "../../common/timing";

export const SLUG = "product-of-array-except-self";

type SolveFn = (nums: number[]) => number[];

@Injectable()
export class ProductOfArrayExceptSelfService {
  solve(nums: number[], approach: string): { result: number[]; elapsedMicros: number } {
    const algorithm = getSolution(SLUG, approach) as SolveFn;
    return timed(() => algorithm(nums));
  }
}
