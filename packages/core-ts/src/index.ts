/**
 * NeetCode algorithms as a real, typed TypeScript library.
 *
 * Public surface — import from `@neetcode/core`, not from the internal paths, in app code:
 *
 * ```ts
 * import { getSolution, allMeta, NoSolutionError } from "@neetcode/core";
 *
 * const solve = getSolution("two-sum", "hash-map") as TwoSumFn;
 * solve([2, 7, 11, 15], 9); // -> [0, 1]
 * ```
 */

export * from "./types";
export * from "./errors";
export {
  allSlugs,
  contractCases,
  contractsDir,
  loadMeta,
  notFoundCases,
  rawContract,
  validationCases,
} from "./contracts";
export type { RawContract } from "./contracts";
export { defineProblem } from "./define-problem";
export {
  allMeta,
  approachesFor,
  defaultApproach,
  findApproach,
  getMeta,
  getSolution,
  registeredSlugs,
  verifyRegistry,
} from "./registry";

// Per-problem exports, so a consumer can import one algorithm directly and keep its exact
// signature instead of going through the loosely typed registry.
export { SLUG as TWO_SUM, twoSum, twoSumBruteForce, twoSumHashMap } from "./arrays-and-hashing/two-sum";
export { SLUG as ENCODE_AND_DECODE_STRINGS, encodeAndDecodeStrings, encodeAndDecodeStringsLengthPrefixed, encodeAndDecodeStringsDelimiterEscaped } from "./arrays-and-hashing/encode-and-decode-strings";
export { SLUG as VALID_SUDOKU, validSudoku, validSudokuThreePass, validSudokuSinglePass } from "./arrays-and-hashing/valid-sudoku";
export { SLUG as GROUP_ANAGRAMS, groupAnagrams, groupAnagramsSortedKey, groupAnagramsCountKey } from "./arrays-and-hashing/group-anagrams";
export { SLUG as TOP_K_FREQUENT_ELEMENTS, topKFrequentElements, topKFrequentElementsSorting, topKFrequentElementsBucketSort } from "./arrays-and-hashing/top-k-frequent-elements";
export { SLUG as LONGEST_CONSECUTIVE_SEQUENCE, longestConsecutiveSequence, longestConsecutiveSequenceSorting, longestConsecutiveSequenceHashSet } from "./arrays-and-hashing/longest-consecutive-sequence";
export { SLUG as PRODUCT_OF_ARRAY_EXCEPT_SELF, productOfArrayExceptSelf, productOfArrayExceptSelfBruteForce, productOfArrayExceptSelfPrefixSuffix } from "./arrays-and-hashing/product-of-array-except-self";
export { SLUG as CONTAINS_DUPLICATE, containsDuplicate, containsDuplicateBruteForce, containsDuplicateSorting, containsDuplicateHashSet } from "./arrays-and-hashing/contains-duplicate";
export { SLUG as VALID_ANAGRAM, validAnagram, validAnagramSorting, validAnagramHashMap } from "./arrays-and-hashing/valid-anagram";
