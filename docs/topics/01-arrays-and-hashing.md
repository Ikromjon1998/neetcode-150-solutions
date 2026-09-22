# Topic 01 — Arrays & Hashing

Read this **before** you start the exercises in this topic. It gives you the vocabulary: which
data structures each language offers, how they behave, and what they cost.

> **No answers in here.** This page never says how to solve a particular problem — only what
> tools exist and where each language will trip you up. The worked answers live in
> `solutions/`, behind `make show`.

---

## What this topic is about

One trade, made over and over: **spend memory to stop searching.**

Scanning an array to ask "have I seen this value?" costs O(n) every time you ask. Put the values
in a hash map or hash set first, and the same question costs O(1) — at the price of holding a
second copy of the data in memory.

Almost every problem in this topic is a variation on noticing where that trade applies.

Sorting is the other tool here. It costs O(n log n) up front, but afterwards equal values sit
next to each other and order is guaranteed — sometimes worth more than the raw speed of hashing.

---

## The toolbox

The same operation in all three languages. Everything below is ordinary language knowledge, not
problem-specific technique.

| task | Python | TypeScript | PHP |
|------|--------|------------|-----|
| hash map | `dict` | `Map` | `array` |
| set | `set` | `Set` | array keys |
| is key present | `k in d` | `m.has(k)` | `isset($a[$k])` |
| read with default | `d.get(k, 0)` | `m.get(k) ?? 0` | `$a[$k] ?? 0` |
| count occurrences | `Counter(xs)` | write the loop | `array_count_values($xs)` |
| iterate with index | `enumerate(xs)` | `for (let i = 0; …)` | `foreach ($xs as $i => $x)` |
| sort numbers | `sorted(xs)` | `[...xs].sort((a, b) => a - b)` | `sort($xs)` |
| unique values | `set(xs)` | `new Set(xs)` | `array_unique($xs)` |
| length | `len(xs)` | `xs.length` | `count($xs)` |
| string → characters | `list(s)` | `[...s]` | `mb_str_split($s)` |

### Python

```python
from collections import Counter

seen: dict[int, int] = {}      # hash map: value -> anything you like
seen[5] = 0
if 5 in seen: ...              # O(1)

unique: set[int] = set()       # hash set
unique.add(5)

counts = Counter("hello")      # {'h': 1, 'e': 1, 'l': 2, 'o': 1}
```

### TypeScript

```typescript
const seen = new Map<number, number>();   // hash map
seen.set(5, 0);
if (seen.has(5)) { /* … */ }              // O(1)

const unique = new Set<number>();         // hash set
unique.add(5);

const value = seen.get(5) ?? 0;           // ?? not ||  — see traps below
```

### PHP

```php
$seen = [];                    // an array IS the hash map
$seen[5] = 0;
if (isset($seen[5])) { /* … */ }          // O(1)

$unique = array_flip($xs);     // values become keys: a set, deduplicated
$counts = array_count_values($xs);        // int|string values only
```

---

## What it costs

| operation | hash map / set | sorted array |
|-----------|----------------|--------------|
| insert | O(1) average | — |
| lookup | O(1) average | O(log n) binary search |
| build | O(n) | O(n log n) |
| extra memory | O(n) | O(n) in all three languages here |
| keeps order | insertion order | sorted order |

Two things worth internalising:

**"O(1) average" is not free.** Hashing computes a hash and may resize the table. For small
inputs, a plain O(n²) scan over an array often wins outright, because it allocates nothing. You
will see this in the benchmarks — the `elapsedMicros` field in every API response exists so you
can measure rather than assume.

**Sorting is not O(1) space here.** None of the three languages can sort the caller's array
without either copying it or mutating the caller's data, and a library function should not do
the second.

---

## Traps, per language

### TypeScript

**An object literal is not a hash map.** Its keys are coerced to strings, so `0` and `"0"`
collide, and a key like `"constructor"` collides with `Object.prototype`. Use `Map`.

