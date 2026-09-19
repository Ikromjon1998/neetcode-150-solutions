#!/usr/bin/env python3
"""Manage the split between exercises and reference solutions.

This repository ships **problems, not answers**. Every algorithm in `packages/core-*` is a stub
that raises `UnsolvedError`; the worked answers live under `solutions/` and are applied only
deliberately.

    make status                     which problems are solved, per language
    make show SLUG=two-sum          print the reference answer without touching any file
    make solution SLUG=two-sum      copy the reference over your stub (destructive)
    make extract SLUG=two-sum       the reverse: move YOUR implementation into solutions/
                                    and leave a stub behind. Used when authoring a new exercise.
    make stubs [SLUG=two-sum]       regenerate stub hints after a contract edit. Never touches
                                    solutions/, never overwrites a solved file.
    make restore                    undo `make solution` — put your own files back
    make verify-solutions           apply every reference, run the full suite, prove they pass

Layout mirrored by all three languages:

    packages/core-python/src/neetcode_core/<topic_snake>/<slug_snake>.py   <- stub (live)
    solutions/python/<topic_snake>/<slug_snake>.py                         <- reference

A file under `solutions/` is a byte-for-byte copy of what belongs at the live path. It is an
overlay, not a standalone package: its imports are written for the live location, so it only
compiles once applied.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTRACTS = ROOT / "packages/contracts/problems"
SOLUTIONS = ROOT / "solutions"

# `apply` stashes whatever it overwrites here, so a mis-typed `make solution` never costs you
# work. Deliberately not git-tracked, and deliberately not reliant on git: a learner may not
# have committed, and `git checkout --` would then restore something older than their stub.
BACKUP = ROOT / ".neetcode-backup"

LANGUAGES = ("python", "typescript", "php")


# --------------------------------------------------------------------------------------
# Naming (kept identical to tools/new_problem.py)
# --------------------------------------------------------------------------------------

def snake(slug: str) -> str:
    text = slug.replace("-", "_")
    leading = {"0": "zero", "1": "one", "2": "two", "3": "three", "4": "four",
               "5": "five", "6": "six", "7": "seven", "8": "eight", "9": "nine"}
    if text[0].isdigit():
        text = leading[text[0]] + text[1:]
    return text


def pascal(slug: str) -> str:
    return "".join(part.capitalize() for part in snake(slug).split("_"))


def topic_php(topic: str) -> str:
    return "".join(part.capitalize() for part in topic.replace("-", "_").split("_"))


# --------------------------------------------------------------------------------------
# Problem model
# --------------------------------------------------------------------------------------

@dataclass(frozen=True)
class Approach:
    key: str
    name: str
    time: str
    space: str
    note: str | None


@dataclass(frozen=True)
class Problem:
    id: int
    slug: str
    title: str
    topic: str
    summary: str
    leetcode_url: str | None
    approaches: tuple[Approach, ...]

    # ---- live (exercise) paths
    @property
    def live_python(self) -> Path:
        return ROOT / "packages/core-python/src/neetcode_core" / snake(self.topic) / f"{snake(self.slug)}.py"

    @property
    def live_typescript(self) -> Path:
        return ROOT / "packages/core-ts/src" / self.topic / f"{self.slug}.ts"

    @property
    def live_php(self) -> Path:
        return ROOT / "packages/core-php/src" / topic_php(self.topic) / f"{pascal(self.slug)}.php"

    def live(self, language: str) -> Path:
        return {"python": self.live_python, "typescript": self.live_typescript,
                "php": self.live_php}[language]

    # ---- reference paths
    def reference(self, language: str) -> Path:
        return SOLUTIONS / language / self.live(language).relative_to(
            {"python": ROOT / "packages/core-python/src/neetcode_core",
             "typescript": ROOT / "packages/core-ts/src",
             "php": ROOT / "packages/core-php/src"}[language]
        )

    @property
    def notes(self) -> Path:
        return SOLUTIONS / "notes" / f"{self.id:04d}-{self.slug}.md"

    # ---- test selectors
    #
    # Every selector matches ONE problem exactly. Prefix or substring matching looks fine
    # until the NeetCode pairs arrive — two-sum / two-sum-ii, house-robber / house-robber-ii,
    # word-search / word-search-ii, jump-game / jump-game-ii — and then `make try two-sum`
    # silently runs another problem's tests too, usually an unsolved one.

    @property
    def test_python(self) -> str:
        """Test file path, relative to packages/core-python. An explicit path cannot over-match."""
        return f"tests/{snake(self.topic)}/test_{snake(self.slug)}.py"

    @property
    def test_typescript(self) -> str:
        """Vitest filter. Vitest matches by path substring, so include the `.test.ts` suffix:
        `two-sum.test.ts` is not a substring of `two-sum-ii-….test.ts`."""
        return f"{self.topic}/{self.slug}.test.ts"

    @property
    def test_php_class(self) -> str:
        """Test class name. Wrap in `php_filter()` before passing to --filter."""
        return f"{pascal(self.slug)}Test"


def php_filter(classes: list[str]) -> str:
    r"""PHPUnit --filter matching exactly these test classes.

    PHPUnit matches the filter as a regex against `Namespace\ClassTest::method`. A bare
    `SumTest::` would also match `TwoSumTest::`, so anchor on the namespace separator:
    `\(TwoSumTest|ValidAnagramTest)::`.
    """
    return "\\\\(" + "|".join(classes) + ")::"


def load_problems() -> list[Problem]:
    problems = []
    for path in sorted(CONTRACTS.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        problems.append(Problem(
            id=data["id"], slug=data["slug"], title=data["title"], topic=data["topic"],
            summary=data["summary"], leetcode_url=data.get("leetcodeUrl"),
            approaches=tuple(
                Approach(a["key"], a["name"], a["time"], a["space"], a.get("note"))
                for a in data["approaches"]
            ),
        ))
    return problems


def find(slug: str) -> Problem:
    for problem in load_problems():
        if problem.slug == slug:
            return problem
    sys.exit(f"No contract for slug {slug!r}. Known: {', '.join(p.slug for p in load_problems())}")


# --------------------------------------------------------------------------------------
# Signature extraction — read a working implementation, keep only its shape
# --------------------------------------------------------------------------------------

@dataclass(frozen=True)
class Signature:
    """One approach's callable shape, lifted out of a reference implementation."""

    approach: str
    name: str
    params: str
    returns: str


