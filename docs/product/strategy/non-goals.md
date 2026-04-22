# Non-Goals — Redline

**Status**: Draft v2. **Owner**: Ron.

Non-goals are commitments to *not* build something. Every non-goal here costs us a
plausible-sounding feature request, and we accept that cost because the alternative is
strategy drift.

## Product Non-Goals

1. **Authoring engineering opinions.** Redline does not write recommendations, design
   parameters, or interpretive content. It surfaces gaps; the engineer fills them.
   Crossing this line forfeits Switzerland-neutrality.
2. **Compliance attestation or CPEng sign-off proxy.** Redline does not certify
   compliance with NZS, AS, or any other standard. Output is advisory. The Chartered
   Professional Engineer remains accountable.
3. **Acting as an arbiter between engineer and reviewer.** When the tool flags an issue
   and the senior disagrees, the senior is right. Redline does not adjudicate.
4. **Replacing the senior reviewer.** The Pre-Review engine compresses review rounds;
   it does not eliminate them.
5. **Generic AI writing assistance.** No grammar polish, no style improvement, no tone
   rewrite. There are 50 tools that do this; we are not one of them.
6. **Industry coverage beyond geotechnical.** No structural reports, no environmental
   assessments, no civil drainage. The Standards Knowledge Store is geotech-scoped by
   design.
7. **Mass-produced AI-generated SEO content.** No programmatic AI blog spam, no
   ChatGPT-drafted-and-published articles, no scaled content farms. Current B2B
   content-marketing literature documents that this pattern triggers Google's "scaled
   content abuse" classifier and degrades EEAT (Experience, Expertise, Authority,
   Trust) signals — case studies show 99%+ ranking loss. The Switzerland-neutral
   positioning cannot survive that reputation hit. AI-assisted *drafting* of founder
   content remains allowed; LLM-as-Judge quality gate is required before publishing.
   See `gtm/content-engine.md`.

## GTM Non-Goals (H2 2026)

1. **No third geography.** NZ and AU only. See `strategic-bets.md` Bet 5.
2. **No Tier 1 enterprise sales motion.** *(updated 2026-04-20, Archie CI session)*
   Tier 1 firms (T+T, WSP, Beca — 1000+ employees, government projects) build their
   own AI and require enterprise SOC2. They are not Redline's market. Single PLG funnel
   from free wedge → Pro → Business, targeting Tier 2 firms (5-50 employees,
   residential/commercial geotech). See `strategic-bets.md` Bet 6 market segmentation.
   Provenance: `docs/research/20260420-archie-competitive-intelligence-prompt.md`.
   No SDR team, no outbound enterprise prospecting, no annual contract negotiations.
3. **No paid acquisition spend before the wedge proves out.** Bet 1 must trip its kill
   criterion before we test paid channels. Spending on Google Ads while the free wedge
   converts at unknown rate is conflating two experiments.
4. **No conference sponsorship in H2.** Founder-led conversations only.
5. **No partnership channel.** No reseller, no Big-4 alliance, no software-vendor OEM.
   Partnerships are diluting until product-market fit is signed.
6. **We do not claim engineering credentials we do not hold.** The founder is a data
   scientist who spent 3.5 years embedded in a NZ geotechnical consultancy — not a
   geotechnical engineer. No external surface (web, LinkedIn, sales, podcasts,
   conference talks) may imply he has drafted or reviewed engineering documents in a
   professional engineering capacity. See `positioning.md` → Credibility Boundaries
   and `gtm/content-engine.md` → Voice Constraints. This is reputational and legally
   adjacent — misrepresentation in a market this small is irrecoverable.
7. **We do not claim security or compliance certifications we do not hold.** Pricing
   page, sales decks, and contracts may reference "enterprise security review on
   request" or "contact us about compliance requirements". Specific certifications
   (SOC 2, ISO 27001, HIPAA, etc.) are forbidden until formally attained. See
   `pricing-methodology.md` → Fake-Door Tier Discipline.

## Engineering Non-Goals (H2 2026)

1. **No model training on customer documents.** Zero-training perimeter is enforced.
   Customer documents are read in-session and not retained for fine-tuning. This is
   a non-negotiable trust posture for professional-services data.
2. **No on-premises deployment.** Cloud-only Year 1. Air-gapped enterprise deployments
   are a Phase-2 conversation, not a Sprint-1 distraction.
3. **No mobile client.** The work happens in Word and a browser. Mobile is not the form
   factor for GBR drafting.
4. **Clean break from current employer.** No Redline code, servers, research, or product
   work may touch the current employer's hardware, networks, or paid time. Founder's
   first official day on Redline is 2026-06-01. Strategy and planning work on personal
   time and hardware is permitted before that date; implementation is not. This is
   both a legal requirement (IP/non-compete protection) and a personal integrity
   commitment.

## Why These Non-Goals Now

Each non-goal removes a slice of optionality the founder might otherwise be tempted to
preserve. Optionality is expensive: it forces the build to remain generic, slows
decisions, and dilutes positioning. Commit now; revisit at the H2 strategy refresh.
