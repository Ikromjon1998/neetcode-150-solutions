# AGENTS.md — how to work in this repository

Read this file before changing anything. It is the operating manual for both humans and AI
assistants. `CLAUDE.md` points here; they are the same instructions.

---

## 1. What this repository is

**A practice repo, not a solutions repo.** Every NeetCode 150 problem ships as an unsolved stub
in Python, TypeScript and PHP, with the tests already written and three real applications
already wired up. The learner writes the algorithms.

`make test` FAILS on a fresh clone. That is the starting line, not a bug.

Worked answers exist under `solutions/`, reachable only by a deliberate `make show` /
`make solution`. They are never the default state of the tree.

Served as three real applications:

| Stack | Framework | Port | Docs |
|-------|-----------|------|------|
| Python | FastAPI | 8000 | `/docs` (auto-generated) |
| TypeScript | NestJS | 3000 | `/docs` (`@nestjs/swagger`) |
| PHP | Laravel | 8080 | — |

The point is to feel the same problem land differently in three type systems and three
frameworks. An exercise is not finished when it is scaffolded — it is finished when a reference
solution exists, `make verify-solutions` passes, and `solutions/notes/NNNN-slug.md` explains
what differed and why.

## 2. Layout

```
packages/
  contracts/       JSON. One file per problem. THE SINGLE SOURCE OF TRUTH.
  core-python/     neetcode_core          — algorithms, zero dependencies
  core-ts/         @neetcode/core         — algorithms, zero dependencies
  core-php/        neetcode/core          — algorithms, zero dependencies
apps/
  api-python/      FastAPI    — depends on core-python
  api-node/        NestJS     — depends on core-ts
  api-php/         Laravel    — depends on core-php
docs/
  problems/        GENERATED exercise briefs — never hand-edit, see `make statements`
  *.md             architecture and per-stack guides
solutions/
  {python,typescript,php}/   reference answers (overlays, not a package)
  notes/           the cross-language write-ups  <- the actual deliverable
tools/
  new_problem.py         scaffolds a problem across all three stacks
  solutions.py           extract / apply / show / restore / status
  render_statements.py   regenerates docs/problems/ from the contracts
  validate_contracts.py  checks contracts AND cross-language coverage
  progress.py            the progress table
```

### The hard rule

**Algorithms live in `packages/core-*`. Applications live in `apps/api-*`. The core packages
never import a framework, and never mention HTTP, status codes, or request objects.**

If you find yourself importing `fastapi` inside `packages/core-python`, stop — the thing you
are building belongs in `apps/api-python`.

### The second hard rule

**Never commit an implementation into `packages/core-*` on `main`.** `main` is the exercise set
that everyone forks, so its files ship as stubs raising `UnsolvedError` / `UnsolvedException`.
An answer that lands there turns an exercise into a give-away, and CI fails any push or pull
request to upstream `main` that contains one.

**A solutions repo is the opposite.** Learners click "Use this template" to get their own
repository and commit solved functions to its `main` — that is exactly what should happen. CI
tells the two apart by repository name: the stub check runs only in
`Ikromjon1998/neetcode-150`, and everywhere else CI runs `make test-solved` instead.

```
Ikromjon1998/neetcode-150          <you>/neetcode-150-solutions
  exercises only                     solutions on main
  new problems land here  ─────────► make sync brings them in
```

**Work out which repo you are in before touching anything**: `git remote get-url origin`.

When authoring an exercise, solve in place, then `make extract SLUG=<slug>` to move the answer
into `solutions/` and leave the stub behind.

## 3. The contract is the source of truth

`packages/contracts/problems/NNNN-slug.json` holds the metadata *and* the test cases. All six
test suites read it. Adding a case there tightens Python, TypeScript and PHP at once; there is
no way for them to drift.

```jsonc
{
  "id": 242, "slug": "valid-anagram", "title": "Valid Anagram",
  "difficulty": "easy", "topic": "arrays-and-hashing",
  "summary": "One paragraph. Rendered into the API catalog and the docs.",
  "approaches": [
    { "key": "sorting",  "name": "...", "time": "O(n log n)", "space": "O(n)", "note": "..." },
    { "key": "hash-map", "name": "...", "time": "O(n)", "space": "O(k)", "default": true }
  ],
  "cases":           [{ "name": "...", "input": {...}, "expected": ... }],
  "validationCases": [{ "name": "...", "input": {...}, "status": 422 }],
  "notFoundCases":   [{ "name": "...", "input": {...} }]
}
```

Rules, all enforced by `make test-contracts`:

- Filename must be `{id:04d}-{slug}.json`.
- `slug` and every `approach.key` are kebab-case.
- Exactly one approach carries `"default": true`.
- Every declared approach must be implemented in **all three** languages.
- No `TODO` and no `O(?)` left behind.

