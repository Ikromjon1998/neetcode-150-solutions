#!/usr/bin/env python3
"""Run the tests for every problem you have solved — and only those.

    make test-solved

`make test` runs every problem, so in a solutions repo it stays red until all 150 are done.
This runs the core suites for each (problem, language) pair whose live file is no longer a
stub, so green means "everything I have solved so far is correct".

It is what CI runs in a solutions repo. A problem counts as solved in a language only when
every approach in that file is implemented — the same rule `make status` uses.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

from solutions import is_stub, load_problems, php_filter  # noqa: E402

VENV = ROOT / ".venv/bin"
PYTEST = str(VENV / "pytest") if (VENV / "pytest").exists() else "pytest"


def run(cmd: list[str], cwd: Path) -> tuple[int, str]:
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    return result.returncode, result.stdout + result.stderr


def main() -> int:
    problems = load_problems()
    solved = {
        language: [p for p in problems if p.live(language).exists() and not is_stub(p.live(language))]
        for language in ("python", "typescript", "php")
    }

    total = sum(len(items) for items in solved.values())
    if total == 0:
        print("Nothing solved yet — nothing to test. Pick a problem: make status")
        return 0

    commands = {
        "python": ([PYTEST, "-p", "no:warnings", *[p.test_python for p in solved["python"]]],
                   ROOT / "packages/core-python", r"(\d+ (?:failed|passed)[^\n]*)"),
        "typescript": (["npx", "vitest", "run", "--root", "packages/core-ts",
                        *[p.test_typescript for p in solved["typescript"]]],
                       ROOT, r"Tests\s+(.*?)\n"),
        "php": (["./vendor/bin/phpunit", "--filter",
                 php_filter([p.test_php_class for p in solved["php"]])],
                ROOT / "packages/core-php", r"(Tests: .*|OK \(.*\))"),
    }

    print(f"\nTesting {total} solved implementation(s)\n")
    failed = False
    for language, items in solved.items():
        if not items:
            print(f"  {language:<11} —     nothing solved yet")
            continue
        cmd, cwd, pattern = commands[language]
        code, output = run(cmd, cwd)
        match = re.search(pattern, output)
        summary = match.group(1).strip() if match else "(could not parse result)"
        mark = "pass" if code == 0 else "FAIL"
        print(f"  {language:<11} {mark}  {len(items):>3} problem(s)  {summary}")
        if code != 0:
            failed = True
            print(output[-3000:])

    print()
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
