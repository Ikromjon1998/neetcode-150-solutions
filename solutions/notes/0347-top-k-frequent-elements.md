# 347. Top K Frequent Elements

**Difficulty:** medium · **Topic:** arrays-and-hashing · **Approaches:** sorting, bucket-sort
**LeetCode:** https://leetcode.com/problems/top-k-frequent-elements/

## The problem

The `k` most frequent values in `nums`.

LeetCode accepts any order. This repo pins a canonical one — **descending by frequency, then
ascending by value** — because three implementations returning the same set in three different
orders cannot be compared byte for byte, and comparing them is the point.

That decision is not free, and it shows up in the benchmarks below.

## Approaches

### sorting — O(n log n) time, O(n) space

Tally, then sort the distinct values.

### bucket-sort — O(n) time, O(n) space

A count can never exceed `n`, so an array of `n + 1` buckets indexed by frequency has somewhere
to put every value. Walking it from the back yields descending frequency without ever sorting.

## What differed between the three languages

### Expressing a two-term sort

This is the sharpest split of the three, and it lines up differently from usual:

```python
sorted(counts.items(), key=lambda item: (-item[1], item[0]))        # Python: a tuple key
```
```php
usort($values, fn($a, $b) => [-$counts[$a], $a] <=> [-$counts[$b], $b]);   # PHP: spaceship on arrays
```
```typescript
.sort(([va, ca], [vb, cb]) => cb - ca || va - vb)                   // TypeScript: spell it out
```

Python and PHP both compare sequences element by element, so the whole ordering fits in one
expression. JavaScript has **no array comparison at all** — `[1, 2] < [1, 3]` stringifies both
sides — so the two terms have to be written as an explicit fall-through. Usually PHP is the
odd one out on this kind of thing; here it is JavaScript.

### Tallying

`collections.Counter(nums)` and `array_count_values($nums)` are both single C-level calls.
TypeScript writes the loop. Same pattern as Valid Anagram, and `array_count_values` is the one
place PHP's standard library keeps pace with Python's.

## What differed between the three frameworks

Nothing. This was the first problem with **two** request fields (`nums` and `k`), and the
generated DTOs, FormRequest and Pydantic model all handled it unmodified — including the
`"k is not an integer"` validation case, which all three rejected with 422 on the first run.

## Where I got stuck

**Deciding what "any order" means for a contract-driven repo.** LeetCode's judge accepts any
permutation, so the natural contract expectation is a *set* comparison. But the whole premise
here is that the three apps return byte-identical JSON, and a set comparison would have let
three genuinely different orderings all pass while the HTTP responses visibly disagreed.

Pinning a canonical order was the right call, but it is an honest cost: `bucket-sort` now has to
sort each bucket internally to honour the ascending-value tie-break, which is work the "pure"
algorithm would not do. I left a comment saying so at the site, because a reader benchmarking
the two approaches deserves to know that one of them is carrying a handicap imposed by this
repo rather than by the problem.

## Benchmarks

n = 3000, 200 distinct values, k = 10. Median of 7 runs, microseconds:

| Approach | Python | TypeScript | PHP |
|----------|--------|------------|-----|
| sorting | **44** | **59** | **60** |
| bucket-sort | 260 | 137 | 77 |

**The O(n) approach loses in all three languages, by up to 6×.**

The reason is the bucket array: it is sized `n + 1` — 3001 slots — while there are only 200
distinct values to place in it. Allocating and then walking 3001 mostly-empty buckets costs far
more than sorting 200 entries. Bucket sort wins when the number of distinct values approaches
`n`; here it is 7% of `n`.

Python is worst hit (6×) because `[[] for _ in range(n + 1)]` allocates 3001 real list objects.
PHP's `array_fill(0, n + 1, [])` is cheapest because PHP arrays are copy-on-write, so all 3001
slots initially share one empty array.

This is the second problem in a row where the asymptotically better approach lost on a
realistic input. It is a useful corrective to the LeetCode reflex of reaching for the O(n)
solution and stopping there.
