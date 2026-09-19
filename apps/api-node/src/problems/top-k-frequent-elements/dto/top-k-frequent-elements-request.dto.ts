/** Request DTO for `POST /problems/top-k-frequent-elements`. */

import { ApiProperty } from "@nestjs/swagger";
import { ArrayMinSize, IsArray, IsBoolean, IsInt, IsNumber, IsString } from "class-validator"; // eslint-disable-line
import { IsMatrix } from "../../../common/validators/is-matrix"; // eslint-disable-line

export class TopKFrequentElementsRequestDto {
  @ApiProperty({ description: "TODO: what this field means." })
  @IsArray()
  @IsInt({ each: true })
  nums!: number[];

  @ApiProperty({ description: "TODO: what this field means." })
  @IsInt()
  k!: number;
}