## 4. Two workflows

### A — solving an exercise (what a learner does)

1. Read `docs/problems/NNNN-slug.md`.
2. Edit the three stubs it names. Replace the `raise` / `throw`; leave the registration,
   signatures and docstrings alone.
3. `make test` until green.
4. `make show SLUG=<slug>` if stuck — it prints an answer without touching a file.

### B — authoring a new exercise (what a maintainer does)

```bash
make new-problem ARGS="--id 242 --slug valid-anagram --title 'Valid Anagram' \
  --difficulty easy --topic arrays-and-hashing \
  --input 's:string,t:string' --returns bool --approaches sorting,hash-map"
```

`--input` types: `int`, `string`, `bool`, `float`, `int[]`, `string[]`, `int[][]`, `string[][]`.
`--returns` takes the same set. The **last** `--approaches` entry becomes the default.

That writes ~27 files and wires up every registry. Nothing is overwritten; re-running is safe.
Then:

1. **Fill in the contract** — `packages/contracts/problems/NNNN-slug.json`. Replace every
   placeholder: the summary, the real complexities, and **real test cases**. Six or more
   happy-path cases, and the edge cases you would forget — empty input, duplicates, negatives,
   the answer at either end, non-ASCII for any string problem.
2. **Implement it three times, in place** in `packages/core-*`, idiomatically for each
   language. If all three read identically you have transliterated, not learned.
3. `make test` until green, then `make test-contracts`.
4. **`make extract SLUG=<slug>`** — moves your implementations into `solutions/` and
   regenerates the stubs from the contract. This is the step that turns it into an exercise.
5. `make statements` — regenerates `docs/problems/NNNN-slug.md`.
6. Write `solutions/notes/NNNN-slug.md`. **This is the deliverable.**
7. `make verify-solutions` — proves the reference answers still pass.
8. `make test` — should now be RED for this problem. That is correct.

## 5. Instructions for AI assistants

**First, work out which job you have been given.** They have opposite outcomes.

### "Solve problem X" / "implement two-sum"

The user wants the exercise done. **Check `git remote get-url origin` first.** If this is
`Ikromjon1998/neetcode-150` itself, stop and say so: solving here leaks answers into the
exercise set, and they want their own repo from "Use this template". In a solutions repo, edit
the stubs in `packages/core-*` in place, check with `make try SLUG=<slug>`, and commit to `main`
if asked.

Do **not** run `make extract` — that would move their work into `solutions/` and put the stub
back. Do not touch `solutions/` at all.

### "Add problem X" / "create an exercise for X"

The user wants a new exercise for others to solve. Follow workflow B above end to end, without
asking for confirmation between steps:

1. Confirm the LeetCode id, exact title, difficulty and topic. If unsure of the id, ask — a
   wrong id corrupts the filename and the catalog sort order.
2. Pick two or three approaches — a naive baseline and the optimal one at minimum. The baseline
   is not filler: the differential test compares them.
3. `make new-problem` with the arguments above. Never hand-create those files.
4. Fill the contract with real, non-trivial cases (6+ happy path, 3+ validation).
5. Implement all three idiomatically, in place, until `make test` is green.
6. `make extract SLUG=<slug>` then `make statements`.
7. Write `solutions/notes/NNNN-slug.md` with the real comparison — specifics observed while
   writing it, not generalities you already knew.
8. `make verify-solutions`, then `make test-contracts`.
9. Report what you added and what the cross-language differences turned out to be.

### If you are unsure which

Ask. The cost of guessing wrong is either deleting the user's work or handing them the answers
to an exercise they wanted to attempt.

### Things that will bite you

These are all real, all hit while building this repo, and all already worked around in the
existing code — match the existing pattern rather than rediscovering them:

