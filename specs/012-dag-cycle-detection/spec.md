# Feature Specification: Agent-Skill Graph DAG Validation and Cycle Remediation

**Feature Branch**: `012-dag-cycle-detection`

**Created**: 2026-05-31

**Status**: Draft

## User Scenarios & Testing *(mandatory)*

### User Story 1 — Cycle Detection Report (Priority: P1)

An engineer runs the DAG analysis tool and receives a complete list of every directed cycle in the agent-skill graph, including which nodes and edges form each cycle and the degree of each edge.

**Why this priority**: Cycle detection is the foundational capability. Without it, no remediation or downstream topological analysis is possible. Delivers immediate value even without remediation guidance.

**Independent Test**: Can be fully tested by running the analysis against a graph fixture with known cycles and verifying that every expected cycle appears in the report with correct node sequences and edge degrees.

**Acceptance Scenarios**:

1. **Given** `output/agent_skill_graph.json` contains two directed cycles, **When** the analysis runs, **Then** the cycle report lists exactly two cycles, each with the ordered node sequence, the participating edges, and each edge's degree.
2. **Given** `output/agent_skill_graph.json` contains zero cycles, **When** the analysis runs, **Then** the report states "graph is already a DAG", exits with code 0, and produces no error output.
3. **Given** `output/agent_skill_graph.json` contains a self-loop (a node referencing itself), **When** the analysis runs, **Then** the self-loop is reported as a cycle of length 1 with the edge's degree noted.
4. **Given** `output/agent_skill_graph.json` is missing or contains invalid JSON, **When** the analysis runs, **Then** it exits with a descriptive error message and non-zero exit code; no partial output files are written.

---

### User Story 2 — Prioritised Remediation Plan (Priority: P2)

An engineer reviews a prioritised list of edge-removal suggestions that would break all detected cycles, preferring to remove the edges with the least operational impact first.

**Why this priority**: The cycle report alone tells the engineer a problem exists; the remediation plan tells them what to do about it. The preference ordering (degree-3 → degree-2 → degree-1) protects routing tables from unilateral changes.

**Independent Test**: Can be fully tested against a graph fixture with cycles of mixed edge degrees; verify that the plan only recommends degree-1 removals when no higher-degree alternative exists, and that applying all recommendations leaves the graph acyclic.

**Acceptance Scenarios**:

1. **Given** a cycle containing one degree-3 edge and one degree-1 edge, **When** the remediation plan is generated, **Then** the plan recommends removing the degree-3 edge and does not recommend the degree-1 edge.
2. **Given** a cycle containing only degree-1 edges, **When** the remediation plan is generated, **Then** the plan lists the degree-1 edge removal but marks it as "requires human confirmation" and does not include it in the automated-safe set.
3. **Given** two cycles that share one edge, **When** the remediation plan is generated, **Then** removing that single shared edge appears once in the plan and is noted as breaking both cycles.
4. **Given** the remediation plan is applied (removals simulated in-memory), **When** the graph is re-checked, **Then** zero cycles remain.

---

### User Story 3 — Persisted, Machine-Readable and Human-Readable Output (Priority: P3)

Future automated analysis scripts and the engineering team can consume the analysis results without re-running the tool, via both a JSON file and a Markdown summary.

**Why this priority**: Persistence enables downstream tooling (layer assignment, impact analysis) to build on the DAG validation result without coupling to the analysis script's internals.

**Independent Test**: Can be fully tested by verifying that `output/dag_analysis.json` and `output/dag_analysis.md` are written after a successful run and that their content accurately reflects the cycle report and remediation plan.

**Acceptance Scenarios**:

1. **Given** the analysis completes successfully, **When** `output/dag_analysis.json` is inspected, **Then** it contains a `cycles` array, a `remediation_plan` array, a `dag_verified` boolean, and a `meta` block with run timestamp and graph statistics.
2. **Given** the analysis completes successfully, **When** `output/dag_analysis.md` is read, **Then** it contains a human-readable summary covering: DAG status (clean/cycles found), each cycle with edge details, the remediation plan with degree-labelled suggestions, and the DAG verification result.
3. **Given** the graph has zero cycles, **When** outputs are written, **Then** `dag_verified` is `true`, `cycles` is an empty array, `remediation_plan` is an empty array, and the Markdown states "graph is already a DAG".
4. **Given** a subsequent analysis script imports the graph module, **When** it requests the loaded DiGraph object, **Then** it receives a NetworkX DiGraph with all nodes and edges intact, including per-edge `degree` and `source_file` attributes.

---

### Edge Cases

