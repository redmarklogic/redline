# Feature Specification: Hook-First Enforcement Gaps

**Feature Branch**: `006-hook-enforcement-gaps`

**Created**: 2026-05-26

**Status**: Draft

**Input**: User description: "Hook-first enforcement gaps: ADR-011 mandates that every project rule expressible as a deterministic pattern check must be enforced by a pre-commit hook. A gap analysis against AGENTS.md and .agents/skills/ identified 10 rules currently stated only as instructions with no hook enforcement. The feature closes each gap by adding a dedicated pre-commit hook (or extending an existing one) and wiring it into .pre-commit-config.yaml."

## User Scenarios & Testing *(mandatory)*

### User Story 1 — Developer is blocked when a skill names an agent (Priority: P1)

A developer adds or edits a skill file in `.agents/skills/` that references an agent
persona by name (e.g. "Invoke Ron for this"). The pre-commit hook fires, prints the
offending file and line, cites ADR-010, and aborts the commit.

**Why this priority**: Dependency-direction violations between skills and agents are
the highest-risk architectural erosion per ADR-010 and ADR-011 P8. They accumulate
silently and are the hardest to recover from.

**Independent Test**: Add a skill file containing an agent name; run
`pre-commit run check-skills-persona-names`; observe a non-zero exit code and a
message citing ADR-010.

**Acceptance Scenarios**:

1. **Given** a new `.agents/skills/my-skill/SKILL.md` file containing the word "Kabilan", **When** `pre-commit run check-skills-persona-names` is executed, **Then** the hook exits non-zero and prints the filename, line number, and the offending line.
2. **Given** the same file with `<!-- hook: allow -->` appended to the offending line, **When** the hook is executed, **Then** it exits zero (suppression respected).
3. **Given** a clean skill file containing no agent names, **When** the hook is executed, **Then** it exits zero.

---

### User Story 2 — Developer is blocked by a forbidden Python pattern in source code (Priority: P1)

A developer commits Python source code (in `src/` or `scripts/`) that uses a
forbidden pattern: `argparse`, `archive/` imports, `.env` loaders, `os.getenv`
defaults, section-rule comment separators, or debug statements (`breakpoint()`,
`pdb`). Each dedicated hook fires, identifies the offending line, and aborts the
commit.

**Why this priority**: These rules protect code quality and architectural correctness in
the core source tree. Silent violations were previously only caught in human review.

**Independent Test**: For each hook, introduce the forbidden pattern into a file in the
relevant directory; run the corresponding `pre-commit run <hook-id>`; observe blocking
and a clear error message.

**Acceptance Scenarios**:

1. **Given** `src/rl/example.py` containing `import argparse`, **When** `pre-commit run check-no-argparse` is executed, **Then** it exits non-zero and reports the file and line.
2. **Given** `src/rl/example.py` containing `from archive.old_module import helper`, **When** `pre-commit run check-no-archive-imports` is executed, **Then** it exits non-zero and reports the file and line.
3. **Given** `scripts/run.py` containing `from dotenv import load_dotenv`, **When** `pre-commit run check-no-env-loader` is executed, **Then** it exits non-zero and reports the file and line.
4. **Given** `src/rl/example.py` containing `os.getenv("KEY", "default")`, **When** `pre-commit run check-no-env-defaults` is executed, **Then** it exits non-zero and reports the file and line.
5. **Given** `src/rl/example.py` containing `# ---------------------------------------------------------------------------`, **When** `pre-commit run check-no-section-rules` is executed, **Then** it exits non-zero and reports the file and line.
6. **Given** `src/rl/example.py` containing `breakpoint()`, **When** `pre-commit run check-no-debug-statements` is executed, **Then** it exits non-zero and reports the file and line.
7. **Given** any offending line followed by `# hook: allow`, **When** the corresponding hook is executed, **Then** the hook exits zero (suppression respected).

---

### User Story 3 — Committing a .ipynb file is blocked (Priority: P1)

A developer inadvertently stages a Jupyter notebook file. The `forbidden-ipynb-files`
hook aborts the commit with a message citing the AGENTS.md rule.

**Why this priority**: Notebook files are explicitly forbidden by AGENTS.md. A file
created by an IDE plugin or AI agent must not silently enter the repository.

**Independent Test**: Stage a `.ipynb` file; run `pre-commit run forbidden-ipynb-files`;
observe a non-zero exit code and a clear message.

