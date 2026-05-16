> DRAFT — pending user approval. Do not promote to production.

# Run Agent Topology Sync — Step-by-Step

**See:** `ceremony-agent-topology-sync/SKILL.md` for boundary contract, triggers, and the
Reflection Protocol.

---

## Pre-Session (Facilitating Agent, Solo)

1. Verify a valid trigger exists (quarterly cadence, new hire, strategy pivot, milestone,
   or client feedback batch). If no trigger is present, do not run.
2. Run the session-start staleness check from `hiring-agent-management` →
   `procedures/session-start-staleness-check.md`.
3. Read `docs/product/strategy/strategic-bets.md` and the current roadmap.
4. Diff git log since the last sync date. Identify every decision-bearing file changed:
   ADRs, PRDs, specs, strategy documents.
5. Produce the **Drift Summary**: one sentence per agent stating whether their JD is
   likely stale based on the diff. Flag agents with the most drift first.
6. Distribute the Reflection Protocol (Steps R1–R4 from SKILL.md) to all agents with
   a deadline for Delta Statement submission.

---

## Delta Collection (All Reflecting Agents)

7. Each agent independently completes Steps R1–R4 of the Reflection Protocol.
8. The facilitating agent collects all Delta Statements. Any agent without a Delta
   Statement is flagged — their JD changes are deferred to the next sync.

---

## Gap and Overlap Analysis (Facilitating Agent)

9. Map every responsibility mentioned across all Delta Statements against
   `docs/people/agent-register.md`.
10. Flag **orphans**: responsibilities named in strategy or Delta Statements that no
    agent owns.
11. Flag **overlaps**: responsibilities claimed by two or more agents simultaneously.
12. Flag **Team API friction**: interaction mode mismatches (e.g., agents that should
    be X-as-a-Service but are drifting into Collaboration).
13. Review whether any Delta Statement identifies a framework, guideline, or standard
    that should become a new or updated skill file. Flag these as **skill gap triggers**.

---

## JD Patch Drafting (Facilitating Agent)

14. For each agent with confirmed drift, draft a JD patch addressing:
    - Updated outcomes and decisions (Jesuthasan & Boudreau framing, not task lists)
    - Revised handoffs (fix broken or missing transitions identified in gap analysis)
    - New or deprecated skill assignments
    - Updated notebook access if knowledge-base scope has changed
15. Advisory board agents validate their own patches; the facilitating agent drafts for
    all other agents.
16. All patches land at `docs/people/drafts/agents/<agent>.agent.md`.
    **Never write directly to `.github/agents/` — Draft-first constraint.**

---

## Report Publication (Facilitating Agent)

17. Publish the **Topology Sync Report** to
    `docs/people/drafts/reports/topology-sync-YYYY-MM-DD.md` with:
    - Date and trigger that initiated the sync
    - Agents who participated (with Delta Statements) and those deferred
    - Orphan responsibility list and proposed owners
    - Overlap conflicts and resolution proposals
    - Skill gap triggers (new/updated skills needed)
    - New hire triggers (orphans that cannot be absorbed)
    - List of draft JD patches produced
    - Pending user approvals required before promotion
18. Update `docs/people/agent-register.md`, `org-chart.md`, and `skills-taxonomy.md`
    to reflect the post-sync state.
19. State explicitly: which items require user approval, who owns each next action,
    and the earliest valid date for the next sync.

---

## Promotion Checklist (After User Approval)

- [ ] User has approved each draft JD patch
- [ ] Approved patches moved from `docs/people/drafts/agents/` to `.github/agents/`
- [ ] Skill gap triggers handed off to the appropriate skill author
- [ ] New hire triggers handed off to `hiring-agent-management` HIRE mode
- [ ] `docs/people/agent-register.md` reflects promoted state
- [ ] Sync date recorded as the new baseline for the next quarterly trigger