def signatures_python(source: str) -> list[Signature]:
    pattern = re.compile(
        r'@solution\(SLUG,\s*approach="(?P<key>[^"]+)"\)\s*\n'
        r"def\s+(?P<name>\w+)\((?P<params>.*?)\)\s*->\s*(?P<returns>[^:]+):",
        re.DOTALL,
    )
    return [
        Signature(m["key"], m["name"], " ".join(m["params"].split()), m["returns"].strip())
        for m in pattern.finditer(source)
    ]


def signatures_typescript(source: str) -> list[Signature]:
    block = re.search(r"defineProblem\(SLUG,\s*\{(?P<body>.*?)\}\)", source, re.DOTALL)
    if not block:
        sys.exit("could not find defineProblem(SLUG, { ... }) — is this a solution file?")

    mapping = re.findall(r'["\']?([a-z0-9-]+)["\']?\s*:\s*(\w+)', block["body"])
    found = []
    for key, fn in mapping:
        sig = re.search(
            rf"export function {fn}\((?P<params>.*?)\):\s*(?P<returns>[^{{]+)\{{",
            source, re.DOTALL,
        )
        if not sig:
            sys.exit(f"could not find `export function {fn}` in the solution file")
        found.append(
            Signature(key, fn, " ".join(sig["params"].split()), sig["returns"].strip())
        )
    return found


def signatures_php(source: str) -> list[Signature]:
    block = re.search(r"function solutions\(\): array\s*\{(?P<body>.*?)\n    \}", source, re.DOTALL)
    if not block:
        sys.exit("could not find solutions(): array — is this a solution file?")

    mapping = re.findall(r"'([a-z0-9-]+)'\s*=>\s*self::(\w+)\(\.\.\.\)", block["body"])
    found = []
    for key, method in mapping:
        sig = re.search(
            rf"public static function {method}\((?P<params>.*?)\):\s*(?P<returns>\S+)\s*\n",
            source, re.DOTALL,
        )
        if not sig:
            sys.exit(f"could not find `public static function {method}` in the solution file")
        found.append(
            Signature(key, method, " ".join(sig["params"].split()), sig["returns"].strip())
        )
    return found


EXTRACTORS = {
    "python": signatures_python,
    "typescript": signatures_typescript,
    "php": signatures_php,
}


# --------------------------------------------------------------------------------------
# Stub rendering — the exercise a learner sees
# --------------------------------------------------------------------------------------

def _hint(approach: Approach) -> list[str]:
    """The specification of one approach, drawn entirely from the contract.

    Enough to know *what* to build and what it must cost; never how to build it.
    """
    lines = [f"{approach.name} — target: {approach.time} time, {approach.space} space."]
    if approach.note:
        lines += ["", approach.note]
    return lines


