# Feature Specification: Skill Bloat Reduction

**Feature Branch**: `011-skill-bloat-reduction`

**Created**: 2026-05-30

**Status**: Draft

**Input**: User description: "Reduce skill bloat across 87 custom skills by building an agent-skill reachability graph, identifying orphans, merging redundant clusters, and renaming survivors with consistent prefixes."

## User Scenarios & Testing

### User Story 1 -- Build Agent-Skill Reachability Graph (Priority: P1)

Harriet needs to see which skills are connected to which agents (directly or transitively) so she can identify orphans and redundancy. Currently this mapping exists only as prose in agent JDs and is never validated programmatically.

**Why this priority**: Every downstream decision (orphan detection, merge candidates, rename scope) depends on an accurate graph. Without it, pruning is guesswork.

**Independent Test**: Run the graph-builder script; verify it produces a JSON adjacency list covering all 9 `rl.*` agents, all `speckit.*` agents, and all 87 skills. Spot-check 5 known agent-skill links against JD files.

**Acceptance Scenarios**:

1. **Given** agent JD files in `.github/agents/rl.*.agent.md` and `speckit.*.agent.md`, **When** the graph-builder runs, **Then** it produces `agent_skill_graph.json` with nodes for every agent and every skill directory in `.agents/skills/`.
2. **Given** a skill SKILL.md that references another skill by name (e.g. `speckit-static-checks-run` references `python-static-checks`), **When** the graph-builder parses it, **Then** a degree-2 edge exists from the referencing skill to the referenced skill.
3. **Given** a skill that appears in no agent JD and is referenced by no other skill, **When** the graph is queried for orphans, **Then** that skill appears in the orphan list.
4. **Given** the graph is built, **When** queried for `pm-structural-integrity-auditor`, **Then** it shows edges from at least Ron, Mark, Peter, Graeme, John (5+ agents).

---

### User Story 2 -- Identify and Remove Orphan Skills (Priority: P1)

After building the graph, Harriet finds skills with zero in-degree from any agent (directly or transitively). These skills consume token budget on every session but are never triggered.

**Why this priority**: Orphans are the lowest-risk removals -- no agent depends on them. Removing them delivers immediate token savings with zero routing breakage.

**Independent Test**: Query the graph for nodes with zero in-degree from agent nodes. Cross-reference each candidate against `AGENTS.md`, all agent JDs, and all other SKILL.md files to confirm no implicit reference exists.

**Acceptance Scenarios**:

1. **Given** the reachability graph identifies `mental-models` as an orphan, **When** confirmed by manual review, **Then** the skill directory is deleted or archived.
2. **Given** the reachability graph identifies `ceremony-monthly-editorial-session` as an orphan, **When** Harriet reviews with John (its expected owner), **Then** it is either re-linked to John's routing table or deleted.
3. **Given** the reachability graph identifies `python-crewai` as an orphan, **When** Kabilan confirms CrewAI is not in active use, **Then** the skill is deleted.
4. **Given** a skill flagged as orphan that is actually referenced transitively (false positive), **When** the reviewer checks degree-2+ edges, **Then** the skill is kept and the false positive is documented.

---

### User Story 3 -- Merge Redundant Skill Clusters (Priority: P2)

Kabilan has 50+ skills routed to him. Several clusters overlap (e.g. three Python design skills, four Python quality skills, five EDA skills). Merging within each cluster reduces total skill count without losing content.

**Why this priority**: The Language/Stack layer has the highest skill density. Consolidating clusters reduces Kabilan's skill load from ~50 to ~35-40, improving agent attention budget.

**Independent Test**: For each proposed merge, verify: (a) the merged skill contains all unique content from the source skills, (b) agent JD routing tables reference the merged name, (c) no content was silently dropped.

**Acceptance Scenarios**:

1. **Given** `python-function-design`, `python-class-design`, `python-module-structure` are candidates for merge, **When** their SKILL.md files are compared, **Then** a decision (MERGE, KEEP, or UPDATE) is recorded with rationale.
2. **Given** a MERGE decision for a cluster, **When** executed, **Then** one target skill directory contains the consolidated SKILL.md, source directories are deleted, and all agent JD references are updated.
3. **Given** a KEEP decision (skills are similar but serve distinct purposes), **When** recorded, **Then** both skills are annotated in their Boundary Contract to explain the distinction.
4. **Given** `executing-plans` and `writing-plans` are SUPERSEDED stubs, **When** reviewed, **Then** they are either deleted (if no references remain) or reduced to single-line redirects.

