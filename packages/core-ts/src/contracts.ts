/**
 * Loader for the shared JSON contracts in `packages/contracts/`.
 *
 * One JSON file per problem is the single source of truth for metadata and test cases, and
 * all three languages read it. Adding a case to the JSON immediately tightens the Python,
 * TypeScript and PHP suites at once — there is no way for them to drift apart.
 */

import { existsSync, readdirSync, readFileSync, statSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { UnknownProblemError } from "./errors";
import type {
  Approach,
  ContractCase,
  NotFoundCase,
  ProblemMeta,
  ValidationCase,
} from "./types";

const ENV_VAR = "NEETCODE_CONTRACTS_DIR";

/**
 * Raw decoded contract, before it is narrowed into `ProblemMeta`.
 * `cases` are deliberately `unknown`-shaped: each problem has its own input type and the
 * per-problem test file is where that gets narrowed.
 */
export interface RawContract {
  id: number;
  slug: string;
  title: string;
  difficulty: ProblemMeta["difficulty"];
  topic: ProblemMeta["topic"];
  summary: string;
  approaches: Approach[];
  cases: ContractCase[];
  validationCases?: ValidationCase[];
  notFoundCases?: NotFoundCase[];
  leetcodeUrl?: string;
  neetcodeUrl?: string;
}

/**
 * Locate `packages/contracts/problems`.
 *
 * Walks up from `process.cwd()` rather than from `import.meta.url` or `__dirname` on purpose:
 * this file is compiled to CommonJS for the NestJS app and bundled as ESM elsewhere, and
 * those two module systems disagree about how a module finds its own path. `cwd` works
 * identically under both. `$NEETCODE_CONTRACTS_DIR` overrides it for containers and CI.
 */
export function contractsDir(): string {
  const override = process.env[ENV_VAR];
  if (override) {
    const path = resolve(override);
    if (!existsSync(path) || !statSync(path).isDirectory()) {
      throw new Error(`$${ENV_VAR} points at ${path}, which is not a directory.`);
    }
    return path;
  }

  let current = process.cwd();
  for (;;) {
    const candidate = join(current, "packages", "contracts", "problems");
    if (existsSync(candidate) && statSync(candidate).isDirectory()) return candidate;
    const parent = dirname(current);
    if (parent === current) break;
    current = parent;
  }

  throw new Error(
    `Could not find packages/contracts/problems by walking up from ${process.cwd()}. ` +
      `Set $${ENV_VAR} to point at it explicitly.`,
  );
}

let cache: Map<string, RawContract> | undefined;

function loadAll(): Map<string, RawContract> {
  if (cache) return cache;
  const byslug = new Map<string, RawContract>();
  for (const file of readdirSync(contractsDir()).filter((f) => f.endsWith(".json")).sort()) {
    const data = JSON.parse(readFileSync(join(contractsDir(), file), "utf8")) as RawContract;
    if (byslug.has(data.slug)) throw new Error(`Duplicate contract slug '${data.slug}' in ${file}`);
    byslug.set(data.slug, data);
  }
  cache = byslug;
  return byslug;
}

/** The decoded JSON for one problem, exactly as written on disk. */
export function rawContract(slug: string): RawContract {
  const contract = loadAll().get(slug);
  if (!contract) throw new UnknownProblemError(slug);
  return contract;
}

export function allSlugs(): string[] {
  return [...loadAll().keys()];
}

/** Parse one contract into the typed `ProblemMeta` the rest of the code uses. */
export function loadMeta(slug: string): ProblemMeta {
  const data = rawContract(slug);
  return {
    id: data.id,
    slug: data.slug,
    title: data.title,
    difficulty: data.difficulty,
    topic: data.topic,
    summary: data.summary,
    approaches: data.approaches,
    leetcodeUrl: data.leetcodeUrl,
    neetcodeUrl: data.neetcodeUrl,
  };
}

/** Happy-path cases, typed by the caller who knows this problem's input shape. */
export function contractCases<TInput = Record<string, unknown>, TExpected = unknown>(
  slug: string,
): ContractCase<TInput, TExpected>[] {
  return rawContract(slug).cases as unknown as ContractCase<TInput, TExpected>[];
}

/** Malformed-input cases. Asserted at the HTTP layer only. */
export function validationCases<TInput = Record<string, unknown>>(slug: string): ValidationCase<TInput>[] {
  return (rawContract(slug).validationCases ?? []) as unknown as ValidationCase<TInput>[];
}

/** Well-formed input with no answer. */
export function notFoundCases<TInput = Record<string, unknown>>(slug: string): NotFoundCase<TInput>[] {
  return (rawContract(slug).notFoundCases ?? []) as unknown as NotFoundCase<TInput>[];
}
