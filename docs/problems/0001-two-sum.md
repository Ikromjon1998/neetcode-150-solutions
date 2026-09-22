# 1. Two Sum

🟢 easy · **arrays-and-hashing** · 2 approaches to implement · [LeetCode](https://leetcode.com/problems/two-sum/) · [NeetCode](https://neetcode.io/problems/duplicate-integer)

## The problem

Return the indices of the two numbers in `nums` that add up to `target`. Exactly one solution exists and the same element may not be used twice.

## Examples

Straight from the contract, which is what the tests read:

```json
// pair at the front
{"nums": [2, 7, 11, 15], "target": 9}  ->  [0, 1]
// pair after the first
{"nums": [3, 2, 4], "target": 6}  ->  [1, 2]
// duplicate values
{"nums": [3, 3], "target": 6}  ->  [0, 1]
```

The full set — 6 cases, 5 invalid-input cases, 1 with no answer — is in [`0001-two-sum.json`](../../packages/contracts/problems/0001-two-sum.json).

> **New to arrays and hashing?** Read the topic guide first: [`01-arrays-and-hashing.md`](../topics/01-arrays-and-hashing.md). It covers the data structures you will need in all three languages — no problem answers in it.

## What to implement

| approach | must run in | using | what it is |
|---|---|---|---|
| `brute-force` | O(n^2) | O(1) space | Check every pair. Kept on purpose as the baseline the optimal approach is measured against. |
| `hash-map` *(default)* | O(n) | O(n) space | Trade space for time: remember every value seen so far and look up the complement in O(1). |

The **default** approach is the one used when `?approach=` is omitted.

### Where

Three files, one per language. Each holds a stub per approach; replace the `raise` /
`throw` with your own code and leave everything else alone.

```
packages/core-python/src/neetcode_core/arrays_and_hashing/two_sum.py
packages/core-ts/src/arrays-and-hashing/two-sum.ts
packages/core-php/src/ArraysAndHashing/TwoSum.php
```

Write each one **idiomatically for its language**. If all three end up reading the same,
you have translated rather than learned — and the whole point of this repo is the
difference between the three.

## Check your work

```bash
make try SLUG=two-sum          # just this problem, all three languages
make try SLUG=two-sum LANG=python   # just one language
```

That is the loop. `make test` runs all six suites for every problem when you want it.

Every test is driven by the contract above, so the same cases run in all three languages.
There is also a differential test asserting that your approaches agree with each other —
which is why implementing the naive one first is worth the ten minutes.

Once it passes, the endpoint works in all three apps:

```bash
make run-python       # :8000   (also run-node :3000, run-php :8080)

curl -s 'localhost:8000/problems/two-sum?approach=hash-map' \
  -H 'content-type: application/json' \
  -d '{"nums": [2, 7, 11, 15], "target": 9}'
```

## Stuck?

```bash
make show SLUG=two-sum              # prints a worked answer, touches nothing
make solution SLUG=two-sum          # writes it over your stub (make restore undoes it)
```

There is also a full cross-language write-up — what differed between the three languages
and the three frameworks, and what went wrong — in
[`solutions/notes/0001-two-sum.md`](../../solutions/notes/0001-two-sum.md).
**It contains the answers.** Read it after you have solved this, not before.

---

*Generated from the contract by `make statements`. Do not edit by hand.*
