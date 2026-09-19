# 271. Encode and Decode Strings

**Difficulty:** medium · **Topic:** arrays-and-hashing · **Approaches:** length-prefixed, delimiter-escaped
**LeetCode:** https://leetcode.com/problems/encode-and-decode-strings/

## The problem

Flatten a list of arbitrary strings into one string, and recover the list exactly.

This is the only problem in the repo so far that is a **design exercise with two halves** rather
than a single function. The endpoint therefore runs the full round trip: it encodes the input
and returns what decoding produces, so a correct implementation returns its input unchanged.
That framing is a deliberate adaptation — see "Where I got stuck".

## Approaches

### length-prefixed — O(n) time, O(n) space

Write each string as `<length>#<payload>`.

The length is read **before** the payload, so the payload is never scanned for a delimiter and
may contain absolutely anything — `#`, digits, newlines, even a string that looks like its own
header such as `"4#test"`. That is the whole idea: make the payload opaque rather than trying to
escape it.

### delimiter-escaped — O(n) time, O(n) space

Join on `:`, escaping `\` first and then `:` inside each payload.

Correct, but every character is examined twice and the decoder cannot skip ahead. It exists here
to make the length prefix's advantage concrete rather than asserted.

Order matters when escaping: escape the escape character *before* the delimiter, or decoding
cannot tell `\:` (an escaped delimiter) from `\` followed by a real one.

## What differed between the three languages

### The measure and the slice must agree — the finding of this problem

Everywhere else in this repo the rule for PHP strings is "always use `mb_*`". Here that rule is
**wrong**, and the correct rule is narrower and sharper.

The encoder measures a length and the decoder slices by that length. What matters is not which
unit you pick but that **both halves pick the same one**:

| | Encoder | Decoder | Agree? |
|---|---|---|---|
| Python | `len()` — code points | slice — code points | ✅ |
| TypeScript | `[...word].length` — code points | `chars.slice()` on a spread array | ✅ |
| PHP | `strlen()` — bytes | `substr()` — bytes | ✅ |
| PHP (wrong) | `mb_strlen()` — characters | `substr()` — **bytes** | ❌ |

That last row is the trap, and it works perfectly on ASCII. The non-ASCII contract case
(`["héllo", "日本語", "🙂"]`) is what separates them.

The TypeScript version is the one that needs the most care. `String.prototype.slice` counts
UTF-16 code units, so measuring in code points with `[...word].length` and slicing with
`.slice()` disagree the moment an emoji appears — and the decoder returns *garbage rather than
throwing*. The implementation spreads the encoded string to an array of code points once and
slices that, so both halves are in the same unit.

Three languages, three different natural units, and none of them gets this for free.

### The delimiter decoder does not need `mb_*` in PHP

It scans byte by byte, and that is safe here only because both the delimiter and the escape are
ASCII — no byte of a UTF-8 multi-byte sequence can collide with an ASCII byte. That property is
what UTF-8 was designed for, and it is a good example of a case where reaching for `mb_*`
reflexively would be slower for no benefit.

### The empty list

```
join([])   == ""
split("")  == [""]     # not []
```

True in all three languages. A delimiter-based format simply cannot represent "no elements",
so `delimiter-escaped` needs an explicit `if (empty) return []` in all three. The
length-prefixed encoding needs no such case: an empty input produces an empty encoding, and an
empty encoding decodes to an empty list, because the loop never runs.

That asymmetry is the most concrete argument for the length prefix, and it is a property of the
*format*, not of any language.

## What differed between the three frameworks

Nothing.

## Where I got stuck

**Fitting a two-function design problem into a one-function contract.** Every other problem here
is `input → output`. This one is `encode: list → string` and `decode: string → list`, and the
repo's whole structure — the contract's `cases`, the `?approach=` switch, the differential test
— assumes a single callable.

Three options, and I think the reasoning is worth recording:

1. **Expose `encode` only**, with the expected encoded string in the contract. Rejected: it
   pins one specific encoding as *the* answer, which defeats having two approaches.
2. **Two endpoints.** Rejected: it breaks the uniform shape that makes the generator work, for
   one problem out of 150.
3. **Round trip.** A correct implementation returns its input unchanged. Chosen.

The round trip is a weaker test than checking the encoding directly — it cannot catch an
encoder and decoder that are wrong in exactly compensating ways. In exchange it tests the only
property that actually matters (recoverability) and it tests it against *every* adversarial
payload in the contract, which is where the real bugs are. Recorded as a deliberate trade rather
than an oversight.

The contract cases carry the weight here. `"4#test"` and `"1#a"` exist to break a naive
length-prefix decoder that searches for `#` from the wrong position; `["#", "##", "###"]` and
`["a\\b", "\\", "c"]` exist to break the delimiter version.

## Benchmarks

Four short ASCII strings. Median of 7 runs, microseconds:

| Approach | Python | TypeScript | PHP |
|----------|--------|------------|-----|
| length-prefixed | **2** | **1** | **1** |
| delimiter-escaped | 3 | 2 | 2 |

The delimiter version is consistently slower even at this size, which matches the reasoning:
it touches every character twice and cannot skip. The gap widens with payload length rather
than list length, since escaping is per-character while the length prefix is per-string.
