#!/usr/bin/env python3
"""Check every contract file, and check that the three languages actually honour it.

    make test-contracts

Deliberately dependency-free. It does two jobs:

1. **Schema-shaped validation** of each `packages/contracts/problems/*.json` — required keys,
   enum values, slug format, exactly-one-default, filename matching id and slug.
2. **Cross-language agreement** — every approach declared in a contract must be implemented in
   the Python, TypeScript *and* PHP core packages. A contract that only one language honours
   is the failure mode this repo exists to prevent, and neither a JSON schema nor any single
   language's test suite can catch it.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTRACTS = ROOT / "packages/contracts/problems"

TOPICS = {
    "arrays-and-hashing", "two-pointers", "sliding-window", "stack", "binary-search",
    "linked-list", "trees", "tries", "heap-priority-queue", "backtracking", "graphs",
    "advanced-graphs", "1d-dynamic-programming", "2d-dynamic-programming", "greedy",
    "intervals", "math-and-geometry", "bit-manipulation",
}
DIFFICULTIES = {"easy", "medium", "hard"}
KEBAB = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")

errors: list[str] = []


def fail(contract: str, message: str) -> None:
    errors.append(f"{contract}: {message}")


def check_shape(path: Path, data: dict) -> None:
    name = path.name

    for key in ("id", "slug", "title", "difficulty", "topic", "summary", "approaches", "cases"):
        if key not in data:
            fail(name, f"missing required key {key!r}")
            return

    slug = data["slug"]
    if not KEBAB.match(slug):
        fail(name, f"slug {slug!r} is not kebab-case")
    expected_name = f"{data['id']:04d}-{slug}.json"
    if name != expected_name:
        fail(name, f"filename should be {expected_name} (from id {data['id']} and slug {slug!r})")
    if data["difficulty"] not in DIFFICULTIES:
        fail(name, f"difficulty {data['difficulty']!r} is not one of {sorted(DIFFICULTIES)}")
    if data["topic"] not in TOPICS:
        fail(name, f"topic {data['topic']!r} is not a NeetCode 150 topic")
    if "TODO" in data["summary"]:
        fail(name, "summary still says TODO")

    approaches = data["approaches"]
    if not approaches:
        fail(name, "must declare at least one approach")
        return

    keys = [a["key"] for a in approaches]
    if len(keys) != len(set(keys)):
        fail(name, f"duplicate approach keys: {keys}")
    for approach in approaches:
        if not KEBAB.match(approach["key"]):
            fail(name, f"approach key {approach['key']!r} is not kebab-case")
        for field in ("name", "time", "space"):
            if not approach.get(field):
                fail(name, f"approach {approach['key']!r} is missing {field!r}")
        if approach.get("time") == "O(?)" or approach.get("space") == "O(?)":
            fail(name, f"approach {approach['key']!r} still has a placeholder complexity")

    defaults = [a["key"] for a in approaches if a.get("default")]
    if len(defaults) != 1:
        fail(name, f"exactly one approach must be the default, found {len(defaults)}: {defaults}")

    if not data["cases"]:
        fail(name, "must declare at least one case")
    for case in data["cases"]:
        if "TODO" in case["name"]:
            fail(name, f"case {case['name']!r} was never renamed")
        for field in ("name", "input", "expected"):
            if field not in case:
                fail(name, f"case {case.get('name', '?')!r} is missing {field!r}")

    for case in data.get("validationCases", []):
        if not 400 <= case.get("status", 0) <= 599:
            fail(name, f"validation case {case['name']!r} needs a 4xx/5xx status")


def implemented_approaches(slug: str) -> dict[str, set[str]]:
    """Scrape each language's problem file for the approach keys it registers."""
    found: dict[str, set[str]] = {"python": set(), "typescript": set(), "php": set()}

    for path in (ROOT / "packages/core-python/src/neetcode_core").rglob("*.py"):
        text = path.read_text(encoding="utf-8")
        if f'SLUG = "{slug}"' in text:
            found["python"] = set(re.findall(r'@solution\(SLUG, approach="([^"]+)"\)', text))

    for path in (ROOT / "packages/core-ts/src").rglob("*.ts"):
        text = path.read_text(encoding="utf-8")
        if f'export const SLUG = "{slug}"' in text:
            block = text.split("defineProblem(SLUG,", 1)
            if len(block) == 2:
                found["typescript"] = set(re.findall(r'["\']?([a-z0-9-]+)["\']?\s*:', block[1]))

    for path in (ROOT / "packages/core-php/src").rglob("*.php"):
        text = path.read_text(encoding="utf-8")
        if f"SLUG = '{slug}'" in text:
            found["php"] = set(re.findall(r"'([a-z0-9-]+)'\s*=>\s*self::", text))

    return found


def check_implementations(path: Path, data: dict) -> None:
    slug = data["slug"]
    declared = {a["key"] for a in data["approaches"]}
    found = implemented_approaches(slug)

    for language, keys in found.items():
        if not keys:
            fail(path.name, f"no {language} implementation found for slug {slug!r}")
            continue
        if missing := declared - keys:
            fail(path.name, f"{language} does not implement: {sorted(missing)}")
        if extra := keys - declared:
            fail(path.name, f"{language} implements undeclared approaches: {sorted(extra)}")


def main() -> int:
    files = sorted(CONTRACTS.glob("*.json"))
    if not files:
        print(f"No contracts found in {CONTRACTS}", file=sys.stderr)
        return 1

    seen_slugs: dict[str, str] = {}
    seen_ids: dict[int, str] = {}

    for path in files:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            fail(path.name, f"invalid JSON: {exc}")
            continue

        check_shape(path, data)
        if "slug" not in data or "id" not in data:
            continue

        if data["slug"] in seen_slugs:
            fail(path.name, f"slug {data['slug']!r} also used by {seen_slugs[data['slug']]}")
        seen_slugs[data["slug"]] = path.name

        if data["id"] in seen_ids:
            fail(path.name, f"id {data['id']} also used by {seen_ids[data['id']]}")
        seen_ids[data["id"]] = path.name

        check_implementations(path, data)

    if errors:
        print(f"{len(errors)} problem(s) found:\n", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        return 1

    print(f"{len(files)} contract(s) valid, and implemented in all three languages.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
