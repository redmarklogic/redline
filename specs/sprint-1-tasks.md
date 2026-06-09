# Walking Skeleton — Sprint 1

**Definition**: The thinnest complete vertical slice of Redline that a geotechnical engineer can use end-to-end: upload a Letter of Engagement (LOE), receive a correctly structured Geotechnical Assessment Report skeleton as a DOCX download, with conditional sections determined by submitted flags.

**Milestone**: M1 — ship by 2026-06-30.

**Strategic bet**: [Bet 1 — The Free Skeleton Wedge Beats Paid Acquisition](../docs/product/strategy/strategic-bets.md)

---

## Sub-tasks

### WS-01 — Merge spec 003 (OpenAPI docs) to master

| Field | Value |
|---|---|
| **Status** | In Progress |
| **Spec** | `specs/003-openapi-docs/` |
| **Description** | Merge branch `feature/003-openapi-docs` to master so the main branch includes the re-enabled `/docs` Swagger UI and browser auto-open on `run-app.ps1`. |
| **Dependencies** | None — branch is committed and ready (4b4cffa). |

This task has no functional dependency. It is listed first because leaving a feature branch unmerged while sprint work begins on master creates unnecessary merge overhead. Merge this before starting WS-02.

---

### WS-02 — Conditional section logic input model (spec 002)

| Field | Value |
|---|---|
| **Status** | Not Started |
| **Spec** | `specs/002-skeleton-conditional-logic/tasks.md` — 24 tasks across 7 phases |
| **Shaped Pitch** | `specs/shaped/skeleton-conditional-logic-pitch.md` |
| **Description** | Implement `SectionFlags` input schema, `activate_sections()` pure domain function, route wiring to apply flags, and audit log entry per generation event. Delivers AC2d and AC2f (conditional section inclusion and exclusion driven by engineer-submitted flags). |
| **Dependencies** | WS-01 (clean master branch); spec 001 done (POST /skeletons endpoint exists — already merged). |

Full task breakdown is in `specs/002-skeleton-conditional-logic/tasks.md`. This is the highest-priority unstarted work in the sprint. It can begin immediately after WS-01 is merged.

Execution phases in `tasks.md` (for reference — do not re-specify here):

- Phase 1: Input schema (`SectionFlags`, `SkeletonRequest`, `ReportContext`, `ProjectMetadataDTO`)
- Phase 2: Domain function (`activate_sections` — TDD, all test cases before implementation)
- Phase 3: Route wiring — US1 (flags produce correct sections)
- Phase 4: Safe defaults — US2 (no flags = mandatory sections only)
- Phase 5: Invalid input rejection — US3 (unknown enum values return 422)
- Phase 6: Audit log entry — US4 (structured INFO log per generation event)
- Phase 7: Full suite, linting, edge-case verification

---

### WS-03 — Standards Knowledge Store MVP (Feature N)

| Field | Value |
|---|---|
| **Status** | Not Started |
| **Spec** | Needs spec — no spec file exists |
| **Description** | NZ-only store (3–5 documents) providing verbatim clause text for mandatory limitation clauses (SCOPE-CLAUSE-01, -05, -NEW, -03) and standards references for skeleton sections (NZS 1170.5, NZGS Module 3, NZS 3604:2011, NZBC, MBIE EGE Practice Module 1). Clause wording is retrieved from this store at skeleton generation time — it is never LLM-generated. |
| **Dependencies** | WS-02 Phase 1 (section schema must exist before the store can be wired to section output). Spec 001 done. |

This is an infrastructure dependency of the full skeleton. No skeleton can meet AC2e (standards references) or AC2g (mandatory limitation clauses verbatim from store) without this store in place. It must be scoped and specced before WS-05 can complete.

Per PRD: ADR-006 governs architecture — citation-only, internal, never exposed as a public query interface. The spec for Feature N must reference ADR-006.

---

### WS-04 — Document Parser: LOE metadata extraction (Feature M)

| Field | Value |
|---|---|
| **Status** | Not Started |
| **Spec** | Needs spec — no spec file exists |
| **Description** | LLM-based extraction from an uploaded LOE: project number, client name, site address, date, report type, and conditional section flags. Step 2 (metadata extraction) only. Full deliverable parsing and traceability matrix are deferred to Sprint 2. Delivers the one-click UX: upload LOE, skeleton generates with a live progress indicator. |
| **Dependencies** | WS-02 complete (the input schema `SectionFlags` and `ProjectMetadataDTO` must exist before the parser can populate them). |

Per PRD Decision Log (2026-04-22): no manual-input form. If extraction cannot populate a metadata field, the skeleton generates with that field blank — the user edits in Word. No fallback form is presented.