---

### User Story 4 -- Classify Skills by Source Layer (Priority: P2)

Each skill is classified into one of five layers (Vendor-Framework, SpecKit-Extension, Tool/Platform, Language/Stack, Domain/Ops). The classification determines what pruning actions are permissible.

**Why this priority**: Prevents accidental deletion of vendor skills or SpecKit extension hooks that appear orphaned from `rl.*` agents but are routed from `speckit.*` agents.

**Independent Test**: Every skill in `.agents/skills/` has a layer classification. No vendor-framework skill is in the merge/delete candidate list. All `speckit-*` skills are classified as SpecKit-Extension.

**Acceptance Scenarios**:

1. **Given** the classification runs, **When** it encounters `brainstorming`, `test-driven-development`, or `using-superpowers`, **Then** they are classified as Vendor-Framework and excluded from modification.
2. **Given** `speckit-shaping-gate-check` is classified, **When** the classification checks its metadata (`author: github-spec-kit`), **Then** it is classified as SpecKit-Extension, not orphaned.
3. **Given** `python-linting` is classified, **When** it falls under Language/Stack, **Then** it is eligible for consolidation review.

---

### User Story 5 -- Rename Skills with Consistent Prefixes (Priority: P3)

After pruning and merging, surviving custom skills are renamed using a prefix convention so they sort into logical groups (like `speckit.*` agents do). MCP skills flip from `*-mcp` suffix to `mcp-*` prefix.

**Why this priority**: Naming consistency improves discoverability and reduces routing errors, but is cosmetic relative to actual skill reduction. Executes last to minimize rename churn.

**Independent Test**: After rename, every custom skill directory name matches its declared prefix group. All references in agent JDs, `skills-lock.json`, `AGENTS.md`, and cross-skill references are updated. `prek run -a` passes clean.

**Acceptance Scenarios**:

1. **Given** `cce-mcp` is renamed to `mcp-cce`, **When** all references are updated, **Then** `grep -r "cce-mcp" .github/agents/ .agents/skills/ AGENTS.md` returns zero matches.
2. **Given** `engineering-architecture` is renamed to `arch-engineering`, **When** Peter's JD is updated, **Then** his routing table references `arch-engineering`.
3. **Given** `version-control` is renamed to `git-version-control`, **When** Kabilan's JD is updated, **Then** the routing table references `git-version-control`.
4. **Given** a vendor-framework skill (e.g. `brainstorming`), **When** the rename phase runs, **Then** it is skipped -- vendor skills are never renamed.
5. **Given** all renames are applied, **When** `prek run -a` executes, **Then** it exits with zero errors.

---

### User Story 6 -- Visualize the Agent-Skill Topology (Priority: P3)

Harriet wants a visual graph showing agents, skills, and routing edges so she can spot clusters, orphans, and over-connected hubs at a glance during topology sync ceremonies.

**Why this priority**: Visualization aids decision-making but is not required for the pruning/merge/rename work itself.

**Independent Test**: A Mermaid diagram or Miro board renders without syntax errors, shows all agents and skills as nodes, and correctly represents routing edges.

**Acceptance Scenarios**:

1. **Given** `agent_skill_graph.json` exists, **When** a Mermaid renderer processes it, **Then** it produces a valid graph with no syntax errors.
2. **Given** the graph is rendered, **When** Harriet inspects it, **Then** orphan nodes are visually isolated (no incoming edges from agent nodes).
3. **Given** the graph is rendered, **When** Harriet looks at shared infrastructure skills (cce-mcp, miro-mcp, psi), **Then** they show edges from 4+ agents.

---

### Edge Cases

- **Transitive-only skills**: A skill referenced only by another skill (not directly by any agent) must not be flagged as orphan. The graph must follow transitive edges.
- **Vendor skill with custom override**: If a custom skill exists alongside a vendor skill of the same name (e.g. custom `spec-kit` alongside vendor Spec Kit), the custom one is an extension, not a duplicate.
- **Rename collision**: Two skills could theoretically map to the same prefixed name. The rename map must be validated for uniqueness before execution.
- **Circular skill references**: Skill A references Skill B which references Skill A. The graph builder must handle cycles without infinite loops.
- **`skills-lock.json` format**: Renaming must preserve the lock file format and not break any CI/CD or hook that reads it.
- **Partially routed skills**: A skill mentioned in AGENTS.md prose but not in any agent JD routing table. The graph builder should scan AGENTS.md as an additional source.

