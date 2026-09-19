/**
 * `POST /problems/two-sum`, driven by the shared JSON contract.
 *
 * The identical case list is asserted by `apps/api-python/tests/test_two_sum.py` and by
 * `apps/api-php/tests/Feature/TwoSumTest.php`. If the three apps ever disagree about a
 * payload, one of the three suites goes red.
 */

import type { INestApplication } from "@nestjs/common";
import request from "supertest";
import {
  approachesFor,
  contractCases,
  notFoundCases,
  validationCases,
} from "@neetcode/core";
import { bootTestApp } from "./setup";

interface TwoSumInput {
  nums: unknown;
  target?: unknown;
}

const SLUG = "two-sum";
const URL = `/problems/${SLUG}`;
const APPROACHES = approachesFor(SLUG);
const CASES = contractCases<{ nums: number[]; target: number }, number[]>(SLUG);

describe("POST /problems/two-sum", () => {
  let app: INestApplication;

  beforeAll(async () => {
    app = await bootTestApp();
  });

  afterAll(async () => {
    await app.close();
  });

  const http = () => request(app.getHttpServer());

  describe.each(APPROACHES)("approach=%s", (approach) => {
    it.each(CASES)("$name", async ({ input, expected }) => {
      const { body } = await http()
        .post(URL)
        .query({ approach })
        .send(input)
        .expect(200);

      expect(body.result).toEqual(expected);
      expect(body.problem).toBe(SLUG);
      expect(body.approach.key).toBe(approach);
      expect(body.input).toEqual(input);
      expect(typeof body.elapsedMicros).toBe("number");
    });
  });

  it.each(CASES)("uses the default approach when the query is omitted: $name", async ({ input }) => {
    const { body } = await http().post(URL).send(input).expect(200);
    expect(body.approach.key).toBe("hash-map");
  });

  it.each(validationCases<TwoSumInput>(SLUG))("422s invalid input: $name", async ({ input, status }) => {
    const { body } = await http().post(URL).send(input).expect(status);
    expect(body.error.type).toBe("validation_error");
    expect(body.error.details.length).toBeGreaterThan(0);
  });

  it.each(notFoundCases<TwoSumInput>(SLUG))("404s when no pair exists: $name", async ({ input }) => {
    const { body } = await http().post(URL).send(input).expect(404);
    expect(body.error.type).toBe("no_solution");
  });

  it("422s an unknown approach", async () => {
    const { body } = await http()
      .post(URL)
      .query({ approach: "nope" })
      .send({ nums: [2, 7], target: 9 })
      .expect(422);
    expect(body.error.type).toBe("unknown_approach");
  });

  it("rejects an unexpected field", async () => {
    await http().post(URL).send({ nums: [2, 7], target: 9, targett: 9 }).expect(422);
  });
});
