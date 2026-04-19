# Marketing — Artifact Index

**Owner:** John (Head of Marketing). See `.github/agents/rl.john.agent.md`.

This directory holds all marketing artifacts. John is the only agent that writes here.
Ron writes strategy at `docs/product/strategy/`. Mark writes PRDs at
`docs/product/prds/`. Graeme writes domain knowledge at `docs/knowledge/geotechnical/`.

## Structure

| Path | Contents | Skill |
|------|----------|-------|
| `archive-intelligence.md` | Ground Engineering archive strategy: invisibility protocol, monthly marketing query track (Track A), quarterly product query track (Track B), NZ/AU coverage caveat | n/a (intelligence layer) |
| `the-big-5/` | Content briefs and drafts under the They Ask You Answer / Big 5 framework | `marketing-content-big-5` |
| `seo/keyword-strategy.md` | Traditional keyword + intent map | `marketing-product-led-seo` |
| `seo/keyword-discovery-tools-survey.md` | Survey of API/CLI-accessible keyword + question discovery tools for sourcing Product-Led SEO opportunities | `marketing-product-led-seo` |
| `seo/product-led-seo-briefs/` | Marketing briefs for free programmatic tools, handed to Mark for PRD conversion | `marketing-product-led-seo` |
| `social-selling/linkedin-playbook.md` | The team's LinkedIn social-selling playbook | `marketing-social-selling-linkedin` |
| `social-selling/profiles/` | Per-person PIPA-formatted profile playbooks | `marketing-social-selling-linkedin` |
| `social-selling/sales-navigator-lists.md` | Saved-list specs per ICP segment | `marketing-social-selling-linkedin` |
| `campaigns/` | Per-campaign briefs (each linked to a strategic bet + persona) | varies |
| `signal-reports/` | Monthly market-signal reports fed back to Ron and Mark | n/a (ritual) |
| `drafts/` | In-review content awaiting sign-off | `marketing-ai-content-review` |
| `editorial-calendar.md` | Dynamic schedule of all planned and published content | `marketing-content-big-5` |
| `editorial-style-guide.md` | Brand voice, tone, technical-jargon rules, AI-usage policy | `marketing-ai-content-review` |
| `ai-content-review-log.md` | Append-only log of all AI-assisted content review decisions | `marketing-ai-content-review` |

## Hard Rules

1. Every campaign references a strategic bet from `docs/product/strategy/strategic-bets.md`
   AND a validated persona from `docs/product/personas/` (see P-029 — personas not yet
   validated; no campaign briefs until they are).
2. Every AI-assisted draft passes through `marketing-ai-content-review` before
   publishing.
3. Every domain (geotechnical) claim is verified by Graeme before publishing.
4. Every Product-Led SEO idea is handed to Mark as a marketing brief — John does not
   write the PRD.
5. The monthly signal report is filed on the first business day of every month.
6. The Ground Engineering archive is never cited as a personal corpus. Insights from it
   surface as pattern observations. See `archive-intelligence.md` → Invisibility Protocol.

## Standard Operating Cadences

The recurring rituals for marketing (editorial session, content batching, signal report)
are documented at `docs/product/operations/cadences.md`.
