# 242. Valid Anagram

**Difficulty:** easy · **Topic:** arrays-and-hashing · **Approaches:** sorting, hash-map
**LeetCode:** https://leetcode.com/problems/valid-anagram/

## The problem

Return true when `t` is an anagram of `s` — when both strings contain exactly the same
characters with exactly the same multiplicities. Order is irrelevant; counts are everything.

The useful reframing: *"are these two multisets of characters equal?"* Once it is phrased that
way both approaches are obvious, because there are only two ways to compare multisets —
canonicalise them (sort) or count them.

## Approaches

### sorting — O(n log n) time, O(n) space

Two anagrams have the same sorted form. Three lines, obviously correct, and not O(1) space in
any of the three languages because none of them can sort a string in place.

### hash-map — O(n) time, O(k) space

Count each character in `s`, decrement for each in `t`, and any character that goes below zero
(or any leftover) disqualifies it. O(k) in the **alphabet size**, not the input length — for
lowercase ASCII that is 26 regardless of how long the strings are.

The length check first is not an optimisation. It is what makes the decrement version correct:
without it, `s = "a"`, `t = "aa"` would consume the single `a` and then hit a zero count, which
happens to work — but `s = "aa"`, `t = "a"` would return true.

## What differed between the three languages

This problem is *the* string problem, and the three diverge much more than they did on
Two Sum.

### PHP strings are byte arrays — this is the big one

```php
strlen("héllo")        // 6   ← bytes
mb_strlen("héllo")     // 5   ← characters
str_split("héllo")     // splits the é into two broken bytes
mb_str_split("héllo")  // correct
```

A naive PHP implementation using `strlen` and `str_split` **passes every ASCII test case and
fails only on non-ASCII input**. That is precisely why the contract carries
`{"s": "héllo", "t": "olléh"}`. It is the single most valuable case in the file.

Python iterates code points natively. JavaScript does too — *provided* you spread.

### JavaScript: `[...s]` not `s.split("")`

`split("")` iterates UTF-16 **code units**, so any character outside the Basic Multilingual
Plane (emoji, most CJK extensions) is cut into two lone surrogates. Spreading a string uses
its iterator, which yields code points.

`"héllo"` happens to survive `split("")` because `é` is a single code unit — so even the
non-ASCII test case does not catch this one. It takes an emoji to expose it. Worth knowing,
not worth adding to the contract for this problem.

### Python's standard library does the whole job

```python
return Counter(s) == Counter(t)
```

`collections.Counter` builds the multiset and `==` compares them, both in C. TypeScript and
PHP each need a hand-rolled tally loop of six to ten lines. This is the clearest example in
the repo so far of Python's library reach collapsing a problem — and the reason the three
implementations of this problem look least alike.

PHP has `array_count_values()`, which would work, but it operates on an array of scalars, so
you still pay for `mb_str_split` first, and it gives up the early exit. The explicit loop is
clearer here.

### Summary

| | Length check | Counting | Lines |
|---|---|---|---|
| Python | `len(s)` | `Counter(s) == Counter(t)` | 3 |
| TypeScript | `s.length` | `Map`, two loops | 11 |
| PHP | `mb_strlen(s)` | `array`, two loops, `mb_str_split` | 15 |

## What differed between the three frameworks

Two new Laravel defaults, both caught by the `{"s": "", "t": ""}` case.

### `required` rejects the empty string

```php
's' => ['required', 'string'],   // ✗ 422 on {"s": "", "t": ""}
's' => ['present',  'string'],   // ✓
```

Laravel's `required` fails for `null`, `""`, `[]` and empty Countables. Pydantic and
`class-validator` accept all of those for a declared field, so the Laravel app was 422-ing a
payload the other two answered 200 to.

`present` is the rule that means what you actually want: *the key must be in the payload*. The
generator now emits `present` for every field, and never `required`.

### `ConvertEmptyStringsToNull` rewrites the body before validation

Switching to `present` alone did not fix it. Laravel applies `TrimStrings` and
`ConvertEmptyStringsToNull` to every request by default, so `{"s": ""}` arrives at the
validator as `{"s": null}` and fails the `is_string` check regardless of which presence rule
is used.

```php
// bootstrap/app.php
$middleware->remove([
    ConvertEmptyStringsToNull::class,
    TrimStrings::class,
]);
```

Both defaults were designed for HTML form posts, where a blank text input and an absent one
genuinely do mean the same thing. In a JSON API they do not. Neither Pydantic nor
`class-validator` has any equivalent behaviour.

### And one TypeScript one

The generated e2e test called `contractCases(SLUG)` without type arguments, and the generic
parameters had no defaults — so `input` inferred as `unknown` and `supertest`'s `.send()`
refused it at compile time. Fixed in the library rather than the test:
`contractCases<TInput = Record<string, unknown>, TExpected = unknown>`. A generic without a
sensible default pushes work onto every call site.

## Where I got stuck

**The empty-string case took three attempts**, and each failure pointed somewhere misleading.

First attempt: `required` → 422. The obvious read is "my validation rule is too strict", which
is right. Switched to `present`.

Second attempt: still 422, now with an `is_string` failure. At that point the rule *was*
correct and the error said the value was not a string — which makes no sense for `""` until
you know a middleware rewrote it to `null` before validation ever ran.

The lesson that generalises: **when a validator reports a type that cannot be right, suspect
something upstream of the validator.** Laravel's global middleware runs before the FormRequest
and is invisible from inside it.

**The PHP byte-vs-character issue I got right only because the contract forced it.** The first
implementation used `strlen`/`str_split` and passed 7 of 8 cases. Without the non-ASCII case in
the contract it would have shipped, and it would have been wrong.

## Benchmarks

```bash
curl -s 'localhost:8000/problems/valid-anagram?approach=sorting' \
  -H 'content-type: application/json' -d '{"s":"anagram","t":"nagaram"}' | jq .elapsedMicros
```

| Approach | Python | TypeScript | PHP |
|----------|--------|------------|-----|
| sorting | ~2 µs | ~9 µs | ~2 µs |
| hash-map | ~2 µs | ~6 µs | ~3 µs |

Seven characters is far below where O(n log n) vs O(n) is visible. PHP's hash-map version is
*slower* than its sorting version here, because `mb_str_split` allocates an array of strings
and the loop runs in userland, while `sort()` is C. Python's `Counter` is C on both sides, so
it stays flat.

Worth retrying with a 100,000-character string — that is where the asymptotics finally appear,
and where PHP's `mb_*` overhead stops being the dominant term.
