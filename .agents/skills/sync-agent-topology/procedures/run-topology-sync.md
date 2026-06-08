# Run Agent Topology Sync — Step-by-Step

**See:** `sync-agent-topology/SKILL.md` for boundary contract, triggers, and the
Reflection Protocol.

---

## Pre-Session (Facilitating Agent, Solo)

1. Verify a valid trigger exists (quarterly cadence, new hire, strategy pivot, milestone,
   or client feedback batch). If no trigger is present, do not run.
2. Run the session-start staleness check from `hr-hire-agent` →
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

## SRP Compliance Pass (Facilitating Agent) — MANDATORY

> **This phase is mandatory.** The sync cannot be marked complete without a
> `violations-list.md` artifact. Do not skip, defer, or mark optional.

14. Run the SRP scan algorithm from `procedures/srp-scan-procedure.md`.
15. For every `SKILL.md` file discovered, check:
    - The `name:` frontmatter field for disallowed "and" patterns.
    - The `description:` frontmatter field for multi-concern "and" patterns.
16. For each match found, classify the disposition:
    - **new-violation**: skill is not in the Known Exception Skip-List in `procedures/srp-scan-procedure.md`.
    - **known-exception**: skill is listed in the Known Exception Skip-List.
    - **false-positive**: pattern matched but qualifies as a domain compound noun or
      grammatical "and" per the rules in `procedures/srp-scan-procedure.md`.
17. Produce `violations-list.md` at
    `docs/people/drafts/reports/violations-list.md` with columns:
    `skill name | field flagged | pattern matched | disposition`.
18. New violations (disposition = `new-violation`) are added to the **skill gap triggers**
    list and must be resolved before the next topology sync.

---

## JD Patch Drafting (Facilitating Agent)

19. For each agent with confirmed drift, draft a JD patch addressing:
    - Updated outcomes and decisions (Jesuthasan & Boudreau framing, not task lists)
    - Revised handoffs (fix broken or missing transitions identified in gap analysis)
    - New or deprecated skill assignments
    - Updated notebook access if knowledge-base scope has changed
20. Advisory board agents validate their own patches; the facilitating agent drafts for
    all other agents.
21. All patches land at `docs/people/drafts/agents/<agent>.agent.md`.
    **Never write directly to `.claude/agents/` — Draft-first constraint.**

---

## Report Publication (Facilitating Agent)

22. Publish the **Topology Sync Report** to
    `docs/people/drafts/reports/topology-sync-YYYY-MM-DD.md` with:
    - Date and trigger that initiated the sync
    - Agents who participated (with Delta Statements) and those deferred
    - Orphan responsibility list and proposed owners
    - Overlap conflicts and resolution proposals
    - Skill gap triggers (new/updated skills needed, including SRP violations)
    - New hire triggers (orphans that cannot be absorbed)
    - List of draft JD patches produced
    - Pending user approvals required before promotion
23. Update `docs/people/agent-register.md`, `org-chart.md`, and `skills-taxonomy.md`
    to reflect the post-sync state.
24. State explicitly: which items require user approval, who owns each next action,
    and the earliest valid date for the next sync.

---

## Promotion Checklist (After User Approval)

- [ ] User has approved each draft JD patch
- [ ] Approved patches moved from `docs/people/drafts/agents/` to `.claude/agents/`
- [ ] Skill gap triggers handed off to the appropriate skill author
- [ ] SRP new-violations handed off for resolution before next sync
- [ ] New hire triggers handed off to `hr-hire-agent` HIRE mode
- [ ] `docs/people/agent-register.md` reflects promoted state
- [ ] `violations-list.md` filed in Topology Sync Report folder
- [ ] Sync date recorded as the new baseline for the next quarterly trigger
