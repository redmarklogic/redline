# References

Source material backing the binding rules in `SKILL.md`. All citations sourced via the `Organisational Design & Team Topologies` notebook on 2026-04-20 (NotebookLM session `d1cd9106`).

## Books

- **Team Topologies: Organizing Business and Technology Teams for Fast Flow** — Matthew Skelton & Manuel Pais. IT Revolution Press, 2019.
- **Work Without Jobs: How to Reboot Your Organization's Work Operating System** — Ravin Jesuthasan & John Boudreau. MIT Press, 2022.
- **Reinventing Jobs: A 4-Step Approach for Applying Automation to Work** — Ravin Jesuthasan & John Boudreau. Harvard Business Review Press, 2018.
- **An Elegant Puzzle: Systems of Engineering Management** — Will Larson. Stripe Press, 2019.

## Mapping: SKILL.md rule → source

| SKILL.md rule | Source | Concept |
|---|---|---|
| Step 0 — reactive/ad-hoc screen | Team Topologies | Do not spin up new teams reactively |
| Step 0 — single-function silo screen | Team Topologies | No isolated QA / Ops / DBA teams |
| Step 0 — complicated-subsystem cognitive-load justification | Team Topologies | Complicated-subsystem team only when cognitive load demands it |
| Step 1 — four-step deconstruction (deconstruct / ROIP / automate / optimize) | Reinventing Jobs | Four-step framework |
| Step 1 — three task continuums (repetitive↔variable, etc.) | Reinventing Jobs | Task classification |
| Step 3 — career ladder JD principles (self-contained, short, crisp boundaries) | An Elegant Puzzle | Career ladder design |
| Step 3 — JD must not be a rigid competency repository | Work Without Jobs | Anti-pattern: rigid jobs trap work |
| Step 4 — Team API | Team Topologies | Team API specification |
| Step 4 — File Authority overlap fails the hire | An Elegant Puzzle | Gap-less ownership map |
| AUDIT/PIP — split evaluation from development | Work Without Jobs / Reinventing Jobs | Combining reward and development conversations kills intrinsic motivation |
| AUDIT/PIP — skill-or-will frame, targeted coaching first | An Elegant Puzzle | Compassionate pragmatism with the bottom tail |
| AUDIT/PIP — never rely on single-source self-report; use rubrics | An Elegant Puzzle | Rubrics + wisdom of the crowds |
| Skill Gap step 5 — reject "train an average to top" | Reinventing Jobs / Work Without Jobs | Anti-pattern: hiring/training averages to top performance |
| ORG AUDIT — gap-less ownership map | An Elegant Puzzle | Every responsibility owned by a specific team |
| ORG AUDIT — cognitive load split | Team Topologies | Cognitive load as a fracture-plane signal |
| ORG AUDIT — interaction modes | Team Topologies | Collaboration / X-as-a-Service / Facilitating |
| ORG AUDIT — Conway's Law check | Team Topologies | Org structure constrains system design |
| ORG AUDIT — functional-silo check | Team Topologies | Functional silos destroy fast flow |
| ORG AUDIT — enabling team / ivory-tower trap | Team Topologies | Enabling teams must not become permanent dependencies |
| Skill Gap — common skills taxonomy | Work Without Jobs | Skills hub with shared language |
| REFRESH — continuous alignment of role definitions to evolving strategy | Work Without Jobs | Work as a fluid portfolio, not a fixed job; roles must adapt as work changes |
| REFRESH — advisory-board agents self-update, non-advisory get patches | An Elegant Puzzle | Career ladder ownership: senior roles maintain their own level definitions |
| REFRESH — session-start staleness check | Team Topologies | Sensing mechanism: detect boundary drift before it causes delivery failure |

## Notes

- The acronym "PIP" (Performance Improvement Plan) does not appear in the sources. The AUDIT/PIP workflow adapts the books' performance-management principles (skill-or-will, compassionate pragmatism, split rewards from development) to AI-agent governance.
- "Will" gap is reinterpreted for agents as "the agent is fundamentally mis-scoped or duplicates another agent" — agents have no motivation, but the operational consequence (re-scope, merge, or deprecate) is analogous to the human case.
