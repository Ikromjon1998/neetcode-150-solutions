# 49. Group Anagrams

🟡 medium · **arrays-and-hashing** · 2 approaches to implement · [LeetCode](https://leetcode.com/problems/group-anagrams/)

## The problem

Group the strings so that every group holds exactly the mutual anagrams. LeetCode accepts any order; this repo pins a canonical one — each group sorted ascending, and the groups themselves sorted by their first member — so the three implementations can be compared byte for byte.

## Examples

Straight from the contract, which is what the tests read:

```json
// textbook
{"strs": ["eat", "tea", "tan", "ate", "nat", "bat"]}  ->  [["ate", "eat", "tea"], ["bat"], ["nat", "tan"]]
// empty string
{"strs": [""]}  ->  [[""]]
// single letter
{"strs": ["a"]}  ->  [["a"]]
```

The full set — 8 cases, 3 invalid-input cases — is in [`0049-group-anagrams.json`](../../packages/contracts/problems/0049-group-anagrams.json).

> **New to arrays and hashing?** Read the topic guide first: [`01-arrays-and-hashing.md`](../topics/01-arrays-and-hashing.md). It covers the data structures you will need in all three languages — no problem answers in it.

## What to implement

| approach | must run in | using | what it is |
|---|---|---|---|
| `sorted-key` | O(n k log k) | O(n k) space | Two words are anagrams exactly when their sorted forms match, so the sorted string is a ready-made group key. k is the word length; the log k is the per-word sort. |
| `count-key` *(default)* | O(n k) | O(n k) space | Replace the per-word sort with a 26-slot tally rendered as a key. Linear in the word length, and the clearest place in this repo where the three languages disagree about what may be used as a map key. |

The **default** approach is the one used when `?approach=` is omitted.

### Where

Three files, one per language. Each holds a stub per approach; replace the `raise` /
`throw` with your own code and leave everything else alone.

```
packages/core-python/src/neetcode_core/arrays_and_hashing/group_anagrams.py
packages/core-ts/src/arrays-and-hashing/group-anagrams.ts
packages/core-php/src/ArraysAndHashing/GroupAnagrams.php
```

Write each one **idiomatically for its language**. If all three end up reading the same,
you have translated rather than learned — and the whole point of this repo is the
difference between the three.

## Check your work

```bash
make try SLUG=group-anagrams          # just this problem, all three languages
make try SLUG=group-anagrams LANG=python   # just one language
```

That is the loop. `make test` runs all six suites for every problem when you want it.

Every test is driven by the contract above, so the same cases run in all three languages.
There is also a differential test asserting that your approaches agree with each other —
which is why implementing the naive one first is worth the ten minutes.

Once it passes, the endpoint works in all three apps:

```bash
make run-python       # :8000   (also run-node :3000, run-php :8080)

curl -s 'localhost:8000/problems/group-anagrams?approach=count-key' \
  -H 'content-type: application/json' \
  -d '{"strs": ["eat", "tea", "tan", "ate", "nat", "bat"]}'
```

## Stuck?

```bash
make show SLUG=group-anagrams              # prints a worked answer, touches nothing
make solution SLUG=group-anagrams          # writes it over your stub (make restore undoes it)
```

There is also a full cross-language write-up — what differed between the three languages
and the three frameworks, and what went wrong — in
[`solutions/notes/0049-group-anagrams.md`](../../solutions/notes/0049-group-anagrams.md).
**It contains the answers.** Read it after you have solved this, not before.

---

*Generated from the contract by `make statements`. Do not edit by hand.*
