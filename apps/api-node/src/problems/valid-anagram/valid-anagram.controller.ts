/** HTTP surface for problem 242. */

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
import { ValidAnagramRequestDto } from "./dto/valid-anagram-request.dto";
import { SLUG, ValidAnagramService } from "./valid-anagram.service";

@ApiTags("arrays-and-hashing")
@Controller("problems")
export class ValidAnagramController {
  constructor(private readonly service: ValidAnagramService) {}

  @Post(SLUG)
  // Nest answers POST with 201 by default; FastAPI and Laravel both answer 200 here.
  @HttpCode(HttpStatus.OK)
  @ApiOperation({ summary: "Solve Valid Anagram" })
  @ApiBody({ type: ValidAnagramRequestDto })
  @ApiQuery({ name: "approach", required: false, enum: approachesFor(SLUG) })
  @ApiOkResponse({ type: SolveResponseDto })
  @ApiNotFoundResponse({ type: ErrorResponseDto })
  @ApiUnprocessableEntityResponse({ type: ErrorResponseDto })
  solve(
    @Body() body: ValidAnagramRequestDto,
    @Query("approach", new ApproachPipe(SLUG)) approach: string,
  ): SolveResponseDto<boolean> {
    const { result, elapsedMicros } = this.service.solve(body.s, body.t, approach);
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
      input: { s: body.s, t: body.t },
      result,
      elapsedMicros,
    };
  }
}
