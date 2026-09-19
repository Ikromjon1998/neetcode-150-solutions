/**
 * Shared e2e bootstrap.
 *
 * Boots the real application through `createApp()` — the same factory `main.ts` uses — so the
 * tests exercise the production validation pipe and exception filter. This is the NestJS
 * counterpart of FastAPI's `TestClient(create_app())` and Laravel's `$this->postJson()`.
 */

import http from "node:http";
import type { INestApplication } from "@nestjs/common";
import { createApp } from "../src/app.factory";

/**
 * Turn off HTTP keep-alive for the whole worker.
 *
 * Node 19+ ships `http.globalAgent` with `keepAlive: true`, and supertest goes through the
 * global agent. Express meanwhile closes idle connections after `server.keepAliveTimeout`
 * (5s by default). A request written onto a socket the server is closing at that same moment
 * is never answered and never errors — it simply hangs until Jest's timeout fires, taking
 * every queued request behind it down too.
 *
 * Symptom: one e2e file occasionally takes 270 seconds and reports a burst of consecutive
 * timeouts, while the same requests run 300 times in a row without a problem. Roughly one run
 * in fifteen locally; CI, being slower and more contended, would hit it more often.
 *
 * Tests are short-lived and make a few hundred requests in total, so the cost of a fresh
 * connection each time is irrelevant and the race disappears.
 */
// Replace the agent rather than mutate it: `keepAlive` is a constructor option, not a
// public property on Agent, so assigning to it does not type-check and would not reliably
// affect sockets already pooled.
http.globalAgent = new http.Agent({ keepAlive: false });

export async function bootTestApp(): Promise<INestApplication> {
  const app = await createApp({ logger: false });
  await app.init();
  return app;
}
