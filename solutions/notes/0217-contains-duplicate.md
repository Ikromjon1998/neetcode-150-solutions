# 217. Contains Duplicate

**Difficulty:** easy · **Topic:** arrays-and-hashing · **Approaches:** brute-force, sorting, hash-set
**LeetCode:** https://leetcode.com/problems/contains-duplicate/

## The problem

Return true when any value appears in `nums` more than once, false when every element is
distinct.

The first NeetCode 150 problem, and the cleanest possible demonstration of the central
arrays-and-hashing trade: you can pay O(n²) in time, O(n log n) by imposing order, or O(n) in
time by paying O(n) in space. All three are implemented here, which makes this the best
problem in the repo for actually watching `?approach=` mean something.

## Approaches

### brute-force — O(n²) time, O(1) space

Every pair. The **only** approach here that allocates nothing, which is exactly why it is kept:
below roughly twenty elements it beats both of the others in all three languages, because
building a set or a sorted copy costs more than the comparisons do.

### sorting — O(n log n) time, O(n) space

Duplicates become adjacent once sorted, so one scan of neighbours decides it. Not O(1) space in
any of the three languages — none can sort the caller's array without either copying it or
mutating the caller's data, and a library should not do the second.

### hash-set — O(n) time, O(n) space

Remember what has been seen, return on the first repeat.

The important detail is the **early exit**, and it is the thing every popular one-liner throws
away:

```python
len(set(nums)) != len(nums)          # always consumes the whole input
```

```typescript
new Set(nums).size !== nums.length   // same
```

```php
count(array_unique($nums)) !== count($nums)   // same, and see below
```

All three are shorter. All three are strictly worse: with a duplicate at index 1, the explicit
loop finishes in two operations regardless of input size. Big-O hides that difference entirely;
`elapsedMicros` in the API response does not.

## What differed between the three languages

### Who owns the array — the sharpest contrast in the repo so far

| | Sorting mutates the caller? | What the code must do |
|---|---|---|
| Python | no — `sorted()` returns a new list | nothing |
| TypeScript | **yes** — `Array.prototype.sort` is in-place | `[...nums].sort(...)` |
| PHP | no — arrays are value types with copy-on-write | nothing |

PHP and Python protect you by default through completely different mechanisms — one returns a
new object, the other copies on assignment. JavaScript does neither: `nums.sort()` reorders the
caller's array, and in a library function that is a bug you will not notice until something
downstream depends on the original order.

### And the sort comparator

```javascript
[10, 9, 1].sort()              // [1, 10, 9]  — elements are compared as STRINGS
[10, 9, 1].sort((a, b) => a-b) // [1, 9, 10]
```

The default comparator converts to strings. Python's `sorted()` and PHP's `sort()` both compare
numbers as numbers. This is the JavaScript bug everyone writes exactly once.

### Set types

| | Set |
|---|---|
| Python | `set` — native, `in` is O(1) |
| TypeScript | `Set` — native, `.has()` is O(1) |
| PHP | **none** — array keys stand in for one |

PHP's substitute works precisely because array keys are unique and integer keys stay integers:
`$seen[$value] = true` then `isset($seen[$value])`. It is idiomatic, not a hack, but it only
works for `int|string` values — a set of objects needs `SplObjectStorage`.

### `array_unique` compares as strings

The one PHP landmine here. `array_unique()` defaults to `SORT_STRING`, so `[1, "1"]` counts as
a duplicate. The contract forbids non-integer elements so it could not bite in this repo, but
it is exactly the kind of default that makes the "clever" one-liner wrong as well as slower.

### Adjacent pairs

```python
any(a == b for a, b in pairwise(sorted(nums)))   # itertools.pairwise, 3.10+
```

TypeScript and PHP both index manually with `sorted[i] === sorted[i - 1]`. A small thing, but
it is the third problem in a row where Python's standard library removed a loop.

## What differed between the three frameworks

Nothing new — and that is the result worth recording. Three problems in, the framework
divergences have converged to zero: the generator emits the same validation shape, the same
`@HttpCode(HttpStatus.OK)`, the same `present` rules, and all three endpoints agreed on the
first run.

The one thing this problem did surface was in the **tooling**, not the frameworks: it was the
first problem with three approaches and the second to be generated, which exposed two real
generator bugs (below).

## Where I got stuck

**Nowhere in the algorithm.** All three implementations passed on the first run — which, for a
problem this simple, is the expected outcome and worth noting as the baseline.

**The generator broke twice**, both times only because this was the *third* problem:

1. **`export * from "./topic/slug"` in the TypeScript barrel.** Every problem module exports a
   `SLUG` constant. With one generated problem there is no conflict; with two, the barrel fails
   to compile:

   ```
   TS2308: Module "./arrays-and-hashing/contains-duplicate" has already exported
           a member named 'SLUG'.
   ```

   Fixed by emitting an explicit aliased re-export
   (`export { SLUG as CONTAINS_DUPLICATE, ... }`) instead of a star.

2. **Pint's `ordered_imports` on `routes/api.php`.** The generator inserted each new
   `use App\Problems\X\XController;` directly after the TwoSum one, which is not alphabetical.
   `make lint` failed on a file nobody had hand-edited. The generator now re-sorts the `use`
   block after inserting.

Both are the same class of bug: **a code generator is only tested by its second and third
run.** The first output always looks right.

## Benchmarks

```bash
for a in brute-force sorting hash-set; do
  curl -s "localhost:8000/problems/contains-duplicate?approach=$a" \
    -H 'content-type: application/json' -d '{"nums":[1,2,3,1]}' | jq -r "\"$a: \(.elapsedMicros)µs\""
done
```

Four elements — deliberately far below where the asymptotics appear:

| Approach | Python | TypeScript | PHP |
|----------|--------|------------|-----|
| brute-force | ~1 µs | ~5 µs | ~1 µs |
| sorting | ~2 µs | ~8 µs | ~2 µs |
| hash-set | ~2 µs | ~7 µs | ~2 µs |

**The O(n²) approach is the fastest one here**, in all three languages, because it allocates
nothing. That is the whole reason it is still in the repo. Try it again with 10,000 elements
and the ordering inverts completely — which is a far more useful thing to have measured
yourself than to have read.
