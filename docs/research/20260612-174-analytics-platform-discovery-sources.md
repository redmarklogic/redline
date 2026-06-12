# Source Manifest — Product Analytics Platform Discovery (Issue #174)

**Prepared by:** Linda (Knowledge Infrastructure Operator)
**Date:** 2026-06-12
**Governing artifact:** `specs/shaped/174-analytics-platform-spike.md` (Peter's shaped Pitch)
**Consumer:** Peter — Sprint 3 analytics platform spike, Monday 2026-06-15
**NotebookLM notebook:** Product Analytics Platform Discovery (Issue #174)
**Notebook URL:** https://notebooklm.google.com/notebook/ed73c14f-bf85-4b68-8acd-6fbf18cba050
**Notebook ID:** `ed73c14f-bf85-4b68-8acd-6fbf18cba050`
**Source count:** 50 (38 curated primary sources + 12 selectively imported from a NotebookLM deep-research task that discovered 95)

> **Scope and boundaries (per the Pitch's no-gos):** This manifest is discovery only.
> No accounts were created, no SDKs (software development kits) installed, and no
> test events sent to any platform. Candidates are listed alphabetically within
> category and are **not ranked**; candidate judgment is Peter's, in the Monday spike.

---

## Candidates (14)

### Hosted SaaS

#### 1. Amplitude
| Source in notebook | What it covers |
|---|---|
| HTTP V2 API \| Amplitude Docs — https://amplitude.com/docs/apis/analytics/http-v2 | Server-side event ingestion endpoint accepting JSON events with custom properties. |
| Amplitude Pricing Options — https://amplitude.com/pricing | Free-tier limits and paid plan tiers. |
| Amplitude MCP — https://amplitude.com/mcp-server | Amplitude's official MCP (Model Context Protocol) server page. |

#### 2. Google Analytics 4 (GA4)
| Source in notebook | What it covers |
|---|---|
| Measurement Protocol — https://developers.google.com/analytics/devguides/collection/protocol/ga4 | Server-side HTTP event ingestion protocol for GA4. |
| Google Analytics Data API Overview — https://developers.google.com/analytics/devguides/reporting/data/v1 | Programmatic querying of analytics report data. |
| googleanalytics/google-analytics-mcp (GitHub) — https://github.com/googleanalytics/google-analytics-mcp | Google's official MCP server for Google Analytics (read-only reporting tools). |
| adswerve/GA4-Measurement-Protocol-Python (GitHub) — https://github.com/adswerve/GA4-Measurement-Protocol-Python | A Python client library for sending GA4 Measurement Protocol events. |

#### 3. Heap (Contentsquare)
| Source in notebook | What it covers |
|---|---|
| Track — https://developers.heap.io/reference/track-1 | Heap's server-side track API for custom events with properties. |
| Pricing \| Heap — https://www.heap.io/pricing | Free-tier limits and plan structure. |

#### 4. Mixpanel
| Source in notebook | What it covers |
|---|---|
| Import Events — https://developer.mixpanel.com/reference/import-events | Server-side event ingestion (import) API reference. |
| EU Residency — https://docs.mixpanel.com/docs/privacy/eu-residency | Mixpanel's data-residency options and configuration. |
| Mixpanel Pricing — https://mixpanel.com/pricing | Free-tier limits and first paid tier. |
| Product analytics MCP server (Mixpanel blog) — https://mixpanel.com/blog/product-analytics-mcp-server/ | Mixpanel's official MCP server announcement and positioning. |

#### 5. Pendo
| Source in notebook | What it covers |
|---|---|
| Pendo MCP Server — https://www.pendo.io/product/mcp/ | Pendo's official MCP server product page. |
| Pendo Developers — https://developers.pendo.io/ | Pendo's developer/API integration portal. |
| Pendo Plans and Pricing — https://www.pendo.io/pricing/ | Free-tier limits and plan structure. |

#### 6. Statsig
| Source in notebook | What it covers |
|---|---|
| Statsig Documentation (HTTP API target) — https://docs.statsig.com/http-api | Statsig's HTTP API documentation entry point. |
| Statsig Documentation (MCP target) — https://docs.statsig.com/mcp | Statsig's MCP documentation entry point. |
| Statsig pricing/site — https://statsig.com/pricing | Plan structure and free-tier description. |
| Overview - Statsig Documentation — https://docs.statsig.com/integrations/mcp/overview | Statsig's official MCP server integration documentation. |
| Python Server SDK - Statsig Documentation — https://docs.statsig.com/server-core/python-core | Server-side Python SDK including event logging. |

### Open-source / self-hostable

#### 7. Aptabase
| Source in notebook | What it covers |
|---|---|
| aptabase/aptabase (GitHub) — https://github.com/aptabase/aptabase | Open-source repository describing the product and its event API. |
| Aptabase site — https://aptabase.com/ | Hosted product overview and pricing. |
| aptabase/self-hosting (GitHub) — https://github.com/aptabase/self-hosting | Self-hosting configuration and infrastructure documentation. |

#### 8. Countly
| Source in notebook | What it covers |
|---|---|
| Countly/countly-server (GitHub) — https://github.com/Countly/countly-server | Open-source server repository describing architecture (MongoDB-based) and self-hosting. |
| Pricing and Plans \| Countly — https://countly.com/pricing | Hosted and self-hosted plan structure. |

#### 9. Matomo
| Source in notebook | What it covers |
|---|---|
| Tracking HTTP API — https://developer.matomo.org/api-reference/tracking-api | Server-side HTTP event/tracking ingestion API. |
| Reporting API — https://developer.matomo.org/api-reference/reporting-api | Programmatic querying of analytics reports. |
| Matomo On-Premise Requirements FAQ — https://matomo.org/faq/on-premise/matomo-requirements/ | Self-hosting infrastructure requirements (PHP, MySQL/MariaDB). |
| Matomo Pricing — https://matomo.org/pricing/ | Matomo Cloud pricing and on-premise cost structure. |
| Integrate the MCP Server with OpenAI Codex FAQ — (matomo.org FAQ) | Matomo's documentation for connecting its MCP server to AI tools. |

#### 10. OpenPanel
| Source in notebook | What it covers |
|---|---|
| What is OpenPanel? — https://openpanel.dev/docs | Product and documentation overview. |
| Self-Hosted Mixpanel Alternative (OpenPanel article) — https://openpanel.dev/articles/self-hosted-product-analytics | Vendor article comparing self-hosted product-analytics options including its own footprint. |
| Python \| OpenPanel Analytics — https://openpanel.dev/docs/sdks/python | Official Python SDK for server-side event ingestion. |

#### 11. Plausible
| Source in notebook | What it covers |
|---|---|
| Plausible Events API reference — https://plausible.io/docs/events-api | Server-side event ingestion with custom properties (up to 30 key-value pairs). |
| Plausible Stats API reference — https://plausible.io/docs/stats-api | Programmatic querying of analytics data. |
| Plausible Self-Hosted — https://plausible.io/docs/self-hosting | Self-hosting guide (Docker; PostgreSQL plus ClickHouse). |
| MCP server for Plausible Analytics (GitHub, community) | Community-maintained MCP server for querying Plausible data. |
| EU-hosted web analytics — https://plausible.io/eu-hosted-web-analytics | Data-residency posture: EU incorporation and EU-only hosting for the cloud product. |

#### 12. PostHog
| Source in notebook | What it covers |
|---|---|
| Capture and batch API endpoints — https://posthog.com/docs/api/capture | Server-side HTTP event ingestion with custom properties. |
| Model Context Protocol (MCP) — https://posthog.com/docs/model-context-protocol | PostHog's official MCP server documentation. |
| PostHog pricing — https://posthog.com/pricing | Usage-based pricing and free-tier limits. |
| Self-host PostHog — https://posthog.com/docs/self-host | Official self-hosting (hobby deployment) documentation and support posture. |
| API queries — https://posthog.com/docs/api/queries | Programmatic analytics querying via the query API. |
| PostHog Self-Hosted: Worth the Ops Overhead? (Cotera) — https://cotera.co/articles/posthog-self-hosted-guide | Third-party assessment of self-hosted PostHog's infrastructure and maintenance burden. |

#### 13. Snowplow
| Source in notebook | What it covers |
|---|---|
| Snowplow Documentation — https://docs.snowplow.io/docs/ | Documentation root for the open-source behavioural data pipeline (collector, enrichment, warehouse loading). |

#### 14. Umami
| Source in notebook | What it covers |
|---|---|
| Send server-side events — https://docs.umami.is/docs/guides/send-server-side-events | Guide for emitting events server-side via the API. |
| API Overview — https://docs.umami.is/docs/api | REST API documentation including stats retrieval. |
| Pricing – Umami — https://umami.is/pricing | Umami Cloud free tier and paid plans. |
| Umami Analytics MCP (mcpservers.org listing, community) | Listing for a community-maintained Umami MCP server. |

---

## Provenance

- **Curated primary sources (38):** added directly by Linda via `nlm source add --url`, selected from official documentation, API references, MCP/CLI references, pricing pages, residency pages, and self-hosting guides.
- **Deep-research imports (12):** a NotebookLM deep-research task (task ID `c04e2173-92d4-4f06-818a-b0de3e2ed9dd`, 95 sources discovered) was run against the founder's research prompt; 12 sources were selectively imported by index to stay within NotebookLM's 50-source notebook cap and avoid duplicates and off-topic material. The remaining 83 discovered sources were not imported (duplicates of curated sources, secondary listicles, or off-topic pages).
- The deep-research task also produced a written research report; it lives in the research task attached to the notebook, not as a source.

## Known gaps (not sourced)

1. **Heap MCP:** secondary sources state Heap's MCP exists via Contentsquare; no primary Heap/Contentsquare MCP documentation page was captured.
2. **Statsig duplicate risk:** the two sources titled "Statsig Documentation" (the `/http-api` and `/mcp` targets) may have resolved to the same docs landing page; the imported MCP integration overview and Python Server SDK pages cover the same ground. Not removed — deduplication of a live notebook requires owner confirmation.
3. **Australian-region hosting:** none of the captured hosted-SaaS sources document an Australian analytics-data region (PostHog: US/EU; Mixpanel: US/EU; Plausible: EU). Self-hostable candidates are the residency route captured. This is an observation about source coverage, not a recommendation.
4. **Sub-processor pages:** vendor sub-processor lists were not individually captured for every candidate; the deep-research scan surfaced mostly third-party privacy pages, which were excluded as off-topic.
5. **Snowplow depth:** only the documentation root is captured; pricing/footprint detail would need follow-up if Peter shortlists it.
6. **CLI surfaces:** dedicated CLI references (beyond MCP and HTTP APIs) were not separately captured for most candidates; the docs roots in the notebook are the entry points to verify CLI availability.

## Register status

Register entry for this notebook is staged at `docs/people/drafts/` (Linda operates draft-first on `register.json` pending founder promotion). The Excel notebook index (`G:\My Drive\Library\index-notebooklm.xlsx`) is updated directly per the `notebooklm-index` procedure.
