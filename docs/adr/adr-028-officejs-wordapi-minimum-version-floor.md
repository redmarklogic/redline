# ADR-028 — Office.js WordApi 1.3 Minimum Version Floor

## Summary

The production Word taskpane add-in declares `WordApi 1.3` as its minimum API
version requirement. This floor is driven by `ContentControl.getRange()`, which is
required by the Replace primitive and is absent from WordApi 1.1. Word 2016 and
earlier perpetual licences are explicitly unsupported. The floor may only increase by
a recorded ADR amendment — never by implementation drift.

**Deciders**: Founder (2026-06-14), Peter (architecture).

## Status

Accepted — 2026-06-14

**Constitution review (Peter, per ADR-sync duty):** Constitution Principle XIX added
in the same commit — third-party client API floors are now a first-class
constitutional concern. See `.specify/memory/constitution.md`.

## Context

### Background

Sprint 4 PoC (issue #185) proved three Word primitives — find, mark, replace — using
Office.js inside Script Lab. The spike YAML (`docs/research/20260622-185-officejs-spike/snippet.yaml`)
declares:

```yaml
api_set:
  WordApi: '1.3'
```

The description in that file records the technical reason verbatim:

> WordApi 1.3 floor — most primitives are 1.1, but `ContentControl.getRange()` (used
> in Replace) requires 1.3, so the declared floor is raised to 1.3 to honestly match
> the code.

### Which primitives require which floor

| Primitive | Office.js call | Min WordApi |
|---|---|---|
| Find | `body.search()` | 1.1 |
| Mark | `range.insertContentControl()`, `range.font.highlightColor` | 1.1 |
| Replace | `control.getRange()` | **1.3** |

Find and Mark work on 1.1. The 1.3 floor is driven solely by Replace.

### What WordApi 1.3 means for end-user installations

| Installation | WordApi 1.3? |
|---|---|
| Microsoft 365 (subscription, any channel) | Yes |
| Word 2019 (perpetual) | Yes |
| Word 2016 (perpetual) | **No — unsupported** |
| Word 2013 and earlier | **No — unsupported** |

Word 2016 users cannot load the add-in. Office silently refuses to offer the add-in
when the host does not meet the `Requirements` block in `manifest.xml`. This is a
commercial commitment that must appear in the system requirements before a subscriber
purchases.

### CDN pin vs. version floor

The spike loads Office.js from the evergreen CDN path
`https://appsforoffice.microsoft.com/lib/1/hosted/office.js`. This is the runtime
library, always current. The `api_set` declaration is the **floor** — the minimum
capability the add-in requires from the host. These are independent concerns. The
production manifest must not pin to a version-specific library path
(`lib/1.3/hosted/...`); doing so would freeze Redline out of API sets above 1.3.
The evergreen path is correct and must be preserved.

### Binding constraints at this stage

- Pre-revenue PoC, ~7 weeks to launch backstop.
- Word 2019+ / Microsoft 365 is the realistic target market for legal teams (Word
  2016 perpetual is approaching end-of-extended-support and rarely found in active
  legal practices).
- The existing memory record (`client-minimum-requirements-across-surfaces.md`)
  already notes "Word taskpane needs Word 2016 (WordApi 1.3)" — this ADR is the
  architectural grounding for that commercial note.

## Decision

### D1 — WordApi 1.3 is the declared minimum floor

The production `manifest.xml` for the Redline Word add-in must include:

```xml
<Requirements>
  <Sets DefaultMinVersion="1.3">
    <Set Name="WordApi" MinVersion="1.3"/>
  </Sets>
</Requirements>
```

This is the binding requirement; no Word host below 1.3 will load the add-in.

### D2 — Floor may only increase by ADR amendment

Any future Office.js call added to the production taskpane that requires a WordApi
version above 1.3 **must be evaluated against this ADR before implementation**.
If the call requires a higher floor:

1. File an ADR amendment (or a new ADR superseding this one).
2. Assess the commercial impact (which installations are dropped).
3. Update `manifest.xml` only after the amendment is accepted.

Implementation drift — shipping a call that silently raises the effective floor
without a recorded decision — is prohibited (Constitution Principle XIX).

### D3 — Floor is revisable if Replace is descoped

The 1.3 floor is driven entirely by `ContentControl.getRange()` in the Replace
primitive. If Replace is removed from scope before the production manifest ships,
the floor may be negotiated back to 1.1 via an ADR amendment. This revisability is
recorded explicitly so a future session does not mistake 1.3 for a permanent floor
independent of Replace.

### D4 — Commercial requirement statement

System requirements visible to prospective subscribers must state:

> **Microsoft Word**: Microsoft 365 (any subscription channel) or Word 2019 (perpetual
> licence). Word 2016 and earlier are not supported.

This wording names both qualifying installation types (subscription and perpetual).
Marketing copy reviewed by John must not contradict this floor.

### D5 — Evergreen CDN path is required

The production taskpane must load Office.js from the evergreen path:

```
https://appsforoffice.microsoft.com/lib/1/hosted/office.js
```

Pinning to a version-specific path is prohibited — it caps available API sets and
prevents transparent Office.js updates.

## Options Considered

| Option | Replace supported | WordApi floor | Word 2016 users | Verdict |
|---|---|---|---|---|
| **WordApi 1.3 (selected)** | Yes — `ContentControl.getRange()` available | 1.3 | Dropped | **Selected** |
| WordApi 1.1 | No — `ContentControl.getRange()` absent | 1.1 | Supported | Rejected — Replace is load-bearing |
| Rewrite Replace without `getRange()` | Possible but unproven | 1.1 | Supported | Not attempted — no known clean alternative; revisit only if Word 2016 support becomes a hard commercial requirement |

## Consequences

**Immediate:**

- This ADR is the authority record for the `manifest.xml` `Requirements` block.
- Constitution Principle XIX added in the same commit.
- The memory record `client-minimum-requirements-across-surfaces.md` is now
  architecturally grounded (previously it was an observation without an ADR anchor).

**Ongoing:**

- Every new Office.js API call in the production taskpane is pre-checked against
  this floor before it ships (D2 governance rule).
- Marketing and ToS copy must reflect D4 wording before the first subscriber
  purchase.
- If Replace is descoped, file an ADR amendment to revisit the floor (D3).

**Accepted costs:**

- Word 2016 perpetual users cannot use the taskpane add-in.
- Commercial wording must be accurate before subscriber onboarding — this is a
  dependency on John and Mark.

## Cross-References

- **Spike #185** — `docs/research/20260622-185-officejs-spike/snippet.yaml` — source
  of the `api_set: {WordApi: '1.3'}` floor determination.
- **Issue #190** — `specs/190-adapt-masterjx9-flask-taskpane-template-with-https-dev-certs/`
  — Flask dev harness that will host the taskpane; manifest wiring is issue #191.
- **Issue #191** — manifest and sideload (not yet specced); D1's `manifest.xml`
  snippet is the required `Requirements` block for that issue.
- **Constitution Principle XIX** — `.specify/memory/constitution.md` — third-party
  client API floors are commercial commitments; floor changes require an ADR.
- **`client-minimum-requirements-across-surfaces.md`** — memory record; now
  architecturally grounded by this ADR.
- **ADR-019** — platform compatibility (Windows/Linux); governs the authoring
  toolchain. This ADR governs the Office.js client platform — a distinct concern.
- **ADR-024** — Django web stack; the All-Python Toolchain Boundary. The Office.js
  taskpane is vendored JS (no Node/npm toolchain), compliant with Principle XVII.
