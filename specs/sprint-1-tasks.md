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

This task has no functional dependency. It is listed first because leaving a feature branch unmerged while sprint work begins on master creates unnecessary merge overhead. Merge this before starting WS-03 or WS-04.

---

### WS-03 — Standards Knowledge Store MVP (Feature N)

| Field | Value |
|---|---|
| **Status** | Not Started |
| **Spec** | Needs spec — no spec file exists |
| **Description** | NZ-only store (3–5 documents) providing verbatim clause text for mandatory limitation clauses (SCOPE-CLAUSE-01, -05, -NEW, -03) and standards references for skeleton sections (NZS 1170.5, NZGS Module 3, NZS 3604:2011, NZBC, MBIE EGE Practice Module 1). Clause wording is retrieved from this store at skeleton generation time — it is never LLM-generated. |
| **Dependencies** | WS-01. Spec 001 done. |

This is an infrastructure dependency of the full skeleton. No skeleton can meet AC2e (standards references) or AC2g (mandatory limitation clauses verbatim from store) without this store in place. It must be scoped and specced before WS-05 can complete.

Per PRD: ADR-006 governs architecture — citation-only, internal, never exposed as a public query interface. The spec for Feature N must reference ADR-006.

---

### WS-04 — Document Parser: LOE metadata extraction (Feature M)

| Field | Value |
|---|---|
| **Status** | Not Started |
| **Spec** | Needs spec — no spec file exists |
| **Description** | LLM-based extraction from an uploaded LOE: project number, client name, site address, date, report type, and conditional section flags. Step 2 (metadata extraction) only. Full deliverable parsing and traceability matrix are deferred to Sprint 2. Delivers the one-click UX: upload LOE, skeleton generates with a live progress indicator. |
| **Dependencies** | WS-01. Spec 001 done (input schema exists in the existing POST /skeletons endpoint). |

Per PRD Decision Log (2026-04-22): no manual-input form. If extraction cannot populate a metadata field, the skeleton generates with that field blank — the user edits in Word. No fallback form is presented.

The spec for Feature M must define: acceptable LOE file formats, extraction field list (confirmed: project number, client name, site address, date, report type, section flags), extraction quality threshold (ship at 90%+ accuracy or delay per John's marketing assessment), and failure behaviour.

---

### WS-05 — Audit Log: core subset (Feature L)

| Field | Value |
|---|---|
| **Status** | Not Started |
| **Spec** | Needs spec — no spec file exists |
| **Description** | Log every AI generation event with: timestamp, user ID, model version, input hash, output document hash. Write an OOXML provenance event into every generated DOCX (write-only custom XML part: skeleton generation timestamp, template version, standards applied). |
| **Dependencies** | WS-03 (standards applied list is populated from the Knowledge Store). Spec 001 done. |

Per PRD: audit trail is a Day-1 requirement, not Phase-2. The OOXML provenance event written into the DOCX is a hard requirement for the insurance liability positioning ("Your AI wrote it. Who checked it?").

The spec for Feature L must cover: (a) structured log entry fields (user ID, model version, input hash, output document hash), (b) OOXML provenance write into the DOCX custom XML part (generation timestamp, template version, standards applied). The OOXML provenance write is a cross-cutting concern touching the document builder and must be scoped explicitly.

---

## Dependency Graph

```text
WS-01 (merge spec 003)
  |
  +---> WS-03 (Feature N — Standards Knowledge Store)
  |       |
  |       +---> WS-05 (Feature L — Audit Log: core subset)
  |       +---> Full skeleton AC2e + AC2g satisfied
  |
  +---> WS-04 (Feature M — Document Parser)


Critical path:
WS-01 -> WS-03 -> WS-05 -> end-to-end acceptance

WS-04 is a parallel track that must complete before the one-click LOE UX works.
WS-03 must complete before WS-05 can write the standards-applied list.
```

**Critical path summary**: WS-01 unblocks WS-03 and WS-04 in parallel. WS-05 is the last dependency — it requires WS-03 to supply the standards applied list. End-to-end acceptance cannot run until all four are done.

---

## Sprint Risks

Ranked by severity — highest first.

### Risk 1 (High): Features N, M, and L have no specs — scope is unknown

All three remaining features have no spec files. The sprint contains three substantial implementation unknowns whose complexity is unverified by Peter. Feature N requires an architectural decision about how verbatim clause text is stored, versioned, and retrieved at generation time. Feature M requires an LLM extraction pipeline with a 90%+ accuracy bar before it can ship (per PRD). Feature L introduces OOXML provenance writes into every generated DOCX, a cross-cutting concern touching the document builder. If any of these goes into implementation without a shaped Pitch and a SpecKit task breakdown, scope will expand mid-sprint and M1 will slip.

Mitigation: Peter shapes Features N, M, and L into Pitches before implementation begins. Mark approves scope against appetite. No implementation until Pitches exist in `specs/shaped/`.

### Risk 2 (High): Feature L (Audit Log) is a Day-1 requirement with no escape hatch

The PRD designates the audit trail as a Day-1 requirement, not Phase-2. Feature L depends on WS-03 and introduces OOXML provenance writes. If it runs late, it cannot be quietly dropped — a founder decision record is required. The combination of late dependencies and no spec means it is the most likely feature to be under-scoped.

Mitigation: Feature L spec is written and shaped before WS-03 completes. The OOXML provenance write must be scoped explicitly — it is not a trivial addition to the document builder.

---

## Open gates before sprint start

The following actions must complete before the sprint can run cleanly:

1. **WS-01**: Open a PR for `feature/003-openapi-docs` and merge to master. This is the current branch — it is ready.
2. **Feature N spec**: Peter shapes Feature N into a Pitch. Mark approves. No implementation until `specs/shaped/` contains a Feature N Pitch.
3. **Feature M spec**: Peter shapes Feature M into a Pitch. Mark approves. No implementation until `specs/shaped/` contains a Feature M Pitch.
4. **Feature L spec**: Peter shapes Feature L into a Pitch covering the full Day-1 audit trail requirements. Mark approves.
