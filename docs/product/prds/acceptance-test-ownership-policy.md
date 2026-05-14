# Acceptance Test Ownership Policy — Domain-Specific Use Cases

**Status**: Adopted.
**Source**: Item 5, Launch Planning Session — 2026-05-14.
**Owner**: Mark.
**Participants**: Harriet (role-boundary framing), Mark (product owner definition).

---

## Scope

This policy applies to acceptance tests for use cases where correctness depends on domain knowledge — specifically:

- **Case 1**: A cited standard is an older version than current (e.g. NZS 4431:1989 cited when NZS 4431:2022 is current).
- **Case 2**: A cited standard does not exist (fabricated standard code).
- **Case 3**: A cited standard is from the wrong jurisdiction (an Australian standard substituted where a NZ standard is required).

This policy also applies to any future use case where the test fixture contains a domain claim or where the system's user-facing output carries a domain assertion.

---

## Ownership Model

### What Mark owns

- The full acceptance criterion structure — the "given / when / then" form, testability, edge-case coverage.
- Pass/fail confirmation: Mark confirms that a passing test satisfies the product requirement.
- Engineering implementation oversight for test fixtures and detection logic.

### What Graeme owns (blocking gates)

Graeme holds three blocking gates. Nothing advances past each gate without his explicit sign-off.

| Gate | What Graeme reviews | When |
|---|---|---|
| **Gate 1 — Domain-content assertion** | The specific standard codes, version currency facts, and jurisdiction rules inside the acceptance criterion are factually correct. | After Mark drafts the criterion, before fixture implementation begins. |
| **Gate 2 — Fixture accuracy** | The planted error in the golden fixture is a real, documentable error a practitioner could make. | After Engineering implements the fixture, before detection logic is implemented. |
| **Gate 3 — User-facing explanation accuracy** | The system's explanation of why it flagged the error — the text shown to the user — carries accurate domain claims. | After Engineering runs the test suite and the test passes, before the use case is approved for release. |

Gate 3 does not replace Mark's pass/fail confirmation — both gates must clear independently before the use case ships.

---

## RACI Table

| Activity | Graeme | Mark | Engineering |
|---|---|---|---|
| Define domain rule (what constitutes the error) | **A/R** | C | I |
| Draft acceptance criterion structure | I | **A/R** | I |
| Validate domain-content assertions in criterion (Gate 1) | **A** (blocking) | R | I |
| Implement test fixture (plant the error) | I | C | **A/R** |
| Validate fixture domain accuracy (Gate 2) | **A** (blocking) | R | I |
| Implement detection logic | I | C | **A/R** |
| Confirm test passes against criterion (pass/fail) | I | **A/R** | R |
| Validate domain accuracy of user-facing explanation (Gate 3) | **A** (blocking) | R | I |
| Approve use case for release | I | **R** | I |

*A = Accountable (blocking sign-off). R = Responsible (does the work). C = Consulted. I = Informed.*

---

## Workflow Sequences

### Case 1 — Outdated version (e.g. NZS 4431:1989 cited when :2022 is current)

1. Mark drafts criterion with a placeholder for the current version.
2. Mark consults Graeme: confirm current version and that the older edition is withdrawn.
3. Graeme validates and signs domain-content assertion — **Gate 1**.
4. Mark finalises criterion.
5. Engineering implements fixture (plants the outdated citation).
6. Graeme reviews fixture: confirms the planted citation is a genuine, documentable error — **Gate 2**.
7. Engineering implements detection logic.
8. Engineering runs test suite; test passes.
9. Mark confirms pass/fail — **Mark gate**.
10. Graeme reviews user-facing system output: confirms explanation is domain-accurate — **Gate 3**.
11. Use case approved for release.

### Case 2 — Fabricated standard (non-existent standard code)

1. Mark drafts criterion (no domain content needed — standard is fabricated by definition).
2. Graeme reviews fixture only: confirms the fabricated code is genuinely not a real standard — **Gate 2**.
3. Engineering implements detection logic.
4. Steps 8–11 as above.

### Case 3 — Wrong jurisdiction (Australian standard substituted for NZ)

1. Graeme authors the jurisdiction rule: which Australian standards are inadmissible in NZ GIRs and why. See `docs/knowledge/geotechnical/standards-jurisdiction-rules.md` *(Graeme to create — prerequisite for fixture implementation)*.
2. Mark structures the acceptance criterion around Graeme's rule.
3. Graeme signs domain-content assertion — **Gate 1**.
4. Steps 5–11 as above.

---

## Open Actions

| Action | Owner | Prerequisite for |
|---|---|---|
| Create `docs/knowledge/geotechnical/standards-jurisdiction-rules.md` — jurisdiction rule for Case 3 | Graeme | Case 3 fixture implementation |
| Update `docs/architecture/ai-maker-checker-pattern.md` — document Gate 3 (Graeme domain-accuracy gate) as a named step | Engineering / Mark | Shared architectural understanding |
| Create `domain-accuracy-review` skill — Harriet to scope and commission | Harriet | Consistent Gate 3 reviews across all use cases |
| Validate Email 2 trigger timing (14 days) against expected free-tier activation window | Mark | Co-development recruitment via waitlist |
