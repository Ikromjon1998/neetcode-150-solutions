#!/usr/bin/env python3
"""Scaffold one NeetCode problem across all three stacks.

    make new-problem ARGS="--id 242 --slug valid-anagram --title 'Valid Anagram' \
        --difficulty easy --topic arrays-and-hashing \
        --input 's:string,t:string' --returns bool --approaches sorting,hash-map"

It writes, and wires up, eighteen files:

  packages/contracts/problems/0242-valid-anagram.json   the single source of truth
  packages/core-python/...  algorithm + contract-driven test
  packages/core-ts/...      algorithm + contract-driven test   (+ registry and barrel entries)
  packages/core-php/...     algorithm + contract-driven test   (+ DefaultProblems entry)
  apps/api-python/...       router, schemas, service + e2e test
  apps/api-node/...         module, controller, service, DTO + e2e test  (+ ProblemsModule entry)
  apps/api-php/...          controller, FormRequest + e2e test  (+ route)
  docs/problems/0242-valid-anagram.md   your notes, pre-filled with the comparison headings

Nothing is overwritten. Re-running after a partial failure is safe: existing files are
reported and skipped.

The algorithm bodies are left as `TODO` on purpose — that is the part you are here to write.
Everything around them is generated so it cannot drift between the three languages.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

TOPICS = [
    "arrays-and-hashing", "two-pointers", "sliding-window", "stack", "binary-search",
    "linked-list", "trees", "tries", "heap-priority-queue", "backtracking", "graphs",
    "advanced-graphs", "1d-dynamic-programming", "2d-dynamic-programming", "greedy",
    "intervals", "math-and-geometry", "bit-manipulation",
]


# --------------------------------------------------------------------------------------
# Naming
# --------------------------------------------------------------------------------------

def snake(slug: str) -> str:
    """valid-anagram -> valid_anagram; 3sum -> three_sum (identifiers cannot start with a digit)."""
    text = slug.replace("-", "_")
    leading = {"0": "zero", "1": "one", "2": "two", "3": "three", "4": "four",
               "5": "five", "6": "six", "7": "seven", "8": "eight", "9": "nine"}
    if text[0].isdigit():
        text = leading[text[0]] + text[1:]
    return text


def pascal(slug: str) -> str:
    """valid-anagram -> ValidAnagram."""
    return "".join(part.capitalize() for part in snake(slug).split("_"))


def camel(slug: str) -> str:
    """valid-anagram -> validAnagram."""
    head, *rest = snake(slug).split("_")
    return head + "".join(part.capitalize() for part in rest)


def topic_python(topic: str) -> str:
    return topic.replace("-", "_")


def topic_php(topic: str) -> str:
    return "".join(part.capitalize() for part in topic_python(topic).split("_"))


# --------------------------------------------------------------------------------------
# The --input type mini-language
# --------------------------------------------------------------------------------------

@dataclass(frozen=True)
class Field:
    """One request field, rendered into three validation dialects."""

    name: str
    kind: str  # int | string | bool | float | int[] | string[] | int[][] | string[][]

    @property
    def py_type(self) -> str:
        return {
            "int": "StrictInt", "string": "StrictStr", "bool": "StrictBool", "float": "float",
            "int[]": "list[StrictInt]", "string[]": "list[StrictStr]",
            "int[][]": "list[list[StrictInt]]", "string[][]": "list[list[StrictStr]]",
        }[self.kind]

    @property
    def ts_type(self) -> str:
        return {
            "int": "number", "string": "string", "bool": "boolean", "float": "number",
            "int[]": "number[]", "string[]": "string[]",
            "int[][]": "number[][]", "string[][]": "string[][]",
        }[self.kind]

    @property
    def depth(self) -> int:
        """0 for a scalar, 1 for `T[]`, 2 for `T[][]`."""
        return self.kind.count("[]")

    @property
    def base(self) -> str:
        return self.kind.replace("[]", "")

    @property
    def ts_decorators(self) -> str:
        # `each: true` descends exactly one level, so a 2-D field needs the custom @IsMatrix
        # decorator in common/validators/is-matrix.ts. See that file for why.
        if self.depth == 2:
            return f'  @IsArray()\n  @IsMatrix("{self.base}")'
        rule = {"int": "@IsInt", "string": "@IsString", "bool": "@IsBoolean",
                "float": "@IsNumber"}[self.base]
        if self.depth == 1:
            return f"  @IsArray()\n  {rule}({{ each: true }})"
        return f"  {rule}()"

    @property
    def php_rules(self) -> str:
        check_of = {"int": "is_int", "string": "is_string", "bool": "is_bool",
                    "float": "is_float"}
        if self.depth == 2:
            # Laravel validates nested arrays with a repeated wildcard — the one place its
            # rule DSL is more expressive than class-validator's `each: true`.
            check = check_of[self.base]
            return (f"            '{self.name}' => ['present', 'array'],\n"
                    f"            '{self.name}.*' => ['present', 'array'],\n"
                    f"            '{self.name}.*.*' => ['present', $this->strictType('{check}', "
                    f"'{self.name}.*.*')],")
        if self.depth == 1:
            check = check_of[self.base]
            return (f"            '{self.name}' => ['present', 'array'],\n"
                    f"            '{self.name}.*' => ['present', $this->strictType('{check}', "
                    f"'{self.name}.*')],")
        check = {"int": "is_int", "string": "is_string", "bool": "is_bool",
                 "float": "is_float"}[self.kind]
        # `present`, never `required`: Laravel's `required` rejects the empty string, 0-length
        # arrays and `"0"`. Pydantic and class-validator accept all three for a declared field,
        # so `required` would make the Laravel app 422 payloads the other two answer 200 to.
        # `present` asserts the key exists and leaves emptiness to the type check.
        return (f"            '{self.name}' => ['present', "
                f"$this->strictType('{check}', '{self.name}')],")

    @property
    def php_type(self) -> str:
        return {
            "int": "int", "string": "string", "bool": "bool", "float": "float",
            "int[]": "array", "string[]": "array",
            "int[][]": "array", "string[][]": "array",
        }[self.kind]

    @property
    def example(self) -> object:
        return {
            "int": 0, "string": "", "bool": False, "float": 0.0,
            "int[]": [], "string[]": [], "int[][]": [[]], "string[][]": [[]],
        }[self.kind]


VALID_KINDS = {"int", "string", "bool", "float", "int[]", "string[]", "int[][]", "string[][]"}


def parse_fields(spec: str) -> list[Field]:
    fields = []
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        if ":" not in part:
            sys.exit(f"--input entry {part!r} must look like name:type")
        name, kind = (piece.strip() for piece in part.split(":", 1))
        if kind not in VALID_KINDS:
            sys.exit(f"unknown type {kind!r}; use one of {', '.join(sorted(VALID_KINDS))}")
        if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", name):
            sys.exit(f"field name {name!r} is not a valid identifier")
        fields.append(Field(name, kind))
    if not fields:
        sys.exit("--input must declare at least one field")
    return fields


RETURN_TYPES = {
    "int": ("int", "number", "int"),
    "int[]": ("list[int]", "number[]", "array"),
    "int[][]": ("list[list[int]]", "number[][]", "array"),
    "string": ("str", "string", "string"),
    "string[]": ("list[str]", "string[]", "array"),
    "string[][]": ("list[list[str]]", "string[][]", "array"),
    "bool": ("bool", "boolean", "bool"),
    "float": ("float", "number", "float"),
}


# --------------------------------------------------------------------------------------
# File writing
# --------------------------------------------------------------------------------------

written: list[Path] = []
skipped: list[Path] = []


def write(path: Path, content: str) -> None:
    if path.exists():
        skipped.append(path)
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    written.append(path)


def insert_after(path: Path, anchor: str, addition: str, marker: str) -> None:
    """Insert `addition` after the line containing `anchor`, unless `marker` is already there."""
    text = path.read_text(encoding="utf-8")
    if marker in text:
        skipped.append(path)
        return
    if anchor not in text:
        sys.exit(f"could not find anchor {anchor!r} in {path} — wire it up by hand")
    text = text.replace(anchor, anchor + addition, 1)
    path.write_text(text, encoding="utf-8")
    written.append(path)


def insert_into_list(path: Path, pattern: str, entry: str) -> None:
    """Append `entry` to a bracketed list matched by `pattern` (one capture group: the body).

    The idempotency check looks inside the matched list body, not the whole file. Checking the
    file would false-positive on the `import` line this same run just added, and the entry
    would be silently skipped — which is exactly the bug this comment exists to prevent.
    """
    text = path.read_text(encoding="utf-8")
    match = re.search(pattern, text, re.DOTALL)
    if not match:
        sys.exit(f"could not find the registry list in {path} — wire it up by hand")
    body = match.group(1)
    if re.search(rf"\b{re.escape(entry)}\b", body):
        skipped.append(path)
        return
    replacement = match.group(0).replace(body, body.rstrip().rstrip(",") + f", {entry}")
    text = text[: match.start()] + replacement + text[match.end():]
    path.write_text(text, encoding="utf-8")
    written.append(path)


def sort_php_use_block(path: Path) -> None:
    """Alphabetise the contiguous `use ...;` block in a PHP file.

    Laravel Pint's `ordered_imports` fixer enforces this, so generated files that skip it
    would fail `make lint` the moment they are written. Cheaper to emit it correctly.
    """
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    start = next((i for i, line in enumerate(lines) if line.startswith("use ")), None)
    if start is None:
        return
    end = start
    while end < len(lines) and lines[end].startswith("use "):
        end += 1
    block = sorted(lines[start:end], key=str.lower)
    if block != lines[start:end]:
        path.write_text("".join(lines[:start] + block + lines[end:]), encoding="utf-8")

# --------------------------------------------------------------------------------------
# Generators — one per artefact
# --------------------------------------------------------------------------------------

def gen_contract(a, fields: list[Field]) -> None:
    approaches = []
    for index, key in enumerate(a.approaches):
        approaches.append({
            "key": key,
            "name": key.replace("-", " ").capitalize(),
            "time": "O(?)",
            "space": "O(?)",
            "note": "TODO: why this approach, and what it trades away.",
            **({"default": True} if index == len(a.approaches) - 1 else {}),
        })

    contract = {
        "$schema": "../schema/problem-contract.schema.json",
        "id": a.id,
        "slug": a.slug,
        "title": a.title,
        "difficulty": a.difficulty,
        "topic": a.topic,
        "leetcodeUrl": f"https://leetcode.com/problems/{a.slug}/",
        "summary": "TODO: one paragraph. This is rendered into the API catalog and the docs.",
        "approaches": approaches,
        "cases": [
            {
                "name": "TODO rename me",
                "input": {f.name: f.example for f in fields},
                "expected": None,
            }
        ],
        "validationCases": [
            {"name": "missing " + fields[0].name, "input": {}, "status": 422},
        ],
        "notFoundCases": [],
    }
    write(
        ROOT / "packages/contracts/problems" / f"{a.id:04d}-{a.slug}.json",
        json.dumps(contract, indent=2) + "\n",
    )


def gen_core_python(a, fields: list[Field]) -> None:
    ret = RETURN_TYPES[a.returns][0]
    params = ", ".join(f"{f.name}: {f.py_type.replace('Strict', '').replace('Str', 'str').replace('Bool', 'bool')}" for f in fields)
    params = params.replace("Int", "int")
    args = ", ".join(f.name for f in fields)
    pkg = topic_python(a.topic)
    mod = snake(a.slug)

    body = [
        f'"""{a.id}. {a.title} — https://leetcode.com/problems/{a.slug}/',
        "",
        "TODO: restate the problem in your own words. If you cannot, you have not understood it.",
        "",
        "Every approach below is registered and reachable from the API via `?approach=`, so you",
        "can compare them over the same input without changing any code.",
        '"""',
        "",
        "from __future__ import annotations",
        "",
        "from neetcode_core.registry import solution",
        "",
        f'SLUG = "{a.slug}"',
        "",
    ]
    for key in a.approaches:
        body += [
            "",
            f'@solution(SLUG, approach="{key}")',
            f"def {mod}_{snake(key)}({params}) -> {ret}:",
            f'    """TODO: one line on the idea. Then time and space complexity.',
            "",
            "    Time O(?), space O(?).",
            '    """',
            "    raise NotImplementedError",
        ]

    write(ROOT / "packages/core-python/src/neetcode_core" / pkg / f"{mod}.py", "\n".join(body) + "\n")

    init = ROOT / "packages/core-python/src/neetcode_core" / pkg / "__init__.py"
    if not init.exists():
        write(init, f'"""Topic — {a.topic}."""\n')

    test = f'''"""{a.id}. {a.title}.

Driven by the shared contract:
packages/contracts/problems/{a.id:04d}-{a.slug}.json

No hand-written fixtures: add a case to the JSON and it lands here, in the TypeScript suite
and in the PHP suite at the same time.
"""

from __future__ import annotations

import pytest

from neetcode_core import approaches_for, get_solution
from tests.conftest import contract_cases

SLUG = "{a.slug}"
APPROACHES = approaches_for(SLUG)


@pytest.mark.parametrize("approach", APPROACHES)
@pytest.mark.parametrize("case", contract_cases(SLUG))
def test_solves_every_contract_case(approach: str, case: dict) -> None:
    solve = get_solution(SLUG, approach=approach)
    assert solve({", ".join(f'case["input"]["{f.name}"]' for f in fields)}) == case["expected"]


@pytest.mark.parametrize("case", contract_cases(SLUG))
def test_all_approaches_agree(case: dict) -> None:
    """Differential test — every approach must return the identical answer."""
    results = [
        get_solution(SLUG, approach=approach)({", ".join(f'case["input"]["{f.name}"]' for f in fields)})
        for approach in APPROACHES
    ]
    assert all(result == results[0] for result in results), results
'''
    test_dir = ROOT / "packages/core-python/tests" / pkg
    write(test_dir / "__init__.py", "")
    write(test_dir / f"test_{mod}.py", test)


