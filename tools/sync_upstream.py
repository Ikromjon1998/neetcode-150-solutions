#!/usr/bin/env python3
"""Pull new problems from the platform into your solutions repo, keeping your solutions.

    make sync
    make sync UPSTREAM=https://github.com/<owner>/neetcode-150.git   # a different platform

Repositories created with "Use this template" share no git history with the template, so a
plain `git merge` refuses to run. The first sync joins the two histories
(`--allow-unrelated-histories`); every sync after that is an ordinary merge.

When both sides changed the same file, the conflict is resolved by one rule:

* an exercise file you have **solved** -> keep yours (your solution)
* `README.md`                          -> keep yours (it is your repo's front page)
* everything else                      -> take the platform's (new problems, fixes, tooling)

Anything the rule cannot decide is left conflicted and listed, for you to resolve by hand.
Nothing is pushed — review the result, then `git push` yourself.
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

from solutions import STUB_MARKERS  # noqa: E402

DEFAULT_UPSTREAM = "https://github.com/Ikromjon1998/neetcode-150.git"
REMOTE = "upstream"
BRANCH = "main"

# Files whose change means `make setup` should be re-run after the merge.
DEPENDENCY_FILES = (
    "package.json", "package-lock.json",
    "apps/api-node/package.json", "packages/core-ts/package.json",
    "apps/api-python/pyproject.toml", "packages/core-python/pyproject.toml",
    "apps/api-php/composer.json", "apps/api-php/composer.lock",
    "packages/core-php/composer.json", "packages/core-php/composer.lock",
)


def git(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True)
    if check and result.returncode != 0:
        sys.exit(f"git {' '.join(args)} failed:\n{result.stderr.strip()}")
    return result


def repo_slug(url: str) -> str:
    """`git@github.com:a/b.git` and `https://github.com/a/b` both become `a/b`."""
    match = re.search(r"[:/]([^/:]+/[^/]+?)(?:\.git)?/?$", url.strip())
    return match.group(1).lower() if match else url.strip().lower()


# How each language's problem modules announce themselves. Recognising an exercise by its
# CONTENT rather than by reading the contracts is deliberate: this runs in the middle of a
# merge, where a contract file may itself be conflicted and full of `<<<<<<<` markers. Parsing
# JSON here would crash and strand the learner in a half-resolved merge.
REGISTRATION_MARKERS = (
    "@solution(SLUG, approach=",      # Python
    "defineProblem(SLUG,",            # TypeScript
    "implements ProblemDefinition",   # PHP
)
CORE_PREFIXES = (
    "packages/core-python/src/",
    "packages/core-ts/src/",
    "packages/core-php/src/",
)


def is_solved_exercise(path: str, content: str) -> bool:
    """True when `path` is a live exercise file and `content` has no stub left in it."""
    if not path.startswith(CORE_PREFIXES):
        return False
    registers = any(marker in content for marker in REGISTRATION_MARKERS)
    return registers and not any(marker in content for marker in STUB_MARKERS)


def stage_content(path: str, stage: int) -> str | None:
    """File content at a merge stage: 2 = yours, 3 = the platform's. None if absent."""
    result = git("show", f":{stage}:{path}", check=False)
    return result.stdout if result.returncode == 0 else None


def resolve(path: str) -> str | None:
    """Apply the resolution rule to one conflicted path. Returns 'ours'/'theirs' or None."""
    ours, theirs = stage_content(path, 2), stage_content(path, 3)
    if ours is None or theirs is None:
        return None  # a delete on one side: not something to decide automatically

    if path == "README.md" or is_solved_exercise(path, ours):
        side = "ours"
    else:
        side = "theirs"

    git("checkout", f"--{side}", "--", path)
    git("add", "--", path)
    return side


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--upstream", default=os.environ.get("UPSTREAM") or DEFAULT_UPSTREAM)
    args = parser.parse_args()

    origin = git("remote", "get-url", "origin", check=False).stdout.strip()
    if origin and repo_slug(origin) == repo_slug(args.upstream):
        print("This is the platform repository itself — there is nothing to sync from.")
        print("`make sync` is for solutions repos created with \"Use this template\".")
        return 0

    if git("status", "--porcelain").stdout.strip():
        sys.exit("You have uncommitted changes. Commit or stash them first, then run make sync.")

    remotes = git("remote").stdout.split()
    if REMOTE not in remotes:
        git("remote", "add", REMOTE, args.upstream)
        print(f"Added remote '{REMOTE}' -> {args.upstream}")

    print(f"Fetching {REMOTE}/{BRANCH} ...")
    git("fetch", "--quiet", REMOTE, BRANCH)
    target = f"{REMOTE}/{BRANCH}"

    if git("merge-base", "--is-ancestor", target, "HEAD", check=False).returncode == 0:
        print("Already up to date — no new problems on the platform.")
        return 0

    first_sync = git("merge-base", "HEAD", target, check=False).returncode != 0
    if first_sync:
        print("First sync: joining your history to the platform's (one time only).")

    before = git("rev-parse", "HEAD").stdout.strip()
    merge_args = ["merge", "--no-ff", "--no-edit", target]
    if first_sync:
        merge_args.insert(1, "--allow-unrelated-histories")
    merged = git(*merge_args, check=False)

    kept, taken, unresolved = [], [], []
    if merged.returncode != 0:
        conflicted = git("diff", "--name-only", "--diff-filter=U").stdout.split()
        if not conflicted:
            sys.exit(f"git merge failed:\n{merged.stderr.strip()}")
        for path in conflicted:
            try:
                side = resolve(path)
            except Exception as exc:  # noqa: BLE001 - never strand the user mid-merge
                print(f"  ! could not resolve {path}: {exc}")
                side = None
            (kept if side == "ours" else taken if side == "theirs" else unresolved).append(path)

        if unresolved:
            print("\nResolved what I could. These need you:")
            for path in unresolved:
                print(f"  ! {path}")
            print("\nFix them, `git add` them, then `git commit`.  To abandon: git merge --abort")
            return 1
        git("commit", "--no-edit")

    changed = git("diff", "--name-only", before, "HEAD").stdout.split()
    new_problems = sorted(
        Path(path).stem for path in changed
        if path.startswith("packages/contracts/problems/") and path.endswith(".json")
        and git("cat-file", "-e", f"{before}:{path}", check=False).returncode != 0
    )

    print("\nSynced with the platform.")
    if new_problems:
        print(f"\n  New problems ({len(new_problems)}):")
        for name in new_problems:
            print(f"    + {name}")
    if kept:
        print("\n  Kept your version (you had solved or customised these):")
        for path in kept:
            print(f"    = {path}")
    if taken:
        print(f"\n  Took the platform's version of {len(taken)} other file(s).")
    if any(path in DEPENDENCY_FILES for path in changed):
        print("\n  Dependencies changed — run:  make setup")

    print("\n  Review with `make status`, then push:  git push\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
