"""Loader for the shared JSON contracts in `packages/contracts/`.

One JSON file per problem is the single source of truth for metadata and test cases, and
all three languages read it. Adding a case to the JSON immediately tightens the Python,
TypeScript and PHP suites at once — there is no way for them to drift apart.
"""

from __future__ import annotations

import functools
import json
import os
from pathlib import Path
from typing import Any

from neetcode_core.errors import UnknownProblemError
from neetcode_core.types import Approach, Difficulty, ProblemMeta, Topic

_ENV_VAR = "NEETCODE_CONTRACTS_DIR"


def contracts_dir() -> Path:
    """Locate `packages/contracts/problems`.

    Honours $NEETCODE_CONTRACTS_DIR first (used by Docker images and CI, where the repo
    layout may differ), then walks up from this file looking for the monorepo root.
    """
    override = os.environ.get(_ENV_VAR)
    if override:
        path = Path(override).expanduser().resolve()
        if not path.is_dir():
            raise FileNotFoundError(f"${_ENV_VAR} points at {path}, which is not a directory.")
        return path

    for parent in Path(__file__).resolve().parents:
        candidate = parent / "packages" / "contracts" / "problems"
        if candidate.is_dir():
            return candidate

    raise FileNotFoundError(
        "Could not find packages/contracts/problems by walking up from "
        f"{__file__}. Set ${_ENV_VAR} to point at it explicitly."
    )


@functools.cache
def _raw_contracts() -> dict[str, dict[str, Any]]:
    """Read every contract file once and index it by slug."""
    by_slug: dict[str, dict[str, Any]] = {}
    for path in sorted(contracts_dir().glob("*.json")):
        with path.open(encoding="utf-8") as handle:
            data = json.load(handle)
        slug = data["slug"]
        if slug in by_slug:
            raise ValueError(f"Duplicate contract slug {slug!r} in {path}")
        by_slug[slug] = data
    return by_slug


def raw_contract(slug: str) -> dict[str, Any]:
    """The decoded JSON for one problem, exactly as written on disk."""
    try:
        return _raw_contracts()[slug]
    except KeyError:
        raise UnknownProblemError(slug) from None


def all_slugs() -> tuple[str, ...]:
    return tuple(_raw_contracts())


@functools.cache
def load_meta(slug: str) -> ProblemMeta:
    """Parse one contract into the typed `ProblemMeta` the rest of the code uses."""
    data = raw_contract(slug)
    approaches = tuple(
        Approach(
            key=item["key"],
            name=item["name"],
            time=item["time"],
            space=item["space"],
            note=item.get("note"),
            default=bool(item.get("default", False)),
        )
        for item in data["approaches"]
    )
    return ProblemMeta(
        id=data["id"],
        slug=data["slug"],
        title=data["title"],
        difficulty=Difficulty(data["difficulty"]),
        topic=Topic(data["topic"]),
        summary=data["summary"],
        approaches=approaches,
        leetcode_url=data.get("leetcodeUrl"),
        neetcode_url=data.get("neetcodeUrl"),
    )


def cases(slug: str, section: str = "cases") -> list[dict[str, Any]]:
    """Test cases from a contract. `section` is one of the *Cases keys in the schema."""
    return list(raw_contract(slug).get(section, []))
