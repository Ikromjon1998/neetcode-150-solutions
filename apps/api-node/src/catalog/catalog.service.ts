/**
 * Turns registry metadata into catalog DTOs.
 *
 * Everything here is derived from `@neetcode/core`, so a newly added problem appears in the
 * catalog without anyone editing this file.
 */

import { Injectable } from "@nestjs/common";
import { allMeta, getMeta, type ProblemMeta } from "@neetcode/core";
import type { ProblemSummaryDto } from "../common/dto/solve-response.dto";

@Injectable()
export class CatalogService {
  list(): ProblemSummaryDto[] {
    return allMeta().map(toSummary);
  }

  /** Throws `UnknownProblemError`, which the global filter renders as 404. */
  find(slug: string): ProblemSummaryDto {
    return toSummary(getMeta(slug));
  }
}

function toSummary(meta: ProblemMeta): ProblemSummaryDto {
  return {
    id: meta.id,
    slug: meta.slug,
    title: meta.title,
    difficulty: meta.difficulty,
    topic: meta.topic,
    summary: meta.summary,
    approaches: meta.approaches.map((approach) => ({
      key: approach.key,
      name: approach.name,
      time: approach.time,
      space: approach.space,
      note: approach.note,
      default: approach.default ?? false,
    })),
    leetcodeUrl: meta.leetcodeUrl,
    neetcodeUrl: meta.neetcodeUrl,
    endpoint: `/problems/${meta.slug}`,
  };
}
