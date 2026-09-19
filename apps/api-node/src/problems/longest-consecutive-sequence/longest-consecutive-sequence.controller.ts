/** HTTP surface for problem 128. */

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
import { ErrorResponseDto, SolveResponseDto } from "../../common/dto/solve-response.dto";
import { ApproachPipe } from "../../common/pipes/approach.pipe";
import { LongestConsecutiveSequenceRequestDto } from "./dto/longest-consecutive-sequence-request.dto";
import { SLUG, LongestConsecutiveSequenceService } from "./longest-consecutive-sequence.service";

@ApiTags("arrays-and-hashing")
@Controller("problems")
export class LongestConsecutiveSequenceController {
  constructor(private readonly service: LongestConsecutiveSequenceService) {}

  @Post(SLUG)
  // Nest answers POST with 201 by default; FastAPI and Laravel both answer 200 here.
  @HttpCode(HttpStatus.OK)
  @ApiOperation({ summary: "Solve Longest Consecutive Sequence" })
  @ApiBody({ type: LongestConsecutiveSequenceRequestDto })
  @ApiQuery({ name: "approach", required: false, enum: approachesFor(SLUG) })
  @ApiOkResponse({ type: SolveResponseDto })
  @ApiNotFoundResponse({ type: ErrorResponseDto })
  @ApiUnprocessableEntityResponse({ type: ErrorResponseDto })
  solve(
    @Body() body: LongestConsecutiveSequenceRequestDto,
    @Query("approach", new ApproachPipe(SLUG)) approach: string,
  ): SolveResponseDto<number> {
    const { result, elapsedMicros } = this.service.solve(body.nums, approach);
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
      input: { nums: body.nums },
      result,
      elapsedMicros,
    };
  }
}
