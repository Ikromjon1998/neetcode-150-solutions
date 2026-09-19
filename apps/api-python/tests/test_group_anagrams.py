"""`POST /problems/group-anagrams`, driven by the shared JSON contract."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient
from neetcode_core import approaches_for
from tests.conftest import contract_cases

SLUG = "group-anagrams"
URL = f"/problems/{SLUG}"


@pytest.mark.parametrize("approach", approaches_for(SLUG))
@pytest.mark.parametrize("case", contract_cases(SLUG))
def test_solves_contract_cases(client: TestClient, approach: str, case: dict) -> None:
    response = client.post(URL, json=case["input"], params={"approach": approach})
    assert response.status_code == 200, response.text
    assert response.json()["result"] == case["expected"]


@pytest.mark.parametrize("case", contract_cases(SLUG, "validationCases"))
def test_invalid_input_is_422(client: TestClient, case: dict) -> None:
    response = client.post(URL, json=case["input"])
    assert response.status_code == case["status"], response.text
    assert response.json()["error"]["type"] == "validation_error"
