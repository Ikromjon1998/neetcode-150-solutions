# 08 — Ready-to-paste prompts

Prompts for Claude Cowork, Claude Code, or any assistant working in this repo. They assume
[`AGENTS.md`](../AGENTS.md) is present — it is, at the repo root, and any competent assistant
will read it first.

Copy a prompt, fill in the `«placeholders»`, paste.

> **The one distinction that matters.** This repo ships *exercises*, not answers. "Solve X" and
> "add X" are opposite jobs — one fills in stubs, the other creates new ones. Every prompt below
> says which it is, and you should too.

---

## 1. Add a new exercise

The maintainer job. This is the one you will use most.

```text
Add NeetCode problem «Valid Palindrome» to this repo as a new EXERCISE.

Follow the authoring workflow in AGENTS.md section 4B exactly. In short:

1. Confirm the LeetCode id, exact title, difficulty and topic. Tell me the id before you
   scaffold — a wrong id corrupts the filename and the catalog sort order.
2. Pick 2–3 approaches: a naive baseline plus the optimal one at minimum. The baseline is not
   filler — the differential test compares them.
3. Scaffold with `make new-problem ARGS="..."`. Do not hand-create any of those files.
4. Fill in packages/contracts/problems/NNNN-slug.json with REAL cases:
   - 6+ happy-path cases including empty input, duplicates, negatives, the answer at either
     end, and the "almost" case
   - non-ASCII input if it is a string problem
   - 3+ validationCases
   - notFoundCases if the problem can legitimately have no answer
5. Implement it three times — Python, TypeScript, PHP — IN PLACE in packages/core-*, each one
   IDIOMATIC for its language rather than a transliteration. Run `make test` until green.
6. `make extract SLUG=<slug>` to move your answers into solutions/ and leave stubs behind,
   then `make statements`.
7. Write solutions/notes/NNNN-slug.md. This is the deliverable. Be specific about what
   actually differed between the languages and frameworks — real observations from writing
   this problem, not generic facts you already knew.
8. `make verify-solutions` and `make test-contracts`.
9. `make test` should now be RED for this problem. Confirm that it is.

Then tell me: what you added, what the cross-language differences turned out to be, and
anything that surprised you.
```

## 2. Solve an existing exercise

The learner job. Note how explicitly it forbids touching `solutions/`.

```text
Solve the «two-sum» exercise in this repo.

Read docs/problems/0001-two-sum.md first. Implement the three stubs it names, IN PLACE:
  packages/core-python/src/neetcode_core/arrays_and_hashing/two_sum.py
  packages/core-ts/src/arrays-and-hashing/two-sum.ts
  packages/core-php/src/ArraysAndHashing/TwoSum.php

Rules:
- Do NOT look at solutions/ and do NOT run `make show` or `make solution`. I want your own
  implementation, and I want to compare it against the reference afterwards.
- Do NOT run `make extract` — that would move my work out of place.
- Write each one idiomatically for its language. If all three read the same, you translated.
- Keep the registration, signatures and module docstrings as they are; replace only the
  `raise` / `throw`.
- `make test` until green.

Then tell me what differed between the three, before I read the reference notes.
```

## 3. Add a whole topic

```text
Add these NeetCode problems to this repo as new EXERCISES, one at a time, in this order:

  «125 Valid Palindrome»
  «167 Two Sum II»
  «15 3Sum»

For each one, follow the full AGENTS.md section 4B workflow: scaffold, fill the contract with
real cases, implement three times idiomatically, `make test`, `make extract`, `make statements`,
write solutions/notes/NNNN-slug.md, then `make verify-solutions`.

Finish each problem completely — including its notes and the extract step — before starting
the next. Do not batch the implementations and leave the extraction for the end.

After each one, give me two lines: the approaches you implemented, and the single most
interesting cross-language difference.

When all three are done, run `make progress` and `make status` and show me both.
```

## 4. Review an exercise you already shipped

```text
Review the «two-sum» exercise as a piece of teaching material, not as code.

Check:
- Does the brief in docs/problems/0001-two-sum.md give enough to start, without giving the
  answer away? The stub docstrings come from the contract's approach notes — are those hints
  or spoilers?
- Do the contract's test cases cover the edge cases a learner would actually get wrong? If a
  case is missing, add it and show me which reference implementations fail it.
- Is each of the three reference solutions genuinely idiomatic for its language, or is one a
  transliteration of another?
- Do solutions/notes/0001-two-sum.md's claims still match the code?

Show me the findings before changing anything.
```

## 5. Add a third approach to an existing exercise

```text
Add a «two-pointers» approach to the «valid-palindrome» exercise.

- Add it to the approaches array in the contract, with real complexities and a note explaining
  what it trades away. That note becomes the stub's docstring, so write it as a specification,
  not as an explanation of the code.
- Implement it in all three reference solutions under solutions/.
- `make solution SLUG=valid-palindrome` to apply them, `make test` to confirm the differential
  test still passes, then `make restore`.
- `make statements` to regenerate the brief.
- Update solutions/notes/NNNN-slug.md with the new approach and re-run the benchmark table.

Do not change the default approach unless the new one is genuinely better on the criteria the
contract's note explains.
```

## 6. Explain something in this repo

```text
Explain how «the registry» works in this repo, comparing all three languages.

Read the actual code — packages/core-python/src/neetcode_core/registry.py,
packages/core-ts/src/registry.ts, packages/core-php/src/Registry/ProblemRegistry.php — and
explain what each one does differently, why each ecosystem landed there, and what each
approach costs.

I want to understand the trade-off, not just the mechanism.
```

## 7. Start a fresh session

```text
Read AGENTS.md, then docs/01-architecture.md.

Run `make status` and `make progress`.

Tell me in five lines what you understand this repo to be and what the two workflows are. Then
wait — I will tell you which one we are doing.
```

---

## What makes these work

Five things, if you want to write your own:

1. **Say which job it is.** "Solve X" and "add X" have opposite outcomes here — one fills stubs
   in, the other creates them. An assistant that guesses wrong either deletes your work or
   hands you the answer to something you wanted to attempt.
2. **Point at `AGENTS.md`** rather than restating the rules. It is in the repo, it is current,
   and it lists the framework traps already worked around. Restating it in a prompt guarantees
   the two will drift.
3. **Name the deliverable.** For a new exercise it is `solutions/notes/NNNN-slug.md`, not the
   passing tests. That is the step assistants skip, because green feels like done.
4. **Demand specificity.** "What differed between the languages" invites a Wikipedia answer.
   "What differed *in this code*, that you found *while writing it*" does not.
5. **Forbid the transliteration.** Left alone, an assistant writes the Python version and
   translates it twice. That produces three files and zero learning. Say so.
