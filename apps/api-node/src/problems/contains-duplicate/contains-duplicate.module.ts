import { Module } from "@nestjs/common";
import { ContainsDuplicateController } from "./contains-duplicate.controller";
import { ContainsDuplicateService } from "./contains-duplicate.service";

@Module({
  controllers: [ContainsDuplicateController],
  providers: [ContainsDuplicateService],
})
export class ContainsDuplicateModule {}
