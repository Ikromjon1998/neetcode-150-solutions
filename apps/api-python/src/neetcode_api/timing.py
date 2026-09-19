"""A stopwatch scoped to the algorithm call only."""

from __future__ import annotations

import time
from collections.abc import Callable
from typing import Any, ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")


def timed(fn: Callable[P, R], *args: Any, **kwargs: Any) -> tuple[R, int]:
    """Run `fn` and return `(result, elapsed_microseconds)`.

    `perf_counter_ns` rather than `time()`: it is monotonic and has nanosecond resolution,
    which matters because the fast path of an O(n) solution on a six-element list finishes in
    well under a microsecond.
    """
    start = time.perf_counter_ns()
    result = fn(*args, **kwargs)
    return result, (time.perf_counter_ns() - start) // 1_000
