# Source Reconciliation (Lifecycle: before_specify)

<!-- Extension: source-reconciliation -->

This hook fires before the `specify` workflow phase.

Run a reconciliation pass before writing any spec content. This prevents silent
drift between source documents and generated artifacts.

## When to run

Run when the spec input is an **external `.md` file** (concept doc, research doc,
ADR, prior plan). Skip when the spec input is a conversation with no external doc,
or when the external doc was written in the same session and has not been reviewed
by others.

## Steps

### 1. Identify authoritative sources

List every document that defines concrete data for this feature:
- Concept docs, research docs
- ADRs governing the domain
- Existing plans or prior specs for the same feature
- Domain model docs

Declare which source is the **primary authority** when sources conflict.

### 2. Extract canonical data

Build a reconciliation table of all concrete values:

| Item | Value | Source |
|------|-------|--------|
| Field names | ... | [doc] |
| Section names | ... | [doc] |
| Naming conventions | ... | [doc] |
| Numbering schemes | ... | [doc] |
| Domain terms | ... | [doc] |
| Acceptance criteria IDs | ... | [doc] |

This table is the single reference for all downstream artifacts.

### 3. Flag conflicts

If two sources disagree (e.g., a naming convention differs between a concept doc
and an old plan), **stop and resolve with the user** before proceeding. Do not
silently pick one source.

### 4. Flag ambiguities

If a source uses vague language where the spec needs a concrete value (e.g., "the
correct position" without stating where), add it to a clarification list to resolve
before writing spec content.

### 5. Handle existing artifacts

If a spec directory already contains prior artifacts (e.g., a partially-filled
`specs/NNN-feature/`):

1. Read the existing artifacts
2. Explicitly diff them against the current source documents
3. Note what has changed, what is superseded, what can be carried forward
4. Ask the user: archive, update, or replace?

Do NOT silently inherit decisions from old artifacts. They are drafts from a
different context.

### 6. Update source documents (post-spec)

After reconciliation is complete and the spec is written, propagate clarifications
and conflict resolutions **back into the original source documents**. Remove
contradictions, add missing precision. Source docs should be cleaner after
spec-kit runs, not staler.

---

This command is the sole SSOT for the source-reconciliation rule (ADR-013, Option A).
Migrated from `.agents/skills/spec-kit/SKILL.md` sections
"Source Document Reconciliation" and "Existing Artifact Reconciliation".
