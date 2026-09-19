"""HTTP surface for problem 271."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, status
from neetcode_core import get_meta

from neetcode_api.dependencies import approach_provider
from neetcode_api.http_status import UNPROCESSABLE_CONTENT
from neetcode_api.problems.encode_and_decode_strings.schemas import EncodeAndDecodeStringsRequest
from neetcode_api.problems.encode_and_decode_strings.service import (
    SLUG,
    EncodeAndDecodeStringsService,
)
from neetcode_api.schemas import ErrorResponse, SolveResponse

router = APIRouter(prefix="/problems", tags=["arrays-and-hashing"])


@router.post(
    f"/{SLUG}",
    summary="Solve Encode and Decode Strings",
    response_model=SolveResponse[list[str]],
    response_model_by_alias=True,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponse},
        UNPROCESSABLE_CONTENT: {"model": ErrorResponse},
    },
)
async def solve(
    payload: EncodeAndDecodeStringsRequest,
    approach: Annotated[str, Depends(approach_provider(SLUG))],
    service: Annotated[
        EncodeAndDecodeStringsService, Depends(EncodeAndDecodeStringsService)
    ],
) -> SolveResponse[list[str]]:
    result, elapsed = service.solve(payload.strs, approach)
    chosen = get_meta(SLUG).approach(approach)
    return SolveResponse[list[str]](
        problem=SLUG,
        approach={
            "key": chosen.key,
            "name": chosen.name,
            "time": chosen.time,
            "space": chosen.space,
            "note": chosen.note,
            "default": chosen.default,
        },
        input=payload.model_dump(),
        result=result,
        elapsedMicros=elapsed,
    )