| Trap | Where | Fix already in place |
|------|-------|----------------------|
| `from __future__ import annotations` breaks FastAPI dependency factories | `apps/api-python/src/neetcode_api/dependencies.py` | that file deliberately omits the import |
| Circular import: `registry.ts` ↔ problem modules | `packages/core-ts/src/` | `defineProblem` lives in its own leaf module |
| NestJS answers `POST` with **201** | every controller | `@HttpCode(HttpStatus.OK)` |
| NestJS validation returns **400**, FastAPI returns **422** | `apps/api-node/src/app.factory.ts` | `errorHttpStatusCode: 422` |
| Laravel `required` rejects `""`, `[]` and `"0"` | every FormRequest | use `present`, never `required` |
| Laravel converts `""` to `null` before validation | `apps/api-php/bootstrap/app.php` | `ConvertEmptyStringsToNull` and `TrimStrings` removed |
| Laravel `$request->all()` merges the query string into the body | every FormRequest | inspect `$request->json()->all()` |
| Laravel `integer` accepts the string `"7"` | every FormRequest | explicit `is_int` closure |
| `validated()` key order follows rule evaluation, not declaration | every controller | rebuild the echoed input explicitly |
| PHP `strlen`/`str_split` are byte-wise | any string problem | use `mb_strlen` / `mb_str_split` |
| JS `s.split("")` splits surrogate pairs | any string problem | spread the string: `[...s]` |
| `pytest` (the script) does not add cwd to `sys.path` | both pyproject files | `pythonpath = ["src", "."]` |
| TypeScript `export *` from a problem module collides on `SLUG` | `packages/core-ts/src/index.ts` | explicit aliased re-export: `export { SLUG as TWO_SUM, ... }` |
| Generated TS tests import approach functions **by name** | every `core-ts` problem module | name them `<camelSlug><PascalApproach>` exactly — Python and PHP go through the registry and do not care |
| JS `-0` — `1 * 0 * -3` is `-0`, and deep-equal distinguishes it | numeric-product problems | normalise: `value === 0 ? 0 : value` |
| PHP array with non-sequential keys JSON-encodes as an **object** | any PHP result destined for JSON | `array_values(...)` unless the keys are provably sequential; `array_unique`/`array_filter` both leave gaps |
| JS `/` is float division; a float array index is silently `undefined` | any index arithmetic | `Math.floor`; PHP wants `intdiv`, Python `//` |
| PHP `isset($a, $b)` is **AND**, not OR | multi-tracker membership checks | one `isset()` per tracker, OR-ed |
| `class-validator`'s `each: true` descends only one level | any 2-D input | `@IsMatrix("int"\|"string")` in `common/validators/`; Laravel uses `field.*.*`, Pydantic needs nothing |

### Never

- Never put a framework import in `packages/core-*`.
- Never commit an implementation into `packages/core-*` in the platform repo. In a solutions
  repo it is expected. When authoring an exercise, use `make extract`.
- Never run `extract` to refresh a stub's docstring — use `make stubs`. `extract` copies the
  live file into `solutions/`, and `stubs` is read-only on both `solutions/` and solved files.
- Never hand-edit `docs/problems/*.md`. They are generated by `make statements`; edit the
  contract instead.
- Never hand-write the files `make new-problem` generates.
- Never hard-code test cases in a test file — they belong in the contract JSON.
- Never let the three apps disagree about a status code or a response body. If a framework
  default gets in the way, change the framework config and document it in the table above.
- Never commit, push, or open a PR unless explicitly asked.

## 6. Commands

```bash
make setup             # install all three toolchains (once)
make status            # which problems are solved, per language
make test              # all six suites — RED on a fresh clone, by design
make try SLUG=x        # one problem, all three languages — the solving loop
make test-python       # or -node / -php
make test-contracts    # contract validity + cross-language coverage
make run-all           # all three servers at once (8000 / 3000 / 8080)
make lint              # ruff + tsc + pint
make progress          # progress through the 150

# exercises <-> answers
make show SLUG=x       # print a reference answer, touch nothing
make solution SLUG=x   # write it over the stub
make restore           # undo that
make extract SLUG=x    # move an implementation into solutions/, leave a stub
make stubs [SLUG=x]    # refresh stub hints from the contracts (safe: read-only on answers)
make test-solved       # test only what is solved — what CI runs in a solutions repo
make sync              # pull new problems into a solutions repo, keeping its solutions
make verify-solutions  # apply all references, run everything, restore
make statements        # regenerate docs/problems/ from the contracts

make new-problem ARGS="..."
```

## 7. Response envelope — identical in all three apps

```jsonc
// 200
{
  "problem": "two-sum",
  "approach": { "key": "hash-map", "name": "...", "time": "O(n)", "space": "O(n)",
                "note": "...", "default": true },
  "input":    { "nums": [2, 7, 11, 15], "target": 9 },
  "result":   [0, 1],
  "elapsedMicros": 3
}

// 4xx — every error, in every app
{ "error": { "type": "no_solution", "message": "...", "problem": "two-sum",
             "details": [{ "field": "nums", "message": "..." }] } }
```

| Situation | Status | `error.type` |
|-----------|--------|--------------|
| Body fails validation | 422 | `validation_error` |
| Unknown `?approach=` | 422 | `unknown_approach` |
| Unknown problem slug | 404 | `unknown_problem` |
| Valid input, no answer exists | 404 | `no_solution` |
| Approach is still an unsolved stub | 501 | `not_implemented` |

Any change to this table must be made in all three apps in the same commit.

The 501 is what a learner sees before they solve anything, and its `details` carry the path of
the file to edit — so hitting an unsolved endpoint is itself a hint rather than a crash.
