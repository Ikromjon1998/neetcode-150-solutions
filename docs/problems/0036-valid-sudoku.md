# 36. Valid Sudoku

🟡 medium · **arrays-and-hashing** · 2 approaches to implement · [LeetCode](https://leetcode.com/problems/valid-sudoku/)

## The problem

Decide whether a partially filled 9x9 board breaks any Sudoku rule. Only the filled cells are checked, and the board need not be solvable — a board with no contradictions among its current entries is valid. Empty cells are the string `"."`.

## Examples

Straight from the contract, which is what the tests read:

```json
// valid board
{"board": [["5", "3", ".", ".", "7", ".", ".", ".", "."], ["6", ".", ".", "1", "9", "5", ".", ".", "."], [".", "9", "8", ".", ".", ".", ".", "6", "."], ["8", ".", ".", ".", "6", ".", ".", ".", "3"], ["4", ".", ".", "8", ".", "3", ".", ".", "1"], ["7", ".", ".", ".", "2", ".", ".", ".", "6"], [".", "6", ".", ".", ".", ".", "2", "8", "."], [".", ".", ".", "4", "1", "9", ".", ".", "5"], [".", ".", ".", ".", "8", ".", ".", "7", "9"]]}  ->  true
// duplicate in a column
{"board": [["8", "3", ".", ".", "7", ".", ".", ".", "."], ["6", ".", ".", "1", "9", "5", ".", ".", "."], [".", "9", "8", ".", ".", ".", ".", "6", "."], ["8", ".", ".", ".", "6", ".", ".", ".", "3"], ["4", ".", ".", "8", ".", "3", ".", ".", "1"], ["7", ".", ".", ".", "2", ".", ".", ".", "6"], [".", "6", ".", ".", ".", ".", "2", "8", "."], [".", ".", ".", "4", "1", "9", ".", ".", "5"], [".", ".", ".", ".", "8", ".", ".", "7", "9"]]}  ->  false
// duplicate in a row
{"board": [["5", "5", "3", "5", ".", ".", ".", ".", "."], [".", ".", ".", ".", ".", ".", ".", ".", "."], [".", ".", ".", ".", ".", ".", ".", ".", "."], [".", ".", ".", ".", ".", ".", ".", ".", "."], [".", ".", ".", ".", ".", ".", ".", ".", "."], [".", ".", ".", ".", ".", ".", ".", ".", "."], [".", ".", ".", ".", ".", ".", ".", ".", "."], [".", ".", ".", ".", ".", ".", ".", ".", "."], [".", ".", ".", ".", ".", ".", ".", ".", "."]]}  ->  false
```

The full set — 6 cases, 4 invalid-input cases — is in [`0036-valid-sudoku.json`](../../packages/contracts/problems/0036-valid-sudoku.json).

## What to implement

| approach | must run in | using | what it is |
|---|---|---|---|
| `three-pass` | O(1) | O(1) space | Three independent sweeps, each building a fresh set per unit. The most readable version, and the board is a fixed 81 cells so the constant factor is the only thing that varies. |
| `single-pass` *(default)* | O(1) | O(1) space | Visit each cell once, updating its row, column and box tracker together. The box index is `(r // 3) * 3 + c // 3` — the one line in this problem worth deriving rather than memorising. |

The **default** approach is the one used when `?approach=` is omitted.

### Where

Three files, one per language. Each holds a stub per approach; replace the `raise` /
`throw` with your own code and leave everything else alone.

```
packages/core-python/src/neetcode_core/arrays_and_hashing/valid_sudoku.py
packages/core-ts/src/arrays-and-hashing/valid-sudoku.ts
packages/core-php/src/ArraysAndHashing/ValidSudoku.php
```

Write each one **idiomatically for its language**. If all three end up reading the same,
you have translated rather than learned — and the whole point of this repo is the
difference between the three.

## Check your work

```bash
make try SLUG=valid-sudoku          # just this problem, all three languages
make try SLUG=valid-sudoku LANG=python   # just one language
```

That is the loop. `make test` runs all six suites for every problem when you want it.

Every test is driven by the contract above, so the same cases run in all three languages.
There is also a differential test asserting that your approaches agree with each other —
which is why implementing the naive one first is worth the ten minutes.

Once it passes, the endpoint works in all three apps:

```bash
make run-python       # :8000   (also run-node :3000, run-php :8080)

curl -s 'localhost:8000/problems/valid-sudoku?approach=single-pass' \
  -H 'content-type: application/json' \
  -d '{"board": [["5", "3", ".", ".", "7", ".", ".", ".", "."], ["6", ".", ".", "1", "9", "5", ".", ".", "."], [".", "9", "8", ".", ".", ".", ".", "6", "."], ["8", ".", ".", ".", "6", ".", ".", ".", "3"], ["4", ".", ".", "8", ".", "3", ".", ".", "1"], ["7", ".", ".", ".", "2", ".", ".", ".", "6"], [".", "6", ".", ".", ".", ".", "2", "8", "."], [".", ".", ".", "4", "1", "9", ".", ".", "5"], [".", ".", ".", ".", "8", ".", ".", "7", "9"]]}'
```

## Stuck?

```bash
make show SLUG=valid-sudoku              # prints a worked answer, touches nothing
make solution SLUG=valid-sudoku          # writes it over your stub (make restore undoes it)
```

There is also a full cross-language write-up — what differed between the three languages
and the three frameworks, and what went wrong — in
[`solutions/notes/0036-valid-sudoku.md`](../../solutions/notes/0036-valid-sudoku.md).
**It contains the answers.** Read it after you have solved this, not before.

---

*Generated from the contract by `make statements`. Do not edit by hand.*
