# 49. Group Anagrams

**Difficulty:** medium · **Topic:** arrays-and-hashing · **Approaches:** sorted-key, count-key
**LeetCode:** https://leetcode.com/problems/group-anagrams/

## The problem

Group the input strings so that each group holds exactly the mutual anagrams.

LeetCode accepts any order; this repo pins each group sorted ascending and the groups sorted by
their first member, so the three implementations can be compared byte for byte.

## Approaches

### sorted-key — O(n·k log k) time, O(n·k) space

Two words are anagrams exactly when their sorted forms match, so the sorted string is a
ready-made group key. `k` is the word length; the `log k` is the per-word sort.

### count-key — O(n·k) time, O(n·k) space

Replace the per-word sort with a 26-slot tally. Linear in the word length.

## What differed between the three languages

### What may be used as a map key — the finding of this problem

`count-key` needs a 26-element tally to become a dictionary key, and the three languages give
three completely different answers:

| | Key | Why |
|---|---|---|
| Python | `tuple(counts)` — used **directly** | tuples are hashable and hash **by value** |
| TypeScript | `counts.join(",")` — must serialise | `Map` compares object keys by **reference**; two arrays with identical contents are different keys |
| PHP | `implode(',', $counts)` — must serialise | array keys are `int\|string` only; there is no other option |

Python is the only one of the three that can express "this composite value is the key" without
flattening it to a string. And the two that cannot are forced into it for *opposite* reasons —
JavaScript because its `Map` keys are too permissive (any object, compared by identity), PHP
because its array keys are too restrictive (scalars only).

Getting this wrong in TypeScript is silent: `new Map().set([1,2], "a").get([1,2])` returns
`undefined`, so every word would land in its own group and the output would look like a
plausible list of singletons.

### Canonical ordering, and PHP's list-vs-map problem

Imposing this repo's ordering needed one extra line in PHP that the others did not:

```php
return array_values($ordered);
```

A PHP array with non-sequential integer keys JSON-encodes as an **object**, not an array. After
`usort` the outer array is fine, but the grouping step produced string keys, and without
`array_values` the response would have been `{"0": [...], "1": [...]}` where the Python and
TypeScript apps returned `[[...], [...]]`.

Structurally different JSON, identical `var_dump` output. This is the second problem where the
same PHP hazard appeared (the first was `array_fill` in Product of Array Except Self), which
suggests it is worth a standing rule rather than a per-problem catch: **any PHP function that
returns an array destined for JSON gets `array_values` unless you can prove the keys are already
sequential.**

## What differed between the three frameworks

Nothing — and this was the first problem returning `string[][]`, a nested array. All three
serialised it identically on the first run.

## Where I got stuck

**Nowhere in the algorithm; twice in the tooling.** This was the first problem needing
`string[][]` as an input type, and it exposed that the generator only understood one level of
nesting:

- `class-validator`'s `each: true` descends exactly one level, so `@IsString({ each: true })` on
  a `string[][]` checks whether each *row* is a string and fails every time. There is no
  built-in for this — `@ValidateNested` needs a class per level, and a row of primitives has no
  class to point at. I wrote a `@IsMatrix("int" | "string")` decorator.
- Laravel needed a repeated wildcard, `board.*.*`, which is the one place its rule DSL is *more*
  expressive than `class-validator`'s.
- Pydantic handled `list[list[StrictStr]]` with no special case at all.

Three validation libraries, three completely different amounts of effort for the same
requirement. Pydantic wins this one outright.

## Benchmarks

n = 6 short words. Median of 7 runs, microseconds:

| Approach | Python | TypeScript | PHP |
|----------|--------|------------|-----|
| sorted-key | **3** | **3** | **3** |
| count-key | 4 | 4 | 4 |

Six three-letter words is far too small to separate O(k log k) from O(k) — and `count-key` is
marginally *behind* in all three, because allocating a 26-slot array per word costs more than
sorting three characters. The crossover needs long words, not many of them: try it with
50-character strings and the count key pulls ahead.

Worth noting the three languages are indistinguishable here. Every earlier benchmark in this
repo showed a spread; this one is entirely dominated by fixed per-request overhead.
