"""Endpoints that exist regardless of which problems are solved."""

from __future__ import annotations

from fastapi.testclient import TestClient
from neetcode_core import all_meta


def test_health(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["runtime"] == "python/fastapi"
    assert body["problemsRegistered"] == len(all_meta())


def test_catalog_lists_every_registered_problem(client: TestClient) -> None:
    response = client.get("/problems")
    assert response.status_code == 200
    payload = response.json()
    assert {item["slug"] for item in payload} == {meta.slug for meta in all_meta()}
    for item in payload:
        assert item["endpoint"] == f"/problems/{item['slug']}"
        assert item["approaches"], "every problem must expose at least one approach"


def test_catalog_entry_matches_the_contract(client: TestClient) -> None:
    body = client.get("/problems/two-sum").json()
    assert body["id"] == 1
    assert body["title"] == "Two Sum"
    assert body["difficulty"] == "easy"
    assert body["topic"] == "arrays-and-hashing"
    assert {a["key"] for a in body["approaches"]} == {"brute-force", "hash-map"}


def test_unknown_problem_is_404(client: TestClient) -> None:
    response = client.get("/problems/not-a-real-problem")
    assert response.status_code == 404
    assert response.json()["error"]["type"] == "unknown_problem"


def test_openapi_schema_is_generated(client: TestClient) -> None:
    """Free in FastAPI; the NestJS app needs @nestjs/swagger to match this."""
    schema = client.get("/openapi.json").json()
    assert "/problems/two-sum" in schema["paths"]
    assert "post" in schema["paths"]["/problems/two-sum"]