```typescript
const bad: Record<string, number> = {};
bad[0] = 1;  bad["0"] = 2;     // same key
new Map().set(0, 1).set("0", 2);   // two distinct keys
```

**`.sort()` compares as strings and mutates.**

```typescript
[10, 9, 1].sort()                  // [1, 10, 9]   ← lexicographic
[...xs].sort((a, b) => a - b)      // correct, and does not touch the caller's array
```

**Use `??`, not `||`.** `||` treats `0` and `""` as missing, which is wrong whenever zero is a
legitimate value.

**Map keys compare by reference.** Two arrays with identical contents are *different* keys. If
you ever need a composite key, serialise it to a string first.

### PHP

**Strings are byte arrays.** `strlen("héllo")` is 6, not 5, and `str_split` cuts multi-byte
characters in half. Use `mb_strlen` and `mb_str_split` in every string problem.

**Array keys are `int|string` only** — nothing else can be a key.

**Functions that drop keys.** `array_unique` and `array_filter` preserve the original keys, so
they leave gaps. A PHP array with non-sequential keys **JSON-encodes as an object, not an
array**, which silently changes your API response shape. Re-index with `array_values()` whenever
the result is going out as JSON or being indexed positionally.

**`array_unique` compares as strings by default**, so `[1, "1"]` counts as one value.

**`/` returns a float.** Use `intdiv($a, $b)` for integer division.

### Python

Python has the fewest traps in this topic — which is itself worth noticing when you compare your
three implementations.

- `sorted()` returns a new list; `list.sort()` mutates in place.
- `dict` and `set` need **hashable** keys. Tuples work, lists do not.
- `collections.Counter` and `collections.defaultdict` remove a lot of manual bookkeeping.

---

## The exercises in this topic

<!-- generated:problems -->
*9 exercise(s) in this topic, easiest first. Generated from the contracts — do not edit by hand.*

| # | problem | difficulty | approaches to implement |
|---|---------|------------|-------------------------|
| 1 | [Two Sum](../problems/0001-two-sum.md) | easy | `brute-force`, `hash-map` |
| 217 | [Contains Duplicate](../problems/0217-contains-duplicate.md) | easy | `brute-force`, `sorting`, `hash-set` |
| 242 | [Valid Anagram](../problems/0242-valid-anagram.md) | easy | `sorting`, `hash-map` |
| 36 | [Valid Sudoku](../problems/0036-valid-sudoku.md) | medium | `three-pass`, `single-pass` |
| 49 | [Group Anagrams](../problems/0049-group-anagrams.md) | medium | `sorted-key`, `count-key` |
| 128 | [Longest Consecutive Sequence](../problems/0128-longest-consecutive-sequence.md) | medium | `sorting`, `hash-set` |
| 238 | [Product of Array Except Self](../problems/0238-product-of-array-except-self.md) | medium | `brute-force`, `prefix-suffix` |
| 271 | [Encode and Decode Strings](../problems/0271-encode-and-decode-strings.md) | medium | `length-prefixed`, `delimiter-escaped` |
| 347 | [Top K Frequent Elements](../problems/0347-top-k-frequent-elements.md) | medium | `sorting`, `bucket-sort` |
<!-- /generated:problems -->

Start at the top. Each one asks for two or three approaches — usually a naive one and an optimal
one — and a differential test checks that they agree with each other, so the simple version you
write first becomes a free correctness check on the clever one.

```bash
make try SLUG=contains-duplicate LANG=python
```

---

## Related reading

- [03 — Python & FastAPI](../03-python-fastapi.md), [04 — TypeScript & NestJS](../04-typescript-nestjs.md),
  [05 — PHP & Laravel](../05-php-laravel.md) — per-language idiom tables.
- [06 — Language & framework comparison](../06-language-comparison.md) — the measured
  side-by-side, including benchmarks where the *worse* complexity won.
- `solutions/notes/NNNN-*.md` — the full write-up for each problem. **Contains answers**; read
  one only after you have solved that problem.
