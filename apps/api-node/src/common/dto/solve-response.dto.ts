/**
 * Response shapes shared by every problem endpoint.
 *
 * The envelope is byte-for-byte identical in the FastAPI and Laravel apps. That is what makes
 * the three implementations comparable: you can point the same HTTP client at port 8000, 3000
 * or 8080 and diff the JSON.
 *
 * These are classes, not interfaces, and that is not a style choice. `@nestjs/swagger` builds
 * the OpenAPI schema from runtime metadata emitted by the decorators, and an interface leaves
 * nothing behind at runtime. FastAPI gets the same result for free because Pydantic models
 * are already runtime objects.
 */

import { ApiProperty, ApiPropertyOptional } from "@nestjs/swagger";

export class ApproachInfoDto {
  @ApiProperty({ example: "hash-map" })
  key!: string;

  @ApiProperty({ example: "One-pass hash map" })
  name!: string;

  @ApiProperty({ description: "Big-O time complexity.", example: "O(n)" })
  time!: string;

  @ApiProperty({ description: "Big-O auxiliary space.", example: "O(n)" })
  space!: string;

  @ApiPropertyOptional()
  note?: string;

  @ApiProperty({ default: false })
  default!: boolean;
}

export class ProblemSummaryDto {
  @ApiProperty({ example: 1 }) id!: number;
  @ApiProperty({ example: "two-sum" }) slug!: string;
  @ApiProperty({ example: "Two Sum" }) title!: string;
  @ApiProperty({ enum: ["easy", "medium", "hard"] }) difficulty!: string;
  @ApiProperty({ example: "arrays-and-hashing" }) topic!: string;
  @ApiProperty() summary!: string;
  @ApiProperty({ type: [ApproachInfoDto] }) approaches!: ApproachInfoDto[];
  @ApiPropertyOptional() leetcodeUrl?: string;
  @ApiPropertyOptional() neetcodeUrl?: string;

  @ApiProperty({ description: "Where to POST input.", example: "/problems/two-sum" })
  endpoint!: string;
}

export class SolveResponseDto<T> {
  @ApiProperty({ example: "two-sum" })
  problem!: string;

  @ApiProperty({ type: ApproachInfoDto })
  approach!: ApproachInfoDto;

  @ApiProperty({ type: Object, description: "The validated request body, echoed back." })
  input!: Record<string, unknown>;

  @ApiProperty()
  result!: T;

  @ApiProperty({
    description:
      "Wall-clock time spent inside the algorithm only — routing, validation and " +
      "serialisation are excluded, so the number is comparable across the three apps.",
  })
  elapsedMicros!: number;
}

export class ErrorDetailDto {
  @ApiProperty({ example: "no_solution" }) type!: string;
  @ApiProperty() message!: string;
  @ApiPropertyOptional() problem?: string;
  @ApiPropertyOptional({ type: [Object] }) details?: Array<Record<string, unknown>>;
}

/** Every non-2xx response in all three apps has exactly this shape. */
export class ErrorResponseDto {
  @ApiProperty({ type: ErrorDetailDto })
  error!: ErrorDetailDto;
}
