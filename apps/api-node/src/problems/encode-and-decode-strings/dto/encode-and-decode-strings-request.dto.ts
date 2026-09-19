/** Request DTO for `POST /problems/encode-and-decode-strings`. */

import { ApiProperty } from "@nestjs/swagger";
import { ArrayMinSize, IsArray, IsBoolean, IsInt, IsNumber, IsString } from "class-validator"; // eslint-disable-line
import { IsMatrix } from "../../../common/validators/is-matrix"; // eslint-disable-line

export class EncodeAndDecodeStringsRequestDto {
  @ApiProperty({ description: "TODO: what this field means." })
  @IsArray()
  @IsString({ each: true })
  strs!: string[];
}
