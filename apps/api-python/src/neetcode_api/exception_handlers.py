"""One place where domain errors become HTTP status codes.

The core package raises `NoSolutionError`; it has no idea that 404 exists. The translation
happens here and only here, which is why the same algorithms can sit behind a CLI, a queue
worker or these three web apps without modification.

Status codes are pinned to match the NestJS and Laravel apps exactly:

| Situation                      | Status | `error.type`         |
|--------------------------------|--------|----------------------|
| Body fails validation          | 422    | `validation_error`   |
| Unknown `?approach=`           | 422    | `unknown_approach`   |
| Unknown problem slug           | 404    | `unknown_problem`    |
| Valid input, no answer exists  | 404    | `no_solution`        |
| Approach not implemented yet   | 501    | `not_implemented`    |

FastAPI already returns 422 for body validation; NestJS returns 400 out of the box and
Laravel returns 422 only when the request wants JSON. Both are reconfigured to match.
"""

from __future__ import annotations

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from neetcode_core.errors import (
    NoSolutionError,
    UnknownApproachError,
    UnknownProblemError,
    UnsolvedError,
)

from neetcode_api.http_status import UNPROCESSABLE_CONTENT


def _error(status_code: int, type_: str, message: str, **extra: object) -> JSONResponse:
    payload: dict[str, object] = {"type": type_, "message": message}
    payload.update({key: value for key, value in extra.items() if value is not None})
    return JSONResponse(status_code=status_code, content={"error": payload})


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(RequestValidationError)
    async def _validation(_: Request, exc: RequestValidationError) -> JSONResponse:
        details = [
            {
                "field": ".".join(str(part) for part in err["loc"][1:]) or "body",
                "message": err["msg"],
            }
            for err in exc.errors()
        ]
        return _error(
            UNPROCESSABLE_CONTENT,
            "validation_error",
            "The request body failed validation.",
            details=details,
        )

    @app.exception_handler(UnsolvedError)
    async def _unsolved(_: Request, exc: UnsolvedError) -> JSONResponse:
        """A stub was hit. This is the expected state of an unsolved exercise, not a bug."""
        return _error(
            status.HTTP_501_NOT_IMPLEMENTED,
            "not_implemented",
            f"{exc.slug} / {exc.approach} is an exercise you have not solved yet.",
            problem=exc.slug,
            details=[{"field": "approach", "message": f"Write your solution in {exc.path}"}],
        )

    @app.exception_handler(NoSolutionError)
    async def _no_solution(_: Request, exc: NoSolutionError) -> JSONResponse:
        return _error(status.HTTP_404_NOT_FOUND, "no_solution", exc.detail, problem=exc.slug)

    @app.exception_handler(UnknownProblemError)
    async def _unknown_problem(_: Request, exc: UnknownProblemError) -> JSONResponse:
        return _error(status.HTTP_404_NOT_FOUND, "unknown_problem", str(exc), problem=exc.slug)

    @app.exception_handler(UnknownApproachError)
    async def _unknown_approach(_: Request, exc: UnknownApproachError) -> JSONResponse:
        return _error(
            UNPROCESSABLE_CONTENT,
            "unknown_approach",
            str(exc),
            problem=exc.slug,
            details=[{"field": "approach", "message": f"Available: {', '.join(exc.available)}"}],
        )
