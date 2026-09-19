# `neetcode-core` (Python)

The algorithms, and nothing else. This package has **zero runtime dependencies** — no FastAPI,
no Pydantic, no HTTP. That is deliberate: it means every solution is a plain function you can
import in a REPL, and it means the FastAPI app can be rewritten or thrown away without
touching a single line of algorithm code.

## Install

From the repo root, into the shared virtualenv:

```bash
make setup-python
```

Or directly:

```bash
pip install -e "packages/core-python[dev]"
```

## Use

```python
from neetcode_core import get_solution, all_meta, NoSolutionError

solve = get_solution("two-sum", approach="hash-map")
solve([2, 7, 11, 15], 9)          # -> [0, 1]

get_solution("two-sum")           # default approach from the JSON contract
[m.slug for m in all_meta()]      # -> ['two-sum', ...]
```

Or import the function directly, which is what the unit tests for a single approach do:

```python
from neetcode_core.arrays_and_hashing.two_sum import two_sum_hash_map
```

## Layout

```
src/neetcode_core/
  __init__.py          public surface — apps import from here
  types.py             ProblemMeta, Approach, Difficulty, Topic
  errors.py            NoSolutionError & friends (no HTTP status codes in sight)
  contracts.py         loads packages/contracts/problems/*.json
  registry.py          @solution decorator + pkgutil auto-discovery
  arrays_and_hashing/
    two_sum.py         one module per problem
tests/
  test_registry.py     guards that run against every problem
  arrays_and_hashing/
    test_two_sum.py    contract-driven, no hand-written fixtures
```

## How discovery works

`@solution("two-sum", approach="hash-map")` registers the function as an import side effect.
`discover()` then walks the package with `pkgutil.walk_packages` and imports everything, so a
new file in a topic folder shows up in the API with **no registration step**.

This is the loosest of the three strategies in this repo — TypeScript uses an explicit barrel
and PHP uses a config array. The trade-offs are written up in
[`docs/06-language-comparison.md`](../../docs/06-language-comparison.md).

## Test

```bash
make test-python          # from the repo root
pytest                    # from this directory
pytest -k two_sum -v      # one problem
```

Tests read their cases from the shared JSON contracts, so they cannot drift from the
TypeScript and PHP suites.
