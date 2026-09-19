"""`POST /problems/two-sum`, driven by the shared JSON contract.

The identical case list is asserted by `apps/api-node/test/two-sum.e2e-spec.ts` and by
`apps/api-php/tests/Feature/TwoSumTest.php`. If the three apps ever disagree about a payload,
one of the three suites goes red.
"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient
from neetcode_core import approaches_for
from tests.conftest import contract_cases

SLUG = "two-sum"
URL = f"/problems/{SLUG}"
APPROACHES = approaches_for(SLUG)


@pytest.mark.parametrize("approach", APPROACHES)
@pytest.mark.parametrize("case", contract_cases(SLUG))
def test_solves_contract_cases(client: TestClient, approach: str, case: dict) -> None:
    response = client.post(URL, json=case["input"], params={"approach": approach})
    assert response.status_code == 200, response.text
    body = response.json()
    assert body["result"] == case["expected"]
    assert body["problem"] == SLUG
    assert body["approach"]["key"] == approach
    assert body["input"] == case["input"]
    assert isinstance(body["elapsedMicros"], int)


@pytest.mark.parametrize("case", contract_cases(SLUG))
def test_default_approach_used_when_query_omitted(client: TestClient, case: dict) -> None:
    response = client.post(URL, json=case["input"])
    assert response.status_code == 200
    assert response.json()["approach"]["key"] == "hash-map"


@pytest.mark.parametrize("case", contract_cases(SLUG, "validationCases"))
def test_invalid_input_is_422(client: TestClient, case: dict) -> None:
    response = client.post(URL, json=case["input"])
    assert response.status_code == case["status"], response.text
    error = response.json()["error"]
    assert error["type"] == "validation_error"
    assert error["details"], "a validation failure must say which field was wrong"


@pytest.mark.parametrize("case", contract_cases(SLUG, "notFoundCases"))
def test_no_solution_is_404(client: TestClient, case: dict) -> None:
    response = client.post(URL, json=case["input"])
    assert response.status_code == 404
    assert response.json()["error"]["type"] == "no_solution"


def test_unknown_approach_is_422(client: TestClient) -> None:
    response = client.post(URL, json={"nums": [2, 7], "target": 9}, params={"approach": "nope"})
    assert response.status_code == 422
    assert response.json()["error"]["type"] == "unknown_approach"


def test_unexpected_field_is_rejected(client: TestClient) -> None:
    """`extra="forbid"` — a typo'd field name is a bug, not something to silently ignore."""
    response = client.post(URL, json={"nums": [2, 7], "target": 9, "targett": 9})
    assert response.status_code == 422
