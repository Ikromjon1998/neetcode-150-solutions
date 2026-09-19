import { Module } from "@nestjs/common";
import { EncodeAndDecodeStringsController } from "./encode-and-decode-strings.controller";
import { EncodeAndDecodeStringsService } from "./encode-and-decode-strings.service";

@Module({
  controllers: [EncodeAndDecodeStringsController],
  providers: [EncodeAndDecodeStringsService],
})
export class EncodeAndDecodeStringsModule {}
