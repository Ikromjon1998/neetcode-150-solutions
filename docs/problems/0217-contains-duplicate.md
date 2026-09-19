# 217. Contains Duplicate

🟢 easy · **arrays-and-hashing** · 3 approaches to implement · [LeetCode](https://leetcode.com/problems/contains-duplicate/)

## The problem

Return true when any value appears in `nums` more than once, and false when every element is distinct.

## Examples

Straight from the contract, which is what the tests read:

```json
// has a duplicate
{"nums": [1, 2, 3, 1]}  ->  true
// all distinct
{"nums": [1, 2, 3, 4]}  ->  false
// duplicate at the end
{"nums": [1, 2, 3, 3]}  ->  true
```

The full set — 9 cases, 3 invalid-input cases — is in [`0217-contains-duplicate.json`](../../packages/contracts/problems/0217-contains-duplicate.json).

## What to implement

| approach | must run in | using | what it is |
|---|---|---|---|
| `brute-force` | O(n^2) | O(1) space | The only approach that allocates nothing. On inputs of a handful of elements it wins outright, which is worth seeing before dismissing it. |
| `sorting` | O(n log n) | O(n) space | Duplicates become adjacent once sorted. Not O(1) space in any of these three languages, since none can sort the caller's array in place without mutating it. |
| `hash-set` *(default)* | O(n) | O(n) space | Return on the first repeat, so the early-exit case is far better than O(n) in practice — a duplicate at index 1 costs two operations regardless of input size. |

The **default** approach is the one used when `?approach=` is omitted.

### Where

Three files, one per language. Each holds a stub per approach; replace the `raise` /
`throw` with your own code and leave everything else alone.

```
packages/core-python/src/neetcode_core/arrays_and_hashing/contains_duplicate.py
packages/core-ts/src/arrays-and-hashing/contains-duplicate.ts
packages/core-php/src/ArraysAndHashing/ContainsDuplicate.php
```

Write each one **idiomatically for its language**. If all three end up reading the same,
you have translated rather than learned — and the whole point of this repo is the
difference between the three.

## Check your work

```bash
make try SLUG=contains-duplicate          # just this problem, all three languages
make try SLUG=contains-duplicate LANG=python   # just one language
```

That is the loop. `make test` runs all six suites for every problem when you want it.

Every test is driven by the contract above, so the same cases run in all three languages.
There is also a differential test asserting that your approaches agree with each other —
which is why implementing the naive one first is worth the ten minutes.

Once it passes, the endpoint works in all three apps:

```bash
make run-python       # :8000   (also run-node :3000, run-php :8080)

curl -s 'localhost:8000/problems/contains-duplicate?approach=hash-set' \
  -H 'content-type: application/json' \
  -d '{"nums": [1, 2, 3, 1]}'
```

## Stuck?

```bash
make show SLUG=contains-duplicate              # prints a worked answer, touches nothing
make solution SLUG=contains-duplicate          # writes it over your stub (make restore undoes it)
```

There is also a full cross-language write-up — what differed between the three languages
and the three frameworks, and what went wrong — in
[`solutions/notes/0217-contains-duplicate.md`](../../solutions/notes/0217-contains-duplicate.md).
**It contains the answers.** Read it after you have solved this, not before.

---

*Generated from the contract by `make statements`. Do not edit by hand.*
