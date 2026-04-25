> DRAFT -- pending user approval. Do not promote to production.

# Hire Report: Knowledge Infrastructure Operator (Linda)

**Date:** 2026-04-25  
**Author:** Harriet (Head of People & Agent Development)  
**Status:** Recommended for hire (narrowed scope)  
**Previous verdict:** Rejected (2026-04-24, original 4-responsibility Virtual Librarian scope)

---

## Background

The original "Linda" hire brief proposed a Virtual Librarian with four broad responsibilities including session archiving, domain knowledge curation, and content recommendations. That brief failed 3 of 5 Step 0 gates (Parsimony, Cognitive Load, Strategic Pull). The advisory board unanimously agreed. The founder accepted the reasoning.

The founder then raised a legitimate counter-argument: the digital book library spans ALL domains (geotechnical, software engineering, marketing, org design, strategy). No single existing agent covers this breadth. This is domain-agnostic operational work -- curate, ingest, deduplicate, tag, maintain -- that falls between the cracks of every agent's scope. The founder approved a narrower scope for re-evaluation.

---

## Step 0 -- Gate Screening (narrowed scope)

| Gate | Original Verdict | New Verdict | Justification |
|---|---|---|---|
| **1. Parsimony** (can an existing agent absorb this?) | FAILED | **PASSES** | The library spans all domains. No single agent's scope covers cross-domain content infrastructure. This is the Team Topologies "platform team" pattern -- shared infrastructure consumed by all domain agents. |
| **2. Not reactive** (not a response to a single failure?) | PASSED | **PASSES** | Structural gap identified through systematic org analysis, not triggered by a single agent failure. |
| **3. Not a silo** (not a single-function hand-off bottleneck?) | Borderline | **PASSES** | Session archiving (the silo-risk function) was dropped. Remaining scope is an operational pipeline: curate - ingest - organise - maintain - monitor. Platform service, not functional checkpoint. |
| **4. Cognitive load** (justified complexity split?) | FAILED | **PASSES** | Without Linda, 5+ domain agents each independently manage notebook sourcing, dedup, tagging, and register maintenance. Centralising eliminates N-agent duplication of operational overhead and ensures consistency. |
| **5. Strategic pull** (an active bet requires this?) | FAILED | **PASSES** | Bet 3 (Standards Knowledge Store) is described as "the asset competitors cannot replicate" and "underwrites all KRs." Linda's responsibilities directly support Bet 3's maintenance requirements and curation pipeline. Standards monitoring (responsibility #4) is the operational engine for Bet 3's assumption that "maintenance load is hours per quarter." |

**All 5 gates pass.** The narrowed scope resolves every original failure.

---

## Step 1 -- Work Deconstruction (Jesuthasan & Boudreau)

### Task Table

| # | Task | Rep-Var | Indep-Inter | Det-Judgment | ROIP | Mode |
|---|---|---|---|---|---|---|
| 1a | Scan digital library for new/unindexed books and standards | Repetitive | Independent | Deterministic | Reduce mistakes | Substitute |
| 1b | Parse metadata (title, author, domain, topic area, format) | Repetitive | Independent | Deterministic | Reduce variance | Substitute |
| 1c | Tag entries with domain categories and topic keywords | Repetitive | Independent | Low judgment (taxonomy pre-defined) | Reduce variance | Substitute |
| 1d | Dedup against existing library entries | Repetitive | Independent | Deterministic | Reduce mistakes | Substitute |
| 1e | Index entries for discoverability | Repetitive | Independent | Deterministic | Incrementally improve | Substitute |
| 2a | Create new NotebookLM notebooks for identified domain areas | Variable (triggered) | Independent | Low judgment (thematic grouping) | Create new work | Substitute |
| 2b | Upload sources from digital books to appropriate notebooks | Repetitive | Independent | Deterministic | Reduce variance | Substitute |
| 2c | Dedup sources within notebooks | Repetitive | Independent | Deterministic | Reduce mistakes | Substitute |
| 2d | Organise notebooks thematically (topic coherence) | Variable | Independent | Low judgment | Reduce variance | Substitute |
| 3a | Add/update notebook entries in `register.json` | Repetitive | Independent | Deterministic | Reduce mistakes | Substitute |
| 3b | Remove retired/merged notebook entries from register | Repetitive | Independent | Deterministic | Reduce mistakes | Substitute |
| 3c | Validate register accuracy against live notebooks | Repetitive | Independent | Deterministic | Reduce mistakes | Substitute |
| 4a | Monitor standards body metadata feeds | Repetitive | Independent | Deterministic | Incrementally improve | Substitute |
| 4b | Flag standards updates and route to Graeme | Repetitive | Interactive (handoff) | Deterministic (flag, not judge) | Reduce mistakes | Substitute |
| 5 | Route domain questions to appropriate agent | Repetitive | Interactive (handoff) | Low judgment (routing, not deciding) | Reduce mistakes | Augment |

### Profile Summary

- **15/15** tasks are Repetitive or triggered-Variable
- **13/15** tasks are Independent; 2 involve structured handoffs (not collaborative judgment)
- **14/15** tasks are Deterministic or Low-judgment
- All tasks are **Substitute** (agent fully owns) except routing (Augment)

### Agent vs. Skill Assessment

The playbook flags that Repetitive + Independent + Deterministic tasks "usually belong in a skill, not an agent." However:

1. **Persistent ownership required.** These tasks require an active operator who maintains state (what has been indexed, what is stale, what needs attention). A skill is passive -- loaded on demand. No existing agent's natural workflow would trigger loading a "knowledge infrastructure" skill regularly.
2. **Cross-cutting scope.** This is the founder's core insight. A skill must be loaded by some agent. If no agent's scope naturally covers this work, the skill sits unloaded. The work falls between the cracks -- which is exactly the observed failure mode.
3. **Platform team pattern (Team Topologies).** Platform capabilities justify a dedicated team (or agent) when they provide self-service infrastructure consumed by multiple stream-aligned teams. This pattern explicitly requires ownership, not just documentation.

**Verdict: Agent justified.** The cross-cutting, persistent, operational nature of the work requires an owner, not a procedure.

---

## Step 2 -- Domain Agent Consultation

Pre-completed. All four advisory board members consulted and support the narrowed scope.

| Agent | Position | Constraints set |
|---|---|---|
| Ron | Supports. Cross-cutting infrastructure is a real gap. | Strategy decisions remain Ron's domain. |
| Mark | Supports. No product objection. | Product decisions remain Mark's domain. |
| John | Supports. `redline-research` meets his query needs; Linda supplements infrastructure. | Content creation remains John's domain. |
| Graeme | Supports with firm boundary. | Standards monitoring MUST route through Graeme. Nothing writes to `docs/knowledge/geotechnical/`. |

All constraints encoded in the draft JD as hard constraints.

---

## Step 3 -- Draft JD

See: `docs/people/drafts/agents/rl.linda.agent.md`

Design choices (with framework citations):

| JD element | Framework citation |
|---|---|
| Responsibilities framed as outcomes, not task lists | Jesuthasan & Boudreau: avoid rigid JDs that trap work in a title |
| Explicit "What I Do NOT Do" section | Larson: career ladder JDs state both scope and exclusions |
| Hard constraints are testable ("I MUST NOT...") | Prompt rewriting rules (rag-prompting) |
| X-as-a-Service interaction mode | Team Topologies: platform teams provide self-service, not collaboration |
| Draft-first maturity | Org convention: new agents start in Draft-first mode |

---

## Step 4 -- Team API

| Field | Value |
|---|---|
| **Inputs** | New books/standards for the digital library; notebook creation/update requests from any agent; standards body metadata feeds; register accuracy check requests |
| **Outputs** | Indexed and tagged library entries; populated and deduplicated NotebookLM notebooks; up-to-date `register.json`; standards update alerts routed to Graeme |
| **Interaction mode** | X-as-a-Service |
| **File authority** | `.agents/skills/redline-research/register.json` (direct write) |
| **Handoff partners** | Graeme (all standards triage); Ron/Mark/John (domain questions outside geotechnical); Harriet (org and skill questions) |

### File Authority Overlap Check

| Linda's proposed authority | Overlaps with? | Resolution |
|---|---|---|
| `.agents/skills/redline-research/register.json` | No agent currently claims write authority over this file | No overlap. This is the gap -- nobody owns maintaining it today. |

**Step 4 passes.** No File Authority overlap with any existing agent.

---

## Step 5 -- Skill Gap Check

| Skill needed | Exists? | Status |
|---|---|---|
| `notebooklm-mcp` | Yes | In `.agents/skills/notebooklm-mcp/`. Used by Harriet, Graeme, Ron, John, Mark. No gap. |
| `redline-research` | Yes | In `.agents/skills/redline-research/`. Used by All. Linda uses this for querying and register operations. No gap. |
| `knowledge-infrastructure` | **No** | **GAP.** Linda needs a skill covering: library curation procedures, notebook maintenance procedures, register.json maintenance procedures, standards monitoring procedures. |

### Skill Gap: `knowledge-infrastructure`

**Sourcing options for grounding:**

1. **"Information Architecture and Knowledge Management" notebook** -- EXISTS in `register.json` (id: `information-architecture-km`, access: open). Description: *"Explores the strategic design and management of information systems to make organizational knowledge assets findable, understandable, and actionable. Covers foundational concepts of Information Architecture, Knowledge Architectures, and Knowledge Management."* This is the primary grounding source.

2. **"Organisational Design & Team Topologies" notebook** -- EXISTS (id: `org-design-team-topologies`, access: open). Contains platform team patterns relevant to Linda's X-as-a-Service operating model.

**Recommended remediation:** Query the "Information Architecture and Knowledge Management" notebook to extract operational principles for knowledge curation, indexing, deduplication, and taxonomy design. Draft the `knowledge-infrastructure` skill using the `writing-skills` TDD cycle. This skill should be agent-agnostic (per Skill Naming Rules -- no agent name in skill name or content).

**Status:** Pending notebook grounding. Linda can operate with `notebooklm-mcp` and `redline-research` on day 1, but the dedicated `knowledge-infrastructure` skill should be created before declaring the agent fully equipped.

---

## Step 6 -- Notebook Check

| Required notebook | In register? | Access | Status |
|---|---|---|---|
| Information Architecture and Knowledge Management | Yes (`information-architecture-km`) | Open | Available for skill grounding |
| All open-access notebooks | Yes (13 open notebooks in register) | Open | Available for operational maintenance |
| Advisory-board-only notebooks | Yes (5 in register) | Advisory-board-only | Linda routes through domain agents -- correct |

No missing notebooks. Linda's primary grounding source exists and is accessible.

---

## Recommendation

**HIRE.** The narrowed scope resolves all three original Step 0 failures. The Knowledge Infrastructure Operator role is justified under the following conditions:

1. **Narrowed scope is the scope.** If responsibilities creep beyond the four stated outcomes (curate library, maintain notebooks, maintain register, monitor standards), the role must be re-screened.
2. **Graeme's boundary is non-negotiable.** Standards monitoring routes through Graeme. Linda never writes to `docs/knowledge/geotechnical/`. This is encoded as a hard constraint.
3. **No domain judgment.** Linda organises content; domain agents decide what the content means. This is the critical design constraint that makes the role viable.
4. **`knowledge-infrastructure` skill should be created** before declaring the agent fully equipped. Ground it in the "Information Architecture and Knowledge Management" notebook using the `writing-skills` TDD cycle.
5. **Draft-first maturity.** Linda starts in Draft-first mode. Promotion to Autonomous requires explicit user instruction.

### Next actions (ownership)

| Action | Owner | Dependency |
|---|---|---|
| Approve or reject this hire report | **User** | None |
| If approved: promote `rl.linda.agent.md` from `docs/people/drafts/agents/` to `.github/agents/` | **User** | User approval |
| If approved: update agent register, org chart, skills taxonomy | **Harriet** | User approval |
| Create `knowledge-infrastructure` skill (query IA&KM notebook, TDD cycle) | **Harriet** | User approval + notebook grounding session |

---

## Framework Citations

| Design choice | Source |
|---|---|
| Step 0 gate screening | Team Topologies (Skelton & Pais): "do not create a new team" patterns |
| Work deconstruction before JD | Jesuthasan & Boudreau: four-step work-deconstruction framework |
| Platform team justification | Team Topologies: platform teams provide self-service infrastructure |
| Career-ladder style JD with crisp boundaries | Larson (An Elegant Puzzle): career ladders state both scope and exclusions |
| Outcomes over task lists in JD | Jesuthasan & Boudreau: rigid JDs trap work in a title |
| Skill gap workflow | hiring-agent-management: verify skill exists before hire is complete |
| X-as-a-Service interaction mode | Team Topologies: three interaction modes (Collaboration, X-as-a-Service, Facilitating) |
| Agent vs. skill assessment | hiring-agent-management Step 1: persistent ownership vs. passive procedure |
