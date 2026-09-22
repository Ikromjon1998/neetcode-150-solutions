# Contributing

Thanks for helping. This repository is a **practice set**: every algorithm ships as an unsolved
stub, and people learn by filling them in. That shapes every rule below.

> **Want to solve problems?** You don't need this file. Click **"Use this template"** to get
> your own repository, then read [docs/00-getting-started.md](docs/00-getting-started.md).
> Nothing here applies to you.
>
> Use a **fork** only for what this file describes: changing the platform itself.

---

## The one rule

**Never commit a solved function to `main`.**

`main` is what everyone copies with "Use this template", so a solution committed there turns an
exercise into a give-away for every future learner. CI enforces this: on pull requests into
`main` it fails if any function in `packages/core-*` is implemented.

This rule is only about *this* repository. In your own solutions repo, committing solved
functions to `main` is exactly right, and CI there checks them instead.

Worked answers belong in `solutions/`, where people only see them if they ask (`make show`).

---

## Ways to contribute

### Add a new problem

This is the most useful contribution. The full walkthrough is in
[docs/02-adding-a-problem.md](docs/02-adding-a-problem.md). In short:

```bash
git switch -c add/valid-palindrome

make new-problem ARGS="--id 125 --slug valid-palindrome --title 'Valid Palindrome' \
  --difficulty easy --topic two-pointers --input 's:string' --returns bool \
  --approaches reverse-compare,two-pointers"
```

1. Fill in `packages/contracts/problems/NNNN-slug.json`: a real summary, real complexities,
   and **real test cases** (six or more, including the edge cases people get wrong).
2. Solve it in all three languages, in place, until `make try SLUG=<slug>` is green.
3. `make extract SLUG=<slug>`. This moves your answers into `solutions/` and puts the stubs
   back. **This is the step that makes it an exercise.**
4. `make statements` to regenerate the problem brief.
5. Write `solutions/notes/NNNN-slug.md`: what actually differed between the three languages.
6. `make verify-solutions` then `make test-contracts`.

> **You cannot practise a problem you author.** Writing an exercise means solving it first. If
> you are also using this repo to learn, author the topics you have already mastered, and leave
> the ones you still want to practise to someone else.

### Improve an existing problem

- **A missing edge case** is the best kind of fix. Add it to the problem's contract JSON; all
  six test suites pick it up. Then run `make verify-solutions` to confirm the worked answers
  still pass.
- **A better worked answer**: edit the file in `solutions/`, then `make verify-solutions`.
- **A clearer hint**: approach hints come from the contract's `note` field. Edit it there, then
  run `make stubs SLUG=<slug>` and `make statements`. `make stubs` never touches `solutions/`
  and never overwrites a solved file.

### Write a topic guide

`docs/topics/NN-<topic>.md` is the page a learner reads *before* attempting a topic. One rule
governs it:

> **A topic guide teaches the language, never the answer.** Data structures, syntax, costs and
> per-language traps — yes. How to approach a specific problem — no.

The line is the same one Exercism draws between a *concept* and a *practice exercise*. "PHP has
no Set type, array keys stand in for one" is vocabulary. "To find duplicates, put them in a set"
is the answer to an exercise, and it belongs in `solutions/notes/` instead.

Each guide has a `<!-- generated:problems -->` block listing the topic's exercises. That block is
written by `make statements` — leave it alone and edit the prose around it.

There is deliberately **no automated check** for this rule. Slugs and approach keys appear
legitimately in a guide's prose (`make try SLUG=…`, "sorting is the other tool here"), so any
mechanical check produces more false alarms than catches. It is a review rule.

### Fix a bug or improve the docs

Normal pull requests. Note that `docs/problems/*.md` is **generated**: change the contract and
run `make statements`, never edit those files by hand.

---

## Before you open a pull request

```bash
make test-contracts        # every contract is valid, and implemented in all three languages
make verify-solutions      # every worked answer passes all six suites
make status                # every function shows `todo` — nothing solved on your branch
make lint                  # ruff, tsc and pint
```

- [ ] No solved functions in `packages/core-*`: `make status` shows only `todo`
- [ ] `make try SLUG=<slug>` passes with the reference answers applied
- [ ] New problems have six or more real cases and three or more validation cases
- [ ] `docs/problems/` is regenerated (`make statements`), not hand-edited
- [ ] A new topic guide contains no problem-specific approach — vocabulary only
- [ ] New problems include `solutions/notes/NNNN-slug.md`

CI runs all of this on every pull request.

---

## How the repo is laid out

| Path | What lives there |
|------|------------------|
| `packages/contracts/` | One JSON file per problem: metadata and every test case |
| `packages/core-*/` | The exercises: unsolved stubs, one per approach |
| `solutions/` | Worked answers, and the cross-language write-ups |
| `apps/api-*/` | FastAPI, NestJS and Laravel apps that serve each solved problem |
| `docs/problems/` | Generated problem briefs |
| `docs/topics/` | Topic guides: the language toolbox to read before a topic |
| `tools/` | The scaffolding scripts behind `make` |

[AGENTS.md](AGENTS.md) is the full operating manual, and
[docs/01-architecture.md](docs/01-architecture.md) explains why it is laid out this way.

---

## Licence

By contributing, you agree that your contributions are licensed under the
[MIT License](LICENSE).
