# 242. Valid Anagram

🟢 easy · **arrays-and-hashing** · 2 approaches to implement · [LeetCode](https://leetcode.com/problems/valid-anagram/)

## The problem

Return true when `t` is an anagram of `s` — that is, when both strings contain exactly the same characters with exactly the same multiplicities.

## Examples

Straight from the contract, which is what the tests read:

```json
// classic anagram
{"s": "anagram", "t": "nagaram"}  ->  true
// not an anagram
{"s": "rat", "t": "car"}  ->  false
// both empty
{"s": "", "t": ""}  ->  true
```

The full set — 8 cases, 4 invalid-input cases — is in [`0242-valid-anagram.json`](../../packages/contracts/problems/0242-valid-anagram.json).

> **New to arrays and hashing?** Read the topic guide first: [`01-arrays-and-hashing.md`](../topics/01-arrays-and-hashing.md). It covers the data structures you will need in all three languages — no problem answers in it.

## What to implement

| approach | must run in | using | what it is |
|---|---|---|---|
| `sorting` | O(n log n) | O(n) space | Two anagrams have the same sorted form. Three lines and obviously correct, which is worth something — but the sort dominates, and all three languages must copy the string to sort it. |
| `hash-map` *(default)* | O(n) | O(k) space | Count each character in `s`, decrement for each in `t`, and a single pass over the counts decides it. O(k) in the alphabet size, not the input length. |

The **default** approach is the one used when `?approach=` is omitted.

### Where

Three files, one per language. Each holds a stub per approach; replace the `raise` /
`throw` with your own code and leave everything else alone.

```
packages/core-python/src/neetcode_core/arrays_and_hashing/valid_anagram.py
packages/core-ts/src/arrays-and-hashing/valid-anagram.ts
packages/core-php/src/ArraysAndHashing/ValidAnagram.php
```

Write each one **idiomatically for its language**. If all three end up reading the same,
you have translated rather than learned — and the whole point of this repo is the
difference between the three.

## Check your work

```bash
make try SLUG=valid-anagram          # just this problem, all three languages
make try SLUG=valid-anagram LANG=python   # just one language
```

That is the loop. `make test` runs all six suites for every problem when you want it.

Every test is driven by the contract above, so the same cases run in all three languages.
There is also a differential test asserting that your approaches agree with each other —
which is why implementing the naive one first is worth the ten minutes.

Once it passes, the endpoint works in all three apps:

```bash
make run-python       # :8000   (also run-node :3000, run-php :8080)

curl -s 'localhost:8000/problems/valid-anagram?approach=hash-map' \
  -H 'content-type: application/json' \
  -d '{"s": "anagram", "t": "nagaram"}'
```

## Stuck?

```bash
make show SLUG=valid-anagram              # prints a worked answer, touches nothing
make solution SLUG=valid-anagram          # writes it over your stub (make restore undoes it)
```

There is also a full cross-language write-up — what differed between the three languages
and the three frameworks, and what went wrong — in
[`solutions/notes/0242-valid-anagram.md`](../../solutions/notes/0242-valid-anagram.md).
**It contains the answers.** Read it after you have solved this, not before.

---

*Generated from the contract by `make statements`. Do not edit by hand.*
