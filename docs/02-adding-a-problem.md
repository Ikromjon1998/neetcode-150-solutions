# 02 — Adding a problem

This is the **maintainer** workflow: creating a new exercise for other people to solve. If you
want to *solve* an existing one, read its brief in `docs/problems/` instead — you do not need
this page.

Valid Anagram as the worked example. Seven steps, roughly half an hour once you are used to it.

The shape of it: **you solve the problem first, in place, where the tests run. Then one command
turns your answer into an exercise.** There is no separate "write the stub" step, which is what
stops a stub and its answer from ever drifting apart.

---

## Step 0 — decide the shape

Before touching anything, answer four questions:

| Question | Valid Anagram |
|----------|---------------|
| LeetCode id, exact title? | 242, "Valid Anagram" |
| Difficulty and topic? | easy, `arrays-and-hashing` |
| What does the request body look like? | `{"s": "...", "t": "..."}` — two strings |
| Which approaches will you implement? | `sorting` (naive), `hash-map` (optimal) |

**Always implement at least two approaches.** The naive one is not filler: a differential test
asserts every approach returns the identical answer, so the baseline is what validates the
clever version. And the `?approach=` query parameter makes them comparable at runtime.

---

## Step 1 — scaffold

```bash
make new-problem ARGS="--id 242 --slug valid-anagram --title 'Valid Anagram' \
  --difficulty easy --topic arrays-and-hashing \
  --input 's:string,t:string' --returns bool --approaches sorting,hash-map"
```

### The flags

| Flag | Notes |
|------|-------|
| `--id` | LeetCode number. Drives the filename and the catalog sort order. Get it right. |
| `--slug` | kebab-case. Becomes the URL segment in all three apps. |
| `--input` | `name:type,name:type`. Types: `int`, `string`, `bool`, `float`, `int[]`, `string[]`, `int[][]` |
| `--returns` | Same type vocabulary. |
| `--approaches` | kebab-case keys. **The last one becomes the default.** |

### What it writes

27 files. The ones you will actually touch:

```
packages/contracts/problems/0242-valid-anagram.json          ← step 2
packages/core-python/src/neetcode_core/arrays_and_hashing/valid_anagram.py   ← step 3
packages/core-ts/src/arrays-and-hashing/valid-anagram.ts                     ← step 3
packages/core-php/src/ArraysAndHashing/ValidAnagram.php                      ← step 3
docs/problems/0242-valid-anagram.md                          ← step 5
```

And the ones you will not, because they are generated correctly and wired up for you: six test
files, the FastAPI router/schemas/service, the NestJS module/controller/service/DTO, the
Laravel controller/FormRequest, plus entries in `registry.ts`, `index.ts`,
`DefaultProblems.php`, `problems.module.ts` and `routes/api.php`.

Nothing is overwritten. If a run fails halfway, run it again — existing files are reported and
left alone.

---

## Step 2 — fill in the contract

`packages/contracts/problems/0242-valid-anagram.json`. This is the step that matters most,
because every other file reads it.

```jsonc
{
  "id": 242,
  "slug": "valid-anagram",
  "title": "Valid Anagram",
  "difficulty": "easy",
  "topic": "arrays-and-hashing",
  "summary": "Return true when `t` is an anagram of `s` — that is, when both strings contain
              exactly the same characters with exactly the same multiplicities.",
  "approaches": [
    { "key": "sorting",  "name": "Sort both strings",
      "time": "O(n log n)", "space": "O(n)",
      "note": "Two anagrams have the same sorted form. Three lines and obviously correct." },
    { "key": "hash-map", "name": "Character frequency count",
      "time": "O(n)", "space": "O(k)", "default": true,
      "note": "Count in s, decrement for t. O(k) in the alphabet size, not the input length." }
  ],
  "cases": [
    { "name": "classic anagram",           "input": { "s": "anagram", "t": "nagaram" }, "expected": true  },
    { "name": "not an anagram",            "input": { "s": "rat", "t": "car" },         "expected": false },
    { "name": "both empty",                "input": { "s": "", "t": "" },               "expected": true  },
    { "name": "different lengths",         "input": { "s": "a", "t": "ab" },            "expected": false },
    { "name": "same letters wrong counts", "input": { "s": "aacc", "t": "ccac" },       "expected": false },
    { "name": "non-ascii",                 "input": { "s": "héllo", "t": "olléh" },     "expected": true  }
  ],
  "validationCases": [
    { "name": "missing t",         "input": { "s": "abc" },            "status": 422 },
    { "name": "s is not a string", "input": { "s": 1, "t": "a" },      "status": 422 }
  ],
  "notFoundCases": []
}
```

### How to choose cases

Aim for **six or more** happy-path cases, and deliberately include the ones you would forget:

