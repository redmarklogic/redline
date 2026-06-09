# Phase 0 Research: Skeleton Endpoint

Resolves the unknowns and conflicts surfaced during source-reconciliation and planning. Each entry: **Decision / Rationale / Alternatives considered**.

---

## R1. API layer placement (the `rl`-vs-`marker` fork)

**Decision**: The external HTTP API is a new top layer **`src/marker/api/` inside the existing `marker` package** — not `src/rl/`, not a new sibling package. Dependency direction is `api → functions → domain`. The `marker layers` import-linter contract is extended to `["api", "functions", "domain"]` (api highest). The `marker`/`rl` independence contract is unchanged.

**Rationale** (Peter, Principal Engineer — founder-routed decision, 2026-06-09): the endpoint wraps `build_skeleton`, which lives in `marker`. #51 spans a single bounded context, so routing through the `rl` integration hub buys nothing and would cross the `marker`/`rl` independence boundary for zero benefit. Co-locating the HTTP surface with the context it serves keeps the dependency local and the package self-describing. The API sits *above* `functions` because it orchestrates a call into the builder — exactly the "project-specific higher layer above `functions`" the domain-model guidance anticipates.

**Alternatives considered**:
- *`src/rl/api/` under the recorded hub* — rejected: forces `rl → marker` for a single-context endpoint; the hub-composes-tools pattern is for workflows spanning multiple sibling tools, which #51 is not.
- *New sibling package* — rejected: no new bounded context exists; the skeleton context already is `marker`.
- *`src/marker/` flat (no `api` layer)* — rejected: transport is volatile (ADR-017); isolating it in its own layer contains churn and lets import-linter enforce the one-way dependency.

### Peter's decision — preserved verbatim (key points)

> **Location:** `src/marker/api/` — new top layer inside the existing `marker` package. Not `rl`, not a new sibling.
>
> **Dependency direction:** `api → functions → domain`. Transport imports the builder and domain models; builder and domain import nothing in `api`; transport never touches `engines`/`python-docx` (ADR-004 stays intact). Enforced by extending the `marker layers` import-linter contract to `["api","functions","domain"]`.
>
> **Transport models are not domain models.** `marker.api.schemas` holds HTTP request/response shapes; the route translates them into the domain `ReportStructure` / `ProjectMetadata` before calling the builder. The domain models already carry human-readable aliases (`"Project Number"`, `"Sections"`, `"Heading"`), so for #51 the transport request schema can be a thin pass-through, but it stays in the `api` layer so future HTTP-only concerns (auth context, content-negotiation hints) never leak into the domain.
>
> **Bytes seam.** Today `build_skeleton(...)` only writes to a `Path` and returns `None`. The HTTP contract needs bytes (never base64-in-JSON), preferably streamed. The seam is to let the builder render to a buffer the API can stream — a `functions`/`domain`-layer change. The builder produces bytes; the transport streams them. This keeps byte-production independent of which web framework #78 picks.

> **Package name:** the 2026-04-12 research doc named the sibling `skeleton`; the code shipped it as `marker`. **Founder confirmed (2026-06-09): keep `marker` (code wins).** No rename refactor; Peter's reconciliation ADR ratifies `marker` as the skeleton bounded context.

---

## R2. Reconciliation debt (does anything block #51?)

**Decision**: Two recorded artifacts are stale and **Peter owns their reconciliation**; **neither blocks #51**.

1. **ADR-001 authority table + `docs/architecture/domain-model.md` Context Map** still imply `rl` is the home for everything and predate the `marker` package (Subdomain table shows "Report generation | TBD"; Bounded Contexts table empty). Peter authors a **documentation-reconciliation ADR** ("`marker` sibling + API-layer placement") ratifying the already-shipped, import-linter-enforced boundary, plus the `domain-model.md` update. Lands **before #51 merges**; does not gate the plan or the code.
2. **`marker layers` import-linter contract** needs `"api"` added. This is a `pyproject.toml` edit (volatile internal contract per ADR-017, no ADR needed) and is **part of #51's Phase 0 tasks**.

**Rationale**: the code boundary already exists and is enforced today; the only debt is the *recorded* docs catching up. **Action carried to follow-up** because Peter's subagent could not be resumed in this session (no SendMessage capability) — the founder should re-dispatch Peter to author the reconciliation ADR + Context Map update before #51 merges.

**Alternatives considered**: blocking #51 on the ADR — rejected; the boundary is real now, the ADR records (not creates) it.

---

## R3. Framework binding and the #78 dependency

**Decision**: Build #51 on **FastAPI** now. Ship the two framework-level realisations ADR-018 lists as #78-pending — the **global-exception-handler wiring** and the **streaming-response object** — as a **documented placeholder** (issue #51 "Option B" ordering), flagged in the PR and tracked as a follow-up.

