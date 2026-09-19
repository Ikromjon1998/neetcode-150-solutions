/**
 * Entrypoint.
 *
 *     make run-node                 # from the repo root, http://localhost:3000
 *     npm run start:dev             # from this directory, with watch mode
 *
 * Then open http://localhost:3000/docs. Note how much more work the Swagger setup is here
 * than in FastAPI, where the Pydantic models already *are* the schema.
 */

import { createApp } from "./app.factory";

async function bootstrap(): Promise<void> {
  const app = await createApp();
  const port = Number(process.env["PORT"] ?? 3000);
  await app.listen(port);
  // eslint-disable-next-line no-console
  console.log(`NeetCode NestJS API listening on http://localhost:${port} (docs at /docs)`);
}

void bootstrap();
