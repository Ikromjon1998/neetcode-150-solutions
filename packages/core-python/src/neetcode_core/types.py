"""Value objects shared by every problem.

Nothing here knows about HTTP, FastAPI, or any framework. That separation is the whole
point of this package: the algorithms stay testable in isolation and the apps stay thin.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum


class Difficulty(StrEnum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class Topic(StrEnum):
    """The eighteen NeetCode 150 topics, in roadmap order."""

    ARRAYS_AND_HASHING = "arrays-and-hashing"
    TWO_POINTERS = "two-pointers"
    SLIDING_WINDOW = "sliding-window"
    STACK = "stack"
    BINARY_SEARCH = "binary-search"
    LINKED_LIST = "linked-list"
    TREES = "trees"
    TRIES = "tries"
    HEAP_PRIORITY_QUEUE = "heap-priority-queue"
    BACKTRACKING = "backtracking"
    GRAPHS = "graphs"
    ADVANCED_GRAPHS = "advanced-graphs"
    DP_1D = "1d-dynamic-programming"
    DP_2D = "2d-dynamic-programming"
    GREEDY = "greedy"
    INTERVALS = "intervals"
    MATH_AND_GEOMETRY = "math-and-geometry"
    BIT_MANIPULATION = "bit-manipulation"


@dataclass(frozen=True, slots=True)
class Approach:
    """One implemented way of solving a problem, with its cost."""

    key: str
    name: str
    time: str
    space: str
    note: str | None = None
    default: bool = False


@dataclass(frozen=True, slots=True)
class ProblemMeta:
    """Everything descriptive about a problem. Loaded from the shared JSON contract."""

    id: int
    slug: str
    title: str
    difficulty: Difficulty
    topic: Topic
    summary: str
    approaches: tuple[Approach, ...]
    leetcode_url: str | None = None
    neetcode_url: str | None = None

    @property
    def default_approach(self) -> Approach:
        for approach in self.approaches:
            if approach.default:
                return approach
        return self.approaches[0]

    def approach(self, key: str) -> Approach:
        for approach in self.approaches:
            if approach.key == key:
                return approach
        raise KeyError(key)


@dataclass(frozen=True, slots=True)
class TestCase:
    """A single happy-path case lifted straight out of the JSON contract."""

    name: str
    input: dict[str, object] = field(default_factory=dict)
    expected: object = None
