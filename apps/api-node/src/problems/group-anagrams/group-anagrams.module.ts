import { Module } from "@nestjs/common";
import { GroupAnagramsController } from "./group-anagrams.controller";
import { GroupAnagramsService } from "./group-anagrams.service";

@Module({
  controllers: [GroupAnagramsController],
  providers: [GroupAnagramsService],
})
export class GroupAnagramsModule {}
