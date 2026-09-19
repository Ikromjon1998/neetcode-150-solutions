import { Module } from "@nestjs/common";
import { LongestConsecutiveSequenceController } from "./longest-consecutive-sequence.controller";
import { LongestConsecutiveSequenceService } from "./longest-consecutive-sequence.service";

@Module({
  controllers: [LongestConsecutiveSequenceController],
  providers: [LongestConsecutiveSequenceService],
})
export class LongestConsecutiveSequenceModule {}
