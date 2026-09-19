# 00 — Getting started: learning with this repo

This is the guide for **solving** problems. If you want to *add* new problems for other people,
read [CONTRIBUTING.md](../CONTRIBUTING.md) instead.

Every problem here is an exercise. The tests are written, the three web apps are wired up, and
every algorithm is an empty stub waiting for you. You write the algorithms.

You get **your own repository** for them. Your solutions live there, on `main`, so they count
towards your GitHub profile and anyone can see your work — while the platform keeps handing out
clean exercises to everybody else.

---

## 1. What you need

| Tool | Version | Check |
|------|---------|-------|
| Python | 3.11+ | `python3 --version` |
| Node | 20+ | `node --version` |
| PHP | 8.3+ with `mbstring` | `php --version && php -m \| grep mbstring` |
| Composer | 2.x | `composer --version` |
| GNU Make | any | `make --version` |

macOS: `brew install python node php composer`
Ubuntu: `sudo apt install python3-venv nodejs npm php-cli php-mbstring composer`

---

## 2. Get your own repository

On the platform repo, click **"Use this template" → Create a new repository**. Name it
something like `neetcode-150-solutions`, and make it **public** if you want it to count on your
GitHub profile.

That gives you a normal, standalone repository — not a fork. This matters:

| | Commits count on your profile? | Shows on your profile? |
|---|---|---|
| **Made with "Use this template"** | **yes** | **yes** |
| Made with "Fork" | no, unless merged upstream | listed as a fork |

Then clone it:

```bash
git clone git@github.com:<you>/neetcode-150-solutions.git
cd neetcode-150-solutions
```

> **Want to improve the platform itself** — add a problem, fix a hint, report a bug? That is a
> **fork** of the platform repo, not this. See [CONTRIBUTING.md](../CONTRIBUTING.md).

---

## 3. Install

```bash
make setup
```

Two to four minutes the first time; most of that is npm and Composer downloading packages. It
is safe to run again at any time.

---

## 4. Connect to the platform

Run this once, so you can receive new problems later:

```bash
make sync
```

A repository made from a template shares no git history with it, so the first sync joins the
two together. Do it now, while your copy is still untouched and there is nothing to conflict.
After this, `make sync` is an ordinary update you can run any time (section 9).

**You solve on `main`, in your own repository.** There is no special branch to remember. Your
commits count on your GitHub profile, and because this is your own repo, nobody else's
exercises are affected.

---

## 5. Check that it works

```bash
make status
```

```
problem                              python       ts      php   reference
--------------------------------------------------------------------------
   1. two-sum                          todo     todo     todo   yes
 217. contains-duplicate               todo     todo     todo   yes
  ...
0 / 27 implementations written (9 problems x 3 languages)
```

`todo` means unsolved. That is correct for a fresh start.

```bash
make test
```

**This fails, and it is supposed to.** Every algorithm is an unsolved stub, and the tests are
the specification you are working towards.

To check the setup itself works before you write anything:

```bash
make verify-solutions
```

This temporarily swaps in the worked answers, runs all six test suites (they pass), then puts
your stubs back.

---

## 6. Solve your first problem

**Start with `contains-duplicate`.** It is the gentlest problem here.

### Read the brief

```bash
cat docs/problems/0217-contains-duplicate.md
```

The brief gives you the problem, examples, the approaches to implement with their target
complexity, and the three files to edit. It does not contain the answer.

### Open the stub

```
packages/core-python/src/neetcode_core/arrays_and_hashing/contains_duplicate.py
```

```python
@solution(SLUG, approach="hash-set")
def contains_duplicate_hash_set(nums: list[int]) -> bool:
    """Set membership — target: O(n) time, O(n) space.

    Return on the first repeat, so the early-exit case is far better than O(n) in practice.
    """
    raise UnsolvedError(SLUG, "hash-set", PATH)
```

Replace **only** the `raise` line with your code. Leave the `@solution(...)` line, the function
name, the parameters and the return type as they are. That is how the tests find your function.

### Test it

```bash
make try SLUG=contains-duplicate LANG=python
```

```
217. Contains Duplicate  (contains-duplicate)

  python      fail  36 failed, 213 deselected in 0.06s
  -> still a stub — that is the exercise
     edit: packages/core-python/src/neetcode_core/arrays_and_hashing/contains_duplicate.py
```

Write, run, repeat. When it goes green:

```
  python      pass  36 passed, 213 deselected in 0.02s
```

`make try` runs only this one problem, so it takes about a second. Drop `LANG=python` to check
all three languages at once.

Every problem has **two or three approaches**, one function each. You have solved a problem
when all of them pass. A *differential test* checks that your approaches agree with each other,
so writing the simple one first gives you something to check the clever one against.

---

## 7. How to work a problem

A method that works, especially if you are preparing for interviews:

1. **Understand it.** Restate the problem in your own words. Write down the edge cases (empty
   input, duplicates, negative numbers) before writing code.
2. **Say your approach out loud** before you type. In an interview, explaining your thinking
   counts as much as the code.
3. **Timebox it.** About 15 minutes for easy, 25 for medium, 40 for hard. The stub's docstring
   is your first hint.
4. **Stuck after the timebox plus 10 minutes?** Look at the answer (section 8), understand it,
   then **solve it again from scratch two days later.** Looking is fine. Never re-solving is
   the real mistake.
5. **State the complexity** of your solution, time and space.

### Three languages as a memory tool

