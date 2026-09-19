"""HTTP surface for problem 238."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, status
from neetcode_core import get_meta

from neetcode_api.dependencies import approach_provider
from neetcode_api.http_status import UNPROCESSABLE_CONTENT
from neetcode_api.problems.product_of_array_except_self.schemas import (
    ProductOfArrayExceptSelfRequest,
)
from neetcode_api.problems.product_of_array_except_self.service import (
    SLUG,
    ProductOfArrayExceptSelfService,
)
from neetcode_api.schemas import ErrorResponse, SolveResponse

router = APIRouter(prefix="/problems", tags=["arrays-and-hashing"])


@router.post(
    f"/{SLUG}",
    summary="Solve Product of Array Except Self",
    response_model=SolveResponse[list[int]],
    response_model_by_alias=True,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponse},
        UNPROCESSABLE_CONTENT: {"model": ErrorResponse},
    },
)
async def solve(
    payload: ProductOfArrayExceptSelfRequest,
    approach: Annotated[str, Depends(approach_provider(SLUG))],
    service: Annotated[
        ProductOfArrayExceptSelfService, Depends(ProductOfArrayExceptSelfService)
    ],
) -> SolveResponse[list[int]]:
    result, elapsed = service.solve(payload.nums, approach)
    chosen = get_meta(SLUG).approach(approach)
    return SolveResponse[list[int]](
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
