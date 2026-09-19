"""Auto-registration of problem routers.

Mirrors what `neetcode_core.registry` does for algorithms: walk the package, import every
submodule, and collect the `router` each one exports. Adding a problem therefore needs **no
edit to this file and no edit to `main.py`** — create the folder and it is served.

The NestJS app cannot do this (its module graph is static and resolved at compile time, so
`ProblemsModule` lists its imports explicitly), and the Laravel app chooses not to (it reads
an explicit array from `config/neetcode.php` so that `php artisan config:cache` and
`route:cache` can freeze everything at deploy time). Three ecosystems, three honest answers
to the same question — see `docs/06-language-comparison.md`.
"""

from __future__ import annotations

import importlib
import pkgutil

from fastapi import APIRouter


def all_routers() -> list[APIRouter]:
    """Every `router` exported by a subpackage of `neetcode_api.problems`, in import order."""
    routers: list[APIRouter] = []
    for module_info in pkgutil.iter_modules(__path__, prefix=f"{__name__}."):
        if module_info.name.rsplit(".", 1)[-1].startswith("_"):
            continue
        module = importlib.import_module(module_info.name)
        router = getattr(module, "router", None)
        if isinstance(router, APIRouter):
            routers.append(router)
    return routers
