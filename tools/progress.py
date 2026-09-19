#!/usr/bin/env python3
"""Print your progress through the NeetCode 150.

    make progress

Counts two different things, and the difference matters:

* **available** — exercises that exist in this repo (a contract, stubs in three languages,
  tests, and a rendered brief). Out of the 150.
* **solved** — how many of those you have actually implemented, per language. A file still
  raising `UnsolvedError` counts as unsolved no matter how much is written around it.

Reads `packages/contracts/problems/*.json` and inspects the live source files, so it cannot
drift from reality.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

from solutions import LANGUAGES, is_stub, load_problems  # noqa: E402

CONTRACTS = ROOT / "packages/contracts/problems"

# Topic -> (display name, how many the NeetCode 150 roadmap contains)
TOPICS: dict[str, tuple[str, int]] = {
    "arrays-and-hashing": ("Arrays & Hashing", 9),
    "two-pointers": ("Two Pointers", 5),
    "sliding-window": ("Sliding Window", 6),
    "stack": ("Stack", 7),
    "binary-search": ("Binary Search", 7),
    "linked-list": ("Linked List", 11),
    "trees": ("Trees", 15),
    "tries": ("Tries", 3),
    "heap-priority-queue": ("Heap / Priority Queue", 7),
    "backtracking": ("Backtracking", 9),
    "graphs": ("Graphs", 13),
    "advanced-graphs": ("Advanced Graphs", 6),
    "1d-dynamic-programming": ("1-D Dynamic Programming", 12),
    "2d-dynamic-programming": ("2-D Dynamic Programming", 11),
    "greedy": ("Greedy", 8),
    "intervals": ("Intervals", 6),
    "math-and-geometry": ("Math & Geometry", 8),
    "bit-manipulation": ("Bit Manipulation", 7),
}


def main() -> int:
    problems = load_problems()
    by_topic: dict[str, list] = {topic: [] for topic in TOPICS}
    for problem in problems:
        by_topic.setdefault(problem.topic, []).append(problem)

    available = len(problems)
    total = sum(count for _, count in TOPICS.values())

    solved_all = sum(
        1 for p in problems
        if all(not is_stub(p.live(language)) for language in LANGUAGES)
    )
    solved_any = sum(
        1 for p in problems
        if any(not is_stub(p.live(language)) for language in LANGUAGES)
    )

    print(f"\n  Exercises available   {available:>3} / {total}  of the NeetCode 150")
    print(f"  Solved in all three   {solved_all:>3} / {available}")
    print(f"  Started               {solved_any:>3} / {available}\n")

    print("| # | Topic | Exercises | Solved (py/ts/php) |")
    print("|---|-------|-----------|--------------------|")
    for index, (topic, (label, count)) in enumerate(TOPICS.items(), start=1):
        items = sorted(by_topic.get(topic, []), key=lambda p: p.id)
        per_lang = [
            sum(1 for p in items if not is_stub(p.live(language)))
            for language in LANGUAGES
        ]
        bar = "#" * len(items) + "." * max(0, count - len(items))
        solved = "/".join(str(n) for n in per_lang) if items else "—"
        print(f"| {index:02d} | {label} | {len(items)} / {count} `{bar}` | {solved} |")

    todo = [
        f"{p.id:04d}-{p.slug}"
        for p in problems
        if any(is_stub(p.live(language)) for language in LANGUAGES)
    ]
    if todo:
        print(f"\nStill unsolved ({len(todo)}):")
        for name in todo:
            print(f"  - docs/problems/{name}.md")
    else:
        print("\nEverything available is solved in all three languages. Add more:")
        print("  make new-problem ARGS=\"--id ... --slug ...\"")
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
