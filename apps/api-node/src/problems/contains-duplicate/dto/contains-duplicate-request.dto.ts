/** Request DTO for `POST /problems/contains-duplicate`. */

import { ApiProperty } from "@nestjs/swagger";
import { ArrayMinSize, IsArray, IsBoolean, IsInt, IsNumber, IsString } from "class-validator"; // eslint-disable-line

export class ContainsDuplicateRequestDto {
  @ApiProperty({ description: "TODO: what this field means." })
  @IsArray()
  @IsInt({ each: true })
  nums!: number[];
}
