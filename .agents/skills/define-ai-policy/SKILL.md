---
name: define-ai-policy
description: Use when authoring or reviewing an AI acceptable-use policy document — covering policy structure, the DORA AI capabilities map, and the team's acceptable-use stance.
---

## Boundary Contract

### Applies To
- AI acceptable-use policy document structure: permitted tools, review requirements, human verification thresholds
- DORA AI capabilities model: seven capabilities mapped to Redline's team and context
- Acceptable-use stance: clear policy clauses for each domain role, including the Domain Expert's blocking gate operationalised as a policy clause
- Domain-specific AI governance rules: which AI outputs require expert review before use

### Produces
- AI acceptable-use policy document (co-authored with the Strategy Advisor) in `docs/architecture/`

### Does Not Cover
- Small-batch enforcement mechanics — see `enforce-ai-batch-discipline`
- Geotechnical domain accuracy rules — the Domain Expert owns those
- AI adoption strategy — the Strategy Advisor sets strategic direction
- Code implementation of enforcement tooling — SpecKit and developers implement

## Quick Reference: DORA Seven AI Capabilities

| Capability | Redline Application |
|---|---|
| Use AI in small batches | Configure max PR size; warn on oversized AI PRs |
| AI-accessible data | Version-controlled codebase and well-structured docs |
| Clear AI acceptable-use stance | This policy document (co-authored by the Principal Engineer + the Strategy Advisor) |
| Quality platform | SonarQube + Designite configured and monitored by the Principal Engineer |
| Healthy data ecosystem | Pins-versioned datasets; documented schemas |
| Version control discipline | All AI output committed; no shadow editing |
| User-centric focus | User outcomes drive AI adoption decisions |

See `procedures/ai-acceptable-use-policy.md` for detailed rules, examples, and extended reference.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Treating AI adoption as a velocity lever | DORA: adoption increase correlates with decreased stability. Measure delivery outcomes. |
| Letting domain content flow through AI without the Domain Expert's gate | The Domain Expert's blocking gate applies to AI-generated geotechnical content. |
| Measuring AI impact by lines of code produced | Use SPACE/SEQ/HEART frameworks, not output metrics. |
