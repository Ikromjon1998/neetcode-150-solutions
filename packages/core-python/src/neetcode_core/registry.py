"""Problem registry with import-time auto-discovery.

This is the Python answer to "how does the app find the solutions?", and it is deliberately
different from how the TypeScript and PHP sides do it:

* **Python (here)** — a decorator registers each function as a side effect of importing its
  module, and `discover()` walks the package with `pkgutil` to import every module. Drop a
  new file into a topic folder and it appears in the API with no registration step at all.
* **TypeScript** — an explicit barrel file. The dependency graph is static, so the bundler
  and the type-checker can both see it; the trade-off is that you must add one import line.
* **PHP/Laravel** — a service provider reads a config array and binds a registry singleton,
  which is what lets `php artisan config:cache` freeze the whole thing at deploy time.

None of the three is "best". See `docs/06-language-comparison.md` for why each ecosystem
landed where it did.
"""

from __future__ import annotations

import importlib
import pkgutil
import threading
from collections.abc import Callable
from typing import Any, TypeVar

from neetcode_core.contracts import load_meta
from neetcode_core.errors import UnknownApproachError, UnknownProblemError
from neetcode_core.types import ProblemMeta

SolutionFn = Callable[..., Any]
F = TypeVar("F", bound=SolutionFn)

# slug -> approach key -> implementation
_SOLUTIONS: dict[str, dict[str, SolutionFn]] = {}
_discovered = False
_lock = threading.Lock()


def solution(slug: str, *, approach: str) -> Callable[[F], F]:
    """Register a function as the `approach` implementation of problem `slug`.

    The decorator returns the function untouched, so a registered solution stays an ordinary
    callable you can import and unit-test directly:

        from neetcode_core.arrays_and_hashing.two_sum import two_sum_hash_map
        two_sum_hash_map([2, 7, 11, 15], 9)  # -> [0, 1]
    """

    def decorate(fn: F) -> F:
        bucket = _SOLUTIONS.setdefault(slug, {})
        if approach in bucket:
            raise ValueError(
                f"Approach {approach!r} is already registered for {slug!r} "
                f"by {bucket[approach].__module__}.{bucket[approach].__qualname__}"
            )
        bucket[approach] = fn
        return fn

    return decorate


def discover(force: bool = False) -> None:
    """Import every submodule of `neetcode_core` so the decorators run.

    Idempotent and thread-safe: the apps call it once at startup, the tests call it freely.
    """
    global _discovered
    with _lock:
        if _discovered and not force:
            return
        package = importlib.import_module("neetcode_core")
        for module in pkgutil.walk_packages(package.__path__, prefix=f"{package.__name__}."):
            if module.name.rsplit(".", 1)[-1].startswith("_"):
                continue
            importlib.import_module(module.name)
        _discovered = True


def registered_slugs() -> tuple[str, ...]:
    discover()
    return tuple(sorted(_SOLUTIONS, key=lambda slug: load_meta(slug).id))


def all_meta() -> tuple[ProblemMeta, ...]:
    """Metadata for every registered problem, ordered by LeetCode id."""
    return tuple(load_meta(slug) for slug in registered_slugs())


def get_meta(slug: str) -> ProblemMeta:
    discover()
    if slug not in _SOLUTIONS:
        raise UnknownProblemError(slug)
    return load_meta(slug)


def approaches_for(slug: str) -> tuple[str, ...]:
    discover()
    if slug not in _SOLUTIONS:
        raise UnknownProblemError(slug)
    return tuple(_SOLUTIONS[slug])


def get_solution(slug: str, approach: str | None = None) -> SolutionFn:
    """Look up one implementation. `approach=None` picks the contract's default."""
    discover()
    if slug not in _SOLUTIONS:
        raise UnknownProblemError(slug)
    bucket = _SOLUTIONS[slug]
    key = approach or load_meta(slug).default_approach.key
    if key not in bucket:
        raise UnknownApproachError(slug, key, tuple(bucket))
    return bucket[key]


def verify_registry() -> None:
    """Fail loudly if code and contracts have drifted apart.

    Called by a test and by each app at boot. It catches the two mistakes that are easy to
    make when adding a problem: implementing an approach you forgot to declare in the JSON,
    or declaring one you forgot to implement.
    """
    discover()
    problems = []
    for slug, bucket in _SOLUTIONS.items():
        meta = load_meta(slug)
        declared = {approach.key for approach in meta.approaches}
        implemented = set(bucket)
        if missing := declared - implemented:
            problems.append(f"{slug}: declared in contract but not implemented: {sorted(missing)}")
        if extra := implemented - declared:
            problems.append(f"{slug}: implemented but not declared in contract: {sorted(extra)}")
        defaults = [a.key for a in meta.approaches if a.default]
        if len(defaults) > 1:
            problems.append(f"{slug}: more than one default approach: {defaults}")
    if problems:
        raise RuntimeError("Registry does not match contracts:\n  - " + "\n  - ".join(problems))
