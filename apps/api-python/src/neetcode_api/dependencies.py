"""FastAPI dependency providers.

FastAPI's `Depends` is a function-level injector: it resolves by *call signature*, not by a
type registry. Contrast with NestJS (constructor injection driven by decorator metadata) and
Laravel (a container that autowires from type hints). Same goal, three quite different
mechanisms — `docs/06-language-comparison.md` walks through it.

Note the missing `from __future__ import annotations` at the top of this file, and leave it
missing. That import turns every annotation into a string, and FastAPI has to evaluate the
`Annotated[...]` below to build the OpenAPI schema. Inside a closure the names it would need
(`Query`, `available`) are locals that no longer exist by then, so Pydantic raises
`PydanticUserError: ... is not fully defined`. Deferred annotations and dependency factories
do not mix.
"""

from typing import Annotated

from fastapi import Query
from neetcode_core import approaches_for, get_meta
from neetcode_core.errors import UnknownApproachError


def approach_provider(slug: str):
    """Build a dependency that validates the `?approach=` query parameter.

    Returning a closure keeps the validation in one place while still letting each router
    advertise its own valid keys — and only its own — in the generated OpenAPI schema.
    """
    available = approaches_for(slug)
    default = get_meta(slug).default_approach.key

    def provide(
        approach: Annotated[
            str,
            Query(
                description=f"Which implementation to run. One of: {', '.join(available)}.",
                examples=list(available),
            ),
        ] = default,
    ) -> str:
        if approach not in available:
            raise UnknownApproachError(slug, approach, available)
        return approach

    return provide
