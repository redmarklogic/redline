# DDD Topology Sync Session Report

**Date:** 2026-05-17
**Branch:** `feature/topology-sync`
**Participants:** Peter (Principal Engineer), User (Founder)
**Purpose:** Identify strategic DDD gaps in agent skills, research principles via NotebookLM, map document updates, and design EventStorming automation via Miro MCP.
**For:** Harriet (Head of People & Agent Development) -- to update Peter's skills, create new skills, and update affected documents.

---

## 1. Six DDD Gaps Identified

Six strategic DDD gaps were identified by cross-referencing the current agent skills and architecture documents against canonical DDD literature.

### Gap 1: Ubiquitous Language Stewardship

**Source:** Evans (DDD Blue Book), Vernon (IDDD)

- The Ubiquitous Language is a team effort, not a glossary maintained by one person.
- Language changes MUST trigger code refactors -- the code is an enduring expression of the model.
- Code and speech are the two enduring expressions; documents go stale.
- Every class, method, and variable name must reflect the UL.
- When the team discovers a better term, the code changes immediately.

**Documents to update:**
- Peter's JD (add UL stewardship responsibility)
- `docs/architecture/domain-model.md` (populate the empty UL table)
- `.agents/skills/python-domain-modeling/SKILL.md` (add "language change = code refactor" rule)

### Gap 2: Context Mapping

**Source:** Evans (DDD Blue Book), Vernon (IDDD), Khononov (Learning DDD)

Eight relationship types between bounded contexts:

| Relationship | Description |
|---|---|
| Partnership | Two teams succeed or fail together; synchronise plans |
| Shared Kernel | Shared subset of model; any change needs both teams to agree |
| Customer-Supplier | Downstream has veto/input on upstream priorities |
| Conformist | Downstream conforms to upstream model without influence |
| Anti-Corruption Layer (ACL) | Defensive translation layer isolating downstream from upstream |
| Open Host Service (OHS) | Upstream provides a well-defined protocol/API |
| Published Language | Shared interchange format (e.g., XML schema, JSON schema) |
| Separate Ways | No integration; contexts operate independently |

Key principle: Map the current reality first, not the desired state. The Context Map is a diagnostic tool.

**Documents to update:**
- `docs/architecture/domain-model.md` (populate the empty Context Map section)
- `.agents/skills/engineering-architecture/SKILL.md` (add context mapping principles)

### Gap 3: Subdomain Classification

**Source:** Evans (DDD Blue Book), Khononov (Learning DDD)

| Type | Competitive advantage? | Complexity | Volatility | Build or buy? |
|---|---|---|---|---|
| **Core** | Yes -- this is your differentiator | High | High (changes frequently) | Build in-house |
| **Supporting** | No competitive edge, but needed | Moderate | Moderate | Build (or simple buy) |
| **Generic** | Commodity; everyone needs it | Low-to-moderate | Low (stable) | Buy off-the-shelf |

Classification criteria: competitive advantage, complexity, change frequency, buyability.

**Documents to update:**
- `docs/architecture/domain-model.md` (add Rationale column to subdomain table)
- `.agents/skills/engineering-architecture/SKILL.md` (add classification criteria)

### Gap 4: EventStorming

**Source:** Khononov (Learning DDD), Vernon (IDDD)

Ten-step process extracted from two notebook sources (see Section 5 below for full detail).

Adapted for solo founder + AI agents context: Peter facilitates, Graeme provides domain facts, Mark validates problem framing.

**Documents to update:**
- Peter's JD (add EventStorming facilitation responsibility)
- `.agents/skills/engineering-architecture/SKILL.md` (add EventStorming procedure)

### Gap 5: Anti-Corruption Layer (ACL)

**Source:** Evans (DDD Blue Book), Vernon (IDDD)

- A defensive translation layer between bounded contexts.
- Use when: downstream is Core subdomain, upstream is messy/legacy/third-party.
- Components: Facades (simplified interface) + Adapters (protocol translation) + Translators (model mapping).
- The ACL belongs to the downstream context -- it protects the downstream model.
- Never let external models leak into your Core domain.

**Documents to update:**
- `docs/architecture/domain-model.md` (add ACL pattern reference)
- `.agents/skills/engineering-architecture/SKILL.md` (add ACL pattern guidance)

### Gap 6: Model Evolution Governance

**Source:** Evans (DDD Blue Book), Vernon (IDDD)

- The domain model must constantly adapt as understanding deepens.
- Language changes require team decision (not unilateral).
- CI at model + code level: keep model and code synchronised.
- Tactical evolution patterns:
  - **Value Objects:** replace entirely (immutable by design).
  - **Entities:** update attributes, maintain identity.
  - **Aggregates:** keep small, one transaction per aggregate, eventual consistency between aggregates.