def gen_core_ts(a, fields: list[Field]) -> None:
    ret = RETURN_TYPES[a.returns][1]
    params = ", ".join(f"{f.name}: {f.ts_type}" for f in fields)
    args = ", ".join(f"input.{f.name}" for f in fields)
    fn = camel(a.slug)

    lines = [
        "/**",
        f" * {a.id}. {a.title} — https://leetcode.com/problems/{a.slug}/",
        " *",
        " * TODO: restate the problem in your own words.",
        " */",
        "",
        'import { defineProblem } from "../define-problem";',
        "",
        f'export const SLUG = "{a.slug}";',
    ]
    for key in a.approaches:
        lines += [
            "",
            "/** TODO: one line on the idea. Time O(?), space O(?). */",
            f"export function {fn}{pascal(key)}({params}): {ret} {{",
            f'  throw new Error("Not implemented");',
            "}",
        ]
    lines += [
        "",
        f"export const {fn} = defineProblem(SLUG, {{",
    ]
    for key in a.approaches:
        lines.append(f'  "{key}": {fn}{pascal(key)},')
    lines += ["});", ""]

    write(ROOT / "packages/core-ts/src" / a.topic / f"{a.slug}.ts", "\n".join(lines))

    ts_fields = "\n".join(f"  {f.name}: {f.ts_type};" for f in fields)
    impls = "\n".join(f'  ["{key}", {fn}{pascal(key)}],' for key in a.approaches)
    test = f'''/**
 * {a.id}. {a.title} — driven by packages/contracts/problems/{a.id:04d}-{a.slug}.json.
 *
 * No hand-written fixtures: add a case to the JSON and it lands here, in the Python suite and
 * in the PHP suite at the same time.
 */

import {{ describe, expect, it }} from "vitest";
import {{ contractCases }} from "../../src/index";
import {{ {", ".join(f"{fn}{pascal(k)}" for k in a.approaches)} }} from "../../src/{a.topic}/{a.slug}";

interface Input {{
{ts_fields}
}}

const SLUG = "{a.slug}";
const CASES = contractCases<Input, {ret}>(SLUG);
const IMPLEMENTATIONS = [
{impls}
] as const;

describe.each(IMPLEMENTATIONS)("{a.slug} (%s)", (_key, solve) => {{
  it.each(CASES)("$name", ({{ input, expected }}) => {{
    expect(solve({args})).toEqual(expected);
  }});
}});

describe("{a.slug} differential", () => {{
  it.each(CASES)("all approaches agree: $name", ({{ input }}) => {{
    const results = IMPLEMENTATIONS.map(([, solve]) => solve({args}));
    for (const result of results) expect(result).toEqual(results[0]);
  }});
}});
'''
    write(ROOT / "packages/core-ts/tests" / a.topic / f"{a.slug}.test.ts", test)

    registry = ROOT / "packages/core-ts/src/registry.ts"
    insert_after(
        registry,
        'import { twoSum } from "./arrays-and-hashing/two-sum";',
        f'\nimport {{ {fn} }} from "./{a.topic}/{a.slug}";',
        f'from "./{a.topic}/{a.slug}"',
    )
    insert_into_list(
        registry,
        r"const PROBLEM_MODULES: readonly ProblemModule\[\] = \[(.*?)\];",
        fn,
    )
    # An explicit, aliased re-export — NOT `export *`. Every problem module exports a `SLUG`
    # constant, so a star re-export collides as soon as there is a second problem:
    #   TS2308: Module "..." has already exported a member named 'SLUG'.
    exported = ", ".join([f"SLUG as {snake(a.slug).upper()}", fn] + [f"{fn}{pascal(k)}" for k in a.approaches])
    insert_after(
        ROOT / "packages/core-ts/src/index.ts",
        'export { SLUG as TWO_SUM, twoSum, twoSumBruteForce, twoSumHashMap } from "./arrays-and-hashing/two-sum";',
        f'\nexport {{ {exported} }} from "./{a.topic}/{a.slug}";',
        f'from "./{a.topic}/{a.slug}"',
    )


