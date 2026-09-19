/**
 * Root module.
 *
 * Order matters: `ProblemsModule` is imported before `CatalogModule` so that a concrete
 * route like `POST /problems/two-sum` is registered before the parameterised
 * `GET /problems/:slug`. Express matches in registration order.
 */

import { Module } from "@nestjs/common";
import { CatalogModule } from "./catalog/catalog.module";
import { HealthModule } from "./health/health.module";
import { ProblemsModule } from "./problems/problems.module";

@Module({
  imports: [HealthModule, ProblemsModule, CatalogModule],
})
export class AppModule {}