- the empty input
- duplicates
- negative numbers
- the answer at the very start and the very end of the input
- the "almost" case — same elements, wrong counts or wrong order
- non-ASCII, for any string problem (this is the one that catches PHP's byte-wise functions
  and JavaScript's surrogate-pair splitting)

`validationCases` are asserted at the HTTP layer only — validation is the framework's job, not
the algorithm's. `notFoundCases` are well-formed inputs with no answer; the core raises, and
the apps render 404.

### The three sections and who reads them

| Section | Core suites | App suites |
|---------|-------------|------------|
| `cases` | ✅ | ✅ |
| `validationCases` | ✖ (the algorithm never sees invalid input) | ✅ |
| `notFoundCases` | ✅ (asserts the exception) | ✅ (asserts 404) |

---

## Step 3 — implement, three times

The generated files have the signatures, the registration and the docstring skeletons. You
write the bodies.

**Write each one idiomatically for its language.** If all three read identically, you have
learned nothing — that is the failure mode this whole repo exists to avoid.

```python
# packages/core-python/src/neetcode_core/arrays_and_hashing/valid_anagram.py
@solution(SLUG, approach="hash-map")
def valid_anagram_hash_map(s: str, t: str) -> bool:
    if len(s) != len(t):
        return False
    return Counter(s) == Counter(t)          # the stdlib does the work
```

```typescript
// packages/core-ts/src/arrays-and-hashing/valid-anagram.ts
export function validAnagramHashMap(s: string, t: string): boolean {
  if (s.length !== t.length) return false;
  const counts = new Map<string, number>();   // Map, not {} — no prototype collisions
  for (const char of s) counts.set(char, (counts.get(char) ?? 0) + 1);
  for (const char of t) {
    const remaining = counts.get(char);
    if (remaining === undefined || remaining === 0) return false;
    counts.set(char, remaining - 1);
  }
  return true;
}
```

```php
// packages/core-php/src/ArraysAndHashing/ValidAnagram.php
public static function hashMap(string $s, string $t): bool
{
    if (mb_strlen($s) !== mb_strlen($t)) {    // mb_*, always — strlen counts bytes
        return false;
    }
    $counts = [];
    foreach (mb_str_split($s) as $char) {
        $counts[$char] = ($counts[$char] ?? 0) + 1;
    }
    foreach (mb_str_split($t) as $char) {
        if (($counts[$char] ?? 0) === 0) {
            return false;
        }
        $counts[$char]--;
    }
    return true;
}
```

Notice what already differs, and write it down for step 5: Python has `Counter` in the
standard library; TypeScript needs `Map` rather than an object literal; PHP needs the entire
`mb_*` family or it silently mangles `"héllo"`.

Every function gets a docstring with **the idea in one line** and **the complexity**.

---

## Step 4 — test

```bash
make test
```

Then:

```bash
make test-contracts
```

That second command checks something no single test suite can: that every approach declared in
the contract is implemented in **all three** languages. A contract only Python honours is the
exact drift this repo is built to prevent.

If one language fails and the other two pass, read the failure carefully — you have probably
found a genuine language difference, and it belongs in your notes.

---

## Step 5 — turn it into an exercise

```bash
make extract SLUG=valid-anagram
```

This is the step that makes it a practice problem. It:

- copies your three implementations to `solutions/python|typescript|php/…`
- reads the **signature** of each registered approach out of them
- regenerates each live file as a stub — same module docstring, same registration, same
  signatures, and a docstring per approach built from the contract's `name`, `time`, `space`
  and `note`
- leaves the body as `raise UnsolvedError(SLUG, "<approach>", PATH)`

Because the stub's docstrings come from the contract rather than from your code, they say what
to build and what it must cost, and never how.

```bash
make statements          # regenerate docs/problems/NNNN-slug.md from the contract
```

## Step 6 — write the notes

`solutions/notes/NNNN-slug.md`. **This is the deliverable.** The tests passing is the
precondition, not the goal.

Fill in what was genuinely interesting, delete what was not, and do not pad. The section worth
the most in three months is "Where I got stuck".

```markdown
## What differed between the three languages

- **Counting.** Python's `collections.Counter` does it in one call and compares with `==`.
  TypeScript and PHP both need a hand-rolled tally loop.
- **Strings are not strings.** PHP strings are byte arrays: `strlen("héllo")` is 6, not 5.
  Python iterates code points natively; JavaScript does too, *provided* you spread (`[...s]`)
  rather than `split("")`, which cuts surrogate pairs in half.

## What differed between the three frameworks

- **Laravel's `required` rejects `""`.** The `{"s": "", "t": ""}` case 422'd while FastAPI and
  NestJS returned 200. `present` is the rule that means "the key must exist".
```

## Step 7 — prove it round-trips

```bash
make verify-solutions    # applies every reference, runs all six suites, restores your files
make test                # should now be RED for this problem — that is correct
make test-contracts
make progress
```

`verify-solutions` is what stops reference answers rotting as contracts grow. CI runs it on
every push.

---

## Checklist

```
[ ] make new-problem with the right id, slug, input shape and approaches
[ ] contract: real summary, real complexities, 6+ cases, 3+ validation cases
[ ] three implementations, each idiomatic for its language
[ ] every function has a docstring with the idea and the complexity
[ ] make test           — green with your implementations in place
[ ] make test-contracts — cross-language coverage
[ ] make extract SLUG=… — your answers move to solutions/, stubs left behind
[ ] make statements     — brief regenerated
[ ] solutions/notes/NNNN-slug.md written, no TODO left
[ ] make verify-solutions — references still pass
[ ] make test           — RED again for this problem, as intended
```