**Acceptance Scenarios**:

1. **Given** a staged `analysis.ipynb` file, **When** `pre-commit run forbidden-ipynb-files` is executed, **Then** the hook exits non-zero with a message citing the AGENTS.md rule.
2. **Given** no `.ipynb` files staged, **When** the hook is executed, **Then** it exits zero.

---

### User Story 4 — Hook author is blocked when a new hook lacks an ADR reference (Priority: P2)

A developer commits a new `hooks/check-something.py` without including an ADR
reference in its module docstring (and without a `# no-adr:` exemption comment). The
`check-hook-adr-reference` hook aborts the commit and cites ADR-011 P6.

**Why this priority**: ADR-011 P6 mandates self-documenting hooks. Without this gate,
the documentation discipline degrades silently as new hooks are added.

**Independent Test**: Commit a `hooks/check-something.py` with only a plain docstring
(no "ADR-NNN"); run `pre-commit run check-hook-adr-reference`; observe a non-zero exit
code.

**Acceptance Scenarios**:

1. **Given** `hooks/check-new.py` with a module docstring containing no "ADR-" reference and no `# no-adr:` line, **When** `pre-commit run check-hook-adr-reference` is executed, **Then** it exits non-zero.
2. **Given** `hooks/check-new.py` with a docstring containing "See ADR-011", **When** the hook is executed, **Then** it exits zero.
3. **Given** `hooks/check-new.py` with no module docstring at all, **When** the hook is executed, **Then** it exits non-zero.
4. **Given** `hooks/check-new.py` with no ADR reference but with a `# no-adr: purely technical constraint` comment, **When** the hook is executed, **Then** it exits zero (exemption respected).

---

### User Story 5 — Hardcoded credentials are detected before commit (Priority: P2)

A developer accidentally includes a hardcoded API key, password, or token in a
committed file. The `detect-secrets` hook detects it and aborts the commit.

**Why this priority**: Credential leaks are a security incident. This is the most
cost-effective point to catch them.

**Independent Test**: Stage a file containing a string matching a secret pattern (e.g.
`api_key = "abc123secret"`); run `pre-commit run detect-secrets`; observe a non-zero
exit code.

**Acceptance Scenarios**:

1. **Given** a staged file containing `password = "hunter2"`, **When** `pre-commit run detect-secrets` is executed, **Then** it exits non-zero and identifies the file and line.
2. **Given** a clean file with no secret patterns, **When** the hook is executed, **Then** it exits zero.

---

### Edge Cases

- A skill file legitimately describes an agent-to-skill interaction and must use an agent name for context: suppressed with `<!-- hook: allow -->`.
- A test fixture in `tests/assets/` contains a string that looks like a secret but is intentional test data: handled via `.secrets.baseline` allowlist managed by `detect-secrets`.
- A hook script has no governing ADR and the author knows it: suppressed with `# no-adr: <reason>` in the file.
- `os.getenv("KEY", None)` — this is a borderline case; the hook treats `None` as a default (matches the pattern) since the rule is to use required helpers.
- The `check-hook-adr-reference` hook must not flag itself despite being a hook — it references ADR-011 P6 in its own docstring.

## Requirements *(mandatory)*

### Functional Requirements

**Gap 1 — Skill/agent persona name boundary**
- **FR-001**: The `check-banned-words.py` script MUST accept an `--md-dir` argument that scans `*.md` files recursively in the specified directory for banned words.
- **FR-002**: Markdown scan MUST respect inline `<!-- hook: allow -->` suppression on the same line.
- **FR-003**: A `check-skills-persona-names` hook entry in `.pre-commit-config.yaml` MUST call `check-banned-words.py` with `--md-dir=.agents/skills` and the full list of agent persona names as positional arguments.

**Gap 2 — No argparse in source code**
- **FR-004**: `hooks/check-no-argparse.py` MUST scan `.py` files in directories supplied via `--dirs` for `import argparse` or `from argparse import`.
- **FR-005**: The hook MUST exit non-zero when a match is found, reporting file and line number.

**Gap 3 — No archive imports**
- **FR-006**: `hooks/check-no-archive-imports.py` MUST scan `.py` files in `--dirs` directories for `import archive` or `from archive` imports.

