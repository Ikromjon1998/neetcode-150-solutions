# 128. Longest Consecutive Sequence

🟡 medium · **arrays-and-hashing** · 2 approaches to implement · [LeetCode](https://leetcode.com/problems/longest-consecutive-sequence/)

## The problem

Return the length of the longest run of consecutive integers present in `nums`. The elements need not be adjacent in the array, and duplicates do not extend a run.

## Examples

Straight from the contract, which is what the tests read:

```json
// textbook
{"nums": [100, 4, 200, 1, 3, 2]}  ->  4
// long run with a duplicate
{"nums": [0, 3, 7, 2, 5, 8, 4, 6, 0, 1]}  ->  9
// two runs, longer second
{"nums": [9, 1, 4, 7, 3, -1, 0, 5, 8, -1, 6]}  ->  7
```

The full set — 9 cases, 3 invalid-input cases — is in [`0128-longest-consecutive-sequence.json`](../../packages/contracts/problems/0128-longest-consecutive-sequence.json).

> **New to arrays and hashing?** Read the topic guide first: [`01-arrays-and-hashing.md`](../topics/01-arrays-and-hashing.md). It covers the data structures you will need in all three languages — no problem answers in it.

## What to implement

| approach | must run in | using | what it is |
|---|---|---|---|
| `sorting` | O(n log n) | O(n) space | Once sorted, a run is a stretch of neighbours differing by exactly one. Duplicates must be skipped rather than counted, which is the detail this approach gets wrong first. |
| `hash-set` *(default)* | O(n) | O(n) space | Put everything in a set, then walk a run only from a value whose predecessor is absent. That guard is what keeps it O(n) — without it the inner loop re-walks every run from every member and it degrades to O(n^2). |

The **default** approach is the one used when `?approach=` is omitted.

### Where

Three files, one per language. Each holds a stub per approach; replace the `raise` /
`throw` with your own code and leave everything else alone.

```
packages/core-python/src/neetcode_core/arrays_and_hashing/longest_consecutive_sequence.py
packages/core-ts/src/arrays-and-hashing/longest-consecutive-sequence.ts
packages/core-php/src/ArraysAndHashing/LongestConsecutiveSequence.php
```

Write each one **idiomatically for its language**. If all three end up reading the same,
you have translated rather than learned — and the whole point of this repo is the
difference between the three.

## Check your work

```bash
make try SLUG=longest-consecutive-sequence          # just this problem, all three languages
make try SLUG=longest-consecutive-sequence LANG=python   # just one language
```

That is the loop. `make test` runs all six suites for every problem when you want it.

Every test is driven by the contract above, so the same cases run in all three languages.
There is also a differential test asserting that your approaches agree with each other —
which is why implementing the naive one first is worth the ten minutes.

Once it passes, the endpoint works in all three apps:

```bash
make run-python       # :8000   (also run-node :3000, run-php :8080)

curl -s 'localhost:8000/problems/longest-consecutive-sequence?approach=hash-set' \
  -H 'content-type: application/json' \
  -d '{"nums": [100, 4, 200, 1, 3, 2]}'
```

## Stuck?

```bash
make show SLUG=longest-consecutive-sequence              # prints a worked answer, touches nothing
make solution SLUG=longest-consecutive-sequence          # writes it over your stub (make restore undoes it)
```

There is also a full cross-language write-up — what differed between the three languages
and the three frameworks, and what went wrong — in
[`solutions/notes/0128-longest-consecutive-sequence.md`](../../solutions/notes/0128-longest-consecutive-sequence.md).
**It contains the answers.** Read it after you have solved this, not before.

---

*Generated from the contract by `make statements`. Do not edit by hand.*
