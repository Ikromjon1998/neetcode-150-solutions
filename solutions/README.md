# `solutions/` — spoilers live here

Everything under this directory is an **answer**. If you are here to practise, close it and
open [`docs/problems/`](../docs/problems/) instead.

```
solutions/
  python/<topic_snake>/<slug_snake>.py        reference implementation
  typescript/<topic>/<slug>.ts                reference implementation
  php/<TopicPascal>/<Slug>.php                reference implementation
  notes/NNNN-slug.md                          the cross-language write-up
```

## How to use it

```bash
make show SLUG=two-sum                  # print the answer, touch nothing
make show SLUG=two-sum LANG=php         # just one language
make solution SLUG=two-sum              # write it over your stub
make restore                            # undo that
```

`make solution` backs up whatever it overwrites into `.neetcode-backup/`, so it can never cost
you work. `make restore` puts your files back.

## These files are overlays, not a package

A file here is a byte-for-byte copy of what belongs at the *live* path — for example
`solutions/python/arrays_and_hashing/two_sum.py` is what
`packages/core-python/src/neetcode_core/arrays_and_hashing/two_sum.py` should contain.

Its imports are written for the live location, so nothing here compiles where it sits. That is
deliberate: it keeps `make solution` a plain file copy with no rewriting, and it keeps the
reference answers out of every build, typecheck and test run.

## They are verified, not assumed

Reference solutions rot. This one cannot:

```bash
make verify-solutions
```

applies all 27, runs all six test suites, then restores your files — and CI runs it on every
push. If a contract gains a case the reference answers cannot satisfy, the build goes red.

## The notes

`solutions/notes/NNNN-slug.md` is the long-form write-up for each problem: what actually
differed between the three languages and the three frameworks, what went wrong, and the
measured benchmarks.

They are the most useful thing in this repository and also the most complete spoilers. Read one
**after** you have solved that problem — comparing your three implementations against someone
else's is where most of the value is, and it only works if you have three of your own.

## Adding a reference solution

When you author a new exercise, the flow is:

1. `make new-problem ARGS="…"` — scaffolds the contract, stubs, tests and app wiring.
2. Fill in the contract with real cases.
3. Implement it, **in place** in `packages/core-*`, until `make test` is green.
4. `make extract SLUG=<slug>` — moves your implementation here and leaves a stub behind.
5. Write `solutions/notes/NNNN-slug.md`.
6. `make verify-solutions` — proves the reference still passes.

Step 4 is the important one: you solve it where it runs, then turn it into an exercise. There
is no separate "write the stub" step, and no way for a stub and its answer to drift apart.