**Gap 4 — No .ipynb files**
- **FR-007**: A `forbidden-ipynb-files` entry using `language: fail` MUST be added to `.pre-commit-config.yaml`, matching files with `\.ipynb$`.

**Gap 5 — No custom .env loaders**
- **FR-008**: `hooks/check-no-env-loader.py` MUST scan `.py` files in `--dirs` directories for `load_dotenv`, `from dotenv import`, or `import dotenv`.

**Gap 6 — No env var defaults**
- **FR-009**: `hooks/check-no-env-defaults.py` MUST scan `.py` files in `--dirs` directories for `os.getenv("KEY", ...)` or `os.environ.get("KEY", ...)` patterns with a second argument present.

**Gap 7 — No section-rule comments**
- **FR-010**: `hooks/check-no-section-rules.py` MUST scan `.py` files in `--dirs` directories for comment lines consisting of four or more consecutive dashes (e.g. `# ----`).

**Gap 8 — Hook ADR reference**
- **FR-011**: `hooks/check-hook-adr-reference.py` MUST scan all `.py` files in the hooks directory and fail if any file lacks a module docstring or lacks an "ADR-NNN" reference in its docstring without a `# no-adr:` exemption.

**Gap 9 — No hardcoded credentials**
- **FR-012**: A `detect-secrets` hook from `https://github.com/Yelp/detect-secrets` MUST be wired into `.pre-commit-config.yaml`.
- **FR-013**: A `.secrets.baseline` file MUST be generated and committed alongside the hook configuration.

**Gap 10 — No debug statements**
- **FR-014**: `hooks/check-no-debug-statements.py` MUST scan `.py` files in `--dirs` directories for `breakpoint()`, `import pdb`, `pdb.set_trace()`, `import ipdb`, and `ipdb.set_trace()`.

**Cross-cutting requirements**
- **FR-015**: Every new Python hook script MUST use only the Python standard library (no third-party packages).
- **FR-016**: Every new Python hook script MUST support `# hook: allow` inline suppression on any matched line.
- **FR-017**: Every new Python hook script MUST include a module docstring referencing the governing rule and its ADR number (per ADR-011 P6), or carry a `# no-adr:` exemption.
- **FR-018**: Every new Python hook script body MUST contain no project-specific literals; all project-specific values MUST be supplied as CLI args in `.pre-commit-config.yaml` (ADR-011 P4).
- **FR-019**: All new hook entries in `.pre-commit-config.yaml` MUST include `priority: 0` and `always_run: true`.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: All 10 enforcement gaps produce a non-zero pre-commit exit code when their forbidden pattern is introduced into an appropriate file; verified by manual test for each gap.
- **SC-002**: The full pre-commit suite (`pre-commit run --all-files`) passes on the clean repository after all hooks are wired in.
- **SC-003**: Every new hook script passes the `check-hook-adr-reference` gate (i.e. each references its governing ADR or carries a `# no-adr:` exemption).
- **SC-004**: The `check-banned-words` hook continues to pass (new hook bodies contain no project-specific literals).
- **SC-005**: Inline suppression (`# hook: allow` / `<!-- hook: allow -->`) is verified to unblock a commit for at least one hook.

## Assumptions

- The `detect-secrets` PyPI package will be added as a `pre-commit` managed dependency (not added to `pyproject.toml`), keeping it isolated from the project's runtime and development dependency graph.
- Agent persona names subject to the ADR-010 check are the nine names declared in `AGENTS.md` as of 2026-05-26: Ron, Mark, Graeme, John, Peter, Matt, Kabilan, Linda, Harriet.
- The `check-hook-adr-reference` hook applies to all `.py` files in `hooks/`, including itself; it must therefore reference ADR-011 in its own docstring.
- The `check-no-argparse` hook scans `src/` and `scripts/`; it does not scan `hooks/` (hook scripts are permitted to use argparse as infrastructure tooling).
- `check-no-section-rules` targets `src/` only (not `hooks/` or `tests/`); hook and test infrastructure is exempt.
- `check-no-debug-statements` targets `src/` and `tests/`; it does not target `hooks/` (hook scripts may use `sys.exit` and similar control-flow mechanisms that are not debug instrumentation).
- A `.secrets.baseline` file will be generated via `detect-secrets scan > .secrets.baseline` on the clean repository before the hook is activated, to prevent false positives on existing content.
