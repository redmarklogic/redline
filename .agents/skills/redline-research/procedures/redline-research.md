# Redline Research — Detailed Reference

### Inputs
- Research question from user
- Notebook register at `.agents/skills/redline-research/register.json`
- Project docs under `docs/architecture/` (read before querying notebooks)

### Outputs
- Cited research document at `docs/research/YYYYMMDD-<topic>.md`

### Out of Scope
- Online or web search (use only when user explicitly requests it)
- Code implementation or architecture decisions
- Specification writing (`spec-kit`) or design exploration (`brainstorming`)

### Prerequisites
- **`notebooklm-mcp`**: MCP server must be installed and authenticated.
- **`rag-prompting`**: Load before writing any notebook query.
- **`mermaid-diagrams`**: Load when the research document benefits from visual aids (concept maps, causal chains, system flows).
