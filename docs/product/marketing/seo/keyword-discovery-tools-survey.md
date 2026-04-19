# Keyword and Question Discovery Tools — 2026 Survey

**Owner:** John (Head of Marketing).
**Skill:** [`marketing-product-led-seo`](../../../../.agents/skills/marketing-product-led-seo/SKILL.md).
**Audience:** Founder + future engineering work wiring tools into Copilot agents.
**Last verified:** 2026-04-19 (live vendor pages).

---

## Heads-up on the strategic shift

The founder is now leaning toward pursuing Product-Led SEO sooner than the
Phase-2 timeline I and Ron earlier sketched, on the basis that:

1. The Skeleton Generator already IS a Product-Led SEO asset.
2. LinkedIn becomes the discovery channel that ignites it (founder posts).
3. Free-credits-on-referral builds in a network effect and serves as a usefulness
   signal — and importantly, it sidesteps Ron's earlier KR1 timing concern
   because growth is driven by word-of-mouth, not slow SEO ranking.

I think this is partially right and worth pursuing, but with two caveats I'll
flag for the next strategy session (not in this document):

- The referral mechanic only works if the tool produces a moment of "I have to
  show this to a colleague" delight. We have no evidence yet.
- Ron's positioning bet (Skeleton Generator as expert-grounded GIR drafting,
  not generic AI) must survive the LinkedIn-friendly framing. Marketing must
  not over-simplify it into "AI does your reports".

That conversation belongs with Ron and Mark. **The rest of this document is
the tools survey the founder asked for.**

---

## How to read this survey

The founder's hard filter: **CLI or API access required** for Copilot-agent
wiring. Anything that's GUI-only sits in [§9](#9-gui-only-lower-priority).

Every entry below answers:

- What it does
- Free vs paid (free preferred)
- API/CLI status, auth model, rate limits
- What it answers best
- Honest known issues for Redline's NZ/AU geotechnical use case

