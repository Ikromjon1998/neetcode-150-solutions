"""49. Group Anagrams.

Driven by the shared contract:
packages/contracts/problems/0049-group-anagrams.json

No hand-written fixtures: add a case to the JSON and it lands here, in the TypeScript suite
and in the PHP suite at the same time.
"""

from __future__ import annotations

import pytest

from neetcode_core import approaches_for, get_solution
from tests.conftest import contract_cases

SLUG = "group-anagrams"
APPROACHES = approaches_for(SLUG)


@pytest.mark.parametrize("approach", APPROACHES)
@pytest.mark.parametrize("case", contract_cases(SLUG))
def test_solves_every_contract_case(approach: str, case: dict) -> None:
    solve = get_solution(SLUG, approach=approach)
    assert solve(case["input"]["strs"]) == case["expected"]


@pytest.mark.parametrize("case", contract_cases(SLUG))
def test_all_approaches_agree(case: dict) -> None:
    """Differential test — every approach must return the identical answer."""
    results = [
        get_solution(SLUG, approach=approach)(case["input"]["strs"])
        for approach in APPROACHES
    ]
    assert all(result == results[0] for result in results), results
