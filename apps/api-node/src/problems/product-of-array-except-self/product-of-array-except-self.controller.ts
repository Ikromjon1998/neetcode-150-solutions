/** HTTP surface for problem 238. */

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
import { ProductOfArrayExceptSelfRequestDto } from "./dto/product-of-array-except-self-request.dto";
import { SLUG, ProductOfArrayExceptSelfService } from "./product-of-array-except-self.service";

@ApiTags("arrays-and-hashing")
@Controller("problems")
export class ProductOfArrayExceptSelfController {
  constructor(private readonly service: ProductOfArrayExceptSelfService) {}

  @Post(SLUG)
  // Nest answers POST with 201 by default; FastAPI and Laravel both answer 200 here.
  @HttpCode(HttpStatus.OK)
  @ApiOperation({ summary: "Solve Product of Array Except Self" })
  @ApiBody({ type: ProductOfArrayExceptSelfRequestDto })
  @ApiQuery({ name: "approach", required: false, enum: approachesFor(SLUG) })
  @ApiOkResponse({ type: SolveResponseDto })
  @ApiNotFoundResponse({ type: ErrorResponseDto })
  @ApiUnprocessableEntityResponse({ type: ErrorResponseDto })
  solve(
    @Body() body: ProductOfArrayExceptSelfRequestDto,
    @Query("approach", new ApproachPipe(SLUG)) approach: string,
  ): SolveResponseDto<number[]> {
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
