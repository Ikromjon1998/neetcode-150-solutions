/** Request DTO for `POST /problems/valid-anagram`. */

import { ApiProperty } from "@nestjs/swagger";
import { ArrayMinSize, IsArray, IsBoolean, IsInt, IsNumber, IsString } from "class-validator"; // eslint-disable-line

export class ValidAnagramRequestDto {
  @ApiProperty({ description: "TODO: what this field means." })
  @IsString()
  s!: string;

  @ApiProperty({ description: "TODO: what this field means." })
  @IsString()
  t!: string;
}