## Requirements

### Functional Requirements

- **FR-001**: System MUST parse all `.github/agents/rl.*.agent.md` and `speckit.*.agent.md` files to extract skill routing tables.
- **FR-002**: System MUST parse all `.agents/skills/*/SKILL.md` files to extract cross-skill references (degree-2+ edges).
- **FR-003**: System MUST scan `AGENTS.md` for skill name mentions as an additional routing source.
- **FR-004**: System MUST produce a JSON adjacency list (`agent_skill_graph.json`) with typed nodes (agent, skill) and directed edges.
- **FR-005**: System MUST compute transitive closure of the graph to determine full reachability.
- **FR-006**: System MUST identify orphan skills (zero in-degree from any agent node after transitive closure).
- **FR-007**: System MUST classify every skill into one of five layers: Vendor-Framework, SpecKit-Extension, Tool/Platform, Language/Stack, Domain/Ops.
- **FR-008**: System MUST prevent modification or deletion of Vendor-Framework and SpecKit-Extension skills.
- **FR-009**: System MUST produce a MERGE/DELETE/KEEP/UPDATE decision for each candidate cluster, with rationale.
- **FR-010**: For MERGE decisions, system MUST consolidate content into one target skill, delete source skills, and update all references in agent JDs, `skills-lock.json`, and `AGENTS.md`.
- **FR-011**: For DELETE decisions on orphans, system MUST verify zero references across all files before deletion.
- **FR-012**: System MUST generate a rename map (`old_name -> new_name`) conforming to the prefix convention.
- **FR-013**: System MUST validate the rename map for uniqueness (no two skills map to the same new name).
- **FR-014**: System MUST update all references (agent JDs, `skills-lock.json`, `AGENTS.md`, cross-skill references in SKILL.md files) when renaming.
- **FR-015**: System MUST run `prek run -a` after all changes and confirm zero errors.

### Key Entities

- **Agent**: A persona defined in `.github/agents/*.agent.md` with a skill routing table. Two types: `rl.*` (custom Redline agents) and `speckit.*` (Spec Kit extension agents).
- **Skill**: A directory under `.agents/skills/<name>/` containing a `SKILL.md` file. Has a source layer classification and may reference other skills.
- **Edge**: A directed routing relationship from an agent to a skill (degree 1) or from a skill to another skill (degree 2+).
- **Orphan**: A skill node with zero in-degree from any agent node after transitive closure.
- **Cluster**: A group of 2+ skills with high semantic overlap, candidates for MERGE.
- **Rename Map**: A dictionary mapping `old_skill_name -> new_skill_name` for the prefix normalization phase.

## Success Criteria

### Measurable Outcomes

- **SC-001**: Total custom skill count reduced from 87 to 70 or fewer (at least 20% reduction).
- **SC-002**: Zero orphan skills remain after pruning (every surviving skill is reachable from at least one agent).
- **SC-003**: Every surviving custom skill directory name conforms to its declared prefix group.
- **SC-004**: `prek run -a` passes with zero errors after all changes.
- **SC-005**: No agent JD contains a reference to a deleted or renamed skill under its old name.
- **SC-006**: Kabilan's directly-routed skill count is reduced from ~50 to 40 or fewer.
- **SC-007**: A visual topology graph (Mermaid or Miro) is produced and contains no isolated orphan nodes.

## Assumptions

- The diagnostic approach document (`docs/architecture/skill-bloat-diagnostic-approach.md`) is the authoritative reference for methodology and candidate clusters.
- Vendor-framework skills (Superpowers, Spec Kit core) cannot be modified or deleted. Only custom skills and Spec Kit extensions are in scope.
- SUPERSEDED stubs (`executing-plans`, `writing-plans`) that still exist as files can be deleted if no references remain, or kept as thin redirects if references exist.
- Merge decisions require domain owner approval: Kabilan for Python/EDA skills, John for marketing, Mark for PM, Harriet for hiring/ceremonies, Peter for architecture, Linda for library/NotebookLM.
- The `speckit-*` skills in `.agents/skills/` are custom extensions (not vendor core) but are excluded from merge/rename because they mirror `.specify/extensions/` and are auto-generated by `specify upgrade`.
- `skills-lock.json` must be updated atomically with any skill rename or deletion.
- The rename phase executes in a separate PR after all merges/deletions are complete and merged.