def gen_core_php(a, fields: list[Field]) -> None:
    ret = RETURN_TYPES[a.returns][2]
    cls = pascal(a.slug)
    ns = topic_php(a.topic)
    params = ", ".join(f"{f.php_type} ${f.name}" for f in fields)
    args = ", ".join(f"$input['{f.name}']" for f in fields)

    methods = []
    entries = []
    for key in a.approaches:
        method = camel(key)
        entries.append(f"            '{key}' => self::{method}(...),")
        methods.append(f"""
    /**
     * TODO: one line on the idea. Time O(?), space O(?).
     */
    public static function {method}({params}): {ret}
    {{
        throw new \\RuntimeException('Not implemented');
    }}""")

    php = f"""<?php

declare(strict_types=1);

namespace NeetCode\\Core\\{ns};

use NeetCode\\Core\\Contracts\\ProblemDefinition;

/**
 * {a.id}. {a.title} — https://leetcode.com/problems/{a.slug}/
 *
 * TODO: restate the problem in your own words.
 */
final class {cls} implements ProblemDefinition
{{
    public const SLUG = '{a.slug}';

    public static function slug(): string
    {{
        return self::SLUG;
    }}

    /** @return array<string, callable> */
    public static function solutions(): array
    {{
        return [
{chr(10).join(entries)}
        ];
    }}
{"".join(methods)}
}}
"""
    write(ROOT / "packages/core-php/src" / ns / f"{cls}.php", php)

    test = f"""<?php

declare(strict_types=1);

namespace NeetCode\\Core\\Tests\\{ns};

use NeetCode\\Core\\{ns}\\{cls};
use NeetCode\\Core\\Contracts\\ContractRepository;
use PHPUnit\\Framework\\Attributes\\DataProvider;
use PHPUnit\\Framework\\Attributes\\Test;
use PHPUnit\\Framework\\TestCase;

/**
 * {a.id}. {a.title} — driven by packages/contracts/problems/{a.id:04d}-{a.slug}.json.
 *
 * No hand-written fixtures: add a case to the JSON and it lands here, in the Python suite and
 * in the TypeScript suite at the same time.
 */
final class {cls}Test extends TestCase
{{
    #[Test]
    #[DataProvider('contractCases')]
    public function it_solves_every_contract_case(string $approach, array $input, mixed $expected): void
    {{
        $solve = {cls}::solutions()[$approach];

        $this->assertSame($expected, $solve({args}));
    }}

    /** Differential test — every approach must return the identical answer. */
    #[Test]
    #[DataProvider('inputsOnly')]
    public function all_approaches_agree(array $input): void
    {{
        $results = array_map(
            static fn (callable $solve): mixed => $solve({args}),
            {cls}::solutions(),
        );

        $this->assertCount(1, array_unique(array_map(serialize(...), $results)));
    }}

    /** @return iterable<string, array{{string, array<string, mixed>, mixed}}> */
    public static function contractCases(): iterable
    {{
        $contracts = new ContractRepository();

        foreach (array_keys({cls}::solutions()) as $approach) {{
            foreach ($contracts->cases({cls}::SLUG) as $case) {{
                yield "{{$case['name']}} ({{$approach}})" => [$approach, $case['input'], $case['expected']];
            }}
        }}
    }}

    /** @return iterable<string, array{{array<string, mixed>}}> */
    public static function inputsOnly(): iterable
    {{
        foreach ((new ContractRepository())->cases({cls}::SLUG) as $case) {{
            yield $case['name'] => [$case['input']];
        }}
    }}
}}
"""
    write(ROOT / "packages/core-php/tests" / ns / f"{cls}Test.php", test)

    defaults = ROOT / "packages/core-php/src/Registry/DefaultProblems.php"
    insert_after(
        defaults,
        "use NeetCode\\Core\\ArraysAndHashing\\TwoSum;",
        f"\nuse NeetCode\\Core\\{ns}\\{cls};",
        f"\\{ns}\\{cls};",
    )
    text = defaults.read_text(encoding="utf-8")
    if f"{cls}::class" not in text:
        defaults.write_text(
            text.replace("            TwoSum::class,", f"            TwoSum::class,\n            {cls}::class,"),
            encoding="utf-8",
        )