**Documents to update:**
- Peter's JD (add model evolution governance responsibility)
- `docs/architecture/domain-model.md` (add Governance section)
- `.agents/skills/python-domain-modeling/SKILL.md` (add evolution governance cross-reference)

---

## 2. Document Update Plan

### 2.1 Three-Way Document Split (Approved)

The current `docs/architecture/domain-model.md` conflates living project state with reusable DDD principles. Proposed split:

| Document | Purpose | Content |
|---|---|---|
| `docs/architecture/domain-model.md` | Living project state only (~100-150 lines) | Current subdomain table, bounded contexts, UL table, Context Map, Entity/VO registry. Changes as the project evolves. |
| `.agents/skills/ddd-strategic/SKILL.md` (NEW) + `procedures/` | Strategic DDD principles | Subdomain classification criteria, Context Mapping types, EventStorming process, ACL pattern, UL stewardship rules, evolution governance. Reusable across projects. |
| `.agents/skills/python-domain-modeling/SKILL.md` (EXISTS) | Tactical DDD conventions | Minor additions: "language change = code refactor" rule, evolution governance cross-reference. Already well-developed. |

### 2.2 Full Document-to-Gap Mapping

| Document | Gaps addressed | Action |
|---|---|---|
| `docs/architecture/domain-model.md` | 1, 2, 3, 5, 6 | Populate empty sections, add Rationale column, add Governance section |
| `.agents/skills/ddd-strategic/SKILL.md` (NEW) | 1, 2, 3, 4, 5, 6 | Create new skill with all strategic DDD principles |
| `.agents/skills/python-domain-modeling/SKILL.md` | 1, 6 | Add UL rule, evolution cross-reference |
| `.agents/skills/engineering-architecture/SKILL.md` | 2, 3, 4, 5 | Add context mapping, subdomain classification, EventStorming, ACL content |
| `.agents/skills/miro-mcp/SKILL.md` | 4 | Update tool inventory (new May 2026 tools), add EventStorming procedure reference |
| Peter's JD (`.github/agents/rl.peter.agent.md`) | 1, 4, 6 | Add UL stewardship, EventStorming facilitation, evolution governance responsibilities |

---

## 3. Mermaid Diagram Applicability

Assessed which DDD artifacts can be rendered in Mermaid (v8.8.0 ceiling constraint from VS Code Office Viewer plugin).

### Draw NOW in Mermaid

| Diagram | Mermaid type | Purpose |
|---|---|---|
| Context Map | `flowchart TD` | Bounded context relationships (ACL, OHS, Partnership, etc.) |
| Layer Architecture | `flowchart TD` | Replace current ASCII art in domain-model.md |
| C4 Level 2 Containers | `flowchart TD` + C4 colour conventions | System containers and their interactions |

### Draw LATER in Mermaid (when content exists)

| Diagram | Mermaid type | Purpose |
|---|---|---|
| Aggregate class diagrams | `classDiagram` | Entity/VO relationships within aggregates |
| Domain event flows | `sequenceDiagram` | Event-driven interactions between contexts |
| Entity state diagrams | `stateDiagram-v2` | Lifecycle states of key entities |

### NEVER draw in Mermaid

| Artifact | Reason | Where instead |
|---|---|---|
| EventStorming outputs | Spatial, colour-coded, sticky-note-based; fundamentally incompatible with text diagrams | **Miro** via `layout_create` |

---

## 4. Miro MCP Server Update (May 2026)

### New Tools (May 1, 2026 changelog)

The Miro MCP server now has **28 tools** (up from the ~15 documented in the current `miro-mcp` skill). New tools added:

| Tool | Purpose |
|---|---|
| `layout_create` | **Bulk creator** for frames, sticky notes, shapes, text, cards -- with positioning and parent/child relationships |
| `layout_get_dsl` | Get the DSL specification for `layout_create` |
| `layout_read` | Read current board items as DSL |
| `layout_update` | Update board items via find-and-replace DSL |
| `board_create` | Create a new Miro board |
| `board_search_boards` | Search boards by name/description |
| `comment_list_comments` | List comments on a board |
| `comment_reply` | Reply to a comment |
| `comment_resolve` | Resolve a comment thread |
| `image_create` | Create an image item |
| Code widget CRUD | Create, read, update, delete code widgets |

### Key Correction

Previous finding stated "The current Miro MCP tools cannot create sticky notes." This was **wrong**. The `layout_create` tool creates sticky notes with:
- 16 named fill colours (gray, light_yellow, yellow, orange, light_green, green, dark_green, cyan, light_pink, pink, violet, red, light_blue, blue, dark_blue, black)
- Two shapes: `square` (199dp) and `rectangle` (350dp)
- x/y positioning
- Parent frames (parent/child relationships)
- Tags and connectors support

