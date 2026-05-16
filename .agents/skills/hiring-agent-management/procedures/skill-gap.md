# Skill Gap Workflow

When a required skill does not exist or is inadequate:

1. **Check `skills.sh` for an existing community skill.** Report findings with install command: `npx skills add <owner/repo/skill-name>`. Prefer high install count and reputable authors.
2. **Check `register.json`.** Is a notebook already loaded for this domain?
   - **Yes** → query it via `notebooklm-mcp` using `prompting-guide.md`, then draft the skill following the `writing-skills` TDD cycle.
   - **No** → proceed to step 3.
3. **Identify sourcing options.** Search for relevant books or freely available materials. Consult domain agents (Graeme/John/Ron) where relevant.
4. **Vet every resource before recommending it:**
   - **Currency** — reject resources >3 years old for fast-moving tech domains. Timeless principles (design, systems thinking, org design) are exempt.
   - **Stack relevance** — flag stack-specific books if Redline's stack differs.
   - **Availability** — confirm digital availability. Do not recommend books you cannot verify exist in the stated title.
5. **Reject "train an average to top performance" thinking** (Jesuthasan & Boudreau warning). If the only proposed remedy is "give the agent more general training and hope," that is not a skill gap fix — it is a sign the agent is mis-scoped. Loop back to the AUDIT/PIP procedure (`procedures/audit-pip.md`).
6. **Report to user.** Name resources, explain relevance, note caveats. Wait for user to load notebooks before drafting the skill.
7. **Draft skill** → `docs/people/drafts/skills/<skill-name>/SKILL.md` following the `writing-skills` TDD cycle (RED → GREEN → pressure-test). Never fabricate skill content without notebook grounding.