def gen_api_python(a, fields: list[Field]) -> None:
    ret = RETURN_TYPES[a.returns][0]
    mod = snake(a.slug)
    pkg = ROOT / "apps/api-python/src/neetcode_api/problems" / mod
    py_fields = "\n".join(
        f'    {f.name}: {f.py_type} = Field(description="TODO: what this field means.")'
        for f in fields
    )
    call_args = ", ".join(f"payload.{f.name}" for f in fields)
    sig_args = ", ".join(f"{f.name}: {f.py_type.replace('Strict', '').replace('Str', 'str').replace('Bool', 'bool').replace('Int', 'int')}" for f in fields)
    pass_args = ", ".join(f.name for f in fields)

    write(pkg / "schemas.py", f'''"""Request model for `POST /problems/{a.slug}`.

Strict scalar types on purpose: lax Pydantic would coerce the JSON string `"7"` to `7`, and
this endpoint would then disagree with the NestJS one, where `@IsInt()` rejects it.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictInt, StrictStr  # noqa: F401


class {pascal(a.slug)}Request(BaseModel):
    model_config = ConfigDict(extra="forbid")

{py_fields}
''')

    write(pkg / "service.py", f'''"""Application service for {a.title}.

The seam between HTTP and the algorithm: plain values in, plain values out.
"""

from __future__ import annotations

from neetcode_core import get_solution

from neetcode_api.timing import timed

SLUG = "{a.slug}"


class {pascal(a.slug)}Service:
    def solve(self, {sig_args}, approach: str) -> tuple[{ret}, int]:
        """Return `(result, elapsed_microseconds)`."""
        algorithm = get_solution(SLUG, approach=approach)
        return timed(algorithm, {pass_args})
''')

    write(pkg / "router.py", f'''"""HTTP surface for problem {a.id}."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, status
from neetcode_core import get_meta

from neetcode_api.dependencies import approach_provider
from neetcode_api.http_status import UNPROCESSABLE_CONTENT
from neetcode_api.problems.{mod}.schemas import {pascal(a.slug)}Request
from neetcode_api.problems.{mod}.service import SLUG, {pascal(a.slug)}Service
from neetcode_api.schemas import ErrorResponse, SolveResponse

router = APIRouter(prefix="/problems", tags=["{a.topic}"])


@router.post(
    f"/{{SLUG}}",
    summary="Solve {a.title}",
    response_model=SolveResponse[{ret}],
    response_model_by_alias=True,
    responses={{
        status.HTTP_404_NOT_FOUND: {{"model": ErrorResponse}},
        UNPROCESSABLE_CONTENT: {{"model": ErrorResponse}},
    }},
)
async def solve(
    payload: {pascal(a.slug)}Request,
    approach: Annotated[str, Depends(approach_provider(SLUG))],
    service: Annotated[
        {pascal(a.slug)}Service, Depends({pascal(a.slug)}Service)
    ],
) -> SolveResponse[{ret}]:
    result, elapsed = service.solve({call_args}, approach)
    chosen = get_meta(SLUG).approach(approach)
    return SolveResponse[{ret}](
        problem=SLUG,
        approach={{
            "key": chosen.key,
            "name": chosen.name,
            "time": chosen.time,
            "space": chosen.space,
            "note": chosen.note,
            "default": chosen.default,
        }},
        input=payload.model_dump(),
        result=result,
        elapsedMicros=elapsed,
    )
''')

    write(pkg / "__init__.py", f'''"""Problem {a.id} — {a.title} (topic: {a.topic})."""

from neetcode_api.problems.{mod}.router import router

__all__ = ["router"]
''')

    write(ROOT / "apps/api-python/tests" / f"test_{mod}.py", f'''"""`POST /problems/{a.slug}`, driven by the shared JSON contract."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient
from neetcode_core import approaches_for
from tests.conftest import contract_cases

SLUG = "{a.slug}"
URL = f"/problems/{{SLUG}}"


@pytest.mark.parametrize("approach", approaches_for(SLUG))
@pytest.mark.parametrize("case", contract_cases(SLUG))
def test_solves_contract_cases(client: TestClient, approach: str, case: dict) -> None:
    response = client.post(URL, json=case["input"], params={{"approach": approach}})
    assert response.status_code == 200, response.text
    assert response.json()["result"] == case["expected"]


@pytest.mark.parametrize("case", contract_cases(SLUG, "validationCases"))
def test_invalid_input_is_422(client: TestClient, case: dict) -> None:
    response = client.post(URL, json=case["input"])
    assert response.status_code == case["status"], response.text
    assert response.json()["error"]["type"] == "validation_error"
''')


