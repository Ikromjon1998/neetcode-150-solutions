"""HTTP surface for problem 1.

Every problem module in this app looks exactly like this file: a router, a dependency for the
approach, a service call, and the shared envelope. That regularity is the point — it makes
adding problem 2 a copy-paste-and-rename job, and it is mirrored one-for-one by the NestJS
controller and the Laravel controller.
"""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, status
from neetcode_core import get_meta

from neetcode_api.dependencies import approach_provider
from neetcode_api.http_status import UNPROCESSABLE_CONTENT
from neetcode_api.problems.two_sum.schemas import TwoSumRequest
from neetcode_api.problems.two_sum.service import SLUG, TwoSumService
from neetcode_api.schemas import ErrorResponse, SolveResponse

router = APIRouter(prefix="/problems", tags=["arrays-and-hashing"])


@router.post(
    f"/{SLUG}",
    summary="Solve Two Sum",
    description=(
        "Returns the indices of the two numbers that add up to `target`. "
        "Use `?approach=brute-force` to run the O(n^2) baseline instead of the default "
        "O(n) hash-map implementation."
    ),
    response_model=SolveResponse[list[int]],
    response_model_by_alias=True,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorResponse,
            "description": "No pair sums to target.",
        },
        UNPROCESSABLE_CONTENT: {"model": ErrorResponse, "description": "Invalid input."},
    },
)
async def solve_two_sum(
    payload: TwoSumRequest,
    approach: Annotated[str, Depends(approach_provider(SLUG))],
    service: Annotated[
        TwoSumService, Depends(TwoSumService)
    ],
) -> SolveResponse[list[int]]:
    indices, elapsed = service.solve(payload.nums, payload.target, approach)
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
        result=indices,
        elapsedMicros=elapsed,
    )
