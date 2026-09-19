# 36. Valid Sudoku

**Difficulty:** medium · **Topic:** arrays-and-hashing · **Approaches:** three-pass, single-pass
**LeetCode:** https://leetcode.com/problems/valid-sudoku/

## The problem

Decide whether a partially filled 9×9 board breaks any Sudoku rule. Only the filled cells are
checked and the board need not be solvable — a board with no contradiction among its current
entries is valid. Empty cells are the string `"."`.

The board is a fixed 81 cells, so **every approach here is O(1)** and the only thing that varies
is the constant factor. That makes it an unusually honest benchmark: there is no asymptotic
story to hide behind.

## Approaches

### three-pass — O(1), O(1)

Rows, then columns, then boxes. Each sweep checks exactly one rule, which makes it the easiest
version to convince yourself is correct.

### single-pass — O(1), O(1)

Visit each cell once, updating its row, column and box tracker together. 27 sets, each holding
at most nine entries.

The box index is worth deriving rather than memorising:

```
box = (row // 3) * 3 + column // 3
```

Integer-dividing a coordinate by 3 collapses it to which band of three it falls in. The row
band is then scaled by 3 to leave room for the column band — the same trick as flattening a 2-D
index into 1-D, applied to bands instead of cells.

## What differed between the three languages

### Integer division

The box index needs truncating division, and all three spell it differently:

```python
(row // 3) * 3 + column // 3                                  # Python
Math.floor(row / 3) * 3 + Math.floor(column / 3)              # TypeScript
intdiv($row, 3) * 3 + intdiv($column, 3)                      # PHP
```

JavaScript's `/` is floating-point, always. `7 / 3` is `2.333…`, and using that as an array
index returns `undefined` rather than throwing — so a forgotten `Math.floor` produces a tracker
that is never read and a validator that never fires.

PHP's `/` also returns a float, but a float array index is *truncated with a deprecation
notice* in 8.1+, so it half-works and warns. Python's `//` is the only one that does the right
thing by default.

### Extracting a column

```python
[board[row][column] for row in range(9)]                            # Python
Array.from({ length: 9 }, (_, row) => board[row][column])           # TypeScript
array_column($board, $column)                                       # PHP
```

`array_column` is a genuine PHP win — a single call for something the other two build by hand.
It is designed for arrays of database rows, and a 2-D board is exactly that shape.

### `isset($a, $b)` is AND, not OR

My first PHP `single-pass` had:

```php
if (isset($rows[$row][$cell], $columns[$column][$cell]) || isset($boxes[$box][$cell])) {
```

`isset()` with multiple arguments is true only when **all** of them are set. So that condition
fires only when a cell duplicates in its row *and* its column simultaneously — a far narrower
test than intended, which would have passed the row-duplicate and column-duplicate contract
cases by luck and failed nothing. Rewritten as three separate `isset()` calls OR-ed together.

No equivalent trap in Python or TypeScript: neither has a multi-argument membership test.

## What differed between the three frameworks

Nothing at the algorithm boundary, but this was the first `string[][]` input and the validation
story is in [Group Anagrams](0049-group-anagrams.md) — Pydantic handled the nesting natively,
Laravel needed a `board.*.*` wildcard, and NestJS needed a custom `@IsMatrix` decorator because
`class-validator` cannot express a 2-D element type.

## Where I got stuck

**The `isset` bug, and it is worth being explicit about why it was dangerous.** It did not
crash, it did not fail a type check, and it would have passed a test suite that only contained
LeetCode's two examples. What caught it was the `"duplicate in a box only"` contract case — two
`1`s inside the top-left 3×3 box but in different rows and different columns, so *only* the box
rule is violated.

That case exists because I deliberately asked "what board breaks exactly one of the three
rules?" for each rule. Three cases, one per rule, plus a fourth for a column duplicate far
enough apart to also be box-legal. Two of those four would never appear in a tutorial and both
were necessary.

## Benchmarks

The standard LeetCode example board. Median of 7 runs, microseconds:

| Approach | Python | TypeScript | PHP |
|----------|--------|------------|-----|
| three-pass | 17 | 11 | 16 |
| single-pass | **7** | **8** | **7** |

Consistently about 2× in every language, which is exactly what you would predict: `three-pass`
reads all 81 cells three times and builds 27 intermediate lists to do it, while `single-pass`
reads each cell once.

Both are O(1). The 2× is entirely constant factor, and it is the cleanest demonstration in the
repo that "same complexity" and "same speed" are different claims.
