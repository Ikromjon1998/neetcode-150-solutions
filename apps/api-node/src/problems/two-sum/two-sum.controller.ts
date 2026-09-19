/**
 * HTTP surface for problem 1.
 *
 * Every problem module in this app looks exactly like this file: a controller, the approach
 * pipe, a service call, and the shared envelope. That regularity is the point — it makes
 * adding problem 2 a copy-paste-and-rename job, and it is mirrored one-for-one by the FastAPI
 * router and the Laravel controller.
 */

import { Body, Controller, HttpCode, HttpStatus, Post, Query } from "@nestjs/common";
import {
  ApiBody,
  ApiNotFoundResponse,
  ApiOkResponse,
  ApiOperation,
  ApiQuery,
  ApiTags,
  ApiUnprocessableEntityResponse,
} from "@nestjs/swagger";
import { approachesFor, findApproach } from "@neetcode/core";
import {
  ErrorResponseDto,
  SolveResponseDto,
} from "../../common/dto/solve-response.dto";
import { ApproachPipe } from "../../common/pipes/approach.pipe";
import { TwoSumRequestDto } from "./dto/two-sum-request.dto";
import { SLUG, TwoSumService } from "./two-sum.service";

@ApiTags("arrays-and-hashing")
@Controller("problems")
export class TwoSumController {
  constructor(private readonly service: TwoSumService) {}

  @Post(SLUG)
  // NestJS answers a POST with 201 Created by default. Solving a problem creates nothing, and
  // FastAPI and Laravel both answer 200 here, so it is pinned. Forgetting this line is the
  // single most common reason a Nest endpoint disagrees with its Python twin.
  @HttpCode(HttpStatus.OK)
  @ApiOperation({
    summary: "Solve Two Sum",
    description:
      "Returns the indices of the two numbers that add up to `target`. Use " +
      "`?approach=brute-force` to run the O(n^2) baseline instead of the default O(n) " +
      "hash-map implementation.",
  })
  @ApiBody({ type: TwoSumRequestDto })
  @ApiQuery({ name: "approach", required: false, enum: approachesFor(SLUG) })
  @ApiOkResponse({ type: SolveResponseDto })
  @ApiNotFoundResponse({ type: ErrorResponseDto, description: "No pair sums to target." })
  @ApiUnprocessableEntityResponse({ type: ErrorResponseDto, description: "Invalid input." })
  solve(
    @Body() body: TwoSumRequestDto,
    @Query("approach", new ApproachPipe(SLUG)) approach: string,
  ): SolveResponseDto<number[]> {
    const { result, elapsedMicros } = this.service.solve(body.nums, body.target, approach);
    const chosen = findApproach(SLUG, approach);

    return {
      problem: SLUG,
      approach: {
        key: chosen.key,
        name: chosen.name,
        time: chosen.time,
        space: chosen.space,
        note: chosen.note,
        default: chosen.default ?? false,
      },
      input: { nums: body.nums, target: body.target },
      result,
      elapsedMicros,
    };
  }
}
