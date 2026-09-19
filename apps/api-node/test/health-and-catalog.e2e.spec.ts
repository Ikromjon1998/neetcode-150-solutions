/** Endpoints that exist regardless of which problems are solved. */

import type { INestApplication } from "@nestjs/common";
import request from "supertest";
import { allMeta } from "@neetcode/core";
import { bootTestApp } from "./setup";

describe("health and catalog", () => {
  let app: INestApplication;

  beforeAll(async () => {
    app = await bootTestApp();
  });

  afterAll(async () => {
    await app.close();
  });

  const http = () => request(app.getHttpServer());

  it("reports health", async () => {
    const response = await http().get("/health").expect(200);
    expect(response.body.status).toBe("ok");
    expect(response.body.runtime).toBe("node/nestjs");
    expect(response.body.problemsRegistered).toBe(allMeta().length);
  });

  it("lists every registered problem", async () => {
    const response = await http().get("/problems").expect(200);
    const slugs = response.body.map((item: { slug: string }) => item.slug).sort();
    expect(slugs).toEqual(allMeta().map((meta) => meta.slug).sort());
    for (const item of response.body) {
      expect(item.endpoint).toBe(`/problems/${item.slug}`);
      expect(item.approaches.length).toBeGreaterThan(0);
    }
  });

  it("returns catalog metadata matching the contract", async () => {
    const { body } = await http().get("/problems/two-sum").expect(200);
    expect(body.id).toBe(1);
    expect(body.title).toBe("Two Sum");
    expect(body.difficulty).toBe("easy");
    expect(body.topic).toBe("arrays-and-hashing");
    expect(body.approaches.map((a: { key: string }) => a.key).sort()).toEqual([
      "brute-force",
      "hash-map",
    ]);
  });

  it("404s an unknown problem", async () => {
    const { body } = await http().get("/problems/not-a-real-problem").expect(404);
    expect(body.error.type).toBe("unknown_problem");
  });

  it("serves the generated OpenAPI schema", async () => {
    const { body } = await http().get("/openapi.json").expect(200);
    expect(body.paths["/problems/two-sum"]).toBeDefined();
    expect(body.paths["/problems/two-sum"].post).toBeDefined();
  });
});
