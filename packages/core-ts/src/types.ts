/**
 * Value objects shared by every problem.
 *
 * Nothing here knows about HTTP, NestJS, or any framework. That separation is the whole point
 * of this package: the algorithms stay testable in isolation and the app stays thin.
 */

export type Difficulty = "easy" | "medium" | "hard";

/** The eighteen NeetCode 150 topics, in roadmap order. */
export const TOPICS = [
  "arrays-and-hashing",
  "two-pointers",
  "sliding-window",
  "stack",
  "binary-search",
  "linked-list",
  "trees",
  "tries",
  "heap-priority-queue",
  "backtracking",
  "graphs",
  "advanced-graphs",
  "1d-dynamic-programming",
  "2d-dynamic-programming",
  "greedy",
  "intervals",
  "math-and-geometry",
  "bit-manipulation",
] as const;

export type Topic = (typeof TOPICS)[number];

/** One implemented way of solving a problem, with its cost. */
export interface Approach {
  readonly key: string;
  readonly name: string;
  /** Big-O time, e.g. `"O(n log n)"`. */
  readonly time: string;
  /** Big-O auxiliary space. */
  readonly space: string;
  readonly note?: string;
  /** Exactly one approach per problem sets this; it is used when no key is given. */
  readonly default?: boolean;
}

/** Everything descriptive about a problem. Loaded from the shared JSON contract. */
export interface ProblemMeta {
  readonly id: number;
  readonly slug: string;
  readonly title: string;
  readonly difficulty: Difficulty;
  readonly topic: Topic;
  readonly summary: string;
  readonly approaches: readonly Approach[];
  readonly leetcodeUrl?: string;
  readonly neetcodeUrl?: string;
}

/** A single case lifted straight out of the JSON contract. */
export interface ContractCase<TInput = Record<string, unknown>, TExpected = unknown> {
  readonly name: string;
  readonly input: TInput;
  readonly expected: TExpected;
}

export interface ValidationCase<TInput = Record<string, unknown>> {
  readonly name: string;
  readonly input: TInput;
  readonly status: number;
}

export interface NotFoundCase<TInput = Record<string, unknown>> {
  readonly name: string;
  readonly input: TInput;
}

/** Any registered solution. Signatures vary per problem, so the arguments stay loose here. */
export type SolutionFn = (...args: never[]) => unknown;

/** What a problem module exports so the registry can pick it up. */
export interface ProblemModule {
  readonly slug: string;
  readonly solutions: Readonly<Record<string, SolutionFn>>;
}