def gen_api_node(a, fields: list[Field]) -> None:
    ret = RETURN_TYPES[a.returns][1]
    cls = pascal(a.slug)
    dir_ = ROOT / "apps/api-node/src/problems" / a.slug

    dto_props = "\n\n".join(
        f'  @ApiProperty({{ description: "TODO: what this field means." }})\n'
        f"{f.ts_decorators}\n  {f.name}!: {f.ts_type};"
        for f in fields
    )
    write(dir_ / "dto" / f"{a.slug}-request.dto.ts", f'''/** Request DTO for `POST /problems/{a.slug}`. */

import {{ ApiProperty }} from "@nestjs/swagger";
import {{ ArrayMinSize, IsArray, IsBoolean, IsInt, IsNumber, IsString }} from "class-validator"; // eslint-disable-line
import {{ IsMatrix }} from "../../../common/validators/is-matrix"; // eslint-disable-line

export class {cls}RequestDto {{
{dto_props}
}}
''')

    sig = ", ".join(f"{f.name}: {f.ts_type}" for f in fields)
    call = ", ".join(f.name for f in fields)
    write(dir_ / f"{a.slug}.service.ts", f'''/** Application service for {a.title}: the seam between HTTP and the algorithm. */

import {{ Injectable }} from "@nestjs/common";
import {{ getSolution }} from "@neetcode/core";
import {{ timed }} from "../../common/timing";

export const SLUG = "{a.slug}";

type SolveFn = ({sig}) => {ret};

@Injectable()
export class {cls}Service {{
  solve({sig}, approach: string): {{ result: {ret}; elapsedMicros: number }} {{
    const algorithm = getSolution(SLUG, approach) as SolveFn;
    return timed(() => algorithm({call}));
  }}
}}
''')

    body_call = ", ".join(f"body.{f.name}" for f in fields)
    input_echo = ", ".join(f"{f.name}: body.{f.name}" for f in fields)
    write(dir_ / f"{a.slug}.controller.ts", f'''/** HTTP surface for problem {a.id}. */

import {{ Body, Controller, HttpCode, HttpStatus, Post, Query }} from "@nestjs/common";
import {{
  ApiBody,
  ApiNotFoundResponse,
  ApiOkResponse,
  ApiOperation,
  ApiQuery,
  ApiTags,
  ApiUnprocessableEntityResponse,
}} from "@nestjs/swagger";
import {{ approachesFor, findApproach }} from "@neetcode/core";
import {{ ErrorResponseDto, SolveResponseDto }} from "../../common/dto/solve-response.dto";
import {{ ApproachPipe }} from "../../common/pipes/approach.pipe";
import {{ {cls}RequestDto }} from "./dto/{a.slug}-request.dto";
import {{ SLUG, {cls}Service }} from "./{a.slug}.service";

@ApiTags("{a.topic}")
@Controller("problems")
export class {cls}Controller {{
  constructor(private readonly service: {cls}Service) {{}}

  @Post(SLUG)
  // Nest answers POST with 201 by default; FastAPI and Laravel both answer 200 here.
  @HttpCode(HttpStatus.OK)
  @ApiOperation({{ summary: "Solve {a.title}" }})
  @ApiBody({{ type: {cls}RequestDto }})
  @ApiQuery({{ name: "approach", required: false, enum: approachesFor(SLUG) }})
  @ApiOkResponse({{ type: SolveResponseDto }})
  @ApiNotFoundResponse({{ type: ErrorResponseDto }})
  @ApiUnprocessableEntityResponse({{ type: ErrorResponseDto }})
  solve(
    @Body() body: {cls}RequestDto,
    @Query("approach", new ApproachPipe(SLUG)) approach: string,
  ): SolveResponseDto<{ret}> {{
    const {{ result, elapsedMicros }} = this.service.solve({body_call}, approach);
    const chosen = findApproach(SLUG, approach);

    return {{
      problem: SLUG,
      approach: {{
        key: chosen.key,
        name: chosen.name,
        time: chosen.time,
        space: chosen.space,
        note: chosen.note,
        default: chosen.default ?? false,
      }},
      input: {{ {input_echo} }},
      result,
      elapsedMicros,
    }};
  }}
}}
''')

    write(dir_ / f"{a.slug}.module.ts", f'''import {{ Module }} from "@nestjs/common";
import {{ {cls}Controller }} from "./{a.slug}.controller";
import {{ {cls}Service }} from "./{a.slug}.service";

@Module({{
  controllers: [{cls}Controller],
  providers: [{cls}Service],
}})
export class {cls}Module {{}}
''')

    write(ROOT / "apps/api-node/test" / f"{a.slug}.e2e.spec.ts", f'''/** `POST /problems/{a.slug}`, driven by the shared JSON contract. */

import type {{ INestApplication }} from "@nestjs/common";
import request from "supertest";
import {{ approachesFor, contractCases, validationCases }} from "@neetcode/core";
import {{ bootTestApp }} from "./setup";

const SLUG = "{a.slug}";
const URL = `/problems/${{SLUG}}`;
const CASES = contractCases(SLUG);

describe(`POST ${{URL}}`, () => {{
  let app: INestApplication;

  beforeAll(async () => {{
    app = await bootTestApp();
  }});

  afterAll(async () => {{
    await app.close();
  }});

  const http = () => request(app.getHttpServer());

  describe.each(approachesFor(SLUG))("approach=%s", (approach) => {{
    it.each(CASES)("$name", async ({{ input, expected }}) => {{
      const {{ body }} = await http().post(URL).query({{ approach }}).send(input).expect(200);
      expect(body.result).toEqual(expected);
    }});
  }});

  it.each(validationCases(SLUG))("422s invalid input: $name", async ({{ input, status }}) => {{
    const {{ body }} = await http().post(URL).send(input).expect(status);
    expect(body.error.type).toBe("validation_error");
  }});
}});
''')

    module = ROOT / "apps/api-node/src/problems/problems.module.ts"
    insert_after(
        module,
        'import { TwoSumModule } from "./two-sum/two-sum.module";',
        f'\nimport {{ {cls}Module }} from "./{a.slug}/{a.slug}.module";',
        f'./{a.slug}/{a.slug}.module',
    )
    insert_into_list(module, r"const PROBLEM_MODULES = \[(.*?)\];", f"{cls}Module")


