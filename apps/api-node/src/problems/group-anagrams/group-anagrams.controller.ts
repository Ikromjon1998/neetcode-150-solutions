/** HTTP surface for problem 49. */

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
import { GroupAnagramsRequestDto } from "./dto/group-anagrams-request.dto";
import { SLUG, GroupAnagramsService } from "./group-anagrams.service";

@ApiTags("arrays-and-hashing")
@Controller("problems")
export class GroupAnagramsController {
  constructor(private readonly service: GroupAnagramsService) {}

  @Post(SLUG)
  // Nest answers POST with 201 by default; FastAPI and Laravel both answer 200 here.
  @HttpCode(HttpStatus.OK)
  @ApiOperation({ summary: "Solve Group Anagrams" })
  @ApiBody({ type: GroupAnagramsRequestDto })
  @ApiQuery({ name: "approach", required: false, enum: approachesFor(SLUG) })
  @ApiOkResponse({ type: SolveResponseDto })
  @ApiNotFoundResponse({ type: ErrorResponseDto })
  @ApiUnprocessableEntityResponse({ type: ErrorResponseDto })
  solve(
    @Body() body: GroupAnagramsRequestDto,
    @Query("approach", new ApproachPipe(SLUG)) approach: string,
  ): SolveResponseDto<string[][]> {
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
