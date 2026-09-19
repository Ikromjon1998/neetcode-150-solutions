"""Application service for Two Sum.

The service is the seam between HTTP and the algorithm. It holds no request objects and no
response objects — it takes plain values and returns plain values, which is what lets the
same logic be reused by a CLI or a background job later.
"""

from __future__ import annotations

from neetcode_core import get_solution

from neetcode_api.timing import timed

SLUG = "two-sum"


class TwoSumService:
    """Injected per-request by FastAPI's `Depends`.

    Stateless, so a single shared instance would work equally well. It is a class rather than
    a bare function so that the shape matches the NestJS `@Injectable()` service and the
    Laravel service class — the point of this repo is to compare like with like.
    """

    def solve(self, nums: list[int], target: int, approach: str) -> tuple[list[int], int]:
        """Return `(indices, elapsed_microseconds)`.

        Raises `NoSolutionError` when no pair exists; the exception handler turns that into a
        404. The service never mentions status codes.
        """
        algorithm = get_solution(SLUG, approach=approach)
        return timed(algorithm, nums, target)
