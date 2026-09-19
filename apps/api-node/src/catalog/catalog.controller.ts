/**
 * Catalog endpoints — the same two routes exist in all three apps.
 *
 * Route order matters: this controller is registered *after* the problem modules in
 * `AppModule`, so `POST /problems/two-sum` is matched by its own controller and only the
 * unclaimed `GET /problems/:slug` falls through to here.
 */

import { Controller, Get, Param } from "@nestjs/common";
import { ApiNotFoundResponse, ApiOkResponse, ApiTags } from "@nestjs/swagger";
import {
  ErrorResponseDto,
  ProblemSummaryDto,
} from "../common/dto/solve-response.dto";
import { CatalogService } from "./catalog.service";

@ApiTags("catalog")
@Controller("problems")
export class CatalogController {
  constructor(private readonly catalog: CatalogService) {}

  @Get()
  @ApiOkResponse({ type: [ProblemSummaryDto], description: "Every solved problem." })
  list(): ProblemSummaryDto[] {
    return this.catalog.list();
  }

  @Get(":slug")
  @ApiOkResponse({ type: ProblemSummaryDto })
  @ApiNotFoundResponse({ type: ErrorResponseDto })
  find(@Param("slug") slug: string): ProblemSummaryDto {
    return this.catalog.find(slug);
  }
}
