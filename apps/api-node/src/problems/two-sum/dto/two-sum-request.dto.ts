/**
 * Request DTO for `POST /problems/two-sum`.
 *
 * `class-validator` decorators are the NestJS counterpart of a Pydantic model and of a
 * Laravel FormRequest. The mechanism is different in one way that matters: these decorators
 * validate an *already-parsed* object, they do not parse it. That is why `@IsInt()` rejects
 * the JSON string `"7"` outright instead of coercing it — and why the Pydantic model in the
 * FastAPI app uses `StrictInt` rather than `int`, so that the two apps agree.
 */

import { ApiProperty } from "@nestjs/swagger";
import { ArrayMinSize, IsArray, IsInt } from "class-validator";

export class TwoSumRequestDto {
  @ApiProperty({
    type: [Number],
    minItems: 2,
    example: [2, 7, 11, 15],
    description: "At least two integers. The problem is undefined for shorter input.",
  })
  @IsArray()
  @ArrayMinSize(2)
  @IsInt({ each: true })
  nums!: number[];

  @ApiProperty({ example: 9, description: "The sum the two chosen numbers must produce." })
  @IsInt()
  target!: number;
}
