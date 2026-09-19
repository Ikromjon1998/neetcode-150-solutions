/** `POST /problems/encode-and-decode-strings`, driven by the shared JSON contract. */

import type { INestApplication } from "@nestjs/common";
import request from "supertest";
import { approachesFor, contractCases, validationCases } from "@neetcode/core";
import { bootTestApp } from "./setup";

const SLUG = "encode-and-decode-strings";
const URL = `/problems/${SLUG}`;
const CASES = contractCases(SLUG);

describe(`POST ${URL}`, () => {
  let app: INestApplication;

  beforeAll(async () => {
    app = await bootTestApp();
  });

  afterAll(async () => {
    await app.close();
  });

  const http = () => request(app.getHttpServer());

  describe.each(approachesFor(SLUG))("approach=%s", (approach) => {
    it.each(CASES)("$name", async ({ input, expected }) => {
      const { body } = await http().post(URL).query({ approach }).send(input).expect(200);
      expect(body.result).toEqual(expected);
    });
  });

  it.each(validationCases(SLUG))("422s invalid input: $name", async ({ input, status }) => {
    const { body } = await http().post(URL).send(input).expect(status);
    expect(body.error.type).toBe("validation_error");
  });
});