**Rationale**: FastAPI is named as the framework throughout the grounding material — ADR-018 decision rationale ("FastAPI + Pydantic emit 422 by default"), the live standard's "FastAPI bindings" appendix, the `python-fastapi` skill, and issue #51 itself ("load `fastapi-http-api` skill"). #78 ("tech stack + layer responsibilities — Django / FastAPI / frontend") finalises the broader stack and the specific bindings. Peter's interim layering isolates the framework-specific pieces to two seams so the builder, the bytes seam, and the DTO→domain translation survive any #78 outcome:

- **Route stays thin and raises** typed errors — no per-route `try/except`. When #78 binds the global handler, the route needs zero change (it was already raising).
- **`422` vs `400`** relies on the framework's Pydantic-validation default plus the `json_invalid` detector — no custom mapping to rip out later.
- **Auth** is one `require_bearer` seam enforcing presence + `401`/`WWW-Authenticate`; token verification is a stub behind that seam (SSO #50/#73/#48b).

**Alternatives considered**:
- *Wait for #78 before any work* — rejected: #51 is Option-B-sequenced ahead of #78 deliberately; the placeholder is the agreed mechanism.
- *Abstract the framework now (framework-agnostic transport)* — rejected: over-engineering at Phase 1; the two-seam isolation already bounds the blast radius if #78 swaps frameworks.

---

## R4. Bytes seam — how the builder returns DOCX bytes

**Decision**: Add `DocumentFacade.to_bytes() -> bytes` (protocol + `PythonDocxFacade` impl saving to a `BytesIO`) and a functions-layer `build_skeleton_bytes(structure, metadata) -> bytes`. Keep `build_skeleton(..., output_path)` for the CLI (`src/scripts/marker/create_skeleton.py`).

**Rationale**: `python-docx`'s `Document.save()` accepts a file-like object, so bytes are obtainable without disk I/O. `bytes` is a primitive, so adding `to_bytes()` to the facade respects ADR-004 (Principle V — only primitives cross the facade boundary). The seam lives in `functions`, not `api`, so it is framework-agnostic (Peter's interim §2).

**Alternatives considered**:
- *Route writes to a temp file then reads it back* — rejected: needless disk I/O and a cleanup burden; `BytesIO` is idiomatic.
- *Change `build_skeleton`'s signature to return bytes* — rejected: breaks the existing CLI; additive `build_skeleton_bytes` preserves it.

---

## R5. Skill-path drift (flag for follow-up)

**Decision**: Use `marker.api.*` / `marker.functions.builders` paths throughout the plan and tasks. The `python-fastapi` and `python-testing-api` skill procedures hard-code **stale placeholder paths** (`rl.app.api.routers.skeletons`, `rl.app.api.dependencies.auth`, `rl.app.main`, `from rl.skeleton_generator import build_skeleton`) that match neither the actual layout nor Peter's placement decision. `rl.skeleton_generator` does not exist — confirming the paths are aspirational, not descriptive. **Flag as a follow-up** for the skill owner to update the procedures to `marker.api.*`.

**Rationale**: the skill SKILL.md states the live standard wins on conflict and that drift must be flagged. The skill *patterns* (StreamingResponse, `HTTPBearer(auto_error=False)`, `StarletteHTTPException` handler, `json_invalid`→400) are correct and reused; only the *paths* are wrong.

**Also stale in `python-testing-api`**: it claims `openapi-spec-validator` and `pytest-httpx` are "already in test dependencies." They are **not** in `pyproject.toml`'s `test` group (only `coverage`, `pytest`, `pytest-cov`, `schemathesis`). Phase 0 adds `openapi-spec-validator`, `httpx`, `pytest-mock`. `pytest-httpx` is not needed (#51 makes no outbound HTTP).

**Alternatives considered**: edit the skills now — out of scope for spec-kit (which produces spec/plan/tasks, not skill edits); flagged instead.

---

## R6. Test layout and markers

**Decision**: Tests live under `tests/marker/api/` (mirroring `src/marker/api/`), one test module per source module, grouped into classes. App + client fixtures in `tests/marker/api/conftest.py`. No `/api/v1/` prefix and no `api_v1` marker — #51 is unversioned (Standard §14); request paths are `/skeletons` directly.

**Rationale**: matches the existing `tests/marker/...` mirroring convention (e.g. `tests/marker/functions/test_builders.py`) and the no-versioning rule. The `python-testing-api` `api_v1`/`/api/v1/` conventions assume a versioned API and do not apply.

**Alternatives considered**: adopt the skill's `tests/<pkg>/app/api/v1/` tree — rejected: encodes a `/v1/` prefix the standard defers.

---

## Open follow-ups (tracked, not blocking #51 spec/plan/tasks)

| # | Item | Owner | Blocks? |
|---|------|-------|---------|
| F1 | Reconciliation ADR (`marker` sibling + API placement) + `domain-model.md` Context Map update | Peter | Before #51 **merges**, not the plan |
| F2 | Update `python-fastapi` + `python-testing-api` skill paths to `marker.api.*`; correct the "already in test deps" claim | skill owner | No |
| F3 | Finalise global-handler wiring + streaming-response binding | #78 | Endpoint is placeholder-flagged until then |
| F4 | Real bearer-token verification | SSO #50 / #73 / #48b | Endpoint is presence-only until then |
