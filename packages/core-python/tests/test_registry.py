"""Registry-level guards.

These run against every problem in the package, so they keep paying off as the repo grows:
problem 150 is checked by exactly the same three tests as problem 1.
"""

from __future__ import annotations

import pytest

from neetcode_core import (
    all_meta,
    approaches_for,
    get_solution,
    registered_slugs,
    verify_registry,
)
from neetcode_core.errors import UnknownApproachError, UnknownProblemError


def test_contracts_and_implementations_agree() -> None:
    """Every declared approach is implemented, and vice versa."""
    verify_registry()


def test_auto_discovery_finds_solutions() -> None:
    assert "two-sum" in registered_slugs()


@pytest.mark.parametrize("meta", all_meta(), ids=lambda m: m.slug)
def test_every_problem_has_a_single_default_approach(meta) -> None:
    defaults = [approach for approach in meta.approaches if approach.default]
    assert len(defaults) <= 1, f"{meta.slug} declares {len(defaults)} defaults"
    assert meta.default_approach in meta.approaches


@pytest.mark.parametrize("slug", registered_slugs())
def test_default_approach_resolves_without_an_explicit_key(slug: str) -> None:
    assert callable(get_solution(slug))


def test_unknown_problem_raises() -> None:
    with pytest.raises(UnknownProblemError):
        get_solution("does-not-exist")


def test_unknown_approach_lists_the_available_ones() -> None:
    with pytest.raises(UnknownApproachError) as excinfo:
        get_solution("two-sum", approach="quantum")
    assert set(excinfo.value.available) == set(approaches_for("two-sum"))
