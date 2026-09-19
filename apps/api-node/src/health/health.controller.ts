/** Liveness endpoint. Mirrors FastAPI's `/health` and Laravel's built-in `/up`. */

import { Controller, Get } from "@nestjs/common";
import { ApiOkResponse, ApiTags } from "@nestjs/swagger";
import { registeredSlugs } from "@neetcode/core";

@ApiTags("meta")
@Controller("health")
export class HealthController {
  @Get()
  @ApiOkResponse({ description: "Service is up and the registry loaded." })
  check(): Record<string, unknown> {
    return {
      status: "ok",
      runtime: "node/nestjs",
      version: process.env["npm_package_version"] ?? "1.0.0",
      problemsRegistered: registeredSlugs().length,
    };
  }
}
