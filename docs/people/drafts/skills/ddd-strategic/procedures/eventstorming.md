# EventStorming Procedure

> DRAFT -- pending user approval. Do not promote to production.

**Parent skill:** `ddd-strategic`
**Source:** Khononov (*Learning DDD*), Vernon (*Implementing DDD*)
**Tooling:** Miro via `miro-mcp` (`layout_create`). Never Mermaid.
**Adapted for:** Solo founder + AI agents (Peter facilitates, Graeme provides domain facts, Mark validates problem framing).

---

## Colour Mapping (EventStorming to Miro)

| Element | Physical colour | Miro `fillColor` | Shape |
|---|---|---|---|
| Domain Events | Orange | `orange` | `square` |
| Commands | Light blue | `light_blue` | `square` |
| Actors | Small yellow | `yellow` | `square` (small) |
| Pain Points | Pink/red (rotated) | `light_pink` | `square` |
| Policies | Violet/lilac | `violet` | `square` |
| Read Models | Green | `green` | `square` |
| External Systems | Pink | `pink` | `square` |
| Aggregates | Large pale yellow | `light_yellow` | `rectangle` |
| Bounded Contexts | Frames | Frame item | -- |
| Pivotal Events | Vertical line | Shape (tall narrow) | -- |

---

## Steps

### Setup

1. Create a new Miro board (`board_create`) or use an existing one.
2. Register the board in `.agents/skills/miro-mcp/register.json`.
3. Create a large frame as the modelling surface (`layout_create`).

### Step 1: Domain Events

Brainstorm all domain events -- things that happened in the system. Write each on an **orange** sticky note in past tense (e.g., "Proposal Submitted", "Review Completed"). No filtering at this stage.

**Tool:** `layout_create` with fillColor=`orange`, shape=`square`.

### Step 2: Timeline

Arrange events left-to-right in chronological order. Identify parallel flows (events happening simultaneously on different swim lanes).

**Tool:** `layout_update` to reposition x/y coordinates.

### Step 3: Pain Points

Mark problematic areas with **light pink** sticky notes. Bottlenecks, manual workarounds, knowledge gaps, process breakdowns.

**Note:** Physical workshops rotate pain points 45 degrees. Miro sticky notes do not support rotation -- use colour differentiation instead.

**Tool:** `layout_create` with fillColor=`light_pink`.

### Step 4: Pivotal Events

Identify events that represent significant business transitions (e.g., "Order Placed" separates browsing from fulfilment). Mark with vertical divider lines. These often become bounded context boundaries.

**Tool:** `layout_create` with shape item (tall narrow rectangle).

### Step 5: Commands and Actors

For each event, identify:
- **Command** (light blue): What action triggered the event? Imperative mood (e.g., "Submit Proposal").
- **Actor** (yellow, small): Who or what issued the command? Person, role, system, or time trigger.

Place commands to the left of their events. Actors below/beside commands.

**Tool:** `layout_create` with fillColor=`light_blue` (commands) and fillColor=`yellow` (actors).

### Step 6: Policies

Identify automation rules: "Whenever [event], then [command]." Write on **violet** sticky notes. Policies connect events to commands without human intervention.

Example: "Whenever Review Completed, then Notify Author."

**Tool:** `layout_create` with fillColor=`violet`.

### Step 7: Read Models

What information does the actor need to make a decision before issuing a command? Write on **green** sticky notes. Place near the actor/command pair. These become the views/queries in the system.

**Tool:** `layout_create` with fillColor=`green`.

### Step 8: External Systems

Identify systems outside the bounded context that send events or receive commands. Write on **pink** sticky notes. Position at the edges of the timeline (distinguished from pain points by position).

Examples: payment gateway, email service, standards database.

**Tool:** `layout_create` with fillColor=`pink`.

### Step 9: Aggregates

Cluster related commands + events around a central concept. Name the aggregate on a **large light-yellow** sticky note (rectangle shape). The aggregate is the consistency boundary.

**Tool:** `layout_create` with fillColor=`light_yellow`, shape=`rectangle`.

### Step 10: Bounded Contexts

Draw boundaries (frames) around groups of aggregates that share a ubiquitous language. Label each frame. Where the language changes, a new context begins.

**Tool:** `layout_create` with frame items enclosing related aggregates.

---

## Post-EventStorming Outputs

| Output | Tool | Destination |
|---|---|---|
| Context Map | `diagram_create` (Mermaid flowchart) | `docs/architecture/domain-model.md` |
| Summary document | `doc_create` | Miro board |
| UL glossary per context | Manual | `docs/architecture/domain-model.md` UL table |
| Subdomain classification | `procedures/subdomain-classification.md` | `docs/architecture/domain-model.md` |
| Action items table | `table_create` + `table_sync_rows` | Miro board |
| Board state audit | `layout_read` | -- |

---

## Current Limitations

- **Connectors (arrows):** `layout_create` handles items but connectors between sticky notes (for Policy flows) may need the REST API. No MCP tool for connector creation currently.
- **Rotation:** Miro sticky notes do not support rotation. Use colour differentiation for pain points.
- **Tags:** REST API supports tags but these are not exposed via MCP tools currently.
