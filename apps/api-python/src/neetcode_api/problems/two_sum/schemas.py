"""Request/response models for `POST /problems/two-sum`.

`StrictInt` rather than `int` is a deliberate choice at the API boundary. In its default lax
mode Pydantic would happily coerce the JSON string `"7"` into `7`, and the endpoint would
then disagree with the NestJS one (`class-validator`'s `@IsInt()` rejects it outright). Being
strict here keeps all three apps answering identically for the same payload.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, StrictInt


class TwoSumRequest(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        json_schema_extra={"examples": [{"nums": [2, 7, 11, 15], "target": 9}]},
    )

    nums: list[StrictInt] = Field(
        min_length=2,
        description="At least two integers. The problem is undefined for shorter input.",
    )
    target: StrictInt = Field(description="The sum the two chosen numbers must produce.")


class TwoSumResult(BaseModel):
    """The two indices, ascending."""

    indices: list[int] = Field(min_length=2, max_length=2, examples=[[0, 1]])
