/** Application service for Encode and Decode Strings: the seam between HTTP and the algorithm. */

import { Injectable } from "@nestjs/common";
import { getSolution } from "@neetcode/core";
import { timed } from "../../common/timing";

export const SLUG = "encode-and-decode-strings";

type SolveFn = (strs: string[]) => string[];

@Injectable()
export class EncodeAndDecodeStringsService {
  solve(strs: string[], approach: string): { result: string[]; elapsedMicros: number } {
    const algorithm = getSolution(SLUG, approach) as SolveFn;
    return timed(() => algorithm(strs));
  }
}
