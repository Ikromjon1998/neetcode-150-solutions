# `packages/contracts`

JSON. No code. **The single source of truth for every problem in this repo.**

One file per problem holds the metadata *and* the test cases, and six test suites across three
languages read it. Adding a case here tightens Python, TypeScript and PHP at once — the
implementations cannot drift apart.

```
problems/
  0001-two-sum.json
  0242-valid-anagram.json
schema/
  problem-contract.schema.json
```

Filenames are `{id:04d}-{slug}.json`, enforced by `make test-contracts`.

## Shape

```jsonc
{
  "id": 1, "slug": "two-sum", "title": "Two Sum",
  "difficulty": "easy",                    // easy | medium | hard
  "topic": "arrays-and-hashing",           // one of the 18 NeetCode topics
  "leetcodeUrl": "https://leetcode.com/problems/two-sum/",
  "summary": "One paragraph. Rendered into the API catalog and the docs.",

  "approaches": [
    { "key": "brute-force", "name": "Nested loops",
      "time": "O(n^2)", "space": "O(1)", "note": "why it is kept" },
    { "key": "hash-map",    "name": "One-pass hash map",
      "time": "O(n)", "space": "O(n)", "default": true }
  ],

  // correct answers — asserted by the core suites AND over HTTP by the app suites
  "cases": [
    { "name": "pair at the front", "input": { "nums": [2,7,11,15], "target": 9 }, "expected": [0,1] }
  ],

  // malformed input — app suites only; validation is the framework's job
  "validationCases": [
    { "name": "fewer than two numbers", "input": { "nums": [1], "target": 1 }, "status": 422 }
  ],

  // well-formed input with no answer — core raises, apps return 404
  "notFoundCases": [
    { "name": "no pair sums to target", "input": { "nums": [1,2,3], "target": 100 } }
  ]
}
```

The full schema, with every field documented, is `schema/problem-contract.schema.json`.

## Rules

All enforced by `make test-contracts`:

- filename matches `{id:04d}-{slug}.json`
- `slug` and every `approach.key` are kebab-case
- ids and slugs are unique across all files
- exactly one approach carries `"default": true`
- every declared approach is implemented in **all three** languages
- no `TODO` in the summary or a case name; no `O(?)` complexity

## Who reads this

| Reader | Section |
|--------|---------|
| `packages/core-python/tests/` | `cases`, `notFoundCases` |
| `packages/core-ts/tests/` | `cases`, `notFoundCases` |
| `packages/core-php/tests/` | `cases`, `notFoundCases` |
| `apps/api-python/tests/` | all three |
| `apps/api-node/test/` | all three |
| `apps/api-php/tests/Feature/` | all three |
| `GET /problems` in all three apps | metadata |
| `tools/progress.py` | metadata |

## Choosing cases

Six or more happy-path cases, deliberately including the ones you would forget: empty input,
duplicates, negatives, the answer at either end, the "almost" case, and **non-ASCII for any
string problem**. That last one is what catches PHP's byte-wise `strlen`/`str_split` and
JavaScript's surrogate-pair splitting — see
[`docs/problems/0242-valid-anagram.md`](../../docs/problems/0242-valid-anagram.md).
