# 238. Product of Array Except Self

**Difficulty:** medium · **Topic:** arrays-and-hashing · **Approaches:** brute-force, prefix-suffix
**LeetCode:** https://leetcode.com/problems/product-of-array-except-self/

## The problem

Each output position holds the product of every input element except the one beneath it.

Division is forbidden. That restriction is the problem — without it this is a one-liner, and
with it you have to find a decomposition instead. The ban is also not arbitrary: the obvious
"total ÷ nums[i]" breaks on a single zero and breaks *differently* on two zeros, so the
division version needs two special cases before it is even correct.

## Approaches

### brute-force — O(n²) time, O(1) auxiliary space

For every index, multiply everything else.

### prefix-suffix — O(n) time, O(1) auxiliary space

The answer at `i` factorises into *(everything left of i)* × *(everything right of i)*. The
first pass writes the left products into the output array; the second walks backwards carrying
the right product in a single scalar. No second array is ever allocated.

The output array does not count toward the space bound — that is the problem's own convention,
and it is the only reason this counts as O(1).

## What differed between the three languages

### Negative zero — the finding of this problem

The case `[-1, 1, 0, -3, 3]` failed in TypeScript and only in TypeScript:

```
expected [ -0, +0, 9, -0, +0 ] to deeply equal [ +0, +0, 9, +0, +0 ]
```

The product for index 0 is `1 * 0 * -3 * 3`, which evaluates left to right as `0 → -0 → -0`.
IEEE 754 has a signed zero and JavaScript exposes it. Python and PHP integers have no signed
zero at all, so both produced a plain `0`.

What makes this worth writing down is **how narrowly it escapes notice**:

- `-0 === 0` is `true`, so no ordinary comparison sees it.
- `JSON.stringify(-0)` is `"0"`, so the HTTP response would have agreed with the other two apps
  regardless.
- Only a structural deep-equal — which is what the test does, and what `Object.is` does — can
  tell them apart.

So this is a bug that is invisible over the wire and visible in a test. Caught by the shared
contract's "contains one zero" case, which is exactly what that case is there for. Fixed by a
`normalizeZero` helper; `value === 0` matches both zeros, so returning the literal normalises
either to `+0`.

### Allocating a pre-filled array

All three needed one, and all three have a trap:

| | Idiom | If you get it wrong |
|---|---|---|
| Python | `[1] * n` | — |
| TypeScript | `new Array(n).fill(1)` | `new Array(n)` alone is **sparse**; holes are `undefined`, and `undefined *= x` is `NaN` |
| PHP | `array_fill(0, n, 1)` | assigning by index into `[]` can produce a non-`list`, which JSON-encodes as an **object** |

The PHP one is the nastiest, because it changes the *shape* of the JSON response rather than a
value, and `var_dump` shows no difference.

## What differed between the three frameworks

Nothing. The generated app layer worked unmodified in all three.

## Where I got stuck

Only on the negative zero, and only briefly, because the failure message was unusually good —
Vitest prints `-0` and `+0` distinctly rather than showing `0` twice and claiming they differ.
A test framework that pretty-printed both as `0` would have produced a genuinely maddening
"expected 0 to equal 0".

## Benchmarks

n = 3000, median of 7 runs, microseconds:

| Approach | Python | TypeScript | PHP |
|----------|--------|------------|-----|
| brute-force | 114,482 | 5,825 | 61,020 |
| prefix-suffix | **85** | **10** | **48** |

Two things stand out.

**The asymptotics are overwhelming.** 1,300× in Python, 580× in TypeScript, 1,270× in PHP. This
is the clearest O(n²)-vs-O(n) demonstration in the repo so far.

**TypeScript is 20× faster than Python at the brute force.** A tight nested numeric loop is
exactly what a JIT is for, and exactly what a bytecode interpreter is worst at. The gap closes
to 8× on the linear version, where there is far less loop body to optimise.
