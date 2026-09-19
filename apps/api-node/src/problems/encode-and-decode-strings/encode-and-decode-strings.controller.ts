/** HTTP surface for problem 271. */

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
import { EncodeAndDecodeStringsRequestDto } from "./dto/encode-and-decode-strings-request.dto";
import { SLUG, EncodeAndDecodeStringsService } from "./encode-and-decode-strings.service";

@ApiTags("arrays-and-hashing")
@Controller("problems")
export class EncodeAndDecodeStringsController {
  constructor(private readonly service: EncodeAndDecodeStringsService) {}

  @Post(SLUG)
  // Nest answers POST with 201 by default; FastAPI and Laravel both answer 200 here.
  @HttpCode(HttpStatus.OK)
  @ApiOperation({ summary: "Solve Encode and Decode Strings" })
  @ApiBody({ type: EncodeAndDecodeStringsRequestDto })
  @ApiQuery({ name: "approach", required: false, enum: approachesFor(SLUG) })
  @ApiOkResponse({ type: SolveResponseDto })
  @ApiNotFoundResponse({ type: ErrorResponseDto })
  @ApiUnprocessableEntityResponse({ type: ErrorResponseDto })
  solve(
    @Body() body: EncodeAndDecodeStringsRequestDto,
    @Query("approach", new ApproachPipe(SLUG)) approach: string,
  ): SolveResponseDto<string[]> {
    const { result, elapsedMicros } = this.service.solve(body.strs, approach);
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
      input: { strs: body.strs },
      result,
      elapsedMicros,
    };
  }
}
