import { Module } from "@nestjs/common";
import { ValidSudokuController } from "./valid-sudoku.controller";
import { ValidSudokuService } from "./valid-sudoku.service";

@Module({
  controllers: [ValidSudokuController],
  providers: [ValidSudokuService],
})
export class ValidSudokuModule {}
