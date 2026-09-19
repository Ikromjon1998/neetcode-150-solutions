import { Module } from "@nestjs/common";
import { ValidAnagramController } from "./valid-anagram.controller";
import { ValidAnagramService } from "./valid-anagram.service";

@Module({
  controllers: [ValidAnagramController],
  providers: [ValidAnagramService],
})
export class ValidAnagramModule {}
