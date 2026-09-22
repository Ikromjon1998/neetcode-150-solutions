#!/usr/bin/env python3
"""Render a spoiler-free problem statement for each contract.

    make statements

Two jobs, both driven by the contracts:

1. `docs/problems/NNNN-slug.md` — one exercise brief per problem, written from scratch.
2. The generated block inside each `docs/topics/NN-<topic>.md` — the list of problems in that
   topic. The prose around it is hand-written and never touched. These
are the exercise briefs: what to build, where to build it, what it must cost, and how to check
it. They deliberately contain **no implementation** — the worked answers and the cross-language
write-up live under `solutions/`, one explicit click away.

Regenerated wholesale every run, so never hand-edit a file in `docs/problems/`. Anything you
want to say about a problem belongs in its contract (which every language reads) or in its
notes under `solutions/notes/`.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTRACTS = ROOT / "packages/contracts/problems"
OUT = ROOT / "docs/problems"
TOPICS_DIR = ROOT / "docs/topics"

# The eighteen NeetCode topics in roadmap order; the index is the file-name prefix.
TOPIC_ORDER = [
    "arrays-and-hashing", "two-pointers", "sliding-window", "stack", "binary-search",
    "linked-list", "trees", "tries", "heap-priority-queue", "backtracking", "graphs",
    "advanced-graphs", "1d-dynamic-programming", "2d-dynamic-programming", "greedy",
    "intervals", "math-and-geometry", "bit-manipulation",
]
DIFFICULTY_ORDER = {"easy": 0, "medium": 1, "hard": 2}

BEGIN = "<!-- generated:problems -->"
END = "<!-- /generated:problems -->"


def topic_doc(topic: str) -> Path:
    """`arrays-and-hashing` -> docs/topics/01-arrays-and-hashing.md"""
    return TOPICS_DIR / f"{TOPIC_ORDER.index(topic) + 1:02d}-{topic}.md"

DIFFICULTY_BADGE = {"easy": "🟢 easy", "medium": "🟡 medium", "hard": "🔴 hard"}


def snake(slug: str) -> str:
    text = slug.replace("-", "_")
    leading = {"0": "zero", "1": "one", "2": "two", "3": "three", "4": "four",
               "5": "five", "6": "six", "7": "seven", "8": "eight", "9": "nine"}
    if text[0].isdigit():
        text = leading[text[0]] + text[1:]
    return text


def pascal(slug: str) -> str:
    return "".join(part.capitalize() for part in snake(slug).split("_"))


def topic_pascal(topic: str) -> str:
    return "".join(part.capitalize() for part in topic.replace("-", "_").split("_"))


def render(data: dict) -> str:
    slug, pid = data["slug"], data["id"]
    topic = data["topic"]
    approaches = data["approaches"]
    default = next((a["key"] for a in approaches if a.get("default")), approaches[0]["key"])

    links = [f"[LeetCode]({data['leetcodeUrl']})"] if data.get("leetcodeUrl") else []
    if data.get("neetcodeUrl"):
        links.append(f"[NeetCode]({data['neetcodeUrl']})")

    lines = [
        f"# {pid}. {data['title']}",
        "",
        f"{DIFFICULTY_BADGE.get(data['difficulty'], data['difficulty'])} · "
        f"**{topic}** · {len(approaches)} approaches to implement"
        + (f" · {' · '.join(links)}" if links else ""),
        "",
        "## The problem",
        "",
        data["summary"],
        "",
        "## Examples",
        "",
        "Straight from the contract, which is what the tests read:",
        "",
        "```json",
    ]
    for case in data["cases"][:3]:
        lines.append(
            f'// {case["name"]}\n'
            f'{json.dumps(case["input"], ensure_ascii=False)}  ->  '
            f'{json.dumps(case["expected"], ensure_ascii=False)}'
        )
    lines += [
        "```",
        "",
        f"The full set — {len(data['cases'])} cases, "
        f"{len(data.get('validationCases', []))} invalid-input cases"
        + (f", {len(data['notFoundCases'])} with no answer" if data.get("notFoundCases") else "")
        + f" — is in [`{pid:04d}-{slug}.json`](../../packages/contracts/problems/{pid:04d}-{slug}.json).",
        "",
        *([
            f"> **New to {topic.replace('-', ' ')}?** Read the topic guide first: "
            f"[`{topic_doc(topic).name}`](../topics/{topic_doc(topic).name}). It covers the "
            "data structures you will need in all three languages — no problem answers in it.",
            "",
        ] if topic_doc(topic).exists() else []),
        "## What to implement",
        "",
        "| approach | must run in | using | what it is |",
        "|---|---|---|---|",
    ]
    for a in approaches:
        marker = " *(default)*" if a["key"] == default else ""
        note = (a.get("note") or "").replace("|", "\\|")
        lines.append(f"| `{a['key']}`{marker} | {a['time']} | {a['space']} space | {note} |")

    lines += [
        "",
        "The **default** approach is the one used when `?approach=` is omitted.",
        "",
        "### Where",
        "",
        "Three files, one per language. Each holds a stub per approach; replace the `raise` /",
        "`throw` with your own code and leave everything else alone.",
        "",
        "```",
        f"packages/core-python/src/neetcode_core/{snake(topic)}/{snake(slug)}.py",
        f"packages/core-ts/src/{topic}/{slug}.ts",
        f"packages/core-php/src/{topic_pascal(topic)}/{pascal(slug)}.php",
        "```",
        "",
        "Write each one **idiomatically for its language**. If all three end up reading the same,",
        "you have translated rather than learned — and the whole point of this repo is the",
        "difference between the three.",
        "",
        "## Check your work",
        "",
        "```bash",
        f"make try SLUG={slug}          # just this problem, all three languages",
        f"make try SLUG={slug} LANG=python   # just one language",
        "```",
        "",
        "That is the loop. `make test` runs all six suites for every problem when you want it.",
        "",
        "Every test is driven by the contract above, so the same cases run in all three languages.",
        "There is also a differential test asserting that your approaches agree with each other —",
        "which is why implementing the naive one first is worth the ten minutes.",
        "",
        "Once it passes, the endpoint works in all three apps:",
        "",
        "```bash",
        "make run-python       # :8000   (also run-node :3000, run-php :8080)",
        "",
        f"curl -s 'localhost:8000/problems/{slug}?approach={default}' \\",
        "  -H 'content-type: application/json' \\",
        f"  -d '{json.dumps(data['cases'][0]['input'], ensure_ascii=False)}'",
        "```",
        "",
        "## Stuck?",
        "",
        "```bash",
        f"make show SLUG={slug}              # prints a worked answer, touches nothing",
        f"make solution SLUG={slug}          # writes it over your stub (make restore undoes it)",
        "```",
        "",
        f"There is also a full cross-language write-up — what differed between the three languages",
        f"and the three frameworks, and what went wrong — in",
        f"[`solutions/notes/{pid:04d}-{slug}.md`](../../solutions/notes/{pid:04d}-{slug}.md).",
        "**It contains the answers.** Read it after you have solved this, not before.",
        "",
        "---",
        "",
        "*Generated from the contract by `make statements`. Do not edit by hand.*",
    ]
    return "\n".join(lines) + "\n"


def render_topic_block(topic: str, problems: list[dict]) -> str:
    """The table of problems in one topic. Easiest first, so there is an obvious starting point."""
    ordered = sorted(problems, key=lambda d: (DIFFICULTY_ORDER.get(d["difficulty"], 9), d["id"]))
    lines = [
        f"*{len(ordered)} exercise(s) in this topic, easiest first. "
        "Generated from the contracts — do not edit by hand.*",
        "",
        "| # | problem | difficulty | approaches to implement |",
        "|---|---------|------------|-------------------------|",
    ]
    for data in ordered:
        name = f"[{data['title']}](../problems/{data['id']:04d}-{data['slug']}.md)"
        approaches = ", ".join(f"`{a['key']}`" for a in data["approaches"])
        lines.append(f"| {data['id']} | {name} | {data['difficulty']} | {approaches} |")
    return "\n".join(lines)


def update_topic_docs(by_topic: dict[str, list[dict]]) -> int:
    """Refresh the generated block in every topic doc that has one. Prose is left alone."""
    updated = 0
    for topic, problems in by_topic.items():
        path = topic_doc(topic)
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        if BEGIN not in text or END not in text:
            print(f"  ! {path.relative_to(ROOT)} has no {BEGIN} block — skipped")
            continue
        head, rest = text.split(BEGIN, 1)
        _, tail = rest.split(END, 1)
        rebuilt = f"{head}{BEGIN}\n{render_topic_block(topic, problems)}\n{END}{tail}"
        if rebuilt != text:
            path.write_text(rebuilt, encoding="utf-8")
            print(f"  ~ {path.relative_to(ROOT)}")
            updated += 1
    return updated


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    written = 0
    by_topic: dict[str, list[dict]] = {}
    for path in sorted(CONTRACTS.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        target = OUT / f"{data['id']:04d}-{data['slug']}.md"
        target.write_text(render(data), encoding="utf-8")
        print(f"  + {target.relative_to(ROOT)}")
        written += 1
        by_topic.setdefault(data["topic"], []).append(data)

    refreshed = update_topic_docs(by_topic)
    print(f"\n{written} statement(s) rendered, {refreshed} topic guide(s) refreshed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
