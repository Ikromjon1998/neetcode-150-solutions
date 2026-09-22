#!/usr/bin/env python3
"""Run one problem's tests in all three languages.

    make try SLUG=two-sum
    make try SLUG=two-sum LANG=python

The loop you live in while solving. Each language gets the narrowest filter that still covers
the problem, so feedback is under a second rather than running all 1,345 assertions.

`make try` always exits 0 so it never prints make's own "Error 1" over the result. Call this
script directly if you want the exit code:

    python3 tools/try_problem.py two-sum && echo solved
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

from solutions import find, is_stub, php_filter  # noqa: E402

VENV = ROOT / ".venv/bin"

GREEN, RED, DIM, BOLD, OFF = "\033[32m", "\033[31m", "\033[2m", "\033[1m", "\033[0m"


def run(cmd: list[str], cwd: Path) -> tuple[int, str]:
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    return result.returncode, result.stdout + result.stderr


def summarise(language: str, output: str) -> str:
    """Pull the one line that says how it went out of three very different reporters."""
    patterns = {
        "python": r"(\d+ (?:failed|passed)[^\n]*)",
        "typescript": r"Tests\s+(.*?)\n",
        "php": r"(Tests: .*|OK \(.*\)|No tests executed!)",
    }
    match = re.search(patterns[language], output)
    return match.group(1).strip() if match else "(could not parse result)"


def first_failure(language: str, output: str) -> str | None:
    """The first genuinely useful line of the failure, for a one-glance diagnosis."""
    # A syntax error means the file never loaded, so no test ran and there is no assertion to
    # report. It is also never an algorithm mistake, so say so plainly rather than talking
    # about failing tests.
    broken = re.search(r"(?:Parse error|syntax error|SyntaxError|IndentationError|error TS\d+)[^\n]*",
                       output)
    if broken:
        return f"syntax error — the file does not compile: {broken.group(0).strip()}"

    for line in output.splitlines():
        stripped = line.strip()
        if "UnsolvedError" in stripped or "UnsolvedException" in stripped:
            return "still a stub — that is the exercise"
        if language == "python" and stripped.startswith(("E   ", "assert ")):
            return stripped[4:].strip() if stripped.startswith("E   ") else stripped
        if language == "typescript" and stripped.startswith("→"):
            return stripped[1:].strip()
        if language == "php" and stripped.startswith("Failed asserting"):
            return stripped
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("slug")
    parser.add_argument("--lang", choices=["python", "typescript", "php"])
    args = parser.parse_args()

    problem = find(args.slug)
    languages = [args.lang] if args.lang else ["python", "typescript", "php"]

    # Exact selectors from the Problem model — see its comment on why prefix matching breaks
    # once two-sum-ii, house-robber-ii and friends exist.
    commands = {
        "python": ([str(VENV / "pytest"), "-p", "no:warnings", problem.test_python],
                   ROOT / "packages/core-python"),
        "typescript": (["npx", "vitest", "run", "--root", "packages/core-ts",
                        problem.test_typescript], ROOT),
        "php": (["./vendor/bin/phpunit", "--filter", php_filter([problem.test_php_class])],
                ROOT / "packages/core-php"),
    }

    print(f"\n{BOLD}{problem.id}. {problem.title}{OFF}  {DIM}({problem.slug}){OFF}")
    print(f"{DIM}brief: docs/problems/{problem.id:04d}-{problem.slug}.md{OFF}\n")

    failed = False
    for language in languages:
        cmd, cwd = commands[language]
        code, output = run(cmd, cwd)
        stub = is_stub(problem.live(language))

        mark = f"{GREEN}pass{OFF}" if code == 0 else f"{RED}fail{OFF}"
        print(f"  {language:<11} {mark}  {DIM}{summarise(language, output)}{OFF}")

        if code != 0:
            failed = True
            detail = first_failure(language, output)
            if detail:
                print(f"{DIM}  -> {detail}{OFF}")
            else:
                # Do not claim output is "below" and then print nothing.
                print(f"{DIM}  -> could not read a result; last lines of the output:{OFF}")
                for line in [ln for ln in output.strip().splitlines() if ln.strip()][-8:]:
                    print(f"{DIM}     {line[:150]}{OFF}")
            print(f"{DIM}     edit: {problem.live(language).relative_to(ROOT)}{OFF}"
                  if stub else f"{DIM}     file: {problem.live(language).relative_to(ROOT)}{OFF}")

    if failed:
        # Name the command for the language that actually failed, not a generic list.
        suffix = {"python": "python", "typescript": "node", "php": "php"}
        which = " / ".join(f"make test-{suffix[lang]}" for lang in languages)
        print(f"\n{DIM}Full output:  {which}{OFF}")
        print(f"{DIM}Stuck:  make show SLUG={problem.slug}{OFF}\n")
    else:
        print(f"\n{GREEN}All three languages pass.{OFF} "
              f"{DIM}Read solutions/notes/{problem.id:04d}-{problem.slug}.md "
              f"to compare.{OFF}\n")

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
