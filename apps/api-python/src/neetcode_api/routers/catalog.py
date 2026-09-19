"""Catalog endpoints — the same two routes exist in all three apps.

Everything here is derived from the registry, so a newly added problem appears in the catalog
without anyone editing this file.
"""

from __future__ import annotations

from fastapi import APIRouter, status
from neetcode_core import all_meta, get_meta
from neetcode_core.types import ProblemMeta

from neetcode_api.schemas import ErrorResponse, ProblemSummary

router = APIRouter(prefix="/problems", tags=["catalog"])


def to_summary(meta: ProblemMeta) -> ProblemSummary:
    return ProblemSummary(
        id=meta.id,
        slug=meta.slug,
        title=meta.title,
        difficulty=meta.difficulty.value,
        topic=meta.topic.value,
        summary=meta.summary,
        approaches=[
            {
                "key": a.key,
                "name": a.name,
                "time": a.time,
                "space": a.space,
                "note": a.note,
                "default": a.default,
            }
            for a in meta.approaches
        ],
        leetcodeUrl=meta.leetcode_url,
        neetcodeUrl=meta.neetcode_url,
        endpoint=f"/problems/{meta.slug}",
    )


@router.get("", summary="List every solved problem")
async def list_problems() -> list[ProblemSummary]:
    return [to_summary(meta) for meta in all_meta()]


@router.get(
    "/{slug}",
    summary="Metadata for one problem",
    responses={status.HTTP_404_NOT_FOUND: {"model": ErrorResponse}},
)
async def get_problem(slug: str) -> ProblemSummary:
    return to_summary(get_meta(slug))
