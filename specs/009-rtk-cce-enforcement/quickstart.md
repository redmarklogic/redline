# Quickstart: RTK + CCE Enforcement

## After implementation, verify with:

### Phase 0 — RTK hook
```bash
rtk uv run --frozen --offline hooks/check-rtk-in-docs.py --dirs=.agents/skills --dirs=.github/instructions --dirs=.github/agents --dirs=docs --dirs=specs
```

### Phase 1 — CCE skill
Read `.agents/skills/cce-mcp/SKILL.md` and confirm decision tree in "When to Use" section.

### Phase 2 — Session audit
```bash
rtk python -m scripts.audit_rtk_cce
```

### Phase 3 — RTK hook validation
Follow `specs/009-rtk-cce-enforcement/validation.md`.
