---
name: test-find-and-fix
description: Use when running the end-to-end test-suite triage-and-fix cycle for the current branch — from initial run through failure triage, fix in priority order, and re-run verification.
---

# Test Find and Fix

Orchestrates the full pytest triage-and-fix sequence. Wraps failure triage in a
triage-first loop: tag every failure before editing any file, reproduce logic
failures before patching, apply fixes in priority order, verify clean exit.

**Boundary contract:**

- **Input**: checked-out branch; working `.venv` (dev-environment prerequisite met).
- **Output**: `rtk uv run pytest` exits 0; every xfail carries inline rationale;
  no fix applied without prior triage.
- **Out of scope**: coverage thresholds and missing-coverage gaps (`python-testing-unit`);
  adding new tests for untested behaviour; prek/lint gates (`prek-find-and-fix`).

## Failure Categories

| Priority | Type | Description | Fix strategy |
|---|---|---|---|
| `blocker` | `setup` | Collection error, import error, conftest failure — prevents other tests from running | Fix immediately before triaging any other failure. |
| `standard` | `logic` | Assertion failure — implementation does not match test expectation | Reproduce with minimal call, then fix implementation or test. |
| `standard` | `contract` | Interface changed — test expectations are stale (wrong signature, renamed symbol, removed endpoint) | Update test to match the new contract; never silently delete. |
| `standard` | `data` | Missing fixture data, bad path, environment-specific resource absent | Fix fixture or data; do not skip unless environment dependency is genuinely out of scope. |
| `flaky` | any | Intermittent failure; passes on re-run without code change | Isolate cause (ordering, concurrency, timing); xfail with rationale only as last resort. |

## Triage Schema

Tag every failure before editing any file. Tags determine fix strategy.

| Tag | Values |
|---|---|
| **Decision** | `fix` · `skip` (xfail with inline rationale) · `delete` (test itself is wrong — duplicates another, tests a removed feature, asserts incorrect behaviour) |
| **Priority** | `blocker` (collection/import/conftest error) · `standard` (assertion failure, wrong behaviour) · `flaky` (intermittent, environment-dependent) |
| **Type** | `setup` (fixture/conftest/import errors) · `logic` (wrong implementation) · `contract` (interface changed — test expectations stale) · `data` (missing fixture data, path issues) |

## Procedure

### Step 1 — Run the test suite

```bash
rtk uv run pytest
```

Capture full output. Do not edit any file yet.

### Step 2 — Triage

For each failure, assign Decision / Priority / Type using the schema above.
List every finding in a triage table before proceeding.

Triage rules:
- Collection errors (import errors, conftest failures, syntax errors in test
  files) are always `blocker` + `setup`. Fix before triaging anything else —
  they mask the true failure count.
- A `delete` decision requires a concrete justification (test is for a removed
  feature, duplicates another test verbatim, asserts known-incorrect behaviour).
  Never delete to make the suite pass; only delete when the test itself is wrong.
- A `skip` decision requires an inline rationale on the `xfail` marker.
  Bare `pytest.mark.skip` without a reason string is not acceptable.
- `flaky` priority: do not fix until the failure has been observed at least twice
  without a code change between runs. A single transient failure is not evidence
  of flakiness.

### Step 3 — Fix in priority order

Apply fixes in this order. Do not advance to the next tier until the current
tier is clean.

**Blockers first — `setup` type:**

Fix collection errors, conftest issues, and import errors before anything else.
These prevent the suite from running and inflate the apparent failure count.

Common causes: missing fixture definition, wrong import path after a refactor,
`conftest.py` syntax error, `__init__.py` missing in a new package.

**`logic` type — reproduce gate (mandatory):**

Before patching any implementation file, reproduce the failure with the minimal
failing call:

```python
# Confirm the test is testing the right thing before changing production code.
# Example: call the function directly with the inputs the test uses and verify
# the assertion fails for the reason stated, not for an unrelated reason.
```

If the failure cannot be reproduced with the minimal call, the test may be
testing a side-effect or ordering dependency — triage as `flaky` or `contract`,
not `logic`.

Once reproduced: fix the implementation. Do not modify the test to make it pass
unless the test assertion is genuinely incorrect (reclassify as `contract`
or `delete` first).

**`contract` type:**

Interface changed; test expectations are stale. Update the test to match the
new contract — wrong argument count, renamed method, changed return shape,
removed route. Do not delete; do not xfail. The test is still valid, just
out of date.

**`data` type:**

Fix the fixture, file path, or environment dependency. If the data is
genuinely environment-specific (e.g., a file present only in CI), xfail
with a rationale string explaining the environment constraint.

### Step 4 — Skip discipline

`pytest.mark.xfail` is the only acceptable skip form. It must carry a reason
string:

```python
@pytest.mark.xfail(reason="<rule ref or issue id> — <why this cannot be fixed now>")
def test_something():
    ...
```

Bare `pytest.mark.skip` or `pytest.mark.skip()` with no reason is a violation
of this skill. `pytest.mark.skipif` is acceptable only when the condition is
machine-detectable (e.g., `sys.platform`, `importlib.util.find_spec`).

### Step 5 — Re-run to verify

```bash
rtk uv run pytest
```

Must exit 0 (all tests pass or xfail as expected). If new failures surface,
repeat triage from Step 2.

## Common Mistakes

| Mistake | Correct behaviour |
|---|---|
| Editing a file before completing the triage table | Complete the full triage table for every failure first. Fixing one failure can mask or surface others — triage gives the full picture. |
| Fixing a `logic` failure without reproducing it | Reproduce with the minimal failing call before touching implementation. An unreproducible failure is a false signal — reclassify before patching. |
| Modifying the test assertion to make a `logic` failure pass | Fix the implementation. Only modify a test when it is genuinely wrong (reclassify as `contract` or `delete` first). |
| Deleting a failing test without a concrete justification | Delete only when the test is wrong (removed feature, duplicate, incorrect assertion). Never delete to inflate the pass rate. |
| Adding a bare `pytest.mark.skip` with no reason | Use `pytest.mark.xfail(reason="...")`. A skip without rationale is not acceptable. |
| Treating a single transient failure as `flaky` | Observe the failure at least twice without a code change before classifying as flaky. |
| Advancing to `contract` or `data` fixes before `setup` blockers are resolved | Fix all `blocker` / `setup` failures first. They mask the true failure count and invalidate triage of downstream tests. |
| Treating a clean re-run as optional | `rtk uv run pytest` must exit 0 before the skill is considered done. A passing triage table is not a substitute for a clean run. |
| Adding new tests for missing coverage during this cycle | Out of scope. Missing-coverage work belongs in `python-testing-unit`. This skill fixes existing failures only. |