def _wrap(text: str, width: int, indent: str) -> list[str]:
    words, line, out = text.split(), "", []
    for word in words:
        candidate = f"{line} {word}".strip()
        if len(indent) + len(candidate) > width:
            out.append(indent + line)
            line = word
        else:
            line = candidate
    if line:
        out.append(indent + line)
    return out


def stub_python(problem: Problem, sigs: list[Signature], rel: str) -> str:
    by_key = {a.key: a for a in problem.approaches}
    out = [
        f'"""{problem.id}. {problem.title}',
        "",
        *_wrap(problem.summary, 98, ""),
        "",
        f"    {problem.leetcode_url}" if problem.leetcode_url else "",
        "",
        "Each function below is an exercise. Replace the `raise` with your implementation, then:",
        "",
        "    make test-python",
        "",
        f"Stuck? `make show SLUG={problem.slug}` prints a worked answer.",
        '"""',
        "",
        "from __future__ import annotations",
        "",
        "from neetcode_core.errors import UnsolvedError",
        "from neetcode_core.registry import solution",
        "",
        f'SLUG = "{problem.slug}"',
        f'PATH = "{rel}"',
    ]
    for sig in sigs:
        approach = by_key[sig.approach]
        out += [
            "",
            "",
            f'@solution(SLUG, approach="{sig.approach}")',
            f"def {sig.name}({sig.params}) -> {sig.returns}:",
            f'    """{_hint(approach)[0]}',
        ]
        if approach.note:
            out += [""] + _wrap(approach.note, 98, "    ")
        out += [
            '    """',
            f'    raise UnsolvedError(SLUG, "{sig.approach}", PATH)',
        ]
    return "\n".join(line for line in out if line is not None) + "\n"


def stub_typescript(problem: Problem, sigs: list[Signature], rel: str) -> str:
    by_key = {a.key: a for a in problem.approaches}
    out = [
        "/**",
        f" * {problem.id}. {problem.title}",
        " *",
        *[f" * {line}" for line in _wrap(problem.summary, 96, "")],
        " *",
        f" * {problem.leetcode_url}" if problem.leetcode_url else " *",
        " *",
        " * Each function below is an exercise. Replace the `throw` with your implementation,",
        " * then run `make test-node`.",
        " *",
        f" * Stuck? `make show SLUG={problem.slug}` prints a worked answer.",
        " */",
        "",
        'import { defineProblem } from "../define-problem";',
        'import { UnsolvedError } from "../errors";',
        "",
        f'export const SLUG = "{problem.slug}";',
        f'const PATH = "{rel}";',
    ]
    for sig in sigs:
        approach = by_key[sig.approach]
        out += ["", "/**", f" * {_hint(approach)[0]}"]
        if approach.note:
            out += [" *"] + [f" * {line}" for line in _wrap(approach.note, 96, "")]
        out += [
            " */",
            f"export function {sig.name}({sig.params}): {sig.returns} {{",
            f'  throw new UnsolvedError(SLUG, "{sig.approach}", PATH);',
            "}",
        ]
    out += ["", f"export const {problem_camel(problem.slug)} = defineProblem(SLUG, {{"]
    for sig in sigs:
        key = sig.approach if re.fullmatch(r"[a-z][a-zA-Z0-9]*", sig.approach) else f'"{sig.approach}"'
        out.append(f"  {key}: {sig.name},")
    out += ["});", ""]
    return "\n".join(out)


def problem_camel(slug: str) -> str:
    head, *rest = snake(slug).split("_")
    return head + "".join(part.capitalize() for part in rest)


