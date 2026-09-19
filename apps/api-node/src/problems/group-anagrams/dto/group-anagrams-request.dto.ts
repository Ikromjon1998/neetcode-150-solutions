/** Request DTO for `POST /problems/group-anagrams`. */

import { ApiProperty } from "@nestjs/swagger";
import { ArrayMinSize, IsArray, IsBoolean, IsInt, IsNumber, IsString } from "class-validator"; // eslint-disable-line
import { IsMatrix } from "../../../common/validators/is-matrix"; // eslint-disable-line

export class GroupAnagramsRequestDto {
  @ApiProperty({ description: "TODO: what this field means." })
  @IsArray()
  @IsString({ each: true })
  strs!: string[];
}
