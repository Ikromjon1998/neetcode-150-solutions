"""Domain errors.

These are raised by the pure algorithms. Each application maps them to an HTTP status in
exactly one place — see the exception handlers in `apps/api-python` and the equivalents in
the NestJS and Laravel apps. The algorithms themselves never mention HTTP.
"""

from __future__ import annotations


class NeetCodeError(Exception):
    """Base class, so an app can catch everything this package throws with one handler."""


class NoSolutionError(NeetCodeError):
    """Input was well formed but no answer exists.

    Distinct from invalid input: `[1, 2, 3]` with target `100` is a perfectly legal request
    that simply has no answer. Apps render this as 404, not 422.
    """

    def __init__(self, slug: str, detail: str = "No solution exists for the given input.") -> None:
        self.slug = slug
        self.detail = detail
        super().__init__(f"{slug}: {detail}")


class UnknownProblemError(NeetCodeError):
    """No problem is registered under that slug."""

    def __init__(self, slug: str) -> None:
        self.slug = slug
        super().__init__(f"Unknown problem: {slug!r}")


class UnknownApproachError(NeetCodeError):
    """The problem exists but has no implementation registered under that approach key."""

    def __init__(self, slug: str, approach: str, available: tuple[str, ...] = ()) -> None:
        self.slug = slug
        self.approach = approach
        self.available = available
        hint = f" Available: {', '.join(available)}." if available else ""
        super().__init__(f"Unknown approach {approach!r} for problem {slug!r}.{hint}")


class UnsolvedError(NeetCodeError):
    """This approach has not been implemented yet — it is still an exercise.

    Raised by every stub. Distinct from a crash: it is the expected state of a freshly cloned
    repository, and it carries the path of the file you are meant to edit. The apps render it
    as `501 Not Implemented` rather than a 500, so hitting the endpoint tells you where to go.
    """

    def __init__(self, slug: str, approach: str, path: str) -> None:
        self.slug = slug
        self.approach = approach
        self.path = path
        super().__init__(
            f"{slug} / {approach} is not implemented yet. Write it in {path}"
        )
