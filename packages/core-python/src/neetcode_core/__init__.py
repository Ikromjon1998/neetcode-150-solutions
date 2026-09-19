"""NeetCode algorithms as a real, installable Python package.

Public surface — import from here, not from the submodules, in application code:

    from neetcode_core import all_meta, get_solution, NoSolutionError

    solve = get_solution("two-sum", approach="hash-map")
    solve([2, 7, 11, 15], 9)  # -> [0, 1]
"""

from neetcode_core.contracts import all_slugs, cases, load_meta, raw_contract
from neetcode_core.errors import (
    NeetCodeError,
    NoSolutionError,
    UnknownApproachError,
    UnknownProblemError,
    UnsolvedError,
)
from neetcode_core.registry import (
    all_meta,
    approaches_for,
    discover,
    get_meta,
    get_solution,
    registered_slugs,
    solution,
    verify_registry,
)
from neetcode_core.types import Approach, Difficulty, ProblemMeta, TestCase, Topic

__version__ = "1.0.0"

__all__ = [
    "Approach",
    "Difficulty",
    "NeetCodeError",
    "NoSolutionError",
    "ProblemMeta",
    "TestCase",
    "Topic",
    "UnknownApproachError",
    "UnknownProblemError",
    "UnsolvedError",
    "all_meta",
    "all_slugs",
    "approaches_for",
    "cases",
    "discover",
    "get_meta",
    "get_solution",
    "load_meta",
    "raw_contract",
    "registered_slugs",
    "solution",
    "verify_registry",
]
