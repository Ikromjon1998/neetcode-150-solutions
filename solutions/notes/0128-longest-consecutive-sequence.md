# 128. Longest Consecutive Sequence

**Difficulty:** medium · **Topic:** arrays-and-hashing · **Approaches:** sorting, hash-set
**LeetCode:** https://leetcode.com/problems/longest-consecutive-sequence/

## The problem

The length of the longest run of consecutive integers present in `nums`. Position in the array
is irrelevant and duplicates do not lengthen a run.

## Approaches

### sorting — O(n log n) time, O(n) space

Once sorted, a run is a stretch of neighbours differing by exactly one. The trap is duplicates:
`[1, 2, 2, 3]` is a run of three, not four. Deduplicating through a set *before* sorting removes
the problem entirely, which is cheaper to reason about than teaching the walk to skip
zero-differences.

### hash-set — O(n) time, O(n) space

Put everything in a set, then walk a run **only from a value whose predecessor is absent**.

That guard is the entire algorithm. Without it the inner loop re-walks every run from every one
of its members and the whole thing is O(n²) — and it still passes every test, which is why this
problem is a classic. With the guard, each run is walked from its smallest member and from
nowhere else, so the inner loop takes O(n) steps *in total* across the whole input.

## What differed between the three languages

### Deduplicate-and-sort

| | | Note |
|---|---|---|
| Python | `sorted(set(nums))` | returns a new densely indexed list |
| TypeScript | `[...new Set(nums)].sort((a, b) => a - b)` | the comparator is mandatory — the default sort compares as strings |
| PHP | `array_values(array_unique($nums))` then `sort()` | **`array_values` is mandatory** |

The PHP one is the interesting case. `array_unique` preserves the original keys, so removing
element 2 from a five-element array leaves keys `0, 1, 3, 4` — and the positional `for` loop
that follows then reads `$ordered[2]`, which does not exist. Python and JavaScript both hand
back a densely indexed sequence for free; PHP hands back a *map* that happens to look like a
list, and re-indexing is on you.

### Building a set from a list

```python
seen = set(nums)                    # Python
```
```typescript
const seen = new Set(nums);         // TypeScript
```
```php
$seen = array_flip($nums);          // PHP — values become keys
```

`array_flip` is PHP's idiomatic set constructor and it deduplicates as a side effect, since
keys are unique. It is a single C-level call, which is part of why the PHP hash-set version is
the fastest of the three below.

### Adjacent pairs

`itertools.pairwise(ordered)` says "every adjacent pair" directly in Python. TypeScript and PHP
both index manually with `ordered[i] - ordered[i - 1]`. Third problem running where Python's
standard library removes a loop.

## What differed between the three frameworks

Nothing.

## Where I got stuck

**Nowhere, but the `array_values` omission would have been a silent bug rather than a crash.**
PHP reads a missing array key as `null` with a warning, not an exception, and `null - 5` is
`-5` — so the walk would have produced a plausible-looking wrong answer on exactly the inputs
that contain duplicates. It was caught by the "duplicate inside a run" contract case, which
exists for precisely that reason.

The general lesson: the contract case that catches a language-specific bug is almost never the
textbook example. It is the awkward one you add because you are suspicious.

## Benchmarks

n = 3000, one long consecutive run, shuffled. Median of 7 runs, microseconds:

| Approach | Python | TypeScript | PHP |
|----------|--------|------------|-----|
| sorting | **124** | 329 | 251 |
| hash-set | 129 | **134** | **46** |

**The O(n) approach does not win in Python.** 129 µs versus 124 µs — a dead heat, and if
anything the sort is ahead. The reason is where the work happens: `sorted()` runs entirely in
C, while the hash-set version's `while value + length in seen` loop runs in the Python
interpreter, one bytecode dispatch per step. An algorithm with better asymptotics loses to one
with a better constant factor, at a size well past where the asymptotics "should" have taken
over.

TypeScript and PHP both behave as the textbook predicts — 2.5× and 5.5× respectively — because
their loops are compiled rather than interpreted.

This is the single best argument in the repo for shipping both approaches and measuring.
