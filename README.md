# NeetCode 150 — practice in three languages at once

An exercise repo. Every problem ships as a **stub in Python, TypeScript and PHP**, with the
tests already written and three real web applications already wired up. You write the
algorithms.

## Start here

Click **"Use this template"** at the top of this page to get your own repository. Then:

```bash
git clone git@github.com:<you>/neetcode-150-solutions.git && cd neetcode-150-solutions
make setup
make sync                                         # connect to this platform, once

cat docs/problems/0217-contains-duplicate.md      # read the brief
make try SLUG=contains-duplicate LANG=python      # red → write code → green
```

You solve on `main` in **your own repo**, so your work counts on your GitHub profile. `make
sync` brings in new problems later and keeps your solutions. Use *fork* only if you want to
improve the platform itself.

**Full guide: [docs/00-getting-started.md](docs/00-getting-started.md)** covers installing,
solving, testing, saving your solutions, and pulling in new problems.

On a fresh clone `make test` is red. That is the starting line, not a bug: every algorithm is
waiting for you.

| | Language | Framework | Port |
|---|----------|-----------|------|
| 🐍 | Python 3.11+ | **FastAPI** | 8000 |
| 🟦 | TypeScript 5 | **NestJS 11** | 3000 |
| 🐘 | PHP 8.3+ | **Laravel 13** | 8080 |

---

## Why three languages

Solving a problem once teaches you the algorithm. Solving it three times teaches you the
languages — because the third implementation is where you stop translating and start noticing.

Nine problems in, the things that actually differed were not the things you would predict:

- **`1 * 0 * -3` is `-0` in JavaScript**, and `-0 === 0` is `true`, and `JSON.stringify(-0)` is
  `"0"` — so it is invisible everywhere except a structural comparison. Python and PHP integers
  have no signed zero. It broke exactly one of three implementations.
- **PHP strings are byte arrays.** `strlen("héllo")` is 6. Every string problem needs `mb_*`,
  and a naive implementation passes every ASCII test.
- **`Map` compares array keys by reference**, so a 26-slot tally can be a dictionary key in
  Python (tuples hash by value) but must be serialised in TypeScript — and in PHP too, for the
  opposite reason (array keys are scalars only).
- **`Array.prototype.sort` mutates and compares as strings.** `[10, 9, 1].sort()` is
  `[1, 10, 9]`, and your caller's array is now reordered.

Full side-by-side in [docs/06-language-comparison.md](docs/06-language-comparison.md).

## Why real frameworks

Because a function in a file is not a system. Once you implement an algorithm here, it is
immediately a working HTTP endpoint in three apps — with request validation, dependency
injection, an error-to-status-code mapping and e2e tests around it:

```bash
make run-python                        # :8000 — Swagger UI at /docs

curl -s localhost:8000/problems/two-sum \
  -H 'content-type: application/json' \
  -d '{"nums":[2,7,11,15],"target":9}'
```

Before you solve it, that endpoint tells you where to go:

```json
{ "error": { "type": "not_implemented",
             "message": "two-sum / hash-map is an exercise you have not solved yet.",
             "details": [{ "field": "approach",
                           "message": "Write your solution in packages/core-python/src/neetcode_core/arrays_and_hashing/two_sum.py" }] } }
```

After you solve it, the response is **byte-for-byte identical** on ports 8000, 3000 and 8080.
That is enforced by tests, and getting there required fixing six framework defaults that
disagree out of the box — all documented at the site.

---

## How it works

### One contract, six test suites

```
packages/contracts/problems/0001-two-sum.json
        │
        ├──► packages/core-python/tests/…      pytest        ┐
        ├──► packages/core-ts/tests/…          vitest        │ your algorithm
        ├──► packages/core-php/tests/…         phpunit       ┘
        │
        ├──► apps/api-python/tests/…           pytest + TestClient   ┐
        ├──► apps/api-node/test/…              jest + supertest      │ over HTTP
        └──► apps/api-php/tests/Feature/…      phpunit + Laravel     ┘
```

One JSON file per problem holds the metadata *and* every test case. You never write a test —
and you cannot make Python pass by weakening a Python test, because the case lives in a file
the other five suites also read.

Nine problems currently produce **1,345 assertions** across the six suites.

### Every problem has more than one approach

```bash
curl 'localhost:8000/problems/contains-duplicate?approach=brute-force'   # O(n²)
curl 'localhost:8000/problems/contains-duplicate?approach=hash-set'      # O(n)
```

You implement all of them. A **differential test** asserts they always agree, so the naive one
you write first becomes the oracle for the clever one — and the response carries
`elapsedMicros`, so you can measure instead of assume.