def gen_api_php(a, fields: list[Field]) -> None:
    cls = pascal(a.slug)
    ns_cls = pascal(a.slug)
    topic_ns = topic_php(a.topic)
    dir_ = ROOT / "apps/api-php/app/Problems" / cls
    rules = "\n".join(f.php_rules for f in fields)
    names = ", ".join(f"'{f.name}'" for f in fields)
    call = ", ".join(f"$input['{f.name}']" for f in fields)
    echo = ", ".join(f"'{f.name}' => $input['{f.name}']" for f in fields)

    write(dir_ / f"{cls}Request.php", f"""<?php

declare(strict_types=1);

namespace App\\Problems\\{cls};

use Illuminate\\Foundation\\Http\\FormRequest;

/**
 * Request validation for `POST /problems/{a.slug}`.
 *
 * Laravel's built-in `integer` rule accepts the numeric string "7"; Pydantic's StrictInt and
 * class-validator's @IsInt() both refuse it. `strictType()` keeps the three apps in agreement.
 */
final class {cls}Request extends FormRequest
{{
    public function authorize(): bool
    {{
        return true;
    }}

    /** @return array<string, mixed> */
    public function rules(): array
    {{
        return [
{rules}
        ];
    }}

    private function strictType(string $check, string $label): callable
    {{
        return static function (string $attribute, mixed $value, callable $fail) use ($check, $label): void {{
            if (! $check($value)) {{
                $fail("{{$label}} has the wrong type.");
            }}
        }};
    }}

    /** Laravel silently drops unknown fields; a typo'd field name is a bug. */
    protected function prepareForValidation(): void
    {{
        $unexpected = array_diff(array_keys($this->json()->all()), [{names}]);

        if ($unexpected !== []) {{
            abort(422, 'Unexpected fields: '.implode(', ', $unexpected));
        }}
    }}
}}
""")

    write(dir_ / f"{cls}Controller.php", f"""<?php

declare(strict_types=1);

namespace App\\Problems\\{cls};

use App\\Http\\Controllers\\Controller;
use App\\Support\\SolveResponse;
use App\\Support\\Timing;
use Illuminate\\Http\\JsonResponse;
use NeetCode\\Core\\{topic_ns}\\{ns_cls};
use NeetCode\\Core\\Exceptions\\UnknownApproachException;
use NeetCode\\Core\\Registry\\ProblemRegistry;

/** HTTP surface for problem {a.id}. */
final class {cls}Controller extends Controller
{{
    public function __construct(private readonly ProblemRegistry $registry) {{}}

    public function __invoke({cls}Request $request): JsonResponse
    {{
        $approach = $this->resolveApproach($request->query('approach'));
        $input = $request->validated();

        $solve = $this->registry->solution({ns_cls}::SLUG, $approach);
        [$result, $elapsedMicros] = Timing::measure(static fn (): mixed => $solve({call}));

        return SolveResponse::make(
            {ns_cls}::SLUG,
            $this->registry->meta({ns_cls}::SLUG)->approach($approach),
            // Explicit: validated() key order follows rule evaluation, not declaration.
            [{echo}],
            $result,
            $elapsedMicros,
        );
    }}

    private function resolveApproach(mixed $requested): string
    {{
        $available = $this->registry->approaches({ns_cls}::SLUG);
        $approach = is_string($requested) && $requested !== ''
            ? $requested
            : $this->registry->meta({ns_cls}::SLUG)->defaultApproach()->key;

        if (! in_array($approach, $available, true)) {{
            throw new UnknownApproachException({ns_cls}::SLUG, $approach, $available);
        }}

        return $approach;
    }}
}}
""")

    write(ROOT / "apps/api-php/tests/Feature" / f"{cls}Test.php", f"""<?php

declare(strict_types=1);

namespace Tests\\Feature;

use NeetCode\\Core\\{topic_ns}\\{ns_cls};
use PHPUnit\\Framework\\Attributes\\DataProvider;
use PHPUnit\\Framework\\Attributes\\Test;
use Tests\\Support\\ContractCases;
use Tests\\TestCase;

/** `POST /problems/{a.slug}`, driven by the shared JSON contract. */
final class {cls}Test extends TestCase
{{
    private const URL = '/problems/{a.slug}';

    #[Test]
    #[DataProvider('solveCases')]
    public function it_solves_every_contract_case(string $approach, array $input, mixed $expected): void
    {{
        $this->postJson(self::URL.'?approach='.$approach, $input)
            ->assertOk()
            ->assertJsonPath('result', $expected);
    }}

    #[Test]
    #[DataProvider('validationCases')]
    public function it_422s_invalid_input(array $input, int $status): void
    {{
        $this->postJson(self::URL, $input)
            ->assertStatus($status)
            ->assertJsonPath('error.type', 'validation_error');
    }}

    /** @return iterable<string, array{{string, array<string, mixed>, mixed}}> */
    public static function solveCases(): iterable
    {{
        return ContractCases::perApproach({ns_cls}::SLUG, array_keys({ns_cls}::solutions()));
    }}

    /** @return iterable<string, array{{array<string, mixed>, int}}> */
    public static function validationCases(): iterable
    {{
        return ContractCases::plain({ns_cls}::SLUG, 'validationCases');
    }}
}}
""")

    routes = ROOT / "apps/api-php/routes/api.php"
    insert_after(
        routes,
        "use App\\Problems\\TwoSum\\TwoSumController;",
        f"\nuse App\\Problems\\{cls}\\{cls}Controller;",
        f"App\\Problems\\{cls}\\{cls}Controller;",
    )
    sort_php_use_block(routes)
    insert_after(
        routes,
        "    // --- problem endpoints (one line per problem) ---",
        f"\n    Route::post('/{a.slug}', {cls}Controller::class);",
        f"Route::post('/{a.slug}'",
    )


