# Research: RTK + CCE Enforcement

## R1: RTK-eligible command detection in Markdown code blocks

**Decision**: Parse fenced code blocks with shell language hints (`bash`, `sh`, `shell`, `console`, or untagged). Extract the first token of each line. Match against an explicit allowlist of RTK-eligible commands.

**Rationale**: Regex-based line scanning is simple, consistent with existing hooks (check-mermaid-syntax.py), and avoids the complexity of a full Markdown parser. Language-hint filtering prevents false positives from Python/JSON/YAML code blocks.

**Alternatives considered**:
- Full Markdown AST parser (markdown-it, mistune) — rejected: adds dependency; overkill for fenced block extraction
- Scan all code blocks regardless of language hint — rejected: too many false positives
- Only scan explicitly tagged `bash`/`sh` blocks — rejected: many instruction files use untagged blocks for shell commands

## R2: RTK-eligible command allowlist

**Decision**: `git`, `pytest`, `ruff`, `docker`, `uv`, `pip`, `mypy`, `prek`, `ls`, `cat`, `find`, `grep`

**Rationale**: These are the commands documented in `rtk.instructions.md` examples or commonly used in this repo's instruction files. RTK is a transparent proxy — any command works, but these are high-value targets where output compression saves the most tokens.

**Alternatives considered**:
- Flag ALL commands — rejected: `rtk` is optional for commands with small output (e.g., `cd`, `echo`)
- Maintain list in a separate config file — rejected: overengineered for a hook; constant at top of script is sufficient

## R3: Session store schema for audit queries

**Decision**: Use `session_store_sql` MCP tool with SQL queries. Tool calls are stored with tool name, input parameters, and timestamps. Filter by `tool_name IN ('run_in_terminal', 'read_file', 'context_search', 'grep_search')`.

**Rationale**: The `session_store_sql` tool already exposes the session store. No direct SQLite access needed. The MCP tool handles schema details.

**Alternatives considered**:
- Direct SQLite access to `.copilot/sessions.db` — rejected: tight coupling to internal schema; MCP tool is the public API
- Chronicle standup integration — rejected: chronicle provides summaries, not raw tool call data needed for compliance counting

## R4: RTK suppression in code blocks

**Decision**: Support `<!-- rtk:skip -->` on the line immediately preceding a fenced code block. When detected, the entire following code block is skipped.

**Rationale**: Follows the pattern established by `<!-- mermaid: allow -->` for mermaid hooks. Line-level suppression within blocks would be more complex and less readable.

**Alternatives considered**:
- Inline suppression per command (e.g., `git status  # rtk:skip`) — rejected: Markdown code blocks don't execute; inline comments would appear in rendered docs
- File-level skip list in hook config — rejected: too coarse; individual blocks may legitimately show raw commands (e.g., explaining what RTK replaces)

## R5: CCE decision tree structure

**Decision**: Replace the "When to Use" / "Do not use when" lists in `cce-mcp/SKILL.md` with a numbered decision tree. Three terminal branches:
1. Discovery/exploration → `context_search`
2. Known file, full content for editing → `read_file`
3. Known file, specific section → `context_search` + `expand_chunk`

**Rationale**: A decision tree is more actionable than a use/don't-use list. Agents can follow the numbered steps sequentially, reducing drift.

**Alternatives considered**:
- Mermaid flowchart — rejected: agents read text better than diagrams; also avoids mermaid rendering issues
- Separate enforcement skill — rejected: fragmenting CCE guidance into two skills increases confusion
