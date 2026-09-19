"""Liveness endpoint. Mirrors Laravel's built-in `/up` and the NestJS `/health` controller."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends
from neetcode_core import registered_slugs

from neetcode_api.config import Settings, get_settings

router = APIRouter(tags=["meta"])


@router.get("/health", summary="Liveness probe")
async def health(settings: Annotated[Settings, Depends(get_settings)]) -> dict[str, object]:
    return {
        "status": "ok",
        "runtime": "python/fastapi",
        "version": settings.version,
        "problemsRegistered": len(registered_slugs()),
    }