A starter stack recommendation is in [§10](#10-recommended-starter-stack-for-redline).
Anti-patterns and risks are in [§11](#11-anti-patterns-and-risks).

---

## 1. Keyword volume and search-data APIs

The tools that tell you "how many people search for X per month, in which country,
how hard is it to rank, what related terms exist".

| Tool | Free? | API/CLI | Auth | Rate / cost | Best for |
|---|---|---|---|---|---|
| **DataForSEO** | Free trial credits; pay-as-you-go after | Full REST API + OpenAPI; SDKs in Python, Node, PHP | HTTP Basic (login + password) | ~$0.05 per 1k task units; no fixed QPS cap on most endpoints | Cheapest comprehensive coverage. Has Google Ads search volume, related keywords, keyword ideas, historical volume, Google Trends, Bing Ads volume, plus Reddit + Pinterest social APIs. Built for programmatic use. |
| **Moz API v3** | $20/month entry tier (50k rows incl.) | JSON-RPC 2.0 over HTTPS; OpenAPI spec | API token (single header) | Tier-based row caps; no per-second throttle on small plans | Cleanest API surface of any SEO tool. Keyword volume, **Search Intent (informational/navigational/commercial/transactional)**, related keywords, ranking keywords, link metrics. Cheapest credible "real" SEO API. |
| **Ahrefs API v3** | No free tier — Enterprise only. **But** [free test queries](https://docs.ahrefs.com/api/docs/free-test-queries) on every endpoint via the docs, no plan needed | REST API + official MCP server for Claude/ChatGPT/Cursor | API key | Quota tied to Enterprise contract | Best link data on the market and very strong NZ/AU keyword coverage. The MCP server is the most direct Copilot wiring of any tool here. **But the price wall is real** — only worth it if Redline commits hard to SEO. |
| **Semrush API** | No free tier; included in Semrush Business plan ($499/mo+) | REST API | API token | Project/quota-based | Comparable to Ahrefs. No reason to pick over Ahrefs unless Redline already pays for Semrush's UI. |
| **Google Ads Keyword Planner API** | Free with any Google Ads account (no spend required) | gRPC + REST via Google Ads API | OAuth 2.0 + developer token (manual approval, can take ~1 week) | Generous; per-developer-token quota | Source-of-truth Google search volume — every other paid tool models from this. Returns ranges (e.g., "1k–10k") for non-spending accounts; exact numbers if you spend. |
| **Bing Webmaster Tools API** | Free | REST API | API key | 5 calls/sec | Verified-site-owner-only data: keyword stats Bing has on **your** site. Useful once Redline ranks; useless for opportunity discovery. |
| **Keywords Everywhere API** | Paid credits ($15 / 100k credits) | REST API | API key | 1 credit per keyword volume lookup | Cheap bulk volume lookups; Google + Bing + YouTube + Amazon + Etsy. Good fit for batch processing keyword lists. |

### Why DataForSEO and Moz lead this category for Redline

DataForSEO's pay-per-task model means a one-off "score 5,000 NZ geotech keyword
ideas" run might cost $5–10 instead of a $200/mo subscription. Moz wins on
**Search Intent classification**, which is exactly what Mark needs to decide
which queries deserve a Skeleton Generator landing page (commercial /
transactional intent) vs a blog post (informational).

---

## 2. SERP-data APIs (real-time Google results, including PAA, autocomplete, related searches)

| Tool | Free? | API/CLI | Auth | Rate / cost | Best for |
|---|---|---|---|---|---|
| **Serper.dev** | 2,500 free queries on signup | REST API | API key | $1 per 1k queries (Starter); down to $0.30/1k at scale; up to 300 QPS | **Cheapest and fastest SERP API.** Returns organic, PAA, related searches, knowledge graph, news, images, autocomplete, scholar, patents. Real-time. Built-in integrations for LangChain, CrewAI, LlamaIndex — so Copilot-agent wiring is already trodden path. |
| **SerpApi** | Free 250 searches/month (50/hour) | REST API + Python/Node/PHP/Ruby/Go SDKs | API key | Starter $25/mo (1k searches); Developer $75/mo (5k) | Most polished SERP API. Has dedicated endpoints for Google Trends, Google Autocomplete, Google Related Questions (PAA), and a **Google Forums API that surfaces Reddit results from the SERP** — useful indirect way to mine Reddit without OAuth. Also offers "U.S. Legal Shield" (they fight Google CAPTCHA litigation for you). |
| **DataForSEO SERP API** | Trial credits | REST | HTTP Basic | ~$0.0006 per Google SERP task at the cheapest tier | Cheapest at scale. Same data shape as competitors but slower (queue-based "task" model unless you pay extra for "live" mode). |
| **Serper / SerpApi Autocomplete** | Same as parent | REST | API key | Same | Bulk Google Autocomplete (the suggestions Google offers as you type) — the rawest source of "what people are about to ask". Backbone of AnswerThePublic-style discovery; trivial to replicate yourself. |
| **ScrapingBee, Bright Data SERP, Apify Google Search Scraper** | Free trials | REST | API key | Variable; usually proxy-credit based | Generic alternatives. Less SEO-specific structure; you'll re-parse PAA and related searches yourself. Pick if you already use them for other scraping. |

### Why this category matters

The fastest, cheapest way to build a "what does Google show people asking about
*soil classification NZ*" pipeline is **SerpApi or Serper.dev hitting Google
Autocomplete + PAA + Related Searches** for a seed list of 50–200 NZ/AU
geotech terms, then deduping and clustering. This replicates 80% of
AnswerThePublic and AlsoAsked at a fraction of the price, with full agent
control.

---

## 3. Question-mining tools (PAA, AnswerThePublic, AlsoAsked, etc.)

This is the category the founder's instinct is most drawn to — "what are people
actually asking?" Honest assessment: **most "question-mining" tools are
visualisation layers on top of Google Autocomplete + PAA**, which you can hit
directly via §2.

| Tool | Free? | API/CLI | Auth | Notes |
|---|---|---|---|---|
| **AlsoAsked** | Limited free; from $15/mo | API on Pro plans (£99/mo+) | API key | Best at recursive PAA scraping (PAA → expand each → PAA again, several layers deep). Genuinely useful UI; the API is paid-only. |
| **AnswerThePublic** | 3 free daily searches; from $9/mo (lifetime deal pattern) | **No public API** as of 2026 (now an NP Digital product) | n/a | Famous "search wheel" visual. GUI-only. Would have to scrape, which violates ToS. **Skip for agent wiring; replicate via §2 instead.** |
| **AnswerSocrates** | Free | No API | n/a | Lightweight free alternative to AnswerThePublic. No API. Useful for ad-hoc browsing. |
| **QuestionDB** | From $15/mo | API on paid plans | API key | Aggregates questions from Reddit, Quora, Stack Exchange, forums. Smaller index than DataForSEO's social APIs. |
| **DIY via Serper/SerpApi** | See §2 | Yes | API key | Hit Google Autocomplete with seeds + alphabet suffixes (`soil classification a`, `soil classification b`, …). Hit PAA endpoint per seed. Recurse. **This is what AlsoAsked does.** |

### Recommendation

For Copilot-agent wiring, **build the question-mining pipeline yourself on top
of SerpApi or Serper.dev**. AlsoAsked is the only paid question-miner with a
real API and it's £99/mo — same money buys you ~100k SerpApi calls plus full
control.

---

## 4. Trend tools (Google Trends and equivalents)

| Tool | Free? | API/CLI | Auth | Notes |
|---|---|---|---|---|
| **Google Trends (official UI)** | Free | **No official API** | n/a | The actual data; no documented programmatic access. |
| **pytrends** (Python library) | Free, OSS | CLI/library | None | Unofficial scraper of Trends. **Frequently breaks** when Google changes the front-end. Strict undocumented rate limits; CAPTCHA risk. Use cautiously and never in a production funnel. |
| **SerpApi Google Trends API** | Counts against your SerpApi quota | REST | API key | Reliable, paid, same data Google shows. The grown-up replacement for pytrends. |
| **DataForSEO Google Trends API** | Pay-per-task | REST | HTTP Basic | Same. Cheaper at scale; queue-based. |
| **Glimpse** | Was a Trends-augmentation tool; **rebranded to skip.dev (April 2024)** and pivoted to AI agents. The keyword-trend product is no longer a focus. | n/a | n/a | Dead for our purposes. Skip. |
| **Exploding Topics** | Limited free; from $39/mo | No public API on lower tiers; API on Enterprise | Custom | Curated list of "trending" topics. Mostly consumer/SaaS bias; weak on engineering verticals. **Probably not useful for NZ geotech.** |
| **DataForSEO Trends tool** | Free GUI at trends.dataforseo.com | n/a (free GUI; paid via API) | n/a | Free interactive explorer; useful for ad-hoc poking. |

### Recommendation

For programmatic trends, use **SerpApi's Google Trends endpoint**. For one-off
human exploration, the official Google Trends UI is fine. Skip pytrends in any
agent — it will silently start returning empty data the day Google ships a
front-end change.

---

## 5. Reddit-specific tools

This category got destroyed in 2023–2024 by Reddit's API policy changes.
Honest current state:

| Tool | Free? | API/CLI | Auth | Status |
|---|---|---|---|---|
| **Reddit official Data API** | Free at 100 queries/min/OAuth client | REST | OAuth 2.0 (client ID + secret + bearer token) | The only legitimate path. Free for non-commercial; **commercial use requires a separate agreement with Reddit**. No AI training on the data. |
| **PRAW** (Python Reddit API Wrapper) | Free, OSS | Python library | OAuth via Reddit | Mature, stable, well-documented. The right way to wire Reddit into a Copilot agent. |
| **Pushshift** | Was the gold standard for historical Reddit search | REST | None historically | **Effectively dead for the public.** Restricted to Reddit moderators only since mid-2023. The public GitHub docs are 7+ years stale. **Do not plan around this.** |
| **GummySearch** | Was a paid Reddit research GUI | GUI + limited API | API key | **Closed 2025-11-30.** Skip. |
| **Subreddit Stats** (subredditstats.com) | Free GUI | No API | n/a | GUI-only stats on individual subreddits. |
| **DataForSEO Social Media — Reddit endpoint** | Pay-per-task | REST | HTTP Basic | Aggregates Reddit engagement metrics on URLs. Useful for brand monitoring; weak for question discovery. |
| **SerpApi Google Forums API** | Counts against SerpApi quota | REST | API key | Returns Reddit results as Google surfaces them in the SERP. **Sneaky way to mine Reddit without touching the Reddit API**, useful when you want only the Reddit threads Google deems authoritative. |
| **Apify Reddit Scraper actors** | Pay-per-result; ~$0.10–1 per 1k items | REST | API key | ToS-grey-area. Reddit's terms forbid scraping outside the Data API. **Avoid for Redline** — the legal exposure on a brand we're trying to build is not worth the saving. |

### Recommendation for Redline

Use the **official Reddit API via PRAW** to mine `r/civilengineering`,
`r/geotechnical`, `r/AskEngineers`, `r/EngineeringStudents`, `r/AskNZ`,
`r/auscivil`, `r/newzealand`, plus a hand-picked list of NZ/AU university
subreddits. 100 QPM is plenty for discovery work. Stay on the free tier; any
commercial productisation of the data needs a Reddit agreement first.

For "what does Reddit show up for *NZ soil classification*" without dealing
with Reddit OAuth at all, **SerpApi's Google Forums API** is the path of
least resistance.

---

## 6. Other forum/Q&A sources (Quora, Stack Exchange, professional forums)

| Tool | Free? | API/CLI | Auth | Notes |
|---|---|---|---|---|
| **Stack Exchange API v2.3** | Free | REST | None for low quota; API key for 10k req/day; OAuth for write | **Underused gem for Redline.** Engineering.stackexchange.com (yes, it exists) plus `engineering.stackexchange.com`-adjacent sites have geotech questions with vote counts that are effectively a popularity signal. Free, official, generous, well-documented. |
| **Quora** | n/a | **No public API**; was deprecated years ago | n/a | Scraping ToS-prohibited. Practical access only via Google → Quora results, i.e., via §2 SERP APIs. |
| **YouTube Data API v3** | Free quota (10k units/day default) | REST | OAuth or API key | YouTube search trends — useful for spotting what tutorial-style content engineers are watching. Quota math is fiddly but workable. |
| **Wikipedia Pageviews API** | Free | REST | None | Free, official, fast. Gives daily pageview counts for any article, e.g. "Soil_classification" or "Cone_penetration_test". A surprisingly clean popularity proxy for technical concepts. |
| **NZGS / AGS / IPENZ forums** | n/a | None — these are PHP forum software with no API | n/a | The actual NZ/AU professional discussion happens here and is invisible to most tools. **Manual review only.** Worth a fortnightly browse by Graeme/founder; don't try to automate. |

---

## 7. LinkedIn discovery — honest assessment

**There is essentially nothing legitimate here for what the founder wants.**

LinkedIn aggressively blocks third-party scraping. Their official APIs
(Marketing Developer Platform, Sales Navigator API, Talent Solutions API) do
not expose post-search or "what are people discussing" data. You cannot, via
any legitimate path, ask "what are NZ civil engineers posting about this week?"

| Tool | Reality |
|---|---|
| **LinkedIn Marketing API** | Restricted partner program. No access to public-feed search-intent data. |
| **Sales Navigator search export tools** (Phantombuster, TexAu, Evaboot, Lemlist) | All do GUI-emulating scraping. **Banned by LinkedIn ToS.** Frequent account bans. Do not use on the founder's primary account. |
| **Taplio, Shield Analytics** | Analyse the founder's *own* LinkedIn performance. Not search-intent discovery. Useful, separate product category. |
| **Inlytics, AuthoredUp** | Same as Taplio — own-account analytics, paid GUIs. |

### Honest recommendation

**For LinkedIn, give up on tooling and go manual.** The founder's first 90 days
of LinkedIn posting is itself the discovery instrument: which posts get
comments, which questions get DMs, which polls show what the audience cares
about. Build a habit (5 min/day) of capturing notable LinkedIn engagement into
a markdown log. That log feeds the monthly signal report.

If we ever need automation, we use the LinkedIn API via my (John's) own
account *for our own analytics* via Taplio or Shield. We do not scrape other
people's posts.

---

## 8. Competitor / SERP analysis (who ranks for what)

| Tool | Free? | API/CLI | Auth | Notes |
|---|---|---|---|---|
| **Ahrefs Site Explorer / Keywords Explorer (API)** | Enterprise only | REST + MCP | API key | Best-in-class for "what keywords does competitor X rank for". Price wall stays the same. |
| **Semrush Domain Analytics API** | Business+ plan | REST | API token | Equivalent to Ahrefs. Pick on UI preference. |
| **DataForSEO Labs API** | Pay-per-task | REST | HTTP Basic | Cheapest competitor-keyword data. "Ranked Keywords" endpoint gives you every keyword a domain ranks for. Excellent value. |
| **Moz API — Ranking Keywords endpoint** | $20+/mo | JSON-RPC | API key | Lighter coverage than Ahrefs but ~50× cheaper. |
| **SerpApi / Serper.dev — competitor SERP scraping** | See §2 | REST | API key | "For each of these 50 queries, who's in positions 1–10?" Trivial to build. |

For Redline specifically: there are very few entrenched competitors in NZ/AU
geotech-software SERPs. **Most of the queries we care about are dominated by
PDFs of standards, university lecture notes, and ResearchGate papers** — i.e.,
not real competitive content. This is good news (an open category) and bad
news (we may not learn much from competitor gap analysis).

---

## 9. GUI-only, lower priority

These have no API or only a GUI/scrape-emulation API. Listed for completeness;
not for Copilot-agent wiring.

- **AnswerThePublic** (NP Digital) — see §3
- **AnswerSocrates** — free GUI question explorer
- **KeySearch** — $24/mo bloggers' SEO tool, no API
- **Ubersuggest** (Neil Patel) — limited free; no real API
- **Keyword Tool (keywordtool.io)** — has paid API but reviews report stale data
- **Soovle, KeywordShitter** — free Autocomplete aggregators; trivial to replace with a Serper.dev script
- **GummySearch** — closed Nov 2025
- **Glimpse** — pivoted to skip.dev; no longer a Trends tool
- **Exploding Topics** — paid GUI, weak on engineering verticals
- **AlsoAsked** — has API but only on £99+/mo plans; replicable via SerpApi PAA endpoint at lower cost

---

## 10. Recommended starter stack for Redline

Goal: free or near-free, fully API-accessible, agent-wireable, and gives 80%
of the discovery signal we need to identify Product-Led SEO opportunities for
NZ/AU geotechnical engineers.

| # | Tool | Cost | What we use it for |
|---|---|---|---|
| 1 | **SerpApi** (Free 250/mo, then $25/mo Starter) | Free → $25/mo | The Swiss Army knife: Google Autocomplete, People Also Ask, Related Searches, Google Trends, Google Forums (Reddit-via-Google). One vendor, one API key, one billing relationship. |
| 2 | **DataForSEO Labs + Keyword Data APIs** (pay-as-you-go) | ~$10/mo at our scale | Bulk keyword volume + Google Ads search-volume data + competitor "Ranked Keywords" + cheap SERP fallback. Granular cost control. |
| 3 | **Reddit official API via PRAW** | Free | Direct mining of NZ/AU geotech and engineering subreddits for question patterns. 100 QPM is more than enough. |
| 4 | **Stack Exchange API v2.3** | Free | Official, generous, perfect for engineering Q&A signal. Vote counts as popularity proxy. |
| 5 | **Wikipedia Pageviews API** | Free | Free popularity signal for technical concepts (CPT, Atterberg limits, soil classification, etc.). Sanity-checks keyword-tool numbers. |

**Total monthly cost at the scale we need: ~$25–35.**

That gets us a Copilot-wireable pipeline that can answer:

- What are NZ engineers Googling about soil classification, CPT, settlement,
  bearing capacity, GIRs?
- What follow-up questions does Google itself surface (PAA)?
- What are engineers actually asking on Reddit and Stack Exchange?
- What Wikipedia articles are getting viewed week-on-week?
- What's the search-volume floor below which a topic isn't worth a Product-Led
  SEO build?

If the discovery work shows a serious commercial opportunity, **then** we add
Ahrefs Enterprise or Moz API for ongoing competitive intelligence. Not before.

---

## 11. Anti-patterns and risks

### Things that look free but aren't, or look API-accessible but aren't

- **AnswerThePublic** — looks free; the meaningful data sits behind a paywall and there's no API.
- **Ahrefs API** — has a free-test-queries page that gives you a taste; the actual API is Enterprise-only.
- **Pushshift** — every blog post written before 2023 recommends it. **It's dead for the public.** Don't plan around it.
- **GummySearch** — every blog post written before late 2025 recommends it. **Closed November 2025.**
- **Glimpse** — pivoted to AI agents under the skip.dev brand. Treat as discontinued for Trends purposes.

### Things that work but will get you in trouble

- **Scraping Google directly** — Google's ToS forbids it; CAPTCHAs make it unreliable; in jurisdictions like the EU there's case law against bulk SERP scraping. Pay SerpApi/Serper/DataForSEO; they handle the proxy and legal layer.
- **Scraping Reddit outside the official API** — explicitly forbidden in [Reddit's Data API Terms §3.2](https://www.redditinc.com/policies/data-api-terms). Reddit will block, and they have monetisation incentives to enforce. Use OAuth + PRAW, period.
- **Scraping LinkedIn** — guaranteed account ban for the founder eventually. Not worth it. Especially not on the account whose growth we're trying to build.
- **Scraping Quora** — same risk profile as Reddit pre-2023. Use SERP APIs to surface Quora hits via Google instead.
- **Using user-generated Reddit content for AI training** — explicitly prohibited (Data API Terms §2.4) without rights-holder permission. Relevant if Mark ever wants to fine-tune a model on engineering-question patterns.

### Pricing traps

- **SerpApi free tier is 250 searches/month, throttled to 50/hour.** Fine for evaluation; you'll hit the wall fast on real discovery work. Plan to pay $25/mo from month 2.
- **Serper.dev's "free 2,500 queries" is one-time on signup**, not monthly. Good for evaluation, useless as a recurring tier.
- **Moz API's $20 entry tier is row-capped, not query-capped.** Easy to misread.
- **DataForSEO has a minimum top-up** (was $50 last I checked). Cheap per-task, but a small upfront commitment.

### Stale-data traps

- Most paid keyword tools refresh search volumes monthly or quarterly, not in real time. For trend-chasing, use the SERP/Trends APIs in §2 and §4 directly.
- Google Trends *itself* normalises and rounds heavily — never trust an absolute number from Trends, only the relative shape over time.

### Geographic coverage traps

- Many cheaper SEO tools (KeySearch, Ubersuggest, Keywords Everywhere) have **weak NZ and AU coverage** compared to US/UK. Verify a sample of NZ-specific terms (e.g., "NZGS guidelines", "MBIE geotechnical") before committing.
- DataForSEO and Moz are good for NZ/AU. Ahrefs is best.

---

## 12. Open question for the next strategy session

Before we wire any of this into a Copilot agent, **the founder, Ron, and Mark
need to confirm** which Product-Led SEO posture we're committing to:

- (A) **Skeleton Generator IS the Product-Led SEO asset** (founder's current
  thinking). No adjacent tools yet. Marketing job becomes: write the landing
  pages, the LinkedIn motion, and the referral mechanic that drive the
  Skeleton Generator's discoverability and shareability.
- (B) **Skeleton Generator + 1–2 small adjacent tools** (e.g., free soil
  classifier, free section checklist). Each adjacent tool ranks for a query
  cluster the Skeleton Generator doesn't, and funnels into it.

Posture A means we use the discovery tools above to **inform landing-page copy
and LinkedIn content topics**. Posture B means we use the discovery tools to
**identify which adjacent tools to brief Mark for PRD work** (per
[`marketing-product-led-seo`](../../../../.agents/skills/marketing-product-led-seo/SKILL.md)).

I'd recommend starting with discovery work that informs both — the tools above
do double duty either way.

---

## References

- [Reddit Data API Terms](https://www.redditinc.com/policies/data-api-terms)
- [Reddit Data API Wiki — rate limits](https://support.reddithelp.com/hc/en-us/articles/16160319875092)
- [PRAW documentation](https://praw.readthedocs.io/en/stable/)
- [SerpApi pricing](https://serpapi.com/pricing) and [endpoint catalogue](https://serpapi.com/search-engine-apis)
- [Serper.dev pricing](https://serper.dev/)
- [DataForSEO API catalogue](https://dataforseo.com/apis)
- [Moz API v3](https://moz.com/products/api)
- [Ahrefs API docs and free test queries](https://docs.ahrefs.com/)
- [Stack Exchange API v2.3](https://api.stackexchange.com/)
- [Wikipedia Pageviews API](https://wikitech.wikimedia.org/wiki/Analytics/AQS/Pageviews)
