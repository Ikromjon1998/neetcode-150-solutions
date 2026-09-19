/** Request DTO for `POST /problems/valid-sudoku`. */

import { ApiProperty } from "@nestjs/swagger";
import { ArrayMinSize, IsArray, IsBoolean, IsInt, IsNumber, IsString } from "class-validator"; // eslint-disable-line
import { IsMatrix } from "../../../common/validators/is-matrix"; // eslint-disable-line

export class ValidSudokuRequestDto {
  @ApiProperty({ description: "TODO: what this field means." })
  @IsArray()
  @IsMatrix("string")
  board!: string[][];
}
