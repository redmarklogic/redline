# Requirements Checklist: Skill Bloat Reduction

**Feature**: 011-skill-bloat-reduction
**Generated**: 2026-05-30

## Functional Requirements

| ID | Requirement | Status |
|---|---|---|
| FR-001 | Parse agent JD files for skill routing tables | [ ] |
| FR-002 | Parse SKILL.md files for cross-skill references | [ ] |
| FR-003 | Scan AGENTS.md for skill name mentions | [ ] |
| FR-004 | Produce JSON adjacency list with typed nodes and directed edges | [ ] |
| FR-005 | Compute transitive closure for full reachability | [ ] |
| FR-006 | Identify orphan skills (zero in-degree after closure) | [ ] |
| FR-007 | Classify every skill into one of five layers | [ ] |
| FR-008 | Prevent modification of Vendor-Framework and SpecKit-Extension skills | [ ] |
| FR-009 | Produce MERGE/DELETE/KEEP/UPDATE decision per cluster with rationale | [ ] |
| FR-010 | Execute MERGE: consolidate content, delete sources, update references | [ ] |
| FR-011 | Execute DELETE: verify zero references before deletion | [ ] |
| FR-012 | Generate rename map with prefix convention | [ ] |
| FR-013 | Validate rename map for uniqueness | [ ] |
| FR-014 | Update all references when renaming | [ ] |
| FR-015 | Run `prek run -a` after all changes with zero errors | [ ] |

## Success Criteria

| ID | Criterion | Status |
|---|---|---|
| SC-001 | Skill count reduced from 87 to 70 or fewer | [ ] |
| SC-002 | Zero orphan skills remain | [ ] |
| SC-003 | Every custom skill name conforms to prefix convention | [ ] |
| SC-004 | `prek run -a` passes clean | [ ] |
| SC-005 | No agent JD references deleted/renamed skills by old name | [ ] |
| SC-006 | Kabilan's routed skill count reduced to 40 or fewer | [ ] |
| SC-007 | Visual topology graph produced with no orphan nodes | [ ] |
