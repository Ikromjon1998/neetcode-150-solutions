"""Test fixtures for the FastAPI app.

`TestClient` drives the real ASGI application in-process — real routing, real validation,
real exception handlers, no network. It is the Python counterpart of `supertest` against a
NestJS `INestApplication` and of Laravel's `$this->postJson()`.
"""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any

import pytest
from fastapi.testclient import TestClient
from neetcode_core import cases

from neetcode_api.main import create_app


@pytest.fixture(scope="session")
def client() -> Iterator[TestClient]:
    with TestClient(create_app()) as test_client:
        yield test_client


def contract_cases(slug: str, section: str = "cases") -> list[Any]:
    return [
        pytest.param(case, id=case["name"].replace(" ", "-"))
        for case in cases(slug, section)
    ]