---

## 5. EventStorming Process (10 Steps)

Extracted from Khononov (Learning DDD) and Vernon (IDDD) via NotebookLM notebook `c04e18d3-e1e6-47f0-879a-d0e4a65adcb0` (Software Architecture & DDD).

### Step 1: Domain Events

Brainstorm all domain events (things that happened). Write each on an **orange** sticky note in past tense (e.g., "Proposal Submitted", "Review Completed"). No filtering -- capture everything.

### Step 2: Timeline

Arrange events left-to-right in chronological order. Identify parallel flows (events happening simultaneously on different swim lanes). This is the first structural insight.

### Step 3: Pain Points

Mark problematic areas with **pink** (or **red**) sticky notes. Bottlenecks, manual workarounds, knowledge gaps, process breakdowns. Rotated 45 degrees in physical workshops (not possible in Miro; use colour differentiation instead).

### Step 4: Pivotal Events

Identify events that represent significant business transitions (e.g., "Order Placed" separates browsing from fulfilment). Mark with vertical divider lines. These often become bounded context boundaries.

### Step 5: Commands and Actors

For each event, identify:
- **Command** (**light blue** sticky note): what action triggered the event? Imperative mood (e.g., "Submit Proposal").
- **Actor** (**yellow** sticky note, small): who or what issued the command? Can be a person, role, system, or time trigger.

Place commands to the left of their events, actors below/beside commands.

### Step 6: Policies

Identify automation rules: "Whenever [event], then [command]." Write on **violet** sticky notes. Policies represent business rules that connect events to commands without human intervention (e.g., "Whenever Review Completed, then Notify Author").

### Step 7: Read Models

What information does the actor need to make a decision before issuing a command? Write on **green** sticky notes. Place near the actor/command pair. These become the views/queries in the system.

### Step 8: External Systems

Identify systems outside your bounded context that send events or receive commands. Write on **pink** sticky notes (distinguished from pain points by position -- external systems sit at the edges). Examples: payment gateway, email service, standards database.

### Step 9: Aggregates

Cluster related commands + events around a central concept. Name the aggregate on a **large light-yellow** sticky note (rectangle shape). The aggregate is the consistency boundary -- all commands targeting it must be transactionally consistent.

### Step 10: Bounded Contexts

Draw boundaries (frames) around groups of aggregates that share a ubiquitous language. These become your bounded contexts. Label each frame. Where the language changes, a new context begins.

### Post-EventStorming Outputs

- Context Map (flowchart showing BC relationships)
- Ubiquitous Language glossary per context
- Subdomain classification (Core/Supporting/Generic)
- Action items and follow-up decisions

---

## 6. EventStorming Automation via Miro MCP

### Colour Mapping: EventStorming Conventions to Miro Sticky Note Colours

| EventStorming element | Physical colour | Miro `fillColor` | Shape |
|---|---|---|---|
| Domain Events | Orange | `orange` | `square` |
| Commands | Light blue | `light_blue` | `square` |
| Actors | Small yellow | `yellow` | `square` (small width) |
| Pain Points | Pink/red (rotated) | `light_pink` or `red` | `square` |
| Policies | Violet/lilac | `violet` | `square` |
| Read Models | Green | `green` | `square` |
| External Systems | Pink | `pink` | `square` |
| Aggregates | Large pale yellow | `light_yellow` | `rectangle` (350dp) |
| Bounded Contexts | Frames/borders | Frame item | -- |
| Pivotal Events | Vertical line | Shape item (tall narrow) | -- |

### Tool Mapping per Step

| Step | What to create | Miro MCP tool | Configuration |
|---|---|---|---|
| Setup | New board | `board_create` | -- |
| Setup | Modelling surface frame | `layout_create` | Frame, large dimensions |
| 1. Domain Events | Orange sticky notes | `layout_create` | fillColor=`orange`, square |
| 2. Timeline | Rearrange events L-to-R | `layout_update` | Reposition x/y |
| 3. Pain Points | Pink sticky notes | `layout_create` | fillColor=`light_pink` |
| 4. Pivotal Events | Vertical divider lines | `layout_create` | Shape (tall narrow rectangle) |
| 5. Commands | Light blue sticky notes | `layout_create` | fillColor=`light_blue` |
| 5. Actors | Small yellow sticky notes | `layout_create` | fillColor=`yellow`, small |
| 6. Policies | Violet sticky notes | `layout_create` | fillColor=`violet` |
| 7. Read Models | Green sticky notes | `layout_create` | fillColor=`green` |
| 8. External Systems | Pink sticky notes | `layout_create` | fillColor=`pink` |
| 9. Aggregates | Large yellow sticky notes | `layout_create` | fillColor=`light_yellow`, rectangle |
| 10. Bounded Contexts | Frames around groups | `layout_create` | Frame items |
| Post | Context Map | `diagram_create` | type=`flowchart` |
| Post | Summary document | `doc_create` | Markdown |
| Post | Action items table | `table_create` + `table_sync_rows` | Columns: Finding, Owner, Status |
| Audit | Read board state | `layout_read` | Returns DSL |

