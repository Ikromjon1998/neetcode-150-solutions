"""1. Two Sum — driven entirely by packages/contracts/problems/0001-two-sum.json.

Note what is *not* here: no hand-written input/expected pairs. Add a case to the JSON and it
lands in this file, in the TypeScript suite and in the PHP suite at the same time.
"""

from __future__ import annotations

import pytest

from neetcode_core import NoSolutionError, approaches_for, get_solution
from tests.conftest import contract_cases

SLUG = "two-sum"
APPROACHES = approaches_for(SLUG)


@pytest.mark.parametrize("approach", APPROACHES)
@pytest.mark.parametrize("case", contract_cases(SLUG))
def test_solves_every_contract_case(approach: str, case: dict) -> None:
    solve = get_solution(SLUG, approach=approach)
    assert solve(case["input"]["nums"], case["input"]["target"]) == case["expected"]


@pytest.mark.parametrize("approach", APPROACHES)
@pytest.mark.parametrize("case", contract_cases(SLUG, "notFoundCases"))
def test_raises_when_no_pair_exists(approach: str, case: dict) -> None:
    solve = get_solution(SLUG, approach=approach)
    with pytest.raises(NoSolutionError):
        solve(case["input"]["nums"], case["input"]["target"])


@pytest.mark.parametrize("case", contract_cases(SLUG))
def test_all_approaches_agree(case: dict) -> None:
    """Differential test: every approach must return the identical answer.

    This is the test that makes adding a new approach cheap and safe — it is automatically
    compared against the ones already trusted.
    """
    results = {
        approach: get_solution(SLUG, approach=approach)(
            case["input"]["nums"], case["input"]["target"]
        )
        for approach in APPROACHES
    }
    assert len(set(map(tuple, results.values()))) == 1, results
