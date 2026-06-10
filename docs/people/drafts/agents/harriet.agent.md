# Draft JD Patch — Harriet (Head of People & Agent Development)

**Status:** DRAFT — Topology Sync 2026-06-10.
**Target file:** `.claude/agents/harriet.md`
**Drafted by:** Harriet (self; Draft-first maturity — founder promotes).
**Root cause:** the topology-sync skill folder was renamed `sync-agent-topology` → `hr-sync-agent-topology` (working-tree rename, 2026-06-10) to match the `hr-*` naming family (`hr-hire-agent`, `hr-audit-agent`, `hr-maintain-agent-registry`). Harriet's routing table still points at the old name. Because Harriet's Hard Constraints forbid loading any skill not in the routing table, the stale name would block the ceremony once the rename is committed.

---

## Patch 1 — Skill routing table row

**REPLACE** (in "Skills Available to Harriet"):

> | Running the Agent Topology Sync ceremony | `sync-agent-topology` |

**WITH**:

> | Running the Agent Topology Sync ceremony | `hr-sync-agent-topology` |

No other changes. Single-row fix; narrowly scoped.
