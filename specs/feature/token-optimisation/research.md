# Research: Token Optimisation via Code Context Engine

**Date**: 2026-05-26  
**Plan**: [plan.md](plan.md)

## Resolved Unknowns

### RU-1: Windows Build Prerequisites for `[local]` Extra

**Decision**: Verify Visual Studio Build Tools (C++ workload) + CMake are installed before attempting `uv tool install "code-context-engine[local]"`.

**Rationale**: The `[local]` extra bundles fastembed + ONNX Runtime and compiles tree-sitter grammars at install time. This requires a C compiler and cmake. Missing tools cause an opaque pip build failure.

**Verification command**:
```powershell
cmake --version
cl /?
```

**Fallback**: If build tools are absent, use Ollama backend (`uv tool install code-context-engine` without `[local]`). Requires Ollama running at `localhost:11434` with `nomic-embed-text` pulled. The `[local]` path is strongly preferred for offline/air-gapped reliability.

---

### RU-2: CCE writes to `.github/copilot-instructions.md`, NOT `AGENTS.md`

**Decision**: Spec Scenario 3 risk framing was incorrect. For VS Code/Copilot, `cce init --agent copilot` writes to `.github/copilot-instructions.md`, not `AGENTS.md`.

**Source**: [CCE VS Code/Copilot docs](https://elara-labs.github.io/code-context-engine/guide/agents/copilot/)

**Impact on spec**: The AGENTS.md corruption risk is eliminated. The new concern is:
1. `.github/copilot-instructions.md` does not currently exist in the repo.
2. CCE creates it with a `<!-- CCE:BEGIN -->` / `<!-- CCE:END -->` block.
3. VS Code Copilot loads **both** `AGENTS.md` (via workspace custom instructions) and `.github/copilot-instructions.md`. They must not conflict.
4. The CCE-injected instruction block must be reviewed to confirm it does not introduce emoji, section rules, or directives that contradict AGENTS.md.

---

### RU-3: `.mcp.json` format for CCE

**Decision**: CCE uses `"command": "cce"` with `"args": ["serve"]`.

**Exact format**:
```json
{
  "mcpServers": {
    "context-engine": {
      "command": "cce",
      "args": ["serve"]
    }
  }
}
```

**Current state**: `.mcp.json` exists in the repo but is empty. CCE will populate it. The empty file must remain after `cce uninstall` to avoid untracked file churn.

---

### RU-4: Embedding backend and first-run download size

**Decision**: Use `fastembed` (`[local]` extra). Model: `BAAI/bge-small-en-v1.5`. First-run download: ~60 MB. Cached at `~/.cache/huggingface/`.

**Alternatives considered**: Ollama (`nomic-embed-text`) — rejected for initial setup because it requires a running Ollama daemon. `fastembed` is self-contained.

---

### RU-5: `cce init` side effects (full list)

`cce init --agent copilot` performs all of the following atomically:
1. Detects embedding backend (fastembed or Ollama)
2. Builds vector, FTS5, and graph indexes (stored locally in `.context-engine/`)
3. Installs git post-commit hooks for auto-reindex
4. Writes `.mcp.json` with MCP server config
5. Creates `.github/copilot-instructions.md` with CCE output compression block

**Uninstall reversal**: `cce uninstall` reverses items 3–5. The index (item 2) is deleted separately.

**VS Code reload**: After init, run `Developer: Reload Window` (not a full editor restart) to pick up the MCP server.

---

### RU-6: Expected Recall@5 for Markdown-heavy repo

**Decision**: Recall@5 ≥ 0.70 is the acceptance threshold. No independent published data exists for Markdown-only retrieval with CCE. The threshold is set conservatively based on:
- CCE achieves Recall@10 = 0.90 on Python source (FastAPI, 53 files)
- Markdown has no AST advantage; retrieval relies on BM25 + dense vector only
- The probe queries are deliberately close-match (not ambiguous) to give CCE the best chance

If Recall@5 < 0.70, re-indexing with a different embedding model (`BAAI/bge-large-en-v1.5`) may improve results before abandoning the tool.

---

## Alternatives Considered

| Alternative | Rejected because |
| --- | --- |
| `kapillamba4/code-memory` | Less mature (39 stars vs 136), no VS Code/Copilot-specific init, claims 50% savings vs CCE's measurable tracking |
| `fluffypony/mcp-code-indexer` | Description-based (not chunk retrieval), requires manual description generation, no savings dashboard |
| VS Code built-in semantic search | Already in use via `semantic_search` tool; problem is full-file `read_file` dominance, not search unavailability |
| Manual prompt scoping (user habit change) | Peter's point: requires knowing which section you need before asking; low leverage for this user's workflow |
