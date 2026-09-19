/**
 * Application service for Two Sum.
 *
 * The service is the seam between HTTP and the algorithm. It holds no request objects and no
 * response objects — it takes plain values and returns plain values, which is what lets the
 * same logic be reused by a CLI or a background job later.
 */

import { Injectable } from "@nestjs/common";
import { getSolution } from "@neetcode/core";
import { timed } from "../../common/timing";

export const SLUG = "two-sum";

type TwoSumFn = (nums: readonly number[], target: number) => number[];

@Injectable()
export class TwoSumService {
  /**
   * Returns the indices and how long the algorithm took.
   *
   * Throws `NoSolutionError` when no pair exists; the global filter turns that into a 404.
   * The service never mentions status codes.
   */
  solve(
    nums: number[],
    target: number,
    approach: string,
  ): { result: number[]; elapsedMicros: number } {
    const algorithm = getSolution(SLUG, approach) as TwoSumFn;
    return timed(() => algorithm(nums, target));
  }
}