def gen_docs(a, fields: list[Field]) -> None:
    write(ROOT / "docs/problems" / f"{a.id:04d}-{a.slug}.md", f"""# {a.id}. {a.title}

**Difficulty:** {a.difficulty} · **Topic:** {a.topic} · **Approaches:** {", ".join(a.approaches)}
**LeetCode:** https://leetcode.com/problems/{a.slug}/

## The problem

TODO: restate it in your own words. If you cannot, you have not understood it yet.

## Approaches

{chr(10).join(f"### {k}{chr(10)}{chr(10)}TODO: the idea in two sentences. Time O(?), space O(?)." + chr(10) for k in a.approaches)}

## What differed between the three languages

TODO. Prompts, not rules — delete the ones that had no interesting answer:

- **Data structures.** Python `dict`, JS `Map` (not an object — string key coercion), PHP array.
- **Iteration.** `enumerate` / `for` with index / `foreach` with `=> $key`.
- **Nullability.** `None` vs `undefined` vs `null` — and which "not found" sentinel each API uses.
- **Immutability.** `tuple` / `readonly` / `readonly class`.
- **Integer behaviour.** Python's arbitrary precision vs. 64-bit in the other two, and JS
  `Number.MAX_SAFE_INTEGER`.

## What differed between the three frameworks

TODO:

- **Validation.** Pydantic model / class-validator DTO / FormRequest. Which one caught what?
- **Wiring.** `Depends()` / constructor injection / container autowiring.
- **Errors.** Which framework fought you about the status code?

## Where I got stuck

TODO: the honest version. This is the section that is worth re-reading in three months.

## Benchmarks

```bash
# once you have implemented it
curl -s 'localhost:8000/problems/{a.slug}?approach={a.approaches[0]}' \\
  -H 'content-type: application/json' -d '{{...}}' | jq .elapsedMicros
```

| Approach | Python | TypeScript | PHP |
|----------|--------|------------|-----|
{chr(10).join(f"| {k} | | | |" for k in a.approaches)}
""")