- What happens when `output/agent_skill_graph.json` is missing or malformed?
- How does the system handle a cycle containing only degree-1 routing edges (no safe automated removal)?
- How does the system handle multiple cycles that share one or more edges (greedy vs. optimal removal)?
- How does the system handle a self-loop (node pointing to itself)?
- How does the system handle a completely disconnected subgraph (no path from or to any agent node)?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST load `output/agent_skill_graph.json` into a NetworkX DiGraph, preserving each edge's `degree` (1, 2, or 3) and `source_file` as edge attributes.
- **FR-002**: System MUST detect all directed cycles in the loaded DiGraph, including self-loops.
- **FR-003**: For each detected cycle, system MUST report the ordered node sequence, the edges involved, and the degree of each edge.
- **FR-004**: System MUST generate a remediation plan listing the minimum-impact edge removal(s) required to break every cycle.
- **FR-005**: Remediation plan MUST rank candidate removals by degree: degree-3 (file-link) preferred first, degree-2 (cross-reference) second, degree-1 (routing) last.
- **FR-006**: Any degree-1 edge suggested for removal MUST be flagged as "requires human confirmation" and excluded from the automated-safe removal set.
- **FR-007**: System MUST handle a zero-cycle graph by reporting "graph is already a DAG" and writing clean, valid output files without error.
- **FR-008**: System MUST simulate applying all automated-safe removals in memory and programmatically verify the resulting graph is acyclic.
- **FR-009**: System MUST write machine-readable results to `output/dag_analysis.json` with the schema described in FR-009a.
- **FR-009a**: `dag_analysis.json` schema MUST include: `meta` (timestamp, graph statistics), `cycles` (array of cycle objects), `remediation_plan` (array of edge-removal objects with `human_confirmation_required` flag), `dag_verified` (boolean).
- **FR-010**: System MUST write a human-readable summary to `output/dag_analysis.md` covering DAG status, each cycle, the remediation plan, and the verification result.
- **FR-011**: The loaded DiGraph MUST be importable as a Python object by subsequent analysis scripts without re-parsing the JSON.
- **FR-012**: System MUST NOT modify any source agent JD files or SKILL.md files.

### Key Entities

- **SkillGraph**: The NetworkX DiGraph loaded from `agent_skill_graph.json`; nodes are agent or skill identifier strings; edges carry `degree` (1/2/3) and `source_file` attributes.
- **Cycle**: An ordered sequence of node identifiers forming a closed directed path; associated with the edges traversed and their degrees.
- **RemediationPlan**: An ordered collection of edge-removal recommendations; each recommendation records the edge (`from`, `to`), its `degree`, the cycle(s) it participates in, a `human_confirmation_required` boolean, and the removal rationale.
- **DAGAnalysisReport**: The top-level output object combining `meta`, `cycles`, `remediation_plan`, and `dag_verified`; serialised to both JSON and Markdown.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A graph with N known directed cycles produces exactly N entries in the `cycles` array — no false positives, no missed cycles.
- **SC-002**: The remediation plan uses the fewest possible degree-1 edge removals; degree-1 edges appear only when no higher-degree edge can break the cycle.
- **SC-003**: After simulating all automated-safe removals, `dag_verified` is `true` — zero cycles remain in the modified graph.
- **SC-004**: Analysis of a graph with up to 500 nodes and 2,000 edges completes in under 30 seconds on a standard developer workstation.
- **SC-005**: A zero-cycle graph produces a clean "already a DAG" result with exit code 0, no errors, and valid (empty-array) output files.
- **SC-006**: The generated `output/dag_analysis.md` is parseable as valid Markdown with no rendering errors (no broken tables, no unclosed code fences).

## Assumptions

- `output/agent_skill_graph.json` is produced by `scripts/build_skill_graph.py` and follows the established schema: top-level keys `meta`, `nodes` (`agents`, `skills`), and `edges` (each with `from`, `to`, `degree`, `source_file`).
- NetworkX will be available as a project dependency; if not already present, it will be added before implementation.
- The analysis script is a standalone tool; it does not modify any source `.md` or agent JD files.
- Degree-1 routing edges represent agent skill-routing tables and carry the highest operational risk if removed; explicit human decision is required for any degree-1 removal.
- The current graph is modest in size (~100 nodes, ~300 edges); the 30-second performance target accounts for anticipated growth to 500 nodes.
- Exact optimal Minimum Feedback Arc Set computation is not required; a greedy heuristic that prioritises removal by degree (highest degree first) is sufficient.
- Outputs are written to `output/`; that directory already exists and is writable.
- "Applying removals" means simulating in-memory only — no source files are changed as part of this feature.
