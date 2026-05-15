# Sequence, Class, State, and ERD Procedures

Load this file after selecting one of: `sequenceDiagram`, `classDiagram`,
`stateDiagram-v2`, or `erDiagram`. Apply the section for your chosen type.

---

## Sequence Diagram (`sequenceDiagram`)

### What It Is For

Shows **runtime behaviour** — the order in which messages are passed between actors or
components over time. Use it to explain *how* the system executes a specific scenario,
not to document all scenarios.

### When to Use vs Alternatives

| Situation | Use |
|---|---|
| Complex or non-obvious runtime interaction | Sequence diagram |
| Every execution path through a feature | Do not diagram — read the code or write tests |
| High-level process for non-technical audience | Flowchart |
| How objects relate structurally | Class diagram |

### Rules

- **Only draw significant or non-obvious scenarios.** If understanding the flow requires
  reading the code or running a debugger, the diagram is probably not adding value. Reserve
  sequence diagrams for interactions that are genuinely hard to understand from code alone.
- Do not document every execution path, every error condition, and every use case. Pick
  the one scenario that is most complex or most likely to be misunderstood.
- Items run left-to-right; time flows top-to-bottom.
- Use `-->>`  (dashed) for return messages, `->>` (solid) for requests.
- Label every arrow with the message or request name.
- Use `participant X as Label` to give actors readable names.

### Common Mistakes

- **Diagramming every path** — documenting success, error, retry, and timeout in one
  sequence diagram. Each significant scenario gets its own diagram.
- **Too many participants** — more than 5-6 actors makes the diagram unreadable. Collapse
  internal implementation details into a single participant if they're not relevant to
  the scenario being explained.
- **Unlabelled arrows** — arrows without message names force the reader to infer the
  interaction. Every arrow must be labelled.

---

## Class Diagram (`classDiagram`)

### What It Is For

Shows the **static code structure** of a single component — its classes, attributes,
methods, and relationships (inheritance, aggregation). This is the deepest zoom level
(code-level detail). It is always optional — engineers can get this from the code itself.

### When to Use vs Alternatives

| Situation | Use |
|---|---|
| Explaining structure of a complex, non-obvious component | Class diagram |
| High-level architectural overview | Flowchart or context diagram — class diagrams show too much detail |
| Data storage and table relationships | ERD |
| All code in a system | Do not diagram — auto-generated class diagrams are unusable |

### Rules

- **Scope strictly to one component.** Do not mix classes from multiple containers or
  services in the same class diagram.
- **Include only attributes and methods relevant to the narrative.** Ask: does this field
  help the reader understand the design decision? If not, omit it.
- Use consistent naming conventions (match the codebase naming style).
- Class diagrams should be drawn manually, not auto-generated from code. Auto-generated
  diagrams include everything and produce an overwhelming mess of overlapping lines.

### Common Mistakes

- **Including every field and method** — produces visual noise. Only show what the
  diagram is trying to explain.
- **Using class diagrams for architectural overviews** — the wrong level of abstraction.
  Use a flowchart or component diagram instead.
- **Crossing services** — a class diagram that includes classes from multiple independent
  services is modelling the wrong thing. Draw one diagram per component.

---

## State Diagram (`stateDiagram-v2`)

### What It Is For

Models the **lifecycle of a document or entity** — the states it can occupy, and the
specific triggers that cause transitions between them. Use it as both a communication
tool and a design tool: drawing the diagram forces you to find edge cases you hadn't
considered.

### When to Use vs Alternatives

| Situation | Use |
|---|---|
| Document or entity with distinct lifecycle phases | State diagram |
| Business process (who does what, in what order) | Flowchart |
| Uniform input→output transition logic | Table |
| Every possible system state including implementation internals | Do not diagram — too complex |

### Rules

- **Document every possible transition, including edge cases.** The value of the diagram
  is in surfacing transitions you hadn't thought about. An incomplete state diagram is
  worse than no diagram — it creates false confidence.
- Always include the initial state `[*]` and at least one terminal state `[*]` (unless
  the lifecycle genuinely has no end).
- Keep state-specific behaviour encapsulated — each state should have a clear meaning.
  Avoid modelling states that are really conditional flags in shared logic.
- Label every transition with the triggering event or condition.

### Common Mistakes

- **Leaving states implicit** — a state that exists in the code but not in the diagram
  leads to unhandled edge cases. If it can happen, draw it.
- **Combining unrelated lifecycles** in one diagram. Each entity or document type gets
  its own state diagram.
- **Omitting the terminal state** — if a document can be archived, deleted, or closed,
  that state must be explicit.

---

## Entity Relationship Diagram (`erDiagram`)

### What It Is For

Visualises a **relational database schema** — how data entities relate to each other
(one-to-many, many-to-many) and what attributes they carry. Use it to design and
communicate data storage structure.

### When to Use vs Alternatives

| Situation | Use |
|---|---|
| Designing or documenting a database schema | ERD |
| Business workflows and domain logic | Flowchart or state diagram — ERDs focus on data storage only |
| Domain model (entities with behaviour) | Class diagram |
| Enterprise-wide data model | Do not diagram — impossible to maintain at that scope |

### Rules

- Show cardinality explicitly using standard notation (Crow's Foot: `||--o{`, `}o--||`, etc.).
- Include only the entities and relationships relevant to the decision being documented.
  An ERD for a single feature does not need to show the entire schema.
- Use singular nouns for entity names (`Project`, not `Projects`).

### Common Mistakes

- **The entity trap** — mapping database relationships directly to application workflows.
  An ERD that shows every CRUD operation is modelling a database wrapper, not a domain.
  Business logic belongs in flowcharts and state diagrams.
- **Enterprise-wide ERD** — spanning the entire organisation's data model in one diagram.
  It becomes impossible to maintain and useless to read. Scope to one feature or domain
  boundary.
- **Missing cardinality** — lines without cardinality notation leave the relationship
  ambiguous (is it one-to-one or one-to-many?). Always annotate.
