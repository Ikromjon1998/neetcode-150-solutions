/**
 * Domain errors.
 *
 * These are thrown by the pure algorithms. The NestJS app maps them to HTTP statuses in a
 * single exception filter — the algorithms themselves never mention HTTP.
 *
 * Note the `Object.setPrototypeOf` in each constructor. Extending a built-in like `Error`
 * from TypeScript compiled down to ES5/ES2015 semantics breaks the prototype chain, so
 * `instanceof` silently returns false and the exception filter stops matching. This is the
 * single most common footgun in custom TypeScript errors; Python and PHP have no equivalent.
 */

export class NeetCodeError extends Error {
  constructor(message: string) {
    super(message);
    this.name = new.target.name;
    Object.setPrototypeOf(this, new.target.prototype);
  }
}

/**
 * Input was well formed but no answer exists.
 *
 * Distinct from invalid input: `[1, 2, 3]` with target `100` is a perfectly legal request
 * that simply has no answer. The app renders this as 404, not 422.
 */
export class NoSolutionError extends NeetCodeError {
  constructor(
    readonly slug: string,
    readonly detail = "No solution exists for the given input.",
  ) {
    super(`${slug}: ${detail}`);
  }
}

/** No problem is registered under that slug. */
export class UnknownProblemError extends NeetCodeError {
  constructor(readonly slug: string) {
    super(`Unknown problem: '${slug}'`);
  }
}

/** The problem exists but has no implementation registered under that approach key. */
export class UnknownApproachError extends NeetCodeError {
  constructor(
    readonly slug: string,
    readonly approach: string,
    readonly available: readonly string[] = [],
  ) {
    super(
      `Unknown approach '${approach}' for problem '${slug}'.` +
        (available.length ? ` Available: ${available.join(", ")}.` : ""),
    );
  }
}

/**
 * This approach has not been implemented yet — it is still an exercise.
 *
 * Thrown by every stub. Distinct from a crash: it is the expected state of a freshly cloned
 * repository, and it carries the path of the file you are meant to edit. The app renders it as
 * `501 Not Implemented` rather than a 500, so hitting the endpoint tells you where to go.
 */
export class UnsolvedError extends NeetCodeError {
  constructor(
    readonly slug: string,
    readonly approach: string,
    readonly path: string,
  ) {
    super(`${slug} / ${approach} is not implemented yet. Write it in ${path}`);
  }
}
