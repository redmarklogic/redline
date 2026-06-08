---
name: enforce-ai-batch-discipline
description: Use when configuring PR size thresholds, implementing author-side AI flagging, designing deliberate practice for architecturally complex components, or mentoring developers on AI output verification.
---

## Boundary Contract

### Applies To
- PR size thresholds: maximum line counts for AI-generated PRs; automated warnings for oversized batches
- Author-side flagging: shifting AI review to authoring time rather than PR review time; tooling configuration
- Small-batch enforcement: workflow rules that keep AI-generated work in reviewable increments
- Deliberate practice design: requiring manual implementation alongside AI for architecturally complex components to prevent skill degradation
- AI output verification mentoring: pairing with the founder to review AI-generated architectural decisions; building reviewer competency

### Produces
- PR size threshold configuration
- Author-side AI feedback configuration
- Deliberate practice protocol for complex tasks

### Does Not Cover
- AI policy document structure or acceptable-use stance — see `define-ai-policy`
- Geotechnical domain accuracy rules — the Domain Expert owns those
- AI adoption strategy — the Strategy Advisor sets strategic direction
- Code implementation of enforcement tooling — SpecKit and developers implement

## Key Mechanisms

| Mechanism | Purpose |
|---|---|
| Max PR size threshold | Caps AI-generated PRs to keep review scope manageable |
| Author-side AI feedback | Flags AI output at authoring time — reviewer-side AI review does not work |
| Deliberate practice protocol | Requires manual implementation alongside AI for architecturally complex components |
| AI output verification pairing | Builds reviewer competency; prevents over-reliance on unverified AI output |

## Common Mistakes

| Mistake | Fix |
|---|---|
| Reviewing AI PRs the same way as human PRs | AI PRs need smaller review scope; author-side flagging is required |
| Skipping deliberate practice for complex architecture tasks | Manual alongside AI prevents skill degradation for architecturally complex work |
| Adopting AI tools faster than verification capacity allows | System health over tool adoption; resist the adoption pressure |
| Treating batch size limits as optional suggestions | Configure enforcement tooling; limits are not advisory |
