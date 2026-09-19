/**
 * Aggregates every problem feature module.
 *
 * This is the TypeScript half of the registry story. The FastAPI app discovers its routers by
 * walking the package with `pkgutil`, and needs no file like this. NestJS cannot: its module
 * graph is resolved at compile time so the injector can be built ahead of any request, which
 * is exactly what makes startup errors (a missing provider, a circular dependency) surface at
 * boot instead of on the first request.
 *
 * ADD NEW PROBLEM MODULES HERE. `npm run new-problem` inserts the import and the entry.
 */

import { Module } from "@nestjs/common";
import { TwoSumModule } from "./two-sum/two-sum.module";
import { EncodeAndDecodeStringsModule } from "./encode-and-decode-strings/encode-and-decode-strings.module";
import { ValidSudokuModule } from "./valid-sudoku/valid-sudoku.module";
import { GroupAnagramsModule } from "./group-anagrams/group-anagrams.module";
import { TopKFrequentElementsModule } from "./top-k-frequent-elements/top-k-frequent-elements.module";
import { LongestConsecutiveSequenceModule } from "./longest-consecutive-sequence/longest-consecutive-sequence.module";
import { ProductOfArrayExceptSelfModule } from "./product-of-array-except-self/product-of-array-except-self.module";
import { ContainsDuplicateModule } from "./contains-duplicate/contains-duplicate.module";
import { ValidAnagramModule } from "./valid-anagram/valid-anagram.module";

const PROBLEM_MODULES = [TwoSumModule, ValidAnagramModule, ContainsDuplicateModule, ProductOfArrayExceptSelfModule, LongestConsecutiveSequenceModule, TopKFrequentElementsModule, GroupAnagramsModule, ValidSudokuModule, EncodeAndDecodeStringsModule];

@Module({ imports: PROBLEM_MODULES })
export class ProblemsModule {}