You do not have to solve every problem in all three languages straight away. A pattern that
works well:

- **Day 0:** solve it in your strongest language.
- **About a week later:** solve it again from scratch in a second language.
- **About three weeks later:** solve it in the third.

Each re-solve checks whether you remember the *pattern*, not just the code. `make status` tracks
each language separately, so you can see what is due.

---

## 8. When you are stuck

```bash
make show SLUG=contains-duplicate              # print a worked answer — changes no files
make show SLUG=contains-duplicate LANG=python  # just one language
```

To put the worked answer into your stub (for example to compare it with yours while it runs):

```bash
make solution SLUG=contains-duplicate   # writes the answer over your stub
make restore                            # puts your version back
```

`make solution` backs up your file before overwriting it, so you cannot lose work.

**After you solve a problem**, read its write-up in `solutions/notes/`, for example
[`solutions/notes/0217-contains-duplicate.md`](../solutions/notes/0217-contains-duplicate.md).
It compares how the problem plays out in Python, TypeScript and PHP. It contains the answers,
so read it *after* solving, not before.

---

## 9. Save your work, and get new problems

### Commit your solutions

```bash
git add packages/core-python packages/core-ts packages/core-php
git commit -m "Solve contains-duplicate in Python"
git push
```

Commit as often as you like — it is your repository. Each push shows on your GitHub profile.

### Check everything you have solved so far

```bash
make test-solved
```

This runs the tests for the problems you have solved and ignores the rest, so it stays green as
you go. It is also what CI runs in your repository, so your commits get a green tick once they
are correct.

### Get new problems

When the platform adds problems:

```bash
make sync
```

It fetches the platform, brings in the new problems, and **keeps your solutions**. The rule it
follows when both sides changed the same file:

- an exercise you have **solved** → your version is kept
- `README.md` → yours is kept, so you can write your own front page
- anything else → the platform's version, so you get fixes and new problems

Anything it cannot decide is left for you, with the files named. Nothing is pushed; review it,
then `git push`.

---

## 10. Track your progress

```bash
make status      # every problem, per language: todo or solved
make progress    # your progress through the NeetCode 150, by topic
```

---

## 11. Try the web apps (optional)

Every solved function is also a working HTTP endpoint in three applications:

```bash
make run-python    # FastAPI  — http://localhost:8000  (Swagger UI at /docs)
make run-node      # NestJS   — http://localhost:3000  (Swagger UI at /docs)
make run-php       # Laravel  — http://localhost:8080
make run-all       # all three at once
```

```bash
curl -s localhost:8000/problems/contains-duplicate \
  -H 'content-type: application/json' \
  -d '{"nums":[1,2,3,1]}'
```

Before you solve it, the endpoint returns **501** and names the file to edit. After you solve
it, all three apps return the same JSON. [01 — Architecture](01-architecture.md) explains how
that works.

---

## Command reference

| Command | What it does |
|---------|--------------|
| `make setup` | Install everything (once) |
| `make status` | Which problems are solved, per language |
| `make try SLUG=x` | Test one problem in all three languages. Add `LANG=python` for one |
| `make test` | Every test suite, for every problem |
| `make show SLUG=x` | Print a worked answer without changing files |
| `make solution SLUG=x` | Write the worked answer over your stub |
| `make restore` | Undo `make solution` |
| `make test-solved` | Test only the problems you have solved |
| `make sync` | Bring in new problems from the platform, keeping your solutions |
| `make verify-solutions` | Check the worked answers pass, then put your files back |
| `make progress` | Your progress through the 150 |
| `make run-all` | Start all three web apps |

---

## Troubleshooting

**`make test` fails everywhere** — expected on unsolved problems. Use `make try SLUG=x` for the
one you are working on, and `make status` to see what is left.

**`UnsolvedError` / `UnsolvedException`** — that is what an unsolved stub raises. Replace the
`raise` / `throw` line with your code.

**My function is not being tested** — you probably renamed it or removed the `@solution(...)`
line. Put the original name and decorator back. The tests find functions by those, and in
TypeScript they import the function by name.

**`Could not find packages/contracts/problems`** — run commands from inside the repo, or set
`NEETCODE_CONTRACTS_DIR` to an absolute path.

**`No module named 'tests'` from pytest** — you are running a `pytest` binary that is not the
one in `.venv`. Use `make try` or `make test-python`.

**`make solution` overwrote something I wanted** — `make restore`. Every overwrite is backed up
to `.neetcode-backup/` first.

**`neetcode/core` not found by Composer** — run `composer install` inside
`packages/core-php` first. The app loads the core package from that directory.

**NestJS cannot resolve `@neetcode/core`** — run `npm run build --workspace @neetcode/core`.
`make setup` does this for you.

**CI is red in my repository** — CI runs `make test-solved` (only what you have solved) plus
lint and type checks on your code. A red tick means one of your solutions is wrong, or your code
does not pass `ruff` / `mypy` / `tsc`. Run `make test-solved` and `make lint` locally to see it.

**`make sync` says I have uncommitted changes** — commit or stash first. Merging on top of
unsaved work would be a good way to lose it.

---

## Where to go next

- [06 — Language & framework comparison](06-language-comparison.md): what actually differs
  between the three, with measurements.
- [01 — Architecture](01-architecture.md): how one JSON file drives six test suites.
- [CONTRIBUTING.md](../CONTRIBUTING.md): add a problem for other people to solve.