# --------------------------------------------------------------------------------------
# Entry point
# --------------------------------------------------------------------------------------


def format_generated_python() -> None:
    """Run `ruff check --fix` over the Python files this run wrote.

    A long slug (`product-of-array-except-self`) pushes a generated import past the 100-column
    limit, and isort then wants it wrapped — while a short slug wants the same import on one
    line. No fixed template satisfies both, so the formatter decides. Best-effort: if ruff is
    not installed the files are still correct, just possibly unsorted.
    """
    targets = [str(path) for path in written if path.suffix == ".py"]
    if not targets:
        return

    for ruff in (ROOT / ".venv/bin/ruff", Path("ruff")):
        try:
            subprocess.run(
                [str(ruff), "check", "--fix", "--quiet", *targets],
                cwd=ROOT, check=False, capture_output=True,
            )
            return
        except (FileNotFoundError, OSError):
            continue


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Scaffold one NeetCode problem across Python/FastAPI, TypeScript/NestJS and PHP/Laravel.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("--id", type=int, required=True, help="LeetCode problem number, e.g. 242")
    parser.add_argument("--slug", required=True, help="kebab-case, e.g. valid-anagram")
    parser.add_argument("--title", required=True, help='e.g. "Valid Anagram"')
    parser.add_argument("--difficulty", required=True, choices=["easy", "medium", "hard"])
    parser.add_argument("--topic", required=True, choices=TOPICS)
    parser.add_argument(
        "--input", required=True, dest="input_spec",
        help="Request fields, e.g. 's:string,t:string' or 'nums:int[],target:int'. "
             f"Types: {', '.join(sorted(VALID_KINDS))}",
    )
    parser.add_argument("--returns", required=True, choices=sorted(RETURN_TYPES))
    parser.add_argument(
        "--approaches", default="brute-force,optimal",
        help="Comma-separated approach keys. The LAST one becomes the default.",
    )
    args = parser.parse_args()

    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", args.slug):
        sys.exit(f"--slug must be kebab-case, got {args.slug!r}")

    args.approaches = [key.strip() for key in args.approaches.split(",") if key.strip()]
    for key in args.approaches:
        if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", key):
            sys.exit(f"approach key must be kebab-case, got {key!r}")

    fields = parse_fields(args.input_spec)

    gen_contract(args, fields)
    gen_core_python(args, fields)
    gen_core_ts(args, fields)
    gen_core_php(args, fields)
    gen_api_python(args, fields)
    gen_api_node(args, fields)
    gen_api_php(args, fields)
    gen_docs(args, fields)
    format_generated_python()

    print(f"\nScaffolded {args.id}. {args.title} ({args.slug})\n")
    for path in written:
        print(f"  + {path.relative_to(ROOT)}")
    for path in sorted(set(skipped)):
        print(f"  = {path.relative_to(ROOT)} (already existed, left alone)")

    print(f"""
Next, in this order:

  1. packages/contracts/problems/{args.id:04d}-{args.slug}.json
     Fill in the summary, real complexities, and REAL TEST CASES. Everything else reads
     this file, so cases you add here are enforced in all three languages at once.

  2. Implement the algorithm three times:
     packages/core-python/src/neetcode_core/{topic_python(args.topic)}/{snake(args.slug)}.py
     packages/core-ts/src/{args.topic}/{args.slug}.ts
     packages/core-php/src/{topic_php(args.topic)}/{pascal(args.slug)}.php

  3. make test

  4. docs/problems/{args.id:04d}-{args.slug}.md
     Write the notes while the differences are still fresh. That is the actual deliverable.
""")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
