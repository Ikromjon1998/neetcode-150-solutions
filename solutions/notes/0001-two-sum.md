# 1. Two Sum

**Difficulty:** easy · **Topic:** arrays-and-hashing · **Approaches:** brute-force, hash-map
**LeetCode:** https://leetcode.com/problems/two-sum/

## The problem

Given an array of integers and a target, return the indices of the two entries that sum to the
target. Exactly one answer exists, and the same element may not be used twice.

The framing matters: it asks for **indices**, not values. That rules out the sort-then-two-
pointers approach that would otherwise be the obvious O(n log n) improvement, because sorting
destroys the indices you were asked for.

## Approaches

### brute-force — O(n²) time, O(1) space

Two nested loops over every pair. Kept deliberately: it is the baseline the differential test
measures the optimal version against, and on inputs of five or six elements it is genuinely
faster in all three languages because it never allocates.

### hash-map — O(n) time, O(n) space

One pass, remembering every value seen so far.

The trick is to look **backwards for the complement** rather than forwards for the partner. By
the time the second number of the pair is the current element, the first is guaranteed to be
in the map already — so one pass is enough, and you never need a second lookup structure or a
pre-population pass.

```
nums = [2, 7, 11, 15], target = 9

i=0  value=2   complement=7   7 not seen   seen={2:0}
i=1  value=7   complement=2   2 IS seen → return [seen[2], 1] = [0, 1]
```

## What differed between the three languages

**The hash map is where all the difference lives.** The loop structure is identical in all
three; the container is not.

- **Python** — `dict` with `if complement in seen`. Integer keys stay integers, `in` is O(1),
  and there is nothing to think about. The shortest of the three by some margin.

- **TypeScript** — `Map`, and it has to be a `Map`. An object literal coerces its keys to
  strings, so `-0` and `0` would collide, numeric keys get re-parsed on every lookup, and a
  key like `"constructor"` reaches `Object.prototype`. `Map` uses SameValueZero on real
  values. The lookup also returns `number | undefined`, so the check is
  `if (j !== undefined)` — **not** `if (j)`, which would be wrong for index 0. That is the one
  genuine correctness trap in this problem, and only JavaScript has it.

- **PHP** — a plain `array` is the hash map, and integer keys stay integers. `isset()` rather
  than `array_key_exists()` because the stored values are indices and are never null, so the
  faster check is also the correct one. (Had the values been nullable, `isset` would have been
  a bug.)

Nothing else differed. No string handling, no numeric overflow, no iteration subtleties — this
is about as close to a clean three-way comparison as an algorithm gets.

## What differed between the three frameworks

**Validation** was the interesting part, and all three needed adjusting to agree on `{"nums":
[1], "target": 1}` → 422:

| | Tool | Adjustment needed |
|---|---|---|
| FastAPI | Pydantic `list[StrictInt]`, `Field(min_length=2)` | `StrictInt`, or `"7"` coerces to `7` |
| NestJS | `@IsArray() @ArrayMinSize(2) @IsInt({each:true})` | none for types; **`errorHttpStatusCode: 422`**, since Nest defaults to 400 |
| Laravel | `['present', 'array', 'min:2']` + an `is_int` closure | the built-in `integer` rule accepts `"7"` |

**`POST` returns 201 in NestJS.** The single most surprising default of the three. The Two Sum
e2e suite failed on it the first time it ran — twelve tests, all `expected 200 "OK", got 201
"Created"`. `@HttpCode(HttpStatus.OK)` on every solve endpoint.

**Laravel merges the query string into `$request->all()`.** The unexpected-field check in
`TwoSumRequest::prepareForValidation()` originally read `$this->all()`, and every request with
`?approach=hash-map` 422'd because `approach` looked like a stray body field. `$this->json()
->all()` is the body and nothing else.

**Key order is not free.** Laravel's `validated()` returns keys in the order the *rules*
evaluated, not the order they were declared, so the echoed `input` came back as
`{target, nums}` while the other two returned `{nums, target}`. The controller now rebuilds
the echo explicitly. An API's key order should not depend on a validator's internals.

## Where I got stuck

**`if (j)` versus `if (j !== undefined)` in TypeScript.** Nothing caught it in the contract
cases at first, because the first test case happens to return `[0, 1]` and `0` as a *stored*
index is fine — it only breaks when the *complement* was found at index 0. The
`"pair at the front"` case `[2, 7, 11, 15]` does exercise it, and it is the reason that case is
first in the contract.

**The `from __future__ import annotations` failure in FastAPI** cost the most time and had
nothing to do with the algorithm. The `approach_provider` factory returns a closure whose
annotation is `Annotated[str, Query(...)]`; with deferred annotations that becomes a *string*
that FastAPI must evaluate later to build the OpenAPI schema — by which point `Query` and
`available` are locals of a function that has already returned. Error:

```
PydanticUserError: `TypeAdapter[...]` is not fully defined
```

27 of 31 app tests failed at once with what looked like an unrelated Pydantic problem. The fix
is one deleted line, and the file now carries a comment explaining why it must stay deleted.

## Benchmarks

```bash
curl -s 'localhost:8000/problems/two-sum?approach=brute-force' \
  -H 'content-type: application/json' -d '{"nums":[2,7,11,15],"target":9}' | jq .elapsedMicros
```

Four elements — far too small for the asymptotics to show, which is itself the lesson:

| Approach | Python | TypeScript | PHP |
|----------|--------|------------|-----|
| brute-force | ~2 µs | ~24 µs | ~1 µs |
| hash-map | ~2 µs | ~16 µs | ~1 µs |

The Node numbers are a cold JIT, not a language verdict; they converge with the others after a
few hundred requests. At n=4 the brute force allocates nothing while the hash map builds a
`Map`, so the O(n²) version is competitive or better in every language. Swap in a
10,000-element array and the ordering inverts — which is the point of shipping both.
