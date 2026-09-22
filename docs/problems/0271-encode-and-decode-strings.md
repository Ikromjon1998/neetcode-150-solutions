# 271. Encode and Decode Strings

🟡 medium · **arrays-and-hashing** · 2 approaches to implement · [LeetCode](https://leetcode.com/problems/encode-and-decode-strings/)

## The problem

Design an encoding that flattens a list of arbitrary strings into one string, and a decoding that recovers the list exactly. Unlike the other problems here this is a design exercise with two halves, so the endpoint runs the full round trip: it encodes the input and returns what decoding produces. A correct implementation therefore returns its input unchanged — and any encoding that cannot survive delimiters, empty strings or digits will not.

## Examples

Straight from the contract, which is what the tests read:

```json
// textbook
{"strs": ["neet", "code", "love", "you"]}  ->  ["neet", "code", "love", "you"]
// empty list
{"strs": []}  ->  []
// single empty string
{"strs": [""]}  ->  [""]
```

The full set — 9 cases, 3 invalid-input cases — is in [`0271-encode-and-decode-strings.json`](../../packages/contracts/problems/0271-encode-and-decode-strings.json).

> **New to arrays and hashing?** Read the topic guide first: [`01-arrays-and-hashing.md`](../topics/01-arrays-and-hashing.md). It covers the data structures you will need in all three languages — no problem answers in it.

## What to implement

| approach | must run in | using | what it is |
|---|---|---|---|
| `length-prefixed` *(default)* | O(n) | O(n) space | Write each string as `<length>#<string>`. The length is read before the payload, so the payload is never scanned for a delimiter and may contain anything at all — including `#` and digits. The standard answer, and the only one here that is unconditionally safe. |
| `delimiter-escaped` | O(n) | O(n) space | Join on a delimiter, escaping any occurrence of it (and of the escape character) inside the payloads. Correct, but every decode has to scan character by character — it exists here to show what the length prefix buys you. |

The **default** approach is the one used when `?approach=` is omitted.

### Where

Three files, one per language. Each holds a stub per approach; replace the `raise` /
`throw` with your own code and leave everything else alone.

```
packages/core-python/src/neetcode_core/arrays_and_hashing/encode_and_decode_strings.py
packages/core-ts/src/arrays-and-hashing/encode-and-decode-strings.ts
packages/core-php/src/ArraysAndHashing/EncodeAndDecodeStrings.php
```

Write each one **idiomatically for its language**. If all three end up reading the same,
you have translated rather than learned — and the whole point of this repo is the
difference between the three.

## Check your work

```bash
make try SLUG=encode-and-decode-strings          # just this problem, all three languages
make try SLUG=encode-and-decode-strings LANG=python   # just one language
```

That is the loop. `make test` runs all six suites for every problem when you want it.

Every test is driven by the contract above, so the same cases run in all three languages.
There is also a differential test asserting that your approaches agree with each other —
which is why implementing the naive one first is worth the ten minutes.

Once it passes, the endpoint works in all three apps:

```bash
make run-python       # :8000   (also run-node :3000, run-php :8080)

curl -s 'localhost:8000/problems/encode-and-decode-strings?approach=length-prefixed' \
  -H 'content-type: application/json' \
  -d '{"strs": ["neet", "code", "love", "you"]}'
```

## Stuck?

```bash
make show SLUG=encode-and-decode-strings              # prints a worked answer, touches nothing
make solution SLUG=encode-and-decode-strings          # writes it over your stub (make restore undoes it)
```

There is also a full cross-language write-up — what differed between the three languages
and the three frameworks, and what went wrong — in
[`solutions/notes/0271-encode-and-decode-strings.md`](../../solutions/notes/0271-encode-and-decode-strings.md).
**It contains the answers.** Read it after you have solved this, not before.

---

*Generated from the contract by `make statements`. Do not edit by hand.*