### Current Limitations

- **Connectors (arrows):** `layout_create` handles items, but connectors between sticky notes (for Policy flows) likely need the REST API. No MCP tool for connector creation currently.
- **Rotation:** Miro sticky notes don't support rotation. Pain Points that are rotated 45 degrees in physical workshops use colour differentiation instead.
- **Tags:** REST API supports colour-coded tags but these are not exposed via MCP tools currently.

---

## 7. Skills to Create or Update

### New Skill: `ddd-strategic`

- **Location:** `.agents/skills/ddd-strategic/SKILL.md` + `procedures/`
- **Content:** All strategic DDD principles from Gaps 1-6 (UL stewardship, Context Mapping types, subdomain classification criteria, EventStorming process, ACL pattern, evolution governance)
- **Procedures subdirectory:** `procedures/eventstorming.md` (10-step process), `procedures/context-mapping.md`, `procedures/subdomain-classification.md`
- **Owner:** Peter
- **Grounding:** NotebookLM notebook `c04e18d3-e1e6-47f0-879a-d0e4a65adcb0` (Software Architecture & DDD)

### Update: `engineering-architecture`

- **Location:** `.agents/skills/engineering-architecture/SKILL.md`
- **Current state:** "Pending notebook grounding" -- structure defined but content not elaborated
- **Add:** Context mapping, subdomain classification, EventStorming, ACL pattern content
- **Cross-reference:** New `ddd-strategic` skill for detailed procedures

### Update: `python-domain-modeling`

- **Location:** `.agents/skills/python-domain-modeling/SKILL.md`
- **Add:** "Language change = code refactor" rule, evolution governance cross-reference to `ddd-strategic`

### Update: `miro-mcp`

- **Location:** `.agents/skills/miro-mcp/SKILL.md`
- **Add:** New May 2026 tools (layout_*, board_create, comments, code widgets), EventStorming procedure reference
- **Correct:** Tool inventory to reflect 28 tools

### Update: `mermaid-diagrams`

- No content changes needed. Already well-governed.
- Reference: `ddd-strategic` procedures should note Mermaid applicability per artifact type.

---

## 8. Peter's JD Updates

The following responsibilities should be added to Peter's agent JD (`.github/agents/rl.peter.agent.md`):

1. **Ubiquitous Language stewardship** -- ensuring the UL is maintained as a team artefact and that language changes trigger code refactors.
2. **EventStorming facilitation** -- leading EventStorming sessions (adapted for solo founder + AI agents), using Miro MCP tools for board automation.
3. **Model evolution governance** -- owning the process for model changes: team decision, CI synchronisation, aggregate sizing.
4. **Context Mapping ownership** -- maintaining the Context Map as a living diagnostic tool in `domain-model.md`.
5. **Subdomain classification rationale** -- ensuring every subdomain has a documented rationale for its Core/Supporting/Generic classification.

---

## 9. Dependencies and Sequencing

Recommended order of execution:

1. **Create `ddd-strategic` skill** (all principles in one place) -- blocks all other updates
2. **Update `engineering-architecture` skill** (cross-reference `ddd-strategic`)
3. **Update `python-domain-modeling` skill** (minor additions)
4. **Update `miro-mcp` skill** (new tool inventory + EventStorming reference)
5. **Update Peter's JD** (new responsibilities)
6. **Update `domain-model.md`** (populate sections using the new skill as reference)
7. **Draw Mermaid diagrams** (Context Map, Layer Architecture, C4 Level 2)

Steps 2-4 can be parallelised. Steps 5-6 depend on Step 1. Step 7 depends on Step 6.

---

## 10. NotebookLM Research Sources

All DDD research was grounded in NotebookLM notebook **Software Architecture & DDD** (ID: `c04e18d3-e1e6-47f0-879a-d0e4a65adcb0`), which contains 10 canonical books:

- Eric Evans -- Domain-Driven Design (Blue Book)
- Vaughn Vernon -- Implementing Domain-Driven Design (IDDD)
- Vlad Khononov -- Learning Domain-Driven Design
- Neal Ford et al. -- Fundamentals of Software Architecture
- John Ousterhout -- A Philosophy of Software Design
- Gang of Four -- Design Patterns
- (+ 4 additional sources in the notebook)
