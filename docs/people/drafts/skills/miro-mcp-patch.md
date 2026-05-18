# Patch: miro-mcp skill

> DRAFT -- pending user approval. Do not promote to production.

**Target file:** `.agents/skills/miro-mcp/SKILL.md`
**Session:** 2026-05-17 DDD Topology Sync
**Reason:** Miro MCP server updated May 1, 2026 with 13 new tools. Current skill documents ~15 tools; actual count is 28.

---

## Changes

### 1. Update description frontmatter

Replace:
```yaml
description: Use when working with Miro boards — creating diagrams, documents, or tables, reading board content, or extracting structured context from visual designs via the Miro MCP server.
```

With:
```yaml
description: Use when working with Miro boards — creating or reading diagrams, documents, tables, layouts (sticky notes, shapes, frames), or extracting structured context from visual designs via the Miro MCP server.
```

### 2. Remove incorrect API note

Delete or replace:
```markdown
**IMPORTANT**: The Miro API does not support programmatic board creation. New boards must be created manually at miro.com, then their URL recorded in `register.json`. Update `status` from `"pending-url"` to `"active"` once the URL is confirmed.
```

With:
```markdown
**Board creation**: Use `board_create` to create boards programmatically, then record the URL in `register.json`. Update `status` from `"pending-url"` to `"active"` once confirmed.
```

### 3. Add new tools to Quick Reference table

Add these rows to the Quick Reference table:

```markdown
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
```

### 4. Add Layout Tools section (after "Available Tools > Content Creation")

```markdown
### Layout Tools (May 2026)
- **`layout_create`** - Create multiple board items (sticky notes, shapes, frames, text, cards) from DSL text with precise positioning and parent/child relationships. Primary tool for EventStorming boards.
- **`layout_get_dsl`** - Get the DSL format specification for `layout_create`
- **`layout_read`** - Read current board items as DSL
- **`layout_update`** - Update board items using find-and-replace DSL

### Board Management (May 2026)
- **`board_create`** - Create a new Miro board programmatically
- **`board_search_boards`** - Search boards by name or description

### Collaboration (May 2026)
- **`comment_list_comments`** - List comments on a board
- **`comment_reply`** - Reply to a comment thread
- **`comment_resolve`** - Resolve a comment thread

### Images (May 2026)
- **`image_create`** - Create image items on boards
```

### 5. Add Sticky Note Colours reference (after Layout Tools)

```markdown
## Sticky Note Colours

`layout_create` supports 16 named fill colours for sticky notes:

| Colour | Hex | Colour | Hex |
|---|---|---|---|
| `gray` | #F5F6F8 | `light_pink` | #FFCEE0 |
| `light_yellow` | #FFF9B1 | `pink` | #EA94BB |
| `yellow` | #F5D128 | `violet` | #C6A2D2 |
| `orange` | #FF9D48 | `red` | #F0939D |
| `light_green` | #D5F692 | `light_blue` | #A6CCF5 |
| `green` | #C9DF56 | `blue` | #6CD8FA |
| `dark_green` | #93D275 | `dark_blue` | #9EA9FF |
| `cyan` | #67C6C0 | `black` | #000000 |

Shapes: `square` (199dp default) and `rectangle` (350dp default).

For EventStorming colour conventions, see `ddd-strategic` `procedures/eventstorming.md`.
```

### 6. Add EventStorming cross-reference to Common Mistakes

Add:
```markdown
- **Using `diagram_create` for EventStorming** -- EventStorming outputs are spatial, colour-coded sticky notes. Use `layout_create`, not `diagram_create`. See `ddd-strategic` `procedures/eventstorming.md`.
- **Skipping `layout_get_dsl` before `layout_create`** -- always fetch the DSL spec first.
```
