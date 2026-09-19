"""Shared pytest helpers.

`contract_cases` turns the JSON contract into pytest parameters, so every case written in
`packages/contracts/problems/*.json` becomes a named, individually reported test here —
and simultaneously in the TypeScript and PHP suites, which read the same file.
"""

from __future__ import annotations

from typing import Any

import pytest

from neetcode_core import cases


def contract_cases(slug: str, section: str = "cases") -> list[Any]:
    """Build `pytest.param` entries whose ids are the human-readable case names."""
    return [
        pytest.param(case, id=case["name"].replace(" ", "-"))
        for case in cases(slug, section)
    ]
