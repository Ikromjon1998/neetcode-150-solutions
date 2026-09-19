/** HTTP surface for problem 347. */

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
import { TopKFrequentElementsRequestDto } from "./dto/top-k-frequent-elements-request.dto";
import { SLUG, TopKFrequentElementsService } from "./top-k-frequent-elements.service";

@ApiTags("arrays-and-hashing")
@Controller("problems")
export class TopKFrequentElementsController {
  constructor(private readonly service: TopKFrequentElementsService) {}

  @Post(SLUG)
  // Nest answers POST with 201 by default; FastAPI and Laravel both answer 200 here.
  @HttpCode(HttpStatus.OK)
  @ApiOperation({ summary: "Solve Top K Frequent Elements" })
  @ApiBody({ type: TopKFrequentElementsRequestDto })
  @ApiQuery({ name: "approach", required: false, enum: approachesFor(SLUG) })
  @ApiOkResponse({ type: SolveResponseDto })
  @ApiNotFoundResponse({ type: ErrorResponseDto })
  @ApiUnprocessableEntityResponse({ type: ErrorResponseDto })
  solve(
    @Body() body: TopKFrequentElementsRequestDto,
    @Query("approach", new ApproachPipe(SLUG)) approach: string,
  ): SolveResponseDto<number[]> {
    const { result, elapsedMicros } = this.service.solve(body.nums, body.k, approach);
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
      input: { nums: body.nums, k: body.k },
      result,
      elapsedMicros,
    };
  }
}
