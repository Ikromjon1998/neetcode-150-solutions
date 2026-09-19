/**
 * Problem registry — explicit, static, type-checked.
 *
 * This is the TypeScript answer to "how does the app find the solutions?", and it is
 * deliberately different from how the Python and PHP sides do it:
 *
 * - **Python** — a decorator registers each function as an import side effect, and
 *   `pkgutil` walks the package. Drop in a file and it appears. No registration step.
 * - **TypeScript (here)** — one `import` line in `PROBLEM_MODULES` below. It costs a line
 *   per problem, and buys three things nothing else can: the bundler can tree-shake, the
 *   type-checker verifies every module really does export a `ProblemModule`, and there is no
 *   filesystem access at import time (so this file works in a browser or a Lambda bundle).
 * - **PHP/Laravel** — a service provider reads a config array, which is what lets
 *   `php artisan config:cache` freeze the whole thing at deploy time.
 *
 * `docs/06-language-comparison.md` covers why each ecosystem landed where it did.
 */

import { twoSum } from "./arrays-and-hashing/two-sum";
import { encodeAndDecodeStrings } from "./arrays-and-hashing/encode-and-decode-strings";
import { validSudoku } from "./arrays-and-hashing/valid-sudoku";
import { groupAnagrams } from "./arrays-and-hashing/group-anagrams";
import { topKFrequentElements } from "./arrays-and-hashing/top-k-frequent-elements";
import { longestConsecutiveSequence } from "./arrays-and-hashing/longest-consecutive-sequence";
import { productOfArrayExceptSelf } from "./arrays-and-hashing/product-of-array-except-self";
import { containsDuplicate } from "./arrays-and-hashing/contains-duplicate";
import { validAnagram } from "./arrays-and-hashing/valid-anagram";
import { defineProblem } from "./define-problem";
import { loadMeta } from "./contracts";
import { UnknownApproachError, UnknownProblemError } from "./errors";
import type { Approach, ProblemMeta, ProblemModule, SolutionFn } from "./types";

/**
 * Every problem module, in no particular order (the registry sorts by LeetCode id).
 *
 * ADD NEW PROBLEMS HERE. `npm run new-problem` does it for you; the generator inserts the
 * import above and the entry below.
 */
const PROBLEM_MODULES: readonly ProblemModule[] = [twoSum, validAnagram, containsDuplicate, productOfArrayExceptSelf, longestConsecutiveSequence, topKFrequentElements, groupAnagrams, validSudoku, encodeAndDecodeStrings];

const BY_SLUG: ReadonlyMap<string, ProblemModule> = new Map(
  PROBLEM_MODULES.map((module) => [module.slug, module]),
);

// Re-exported so problem modules and consumers have one obvious import site.
export { defineProblem };

/** Every registered slug, ordered by LeetCode id. */
export function registeredSlugs(): string[] {
  return [...BY_SLUG.keys()].sort((a, b) => loadMeta(a).id - loadMeta(b).id);
}

/** Metadata for every registered problem, ordered by LeetCode id. */
export function allMeta(): ProblemMeta[] {
  return registeredSlugs().map(loadMeta);
}

export function getMeta(slug: string): ProblemMeta {
  if (!BY_SLUG.has(slug)) throw new UnknownProblemError(slug);
  return loadMeta(slug);
}

export function approachesFor(slug: string): string[] {
  const module = BY_SLUG.get(slug);
  if (!module) throw new UnknownProblemError(slug);
  return Object.keys(module.solutions);
}

/** The approach a problem uses when no key is given. */
export function defaultApproach(slug: string): Approach {
  const { approaches } = getMeta(slug);
  return approaches.find((approach) => approach.default) ?? approaches[0]!;
}

export function findApproach(slug: string, key: string): Approach {
  const approach = getMeta(slug).approaches.find((candidate) => candidate.key === key);
  if (!approach) throw new UnknownApproachError(slug, key, approachesFor(slug));
  return approach;
}

/** Look up one implementation. Omit `approach` to get the contract's default. */
export function getSolution(slug: string, approach?: string): SolutionFn {
  const module = BY_SLUG.get(slug);
  if (!module) throw new UnknownProblemError(slug);
  const key = approach ?? defaultApproach(slug).key;
  const fn = module.solutions[key];
  if (!fn) throw new UnknownApproachError(slug, key, Object.keys(module.solutions));
  return fn;
}

/**
 * Fail loudly if code and contracts have drifted apart.
 *
 * Called by a test and by the NestJS app at boot. It catches the two mistakes that are easy
 * to make when adding a problem: implementing an approach you forgot to declare in the JSON,
 * or declaring one you forgot to implement.
 */
export function verifyRegistry(): void {
  const problems: string[] = [];
  for (const [slug, module] of BY_SLUG) {
    const meta = loadMeta(slug);
    const declared = new Set(meta.approaches.map((a) => a.key));
    const implemented = new Set(Object.keys(module.solutions));

    const missing = [...declared].filter((key) => !implemented.has(key));
    if (missing.length) {
      problems.push(`${slug}: declared in contract but not implemented: ${missing.join(", ")}`);
    }
    const extra = [...implemented].filter((key) => !declared.has(key));
    if (extra.length) {
      problems.push(`${slug}: implemented but not declared in contract: ${extra.join(", ")}`);
    }
    const defaults = meta.approaches.filter((a) => a.default);
    if (defaults.length > 1) {
      problems.push(`${slug}: more than one default approach: ${defaults.map((a) => a.key).join(", ")}`);
    }
  }
  if (problems.length) {
    throw new Error(`Registry does not match contracts:\n  - ${problems.join("\n  - ")}`);
  }
}
