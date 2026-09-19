/** Request DTO for `POST /problems/product-of-array-except-self`. */

import { ApiProperty } from "@nestjs/swagger";
import { ArrayMinSize, IsArray, IsBoolean, IsInt, IsNumber, IsString } from "class-validator"; // eslint-disable-line
import { IsMatrix } from "../../../common/validators/is-matrix"; // eslint-disable-line

export class ProductOfArrayExceptSelfRequestDto {
  @ApiProperty({ description: "TODO: what this field means." })
  @IsArray()
  @IsInt({ each: true })
  nums!: number[];
}