def stub_php(problem: Problem, sigs: list[Signature], rel: str) -> str:
    cls = pascal(problem.slug)
    by_key = {a.key: a for a in problem.approaches}
    out = [
        "<?php",
        "",
        "declare(strict_types=1);",
        "",
        f"namespace NeetCode\\Core\\{topic_php(problem.topic)};",
        "",
        "use NeetCode\\Core\\Contracts\\ProblemDefinition;",
        "use NeetCode\\Core\\Exceptions\\UnsolvedException;",
        "",
        "/**",
        f" * {problem.id}. {problem.title}",
        " *",
        *[f" * {line}" for line in _wrap(problem.summary, 96, "")],
        " *",
        f" * {problem.leetcode_url}" if problem.leetcode_url else " *",
        " *",
        " * Each method below is an exercise. Replace the `throw` with your implementation, then",
        " * run `make test-php`.",
        " *",
        f" * Stuck? `make show SLUG={problem.slug}` prints a worked answer.",
        " */",
        f"final class {cls} implements ProblemDefinition",
        "{",
        f"    public const SLUG = '{problem.slug}';",
        "",
        f"    private const PATH = '{rel}';",
        "",
        "    public static function slug(): string",
        "    {",
        "        return self::SLUG;",
        "    }",
        "",
        "    /** @return array<string, callable> */",
        "    public static function solutions(): array",
        "    {",
        "        return [",
    ]
    for sig in sigs:
        out.append(f"            '{sig.approach}' => self::{sig.name}(...),")
    out += ["        ];", "    }"]

    for sig in sigs:
        approach = by_key[sig.approach]
        out += ["", "    /**", f"     * {_hint(approach)[0]}"]
        if approach.note:
            out += ["     *"] + [f"     * {line}" for line in _wrap(approach.note, 92, "")]
        out += [
            "     */",
            f"    public static function {sig.name}({sig.params}): {sig.returns}",
            "    {",
            f"        throw new UnsolvedException(self::SLUG, '{sig.approach}', self::PATH);",
            "    }",
        ]
    out += ["}", ""]
    return "\n".join(out)


RENDERERS = {"python": stub_python, "typescript": stub_typescript, "php": stub_php}


# --------------------------------------------------------------------------------------
# Commands
# --------------------------------------------------------------------------------------

STUB_MARKERS = ("UnsolvedError", "UnsolvedException")


def is_stub(path: Path) -> bool:
    if not path.exists():
        return False
    return any(marker in path.read_text(encoding="utf-8") for marker in STUB_MARKERS)


def cmd_extract(problems: list[Problem], languages: tuple[str, ...], force: bool) -> int:
    """Move a working implementation into solutions/ and leave a stub in its place.

    The authoring direction: solve it where it runs, then turn it into an exercise.
    """
    for problem in problems:
        for language in languages:
            live = problem.live(language)
            if not live.exists():
                print(f"  ! {problem.slug} [{language}] no live file at {live.relative_to(ROOT)}")
                continue
            # A stub is never extracted, not even with --force. Extracting copies the live file
            # into solutions/, so extracting a stub would overwrite the worked answer with the
            # empty exercise and destroy it. To refresh a stub's docstring after a contract
            # change, use `restub`, which reads the reference and never writes to it.
            if is_stub(live):
                print(f"  = {problem.slug} [{language}] already a stub, skipped "
                      f"(use `restub` to refresh its hint)")
                continue

            source = live.read_text(encoding="utf-8")
            sigs = EXTRACTORS[language](source)
            if not sigs:
                print(f"  ! {problem.slug} [{language}] no registered approaches found")
                continue

            reference = problem.reference(language)
            reference.parent.mkdir(parents=True, exist_ok=True)
            reference.write_text(source, encoding="utf-8")

            rel = str(live.relative_to(ROOT))
            live.write_text(RENDERERS[language](problem, sigs, rel), encoding="utf-8")
            print(f"  + {problem.slug} [{language}] -> {reference.relative_to(ROOT)}, stub written")
    return 0


def cmd_restub(problems: list[Problem], languages: tuple[str, ...]) -> int:
    """Regenerate stubs from the contract, reading signatures from the reference answer.

    Use it after editing an approach's `name`, `time`, `space` or `note` in a contract, so the
    stub's docstring hint matches. Two guarantees:

    * it never writes to `solutions/` — the reference is read, not touched;
    * it never overwrites a solved file — only live files that are still stubs are rewritten,
      so running it on a learner's branch cannot destroy their work.
    """
    for problem in problems:
        for language in languages:
            live, reference = problem.live(language), problem.reference(language)
            if not reference.exists():
                print(f"  ! {problem.slug} [{language}] no reference to read signatures from")
                continue
            if live.exists() and not is_stub(live):
                print(f"  = {problem.slug} [{language}] solved — left alone")
                continue

            sigs = EXTRACTORS[language](reference.read_text(encoding="utf-8"))
            rendered = RENDERERS[language](problem, sigs, str(live.relative_to(ROOT)))
            if live.exists() and live.read_text(encoding="utf-8") == rendered:
                continue
            live.write_text(rendered, encoding="utf-8")
            print(f"  + {problem.slug} [{language}] stub regenerated")
    return 0


