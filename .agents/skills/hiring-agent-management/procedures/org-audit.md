# ORG AUDIT Workflow

Apply Team Topologies' boundary tests:

1. **Read all files in `.github/agents/`** and cross-reference `docs/people/agent-register.md`.
2. **Gap-less ownership map** (Larson). Every responsibility named in `strategic-bets.md` and `roadmap.md` must map to exactly one agent. Report holes (no owner) and overlaps (multiple owners).
3. **Cognitive load check.** Flag any agent whose File Authority spans more than two distinct domains. Cognitive overload is a fracture-plane signal — propose a split.
4. **Interaction mode check.** Each pair of frequently-collaborating agents should have a declared mode (Collaboration / X-as-a-Service / Facilitating). Flag pairs that talk constantly when they should be X-as-a-Service.
5. **Conway's Law check.** Does the agent topology match the artifact topology? If two agents jointly own one artifact category with no clean split, the artifact will reflect the muddle. Propose either a merge or a clean fracture plane.
6. **Fracture plane audit (shared File Authority).** For each pair of adjacent agents in the handoff chain, check whether their File Authority overlaps. Shared write access to the same directory is the primary smell for a missing fracture plane. For each overlap found: (a) determine whether the default interaction mode should be X-as-a-Service (clean boundary) rather than Collaboration (blurred boundary), and (b) propose either splitting the directory into agent-owned subdirectories or assigning sole write authority to one agent with read-only access for the other.
7. **Skill boundary contract check.** For each skill in `.agents/skills/`, verify the skill file declares: (a) what inputs it accepts, (b) what outputs it produces, and (c) what is explicitly out of scope. A skill without these three declarations is a leaky interface contract (DDD: information leakage). Flag missing declarations and recommend adding a Boundary Contract section.
8. **Functional-silo check.** Flag any agent whose entire scope is a single function applied to everyone else's output (e.g., a generic "reviewer agent"). Recommend embedding that capability as a skill instead.
9. **"Enabling team" trap check.** If an agent positions itself as a permanent dependency that other agents must always route through (an "ivory tower"), flag it. Enabling agents should make others self-sufficient, not create permanent bottlenecks.
10. **Output** → `docs/people/drafts/reports/org-audit-<YYYY-MM-DD>.md`.
