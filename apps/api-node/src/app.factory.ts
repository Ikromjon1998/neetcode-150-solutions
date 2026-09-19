/**
 * Builds a fully configured application.
 *
 * Extracted from `main.ts` so the e2e tests boot the *same* app the server does — same
 * validation pipe, same exception filter, same Swagger setup. A test that configures its own
 * pipeline is a test that can pass while production is broken.
 */

import { INestApplication, LogLevel, ValidationPipe } from "@nestjs/common";
import { NestFactory } from "@nestjs/core";
import { DocumentBuilder, SwaggerModule } from "@nestjs/swagger";
import { verifyRegistry } from "@neetcode/core";
import { AppModule } from "./app.module";
import { DomainExceptionFilter } from "./common/filters/domain-exception.filter";

const UNPROCESSABLE_CONTENT = 422;

export interface CreateAppOptions {
  /** Pass `false` from tests — otherwise every boot prints the full route table. */
  logger?: LogLevel[] | false;
}

export async function createApp(options: CreateAppOptions = {}): Promise<INestApplication> {
  // Fail the boot if a contract declares an approach nobody implemented. A container that
  // cannot serve correct answers should never pass its readiness check.
  verifyRegistry();

  const app = await NestFactory.create(AppModule, {
    logger: options.logger ?? ["error", "warn", "log"],
  });

  app.useGlobalPipes(
    new ValidationPipe({
      // Strip properties with no decorator...
      whitelist: true,
      // ...and reject the request outright when there are any. A typo'd field name is a bug,
      // not something to silently ignore. Matches Pydantic's `extra="forbid"`.
      forbidNonWhitelisted: true,
      transform: true,
      // Nest defaults to 400 here; FastAPI uses 422. Pinned so all three apps agree.
      errorHttpStatusCode: UNPROCESSABLE_CONTENT,
    }),
  );

  app.useGlobalFilters(new DomainExceptionFilter());

  const config = new DocumentBuilder()
    .setTitle("NeetCode API (TypeScript / NestJS)")
    .setDescription(
      "Each solved problem is a feature module: a controller, a validated request DTO, a " +
        "service, and tests driven by the shared JSON contract in `packages/contracts`. " +
        "The algorithms themselves live in the framework-free `@neetcode/core` package.",
    )
    .setVersion("1.0.0")
    .build();
  SwaggerModule.setup("docs", app, SwaggerModule.createDocument(app, config), {
    jsonDocumentUrl: "openapi.json",
  });

  return app;
}
