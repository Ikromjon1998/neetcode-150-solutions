"""Response shapes shared by every problem endpoint.

The envelope is byte-for-byte identical in the NestJS and Laravel apps. That is what makes
the three implementations comparable: you can point the same HTTP client at port 8000, 3000
or 8080 and diff the JSON.
"""

from __future__ import annotations

from typing import Any, Generic, Literal, TypeVar

from pydantic import BaseModel, ConfigDict, Field

T = TypeVar("T")


class ApproachInfo(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    key: str = Field(examples=["hash-map"])
    name: str = Field(examples=["One-pass hash map"])
    time: str = Field(description="Big-O time complexity.", examples=["O(n)"])
    space: str = Field(description="Big-O auxiliary space.", examples=["O(n)"])
    note: str | None = None
    is_default: bool = Field(default=False, alias="default")


class ProblemSummary(BaseModel):
    """The catalog entry for one problem."""

    model_config = ConfigDict(populate_by_name=True)

    id: int = Field(examples=[1])
    slug: str = Field(examples=["two-sum"])
    title: str = Field(examples=["Two Sum"])
    difficulty: Literal["easy", "medium", "hard"]
    topic: str = Field(examples=["arrays-and-hashing"])
    summary: str
    approaches: list[ApproachInfo]
    leetcode_url: str | None = Field(default=None, alias="leetcodeUrl")
    neetcode_url: str | None = Field(default=None, alias="neetcodeUrl")
    endpoint: str = Field(description="Where to POST input.", examples=["/problems/two-sum"])


class SolveResponse(BaseModel, Generic[T]):
    """The envelope returned by every `POST /problems/{slug}` endpoint."""

    model_config = ConfigDict(populate_by_name=True)

    problem: str = Field(examples=["two-sum"])
    approach: ApproachInfo
    input: dict[str, Any]
    result: T
    elapsed_micros: int = Field(
        alias="elapsedMicros",
        description="Wall-clock time spent inside the algorithm only — routing, validation "
        "and serialisation are excluded, so the number is comparable across the three apps.",
    )


class ErrorDetail(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    type: str = Field(examples=["no_solution"])
    message: str
    problem: str | None = None
    details: list[dict[str, Any]] | None = None


class ErrorResponse(BaseModel):
    """Every non-2xx response in all three apps has exactly this shape."""

    error: ErrorDetail
