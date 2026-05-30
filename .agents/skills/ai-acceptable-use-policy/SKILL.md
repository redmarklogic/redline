---
name: ai-acceptable-use-policy
description: Use when defining AI tool governance rules, enforcing small-batch discipline on AI-generated code, designing an acceptable-use policy for a small engineering team, or operationalising DORA AI capabilities.
---

## Boundary Contract

### Applies To
- AI acceptable-use policy structure: permitted tools, review requirements, human verification thresholds
- DORA AI capabilities model: seven capabilities mapped to Redline's team
- Small-batch enforcement: max PR size thresholds, automated warnings for oversized AI PRs
- Author-side AI feedback configuration (flagging at authoring time, not PR review time)
- Deliberate practice design for architecturally complex components
- AI output verification mentoring
- Domain-specific AI governance rules: the Domain Expert's blocking gate operationalised as a policy clause

### Produces
- AI acceptable-use policy document (co-authored with the Strategy Advisor) in `docs/architecture/`
- PR size threshold configuration

### Does Not Cover
- Geotechnical domain accuracy rules — the Domain Expert owns those
- AI adoption strategy — the Strategy Advisor sets strategic direction
- Code implementation of enforcement tooling — SpecKit and developers implement

## Quick Reference: DORA Seven AI Capabilities

| Capability | Redline Application |
|---|---|
| Use AI in small batches | Configure max PR size; warn on oversized AI PRs |
| AI-accessible data | Version-controlled codebase and well-structured docs |
| Clear AI acceptable-use stance | This policy document (co-authored the Principal Engineer + the Strategy Advisor) |
| Quality platform | SonarQube + Designite configured and monitored by the Principal Engineer |
| Healthy data ecosystem | Pins-versioned datasets; documented schemas |
| Version control discipline | All AI output committed; no shadow editing |
| User-centric focus | User outcomes drive AI adoption decisions |


See `procedures/ai-acceptable-use-policy.md` for detailed rules, examples, and extended reference.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Treating AI adoption as a velocity lever | DORA: adoption increase correlates with decreased stability. Measure delivery outcomes. |
| Reviewing AI PRs the same way as human PRs | AI PRs need smaller review scope and author-side flagging; reviewer-side AI review does not work. |
| Skipping deliberate practice for complex architecture tasks | Manual alongside AI prevents skill degradation for architecturally complex work. |
| Letting domain content flow through AI without the Domain Expert's gate | the Domain Expert's blocking gate applies to AI-generated geotechnical content. |
| Adopting AI tools faster than verification capacity allows | System health over tool adoption; resist the adoption pressure. |
| Measuring AI impact by lines of code produced | Use SPACE/SEQ/HEART frameworks, not output metrics. |
