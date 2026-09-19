# 238. Product of Array Except Self

🟡 medium · **arrays-and-hashing** · 2 approaches to implement · [LeetCode](https://leetcode.com/problems/product-of-array-except-self/)

## The problem

Return an array where each position holds the product of every element of `nums` except the one at that position. Division is not allowed, which is what makes the problem interesting — the obvious total-product-divided-by-self approach breaks on zeros anyway.

## Examples

Straight from the contract, which is what the tests read:

```json
// textbook
{"nums": [1, 2, 3, 4]}  ->  [24, 12, 8, 6]
// contains one zero
{"nums": [-1, 1, 0, -3, 3]}  ->  [0, 0, 9, 0, 0]
// contains two zeros
{"nums": [0, 1, 0]}  ->  [0, 0, 0]
```

The full set — 8 cases, 3 invalid-input cases — is in [`0238-product-of-array-except-self.json`](../../packages/contracts/problems/0238-product-of-array-except-self.json).

## What to implement

| approach | must run in | using | what it is |
|---|---|---|---|
| `brute-force` | O(n^2) | O(1) space | For every index, multiply everything else. The baseline, and the only one that needs no auxiliary reasoning. |
| `prefix-suffix` *(default)* | O(n) | O(1) space | Each answer is (product of everything to the left) x (product of everything to the right). Two passes, reusing the output array as the accumulator, so the extra space is a single running variable. |

The **default** approach is the one used when `?approach=` is omitted.

### Where

Three files, one per language. Each holds a stub per approach; replace the `raise` /
`throw` with your own code and leave everything else alone.

```
packages/core-python/src/neetcode_core/arrays_and_hashing/product_of_array_except_self.py
packages/core-ts/src/arrays-and-hashing/product-of-array-except-self.ts
packages/core-php/src/ArraysAndHashing/ProductOfArrayExceptSelf.php
```

Write each one **idiomatically for its language**. If all three end up reading the same,
you have translated rather than learned — and the whole point of this repo is the
difference between the three.

## Check your work

```bash
make try SLUG=product-of-array-except-self          # just this problem, all three languages
make try SLUG=product-of-array-except-self LANG=python   # just one language
```

That is the loop. `make test` runs all six suites for every problem when you want it.

Every test is driven by the contract above, so the same cases run in all three languages.
There is also a differential test asserting that your approaches agree with each other —
which is why implementing the naive one first is worth the ten minutes.

Once it passes, the endpoint works in all three apps:

```bash
make run-python       # :8000   (also run-node :3000, run-php :8080)

curl -s 'localhost:8000/problems/product-of-array-except-self?approach=prefix-suffix' \
  -H 'content-type: application/json' \
  -d '{"nums": [1, 2, 3, 4]}'
```

## Stuck?

```bash
make show SLUG=product-of-array-except-self              # prints a worked answer, touches nothing
make solution SLUG=product-of-array-except-self          # writes it over your stub (make restore undoes it)
```

There is also a full cross-language write-up — what differed between the three languages
and the three frameworks, and what went wrong — in
[`solutions/notes/0238-product-of-array-except-self.md`](../../solutions/notes/0238-product-of-array-except-self.md).
**It contains the answers.** Read it after you have solved this, not before.

---

*Generated from the contract by `make statements`. Do not edit by hand.*
