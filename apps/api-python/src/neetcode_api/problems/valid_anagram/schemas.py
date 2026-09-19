"""Request model for `POST /problems/valid-anagram`.

Strict scalar types on purpose: lax Pydantic would coerce the JSON string `"7"` to `7`, and
this endpoint would then disagree with the NestJS one, where `@IsInt()` rejects it.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictInt, StrictStr  # noqa: F401


class ValidAnagramRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    s: StrictStr = Field(description="TODO: what this field means.")
    t: StrictStr = Field(description="TODO: what this field means.")
