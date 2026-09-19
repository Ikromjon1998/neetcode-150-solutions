# 347. Top K Frequent Elements

🟡 medium · **arrays-and-hashing** · 2 approaches to implement · [LeetCode](https://leetcode.com/problems/top-k-frequent-elements/)

## The problem

Return the `k` most frequent values in `nums`. LeetCode accepts any order; this repo pins a canonical one — descending by frequency, then ascending by value — so the three implementations can be compared byte for byte.

## Examples

Straight from the contract, which is what the tests read:

```json
// textbook
{"nums": [1, 1, 1, 2, 2, 3], "k": 2}  ->  [1, 2]
// single element
{"nums": [1], "k": 1}  ->  [1]
// tie broken by value
{"nums": [1, 2], "k": 2}  ->  [1, 2]
```

The full set — 9 cases, 4 invalid-input cases — is in [`0347-top-k-frequent-elements.json`](../../packages/contracts/problems/0347-top-k-frequent-elements.json).

## What to implement

| approach | must run in | using | what it is |
|---|---|---|---|
| `sorting` | O(n log n) | O(n) space | Tally, then sort the distinct values. The sort dominates, but on the small inputs this problem usually sees it is the fastest of the two. |
| `bucket-sort` *(default)* | O(n) | O(n) space | A count can never exceed n, so an array of n+1 buckets indexed by frequency replaces the sort entirely. Walking it from the back yields values in descending frequency for free. |

The **default** approach is the one used when `?approach=` is omitted.

### Where

Three files, one per language. Each holds a stub per approach; replace the `raise` /
`throw` with your own code and leave everything else alone.

```
packages/core-python/src/neetcode_core/arrays_and_hashing/top_k_frequent_elements.py
packages/core-ts/src/arrays-and-hashing/top-k-frequent-elements.ts
packages/core-php/src/ArraysAndHashing/TopKFrequentElements.php
```

Write each one **idiomatically for its language**. If all three end up reading the same,
you have translated rather than learned — and the whole point of this repo is the
difference between the three.

## Check your work

```bash
make try SLUG=top-k-frequent-elements          # just this problem, all three languages
make try SLUG=top-k-frequent-elements LANG=python   # just one language
```

That is the loop. `make test` runs all six suites for every problem when you want it.

Every test is driven by the contract above, so the same cases run in all three languages.
There is also a differential test asserting that your approaches agree with each other —
which is why implementing the naive one first is worth the ten minutes.

Once it passes, the endpoint works in all three apps:

```bash
make run-python       # :8000   (also run-node :3000, run-php :8080)

curl -s 'localhost:8000/problems/top-k-frequent-elements?approach=bucket-sort' \
  -H 'content-type: application/json' \
  -d '{"nums": [1, 1, 1, 2, 2, 3], "k": 2}'
```

## Stuck?

```bash
make show SLUG=top-k-frequent-elements              # prints a worked answer, touches nothing
make solution SLUG=top-k-frequent-elements          # writes it over your stub (make restore undoes it)
```

There is also a full cross-language write-up — what differed between the three languages
and the three frameworks, and what went wrong — in
[`solutions/notes/0347-top-k-frequent-elements.md`](../../solutions/notes/0347-top-k-frequent-elements.md).
**It contains the answers.** Read it after you have solved this, not before.

---

*Generated from the contract by `make statements`. Do not edit by hand.*
