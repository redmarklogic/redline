# Hook CLI Contracts

**Feature**: 006-hook-enforcement-gaps  
**Date**: 2026-05-26

These are the command-line contracts for each Python hook. All project-specific values live here (in `.pre-commit-config.yaml`), never in the hook body (ADR-011 P4).

---

## check-banned-words (Gap 1 — check-skills-persona-names)

```
rtk uv run --frozen --offline hooks/check-banned-words.py \
  --md-dir=.agents/skills \
  Ron Mark Graeme John Peter Matt Kabilan Linda Harriet
```

| Argument | Required | Description |
|----------|----------|-------------|
| `--hooks-dir=<dir>` | When scanning .py files | Directory of hook scripts to scan |
| `--md-dir=<dir>` | When scanning .md files | Directory of Markdown files to scan recursively |
| `word [word ...]` | Yes | One or more banned words (whole-word, case-sensitive) |

Exit: `0` clean, `1` violations found.

---

## check-no-argparse (Gap 2)

```
rtk uv run --frozen --offline hooks/check-no-argparse.py \
  --dirs=src \
  --dirs=scripts
```

| Argument | Required | Description |
|----------|----------|-------------|
| `--dirs=<dir>` | Yes (repeatable) | Directory to scan recursively for `.py` files |

Exit: `0` clean, `1` violations found.

---

## check-no-archive-imports (Gap 3)

```
rtk uv run --frozen --offline hooks/check-no-archive-imports.py \
  --dirs=src
```

Same `--dirs` contract as check-no-argparse.

---

## forbidden-ipynb-files (Gap 4)

Config-only. No Python script.

```yaml
- id: forbidden-ipynb-files
  name: forbidden ipynb files
  entry: "found .ipynb notebook file; AGENTS.md forbids notebook creation; remove it"
  language: fail
  files: \.ipynb$
  priority: 0
```

---

## check-no-env-loader (Gap 5)

```
rtk uv run --frozen --offline hooks/check-no-env-loader.py \
  --dirs=src \
  --dirs=scripts
```

Same `--dirs` contract as check-no-argparse.

---

## check-no-env-defaults (Gap 6)

```
rtk uv run --frozen --offline hooks/check-no-env-defaults.py \
  --dirs=src \
  --dirs=scripts
```

Same `--dirs` contract as check-no-argparse.

---

## check-no-section-rules (Gap 7)

```
rtk uv run --frozen --offline hooks/check-no-section-rules.py \
  --dirs=src
```

Scans `src/` only. `hooks/` and `tests/` are exempt (per spec Assumptions).

---

## check-hook-adr-reference (Gap 8)

```
rtk uv run --frozen --offline hooks/check-hook-adr-reference.py \
  --hooks-dir=hooks
```

| Argument | Required | Description |
|----------|----------|-------------|
| `--hooks-dir=<dir>` | Yes | Directory containing hook `.py` scripts to audit |

---

## detect-secrets (Gap 9)

Managed by pre-commit. Not a project script.

```yaml
- repo: https://github.com/Yelp/detect-secrets
  rev: v1.5.0
  hooks:
    - id: detect-secrets
      args: ["--baseline", ".secrets.baseline"]
      priority: 0
```

Baseline regeneration (run once on clean repo before activation):
```
rtk uv run detect-secrets scan > .secrets.baseline
```

---

## check-no-debug-statements (Gap 10)

```
rtk uv run --frozen --offline hooks/check-no-debug-statements.py \
  --dirs=src \
  --dirs=tests
```

Scans `src/` and `tests/`. `hooks/` is exempt (per spec Assumptions).
