import { Module } from "@nestjs/common";
import { TwoSumController } from "./two-sum.controller";
import { TwoSumService } from "./two-sum.service";

@Module({
  controllers: [TwoSumController],
  providers: [TwoSumService],
})
export class TwoSumModule {}
