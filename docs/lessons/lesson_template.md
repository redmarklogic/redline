# Lesson Template

> Copy this file as `docs/lessons/NNNN-kebab-case-short-summary.md` where `NNNN` is the
> next four-digit sequence number. Delete this header block after copying.

---

# NNNN — Short descriptive title

**Date**: YYYY-MM-DD

**Skill**: `skill-name` (link: `.github/skills/<skill-name>/SKILL.md`)

**Context**: What project, data type, or task were we working on? 1-2 sentences that anchor
the learning to a concrete situation.

**Observation**: What did we see, or what did the reviewer point out? Be concrete: describe
the actual artefact (plot shape, code pattern, error message, metric value) -- not a
restatement of the principle.

**Root Cause**: Why did this happen? Identify the underlying decision, assumption, or
omission that produced the observation -- not a restatement of the symptom. If the cause
is unknown, write "Unknown" and leave a note for investigation.

**Principle**: The generalizable takeaway -- what to do or avoid in future. This should be
actionable and transferable to other projects or datasets.

**Source**: Link to the notebook, section, file, or conversation where the observation arose
(e.g., `src/notebooks/eda/005-july-ch4-hotspots.qmd`, Section 2.1).

---

## Filing guidelines

### When to create a new lesson file

- A concrete, non-obvious insight emerged from a conversation with the LLM or a review
  session that would change how you approach similar work in future.
- The insight is **self-contained**: it has a clear context, a specific observation, and a
  generalizable principle -- all three fields can be filled without hand-waving.
- The user explicitly asks to document a learning.

### When NOT to create a new lesson file

- The observation is **too vague** to state a concrete principle (e.g., "plots should be
  clear"). Hold off until you have a specific example.
- The insight is **already covered** by an existing lesson file. Instead, update the
  existing file if new evidence strengthens or refines the principle.
- The conversation is still evolving -- the principle is not yet settled. Wait until there
  is enough information to write all three fields confidently.
- The observation is **project-specific trivia** (e.g., a one-off data quirk) with no
  transferable principle.

### When to update an existing lesson file

- New evidence from a different context reinforces or nuances the same principle.
- The original observation was incomplete and new information fills the gap.
- Add the new context/observation as an additional `---` section below the original,
  preserving the original entry.

### Naming conventions

- **Prefix**: four-digit zero-padded sequence number (`0001`, `0002`, ...).
- **Slug**: kebab-case summary of the principle, max ~6 words.
- **Examples**: `0001-read-plot-before-narrative.md`,
  `0002-remove-redundant-visualisations.md`.

### Linking to skills

- Each lesson should reference the skill it feeds (e.g., `eda-interpreting-data`). Over
  time, mature lessons get distilled into the corresponding `SKILL.md` as permanent rules.