The spec for Feature M must define: acceptable LOE file formats, extraction field list (confirmed: project number, client name, site address, date, report type, section flags), extraction quality threshold (ship at 90%+ accuracy or delay per John's marketing assessment), and failure behaviour.

---

### WS-05 — Audit Log: core subset (Feature L)

| Field | Value |
|---|---|
| **Status** | Not Started |
| **Spec** | Needs spec — no spec file exists |
| **Description** | Log every AI generation event with: timestamp, user ID, model version, input hash, output document hash. Write an OOXML provenance event into every generated DOCX (write-only custom XML part: skeleton generation timestamp, template version, standards applied). |
| **Dependencies** | WS-02 Phase 6 (US4 audit log entry in the route handler is the foundation — Feature L extends it). WS-03 (standards applied list is populated from the Knowledge Store). |

Per PRD: audit trail is a Day-1 requirement, not Phase-2. The OOXML provenance event written into the DOCX is a hard requirement for the insurance liability positioning ("Your AI wrote it. Who checked it?").

The spec for Feature L must distinguish between: (a) the structured log entry already scoped in WS-02 Phase 6 (section flags + activated sections), and (b) the additional fields Feature L adds (user ID, model version, input hash, output document hash, OOXML provenance). Do not re-spec what WS-02 already delivers.

---

## Dependency Graph

```
WS-01 (merge spec 003)
  |
  v
WS-02 Phase 1 (input schema)
  |
  +---> WS-02 Phase 2 (domain function)
  |       |
  |       v
  |     WS-02 Phase 3-5 (route wiring, safe defaults, validation)
  |       |
  |       +---> WS-02 Phase 6 (audit log entry)
  |       |       |
  |       |       v
  |       |     WS-05 (Feature L — Audit Log: core subset)
  |       |
  |       +---> WS-04 (Feature M — Document Parser)
  |
  v
WS-03 (Feature N — Standards Knowledge Store)
  |
  +---> WS-05 (standards applied list)
  +---> Full skeleton AC2e + AC2g satisfied


Critical path:
WS-01 -> WS-02 Ph1 -> WS-02 Ph2 -> WS-02 Ph3-5 -> WS-04 -> end-to-end acceptance
                                                  -> WS-02 Ph6 -> WS-05

WS-03 is a parallel track that must complete before AC2e/AC2g can pass.
WS-03 is not on the critical path for route wiring, but it is on the critical path
for the full skeleton to pass acceptance.
```

**Critical path summary**: WS-01 then WS-02 (all phases) is the spine. WS-03 and WS-04 can be scoped in parallel while WS-02 is in progress. WS-05 is the last dependency to resolve before end-to-end acceptance testing can run.

---

## Sprint Risks

Ranked by severity — highest first.

### Risk 1 (High): Feature N and Feature M have no specs — scope is unknown

Features N (Standards Store) and M (Document Parser) have no spec files. The sprint contains two substantial implementation unknowns whose complexity is unverified by Peter. Feature N requires an architectural decision about how verbatim clause text is stored, versioned, and retrieved at generation time. Feature M requires an LLM extraction pipeline with a 90%+ accuracy bar before it can ship (per PRD). If either of these goes into implementation without a shaped Pitch and a SpecKit task breakdown, scope will expand mid-sprint and M1 will slip.

Mitigation: Peter shapes Feature N and Feature M into Pitches before implementation begins. Mark approves scope against appetite. No implementation until Pitches exist in `specs/shaped/`.

### Risk 2 (High): Feature L (Audit Log) has no spec and extends two other unfinished features

Feature L depends on WS-02 Phase 6 (audit log entry) and WS-03 (standards applied list from the Knowledge Store). It also introduces OOXML provenance writes into every generated DOCX, which is a cross-cutting concern touching the document builder. The combination of late dependencies and no spec means Feature L is at risk of being cut or under-scoped. Since the PRD designates the audit trail as a Day-1 requirement (not Phase-2), cutting it is not acceptable without a founder decision.

Mitigation: Feature L spec is written and shaped before WS-02 Phase 6 completes. The OOXML provenance write must be scoped explicitly — it is not a trivial addition to the document builder.

### Risk 3 (Medium): WS-02 conditional logic "as appropriate" triggers may expand scope mid-implementation

The 2023 ENZ/NZGS guideline's conditional rules CL-G1, CL-G3, and CL-G4 use the phrase "as appropriate to the site and development." This phrase is not defined in the guideline — it is practitioner judgment. The Pitch (`specs/shaped/skeleton-conditional-logic-pitch.md`) resolves this through project type flags and site condition parameters. If the implementation team discovers that the mapping from flags to activated sections is ambiguous for edge cases not covered in `tasks.md`, the Phase 2 domain function will grow in complexity. This is a risk to WS-02 timeline, not a risk to the approach.

Mitigation: The TDD discipline in Phase 2 (T006: all failing tests written before implementation) surfaces edge cases before they become implementation surprises. Any scope question that emerges during T006 is escalated to Peter before T008 begins.

---

## Open gates before sprint start

The following actions must complete before the sprint can run cleanly:

1. **WS-01**: Open a PR for `feature/003-openapi-docs` and merge to master. This is the current branch — it is ready.
2. **Feature N spec**: Peter shapes Feature N into a Pitch. Mark approves. No implementation until `specs/shaped/` contains a Feature N Pitch.
3. **Feature M spec**: Peter shapes Feature M into a Pitch. Mark approves. No implementation until `specs/shaped/` contains a Feature M Pitch.
4. **Feature L spec**: Peter shapes Feature L into a Pitch, distinguishing the WS-02 Phase 6 scope from the additional Day-1 audit trail requirements. Mark approves.
