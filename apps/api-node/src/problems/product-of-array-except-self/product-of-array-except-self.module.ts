import { Module } from "@nestjs/common";
import { ProductOfArrayExceptSelfController } from "./product-of-array-except-self.controller";
import { ProductOfArrayExceptSelfService } from "./product-of-array-except-self.service";

@Module({
  controllers: [ProductOfArrayExceptSelfController],
  providers: [ProductOfArrayExceptSelfService],
})
export class ProductOfArrayExceptSelfModule {}
