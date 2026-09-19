# CLAUDE.md

See **[AGENTS.md](./AGENTS.md)** — the operating manual for this repository.

The one thing to get right before anything else: **this is a practice repo, not a solutions
repo.** Every algorithm in `packages/core-*` ships as an unsolved stub, and `make test` fails
on a fresh clone by design.

So work out which job you have been given:

- **"Solve problem X"** → implement the stubs in `packages/core-*` in place. **Check
  `git remote get-url origin` first**: in `Ikromjon1998/neetcode-150` (the platform) solutions
  must never be committed — the user wants their own repo from "Use this template". In a
  solutions repo, solving on `main` is correct. Do not touch `solutions/`.
- **"Add problem X"** → author a new *exercise*: scaffold, fill the contract, implement, then
  `make extract` to move your answer into `solutions/` and leave a stub behind.

Guessing wrong either deletes the user's work or hands them the answers. If it is ambiguous,
ask.

Also:

- Algorithms go in `packages/core-*`. They never import a framework.
- Applications go in `apps/api-*`. They never contain an algorithm.
- `packages/contracts/problems/*.json` is the single source of truth. All six test suites read it.
- `docs/problems/*.md` is generated — edit the contract, then `make statements`.
- An exercise is finished when `make verify-solutions` passes and `solutions/notes/NNNN-slug.md`
  is written.
