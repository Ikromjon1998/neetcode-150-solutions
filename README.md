# My NeetCode 150 solutions — Python, TypeScript and PHP

[![CI](https://github.com/Ikromjon1998/neetcode-150-solutions/actions/workflows/ci.yml/badge.svg)](https://github.com/Ikromjon1998/neetcode-150-solutions/actions/workflows/ci.yml)

I'm solving the [NeetCode 150](https://neetcode.io/practice) three times over — once in
**Python**, once in **TypeScript** and once in **PHP** — to learn what each language and its
type system actually does differently, rather than just the algorithms.

Built on [**neetcode-150**](https://github.com/Ikromjon1998/neetcode-150), the practice platform
I wrote for this. Every problem is tested against a shared contract in all three languages, so a
solution is only "done" when all three agree.

---

## Where my code is

**The solutions I have written are the implemented functions here:**

```
packages/core-python/src/neetcode_core/<topic>/<problem>.py
packages/core-ts/src/<topic>/<problem>.ts
packages/core-php/src/<Topic>/<Problem>.php
```

Everything else comes from the platform: the tests, the problem briefs, the three web
applications, and the tooling.

> **`solutions/` is not my work.** That folder holds the platform's reference answers, which
> ship with every copy of it. Mine are the files listed above.

Each problem asks for **two or three different approaches** — typically a naive one and an
optimal one — and a differential test checks that they agree with each other.

## Progress

```bash
make status      # every problem, per language
make progress    # progress through the 150, by topic
```

## Why three languages

Solving something once teaches you the algorithm. Solving it three times teaches you the
languages, because the third time you stop translating and start noticing. A few things that has
surfaced so far:

- `1 * 0 * -3` is `-0` in JavaScript, and `-0 === 0` is `true`, so it hides from every ordinary
  comparison. Python and PHP integers have no signed zero at all.
- PHP strings are byte arrays: `strlen("héllo")` is 6, not 5.
- A `Map` compares array keys by reference, so a character-count array can be a dictionary key in
  Python but has to be serialised in TypeScript — and in PHP too, for the opposite reason.

## Running it

```bash
make setup                                  # once
make try SLUG=contains-duplicate            # test one problem in all three languages
make test-solved                            # test everything I have solved so far
make sync                                   # pull in new problems from the platform
```

Every solved function is also a live HTTP endpoint in three applications — FastAPI, NestJS and
Laravel — held to byte-identical responses by the test suite:

```bash
make run-all     # :8000 FastAPI  ·  :3000 NestJS  ·  :8080 Laravel
```

## Want to try it yourself?

Go to [neetcode-150](https://github.com/Ikromjon1998/neetcode-150) and click **"Use this
template"**. You get your own copy with every algorithm blanked out, ready to solve.

## Licence

[MIT](LICENSE).
