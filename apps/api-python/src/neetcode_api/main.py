"""FastAPI application factory.

Run it:

    make run-python                       # from the repo root
    uvicorn neetcode_api.main:app --reload --port 8000

Then open http://localhost:8000/docs — FastAPI generates that Swagger UI from the Pydantic
models for free. The NestJS app needs `@nestjs/swagger` decorators to reach parity, and the
Laravel app has no equivalent at all without a third-party package. That difference is one of
the more practical things this repo demonstrates.
"""

from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from neetcode_core import discover, verify_registry

from neetcode_api.config import Settings, get_settings
from neetcode_api.exception_handlers import register_exception_handlers
from neetcode_api.problems import all_routers
from neetcode_api.routers import catalog, health


@asynccontextmanager
async def lifespan(_: FastAPI):
    """Startup/shutdown hook.

    `verify_registry()` fails the boot if a contract declares an approach nobody implemented.
    Failing at startup rather than on the first request is the whole reason to do this here:
    a container that cannot serve correct answers should never pass its readiness check.
    """
    discover()
    verify_registry()
    yield


def create_app(settings: Settings | None = None) -> FastAPI:
    """Application factory — lets tests build an isolated app with overridden settings."""
    settings = settings or get_settings()

    app = FastAPI(
        title=settings.app_name,
        version=settings.version,
        summary="NeetCode 150 solutions, served as a real API.",
        description=(
            "Each solved problem is a feature module: a router, a validated request DTO, a "
            "service, and tests driven by the shared JSON contract in `packages/contracts`. "
            "The algorithms themselves live in the dependency-free `neetcode-core` package."
        ),
        docs_url=settings.docs_url,
        openapi_url=settings.openapi_url,
        lifespan=lifespan,
    )

    register_exception_handlers(app)
    app.include_router(health.router)
    app.include_router(catalog.router)
    for router in all_routers():
        app.include_router(router)

    return app


app = create_app()
