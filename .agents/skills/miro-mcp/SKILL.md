---
name: miro-mcp
description: Use when working with Miro boards — creating or reading diagrams, documents, tables, layouts (sticky notes, shapes, frames), or extracting structured context from visual designs via the Miro MCP server.
---

## Boundary Contract

## Quick Reference

| Task | Tool |
|------|------|
| Get diagram DSL spec | `diagram_get_dsl` |
| Create diagram | `diagram_create` |
| Create document | `doc_create` |
| Read document | `doc_get` |
| Edit document | `doc_update` |
| Create table | `table_create` |
| Add/update table rows | `table_sync_rows` |
| Read table data | `table_list_rows` |
| Discover board contents | `context_explore` |
| Extract item details | `context_get` |
| List board items | `board_list_items` |
| Create layout items (sticky notes, shapes, frames, text, cards) | `layout_create` |
| Get layout DSL spec | `layout_get_dsl` |
| Read board items as DSL | `layout_read` |
| Update layout items | `layout_update` |
| Create a new board | `board_create` |
| Search boards | `board_search_boards` |
| List comments | `comment_list_comments` |
| Reply to a comment | `comment_reply` |
| Resolve a comment | `comment_resolve` |
| Create an image | `image_create` |


See `procedures/miro-mcp.md` for detailed rules, examples, and extended reference.

## Common Mistakes

- **Skipping `diagram_get_dsl` before `diagram_create`** — the DSL format is not obvious; always fetch the spec first or the diagram will fail.
- **Calling `context_get` without `context_explore` first** — you need item URLs from `context_explore`; guessing URLs will fail.
- **Placing all items at `(0, 0)`** — items stack on top of each other. Use spacing: diagrams 2000–3000 units apart, documents 500–1000 units.
- **Calling `doc_update` without `doc_get` first** — `doc_update` requires the version token from `doc_get`; skipping causes a version conflict error.
- **Using `table_sync_rows` without `key_column`** — without a key column every call inserts new rows instead of updating existing ones.
- **Using `diagram_create` for EventStorming** — EventStorming uses `layout_create` (spatial, colour-coded sticky notes), not `diagram_create`.
- **Skipping `layout_get_dsl` before `layout_create`** — always fetch the DSL spec first.