def cmd_apply(problems: list[Problem], languages: tuple[str, ...], force: bool) -> int:
    """Copy the reference answer over the live file. Destructive — it overwrites your work."""
    for problem in problems:
        for language in languages:
            reference, live = problem.reference(language), problem.live(language)
            if not reference.exists():
                print(f"  ! {problem.slug} [{language}] no reference solution")
                continue
            if not is_stub(live) and not force:
                print(f"  = {problem.slug} [{language}] already solved — pass --force to overwrite")
                continue

            backup = BACKUP / live.relative_to(ROOT)
            backup.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(live, backup)

            shutil.copyfile(reference, live)
            print(f"  + {problem.slug} [{language}] reference applied to {live.relative_to(ROOT)}")

    print(f"\nWhatever was overwritten is saved under {BACKUP.name}/."
          f"\nPut it back with:  make restore")
    return 0


def cmd_restore() -> int:
    """Undo `apply`: put back whatever it overwrote."""
    if not BACKUP.exists():
        print(f"Nothing to restore — {BACKUP.name}/ does not exist.")
        return 0

    restored = 0
    for backup in sorted(BACKUP.rglob("*")):
        if backup.is_dir():
            continue
        live = ROOT / backup.relative_to(BACKUP)
        live.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(backup, live)
        print(f"  + {live.relative_to(ROOT)}")
        restored += 1

    shutil.rmtree(BACKUP)
    print(f"\n{restored} file(s) restored; {BACKUP.name}/ removed.")
    return 0


def cmd_show(problems: list[Problem], languages: tuple[str, ...]) -> int:
    """Print the reference answer. Touches no files."""
    fences = {"python": "python", "typescript": "typescript", "php": "php"}
    for problem in problems:
        for language in languages:
            reference = problem.reference(language)
            if not reference.exists():
                print(f"# {problem.slug} [{language}] — no reference solution\n")
                continue
            print(f"# {'=' * 78}")
            print(f"# {problem.id}. {problem.title} — {language}")
            print(f"# {reference.relative_to(ROOT)}")
            print(f"# {'=' * 78}\n")
            print(f"```{fences[language]}")
            print(reference.read_text(encoding="utf-8").rstrip())
            print("```\n")
        if problem.notes.exists():
            print(f"Full write-up: {problem.notes.relative_to(ROOT)}\n")
    return 0


def cmd_status(problems: list[Problem], assert_stubs: bool) -> int:
    solved_total = 0
    print(f"\n{'problem':<34} {'python':>8} {'ts':>8} {'php':>8}   reference")
    print("-" * 74)

    not_stubbed = []
    for problem in problems:
        cells, solved_here = [], 0
        for language in LANGUAGES:
            live = problem.live(language)
            if not live.exists():
                cells.append("missing")
            elif is_stub(live):
                cells.append("todo")
            else:
                cells.append("solved")
                solved_here += 1
                not_stubbed.append(f"{problem.slug} [{language}]")
        have_ref = all(problem.reference(language).exists() for language in LANGUAGES)
        solved_total += solved_here
        print(f"{problem.id:>4}. {problem.slug:<28} "
              + " ".join(f"{c:>8}" for c in cells)
              + ("   yes" if have_ref else "   --"))

    total = len(problems) * len(LANGUAGES)
    print("-" * 74)
    print(f"{solved_total} / {total} implementations written "
          f"({len(problems)} problems x {len(LANGUAGES)} languages)\n")

    if assert_stubs and not_stubbed:
        print("Expected every live file to be an unsolved stub, but these are implemented:",
              file=sys.stderr)
        for entry in not_stubbed:
            print(f"  - {entry}", file=sys.stderr)
        return 1
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("command", choices=["extract", "restub", "apply", "restore", "show", "status"])
    parser.add_argument("--slug", help="one problem; omit for all")
    parser.add_argument("--lang", choices=LANGUAGES, help="one language; omit for all three")
    parser.add_argument("--force", action="store_true",
                        help="apply: overwrite a solved file")
    parser.add_argument("--assert-stubs", action="store_true",
                        help="status: exit non-zero if any live file is implemented (CI guard)")
    args = parser.parse_args()

    if args.command == "restore":
        return cmd_restore()

    problems = [find(args.slug)] if args.slug else load_problems()
    languages = (args.lang,) if args.lang else LANGUAGES

    if args.command == "extract":
        return cmd_extract(problems, languages, args.force)
    if args.command == "restub":
        return cmd_restub(problems, languages)
    if args.command == "apply":
        return cmd_apply(problems, languages, args.force)
    if args.command == "show":
        return cmd_show(problems, languages)
    return cmd_status(problems, args.assert_stubs)


if __name__ == "__main__":
    raise SystemExit(main())
