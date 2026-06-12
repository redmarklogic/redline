# DRAFT register.json entry — Product Analytics Platform Discovery (Issue #174)

**Status:** Staged for promotion into `.agents/skills/redline-research/register.json`.
Linda operates draft-first on `register.json`; founder instruction promotes this entry.

**Prepared by:** Linda, 2026-06-12
**Notebook created:** 2026-06-12, populated with 50 sources (see manifest at
`docs/research/20260612-174-analytics-platform-discovery-sources.md`)

```json
{
  "id": "analytics-platform-discovery-174",
  "name": "Product Analytics Platform Discovery (Issue #174)",
  "url": "https://notebooklm.google.com/notebook/ed73c14f-bf85-4b68-8acd-6fbf18cba050",
  "description": "Discovery corpus for the Sprint 3 analytics platform spike (GitHub issue #174, governed by specs/shaped/174-analytics-platform-spike.md). Primary sources on 14 product-analytics platform candidates for a Django-on-Cloud-Run SaaS emitting events server-side: agent-operable surfaces (CLI, MCP server, HTTP ingestion and query APIs), Python/server-side ingestion docs, pricing and free tiers, data-residency and compliance posture, and self-hosting footprint. Hosted SaaS candidates: Amplitude, Google Analytics 4, Heap, Mixpanel, Pendo, Statsig. Open-source/self-hostable: Aptabase, Countly, Matomo, OpenPanel, Plausible, PostHog, Snowplow, Umami. Contains no ranking or recommendation — candidate judgment belongs to the spike.",
  "topic_area": "AI & software architecture",
  "topics": [
    "product analytics",
    "event ingestion",
    "MCP servers",
    "analytics APIs",
    "server-side tracking",
    "data residency",
    "self-hosted analytics",
    "pricing free tiers",
    "Django instrumentation",
    "agent-operable tooling"
  ],
  "content_types": ["official-docs", "api-references", "pricing-pages", "github-repos", "vendor-blogs", "third-party-guides"],
  "use_cases": [
    "Fill the shortlist table columns for the #174 spike (agent surface, residency, cost, server-side ingestion fit)",
    "Verify whether a candidate's MCP server is official or community-maintained",
    "Check a candidate's server-side Python ingestion options and custom-property support",
    "Compare self-hosting infrastructure footprints (containers, databases, maintenance burden)",
    "Pull free-tier limits and first-paid-tier pricing for the $100/month ceiling check"
  ],
  "access": "open",
  "added": "2026-06-12",
  "owner": "peter",
  "consumers": ["peter", "brent", "mark", "linda"]
}
```

**Notes for promotion:**
- `owner` proposed as `peter` — he commissioned-adjacent (spike executor) and makes all
  content/currency judgments for this notebook. Linda remains the mechanical operator.
- `consumers` proposed minimally; widen on request.
- Notebook is time-boxed to the spike; after the founder's Monday decision it can be
  retained for #175 wiring or retired (owner's call).