Two of the nine problems turned out to be faster with the *worse* complexity on realistic
input. That is not a thing you learn by reading.

---

## Commands

```bash
make setup                     install all three toolchains (once)
make status                    which problems you have solved, per language
make test                      all six suites   (also test-python / -node / -php)
make run-all                   all three servers at once

make test-solved               test only the problems you have solved
make sync                      bring in new problems, keeping your solutions

make show SLUG=two-sum         print a worked answer — touches nothing
make solution SLUG=two-sum     write it over your stub
make restore                   undo that

make progress                  your progress through the 150
```

## Layout

```
docs/problems/            the exercise briefs — start here
packages/
  contracts/              JSON: metadata + every test case. The single source of truth.
  core-python/            neetcode_core     ← your Python goes here
  core-ts/                @neetcode/core    ← your TypeScript goes here
  core-php/               neetcode/core     ← your PHP goes here
apps/
  api-python/             FastAPI      — routers, Pydantic models, Depends()
  api-node/               NestJS       — modules, DTOs, pipes, exception filter
  api-php/                Laravel      — controllers, FormRequests, service provider
solutions/                worked answers + the cross-language write-ups (spoilers)
tools/                    scaffolding, contract validation, progress
```

The core packages have **zero runtime dependencies** — no framework, no HTTP, no notion of a
status code. That is what keeps the algorithms testable on their own and the framework
comparison honest.

## Documentation

| | |
|---|---|
| [00 — Getting started](docs/00-getting-started.md) | **Start here.** Install, solve, test, save your work |
| [01 — Architecture](docs/01-architecture.md) | Why the layers are where they are |
| [02 — Adding a problem](docs/02-adding-a-problem.md) | Authoring a new exercise |
| [03 — Python & FastAPI](docs/03-python-fastapi.md) | The stack, idioms, and traps |
| [04 — TypeScript & NestJS](docs/04-typescript-nestjs.md) | The stack, idioms, and traps |
| [05 — PHP & Laravel](docs/05-php-laravel.md) | The stack, idioms, and traps |
| [06 — Language & framework comparison](docs/06-language-comparison.md) | The side-by-side |
| [07 — Testing strategy](docs/07-testing-strategy.md) | Why one JSON file drives six suites |
| [08 — Ready-to-paste AI prompts](docs/08-ai-prompts.md) | For Claude Code / Cowork |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Adding problems for other people to solve |
| [AGENTS.md](AGENTS.md) | Operating manual for humans and AI assistants |

## Progress

`make progress` for the live table.

| # | Topic | Exercises available |
|---|-------|---------------------|
| 01 | Arrays & Hashing | **9 / 9** ✅ |
| 02 | Two Pointers | 0 / 5 |
| 03 | Sliding Window | 0 / 6 |
| 04 | Stack | 0 / 7 |
| 05 | Binary Search | 0 / 7 |
| 06 | Linked List | 0 / 11 |
| 07 | Trees | 0 / 15 |
| 08 | Tries | 0 / 3 |
| 09 | Heap / Priority Queue | 0 / 7 |
| 10 | Backtracking | 0 / 9 |
| 11 | Graphs | 0 / 13 |
| 12 | Advanced Graphs | 0 / 6 |
| 13 | 1-D Dynamic Programming | 0 / 12 |
| 14 | 2-D Dynamic Programming | 0 / 11 |
| 15 | Greedy | 0 / 8 |
| 16 | Intervals | 0 / 6 |
| 17 | Math & Geometry | 0 / 8 |
| 18 | Bit Manipulation | 0 / 7 |

## Your solutions, and everyone else's exercises

```
this repo (the platform)          your repo (from "Use this template")
  exercises only, always          your solutions, on main
  new problems land here  ──────► make sync brings them in, keeping your work
```

Two repositories, two jobs. This one always hands out clean exercises. Yours holds your
solutions, counts on your GitHub profile, and stays up to date with `make sync`.

CI knows the difference: here it checks that every function is still unsolved, and in your repo
it instead runs `make test-solved` — the problems you have finished — so a green tick means
your work is correct, not that you have finished all 150.

## Contributing

New problems are the most useful contribution, and the scaffolding does most of the work. See
**[CONTRIBUTING.md](CONTRIBUTING.md)**. The one rule: never commit a solved function to `main`.

## Requirements

Python 3.11+ · Node 20+ · PHP 8.3+ with `mbstring` · Composer 2

## Licence

[MIT](LICENSE). Use it to teach, fork it, build a course on it — whatever helps.
