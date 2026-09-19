import { Module } from "@nestjs/common";
import { TopKFrequentElementsController } from "./top-k-frequent-elements.controller";
import { TopKFrequentElementsService } from "./top-k-frequent-elements.service";

@Module({
  controllers: [TopKFrequentElementsController],
  providers: [TopKFrequentElementsService],
})
export class TopKFrequentElementsModule {}
