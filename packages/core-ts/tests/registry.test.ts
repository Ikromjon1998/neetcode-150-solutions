/**
 * Registry-level guards.
 *
 * These run against every problem in the package, so they keep paying off as the repo grows:
 * problem 150 is checked by exactly the same tests as problem 1.
 */

import { describe, expect, it } from "vitest";
import {
  allMeta,
  approachesFor,
  getSolution,
  registeredSlugs,
  UnknownApproachError,
  UnknownProblemError,
  verifyRegistry,
} from "../src/index";

describe("registry", () => {
  it("agrees with the JSON contracts", () => {
    expect(() => verifyRegistry()).not.toThrow();
  });

  it("registers two-sum", () => {
    expect(registeredSlugs()).toContain("two-sum");
  });

  it("orders problems by LeetCode id", () => {
    const ids = allMeta().map((meta) => meta.id);
    expect(ids).toEqual([...ids].sort((a, b) => a - b));
  });

  it.each(allMeta())("$slug declares at most one default approach", (meta) => {
    expect(meta.approaches.filter((a) => a.default).length).toBeLessThanOrEqual(1);
  });

  it.each(registeredSlugs())("%s resolves a default approach without an explicit key", (slug) => {
    expect(typeof getSolution(slug)).toBe("function");
  });

  it("throws UnknownProblemError for an unregistered slug", () => {
    expect(() => getSolution("does-not-exist")).toThrow(UnknownProblemError);
  });

  it("lists the available approaches when the key is wrong", () => {
    try {
      getSolution("two-sum", "quantum");
      expect.unreachable("should have thrown");
    } catch (error) {
      expect(error).toBeInstanceOf(UnknownApproachError);
      expect([...(error as UnknownApproachError).available].sort()).toEqual(
        approachesFor("two-sum").sort(),
      );
    }
  });
});
