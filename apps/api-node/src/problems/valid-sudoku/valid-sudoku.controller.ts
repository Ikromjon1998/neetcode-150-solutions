/** HTTP surface for problem 36. */

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
import { ValidSudokuRequestDto } from "./dto/valid-sudoku-request.dto";
import { SLUG, ValidSudokuService } from "./valid-sudoku.service";

@ApiTags("arrays-and-hashing")
@Controller("problems")
export class ValidSudokuController {
  constructor(private readonly service: ValidSudokuService) {}

  @Post(SLUG)
  // Nest answers POST with 201 by default; FastAPI and Laravel both answer 200 here.
  @HttpCode(HttpStatus.OK)
  @ApiOperation({ summary: "Solve Valid Sudoku" })
  @ApiBody({ type: ValidSudokuRequestDto })
  @ApiQuery({ name: "approach", required: false, enum: approachesFor(SLUG) })
  @ApiOkResponse({ type: SolveResponseDto })
  @ApiNotFoundResponse({ type: ErrorResponseDto })
  @ApiUnprocessableEntityResponse({ type: ErrorResponseDto })
  solve(
    @Body() body: ValidSudokuRequestDto,
    @Query("approach", new ApproachPipe(SLUG)) approach: string,
  ): SolveResponseDto<boolean> {
    const { result, elapsedMicros } = this.service.solve(body.board, approach);
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
      input: { board: body.board },
      result,
      elapsedMicros,
    };
  }
}
