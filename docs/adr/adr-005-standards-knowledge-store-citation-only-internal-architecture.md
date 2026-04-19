# ADR-005 — Standards Knowledge Store: Citation-Only, Internal-Only Architecture

## Decision

The Standards Knowledge Store stores clause references and applicability mappings only —
never full proprietary text. It is used exclusively as an internal engine powering
Redline features (skeleton generation, Pre-Review checks); it is never exposed as a
public-facing query interface.

## Status

Accepted. 2026-04-19.

## Context

Redline's Standards Knowledge Store is the curated corpus of NZ and AU geotechnical
standards (NZS 3910, AS 4000, AS/NZS 4122, NZGS guidance, ACENZ guidance) that
underpins every Redline output. Two design questions required resolution before any
content could be ingested into a production system:

1. **IP risk**: NZS and AS publications carry Crown and corporate copyright respectively.
   Reproducing full clause text in a commercial software product without a licence is a
   legal exposure. Injunctive relief — not a trial win — is sufficient to pause the
   product while litigation proceeds, which is effectively fatal at pre-revenue stage.

2. **Architecture exposure**: A public-facing "chatbot" interface that accepts project
   descriptions and returns relevant standards content would directly commoditise the
   knowledge architecture, invite head-on comparison with ChatGPT and Gemini, and
   contradict the "we are not a chatbot" anti-positioning established in
   `docs/product/strategy/positioning.md`.

Graeme (Principal Geotechnical Engineer, 25+ years in a large NZ consultancy) provided
domain advisory on 2026-04-19. Ron (Strategy & GTM Advisor) provided strategic framing.
The full Graeme advisory is at
`docs/knowledge/geotechnical/standards-and-codes/nz-au-standards-ip-classification.md`.

## Options Considered

- **Option A — Full text storage, internal only**: Ingest complete clause text into the
  index; use it exclusively inside Redline's internal pipeline; never expose it directly
  to end users. Reduces product friction. Maximises IP risk (storing full text creates
  a larger copyright footprint than storing references).

- **Option B — Full text storage, public interface**: Expose the index as a
  public-facing query tool. Maximises reach and SEO value. Maximises both IP risk and
  competitive intelligence exposure; directly contradicts positioning.

- **Option C — Citation-only, internal only** *(selected)*: Store clause references,
  applicability mappings, and derived guidance summaries only — never full proprietary
  text. Use the index exclusively inside Redline features. Engineer users are directed
  to read the source standard (via clause reference and a "where to find this standard"
  link). Public-facing SEO tools drawing on the index are a Phase-2 decision
  (see `docs/product/strategy/decisions/parked-decisions.md` P-019 and P-026).

- **Option D — No internal standards index**: Rely solely on public LLM training data
  for standards awareness. Lowest IP risk. Forfeits Bet 3 — the Standards Knowledge
  Store is the moat.

## Decision Rationale

**Citation-only is both professionally defensible and legally lower-risk.**
Graeme's advisory (high confidence) confirms that clause references without text
reproduction are the universal standard in engineering practice — engineering reports,
GBRs, GIRs, and contracts routinely cite "NZS 3910:2013 Clause 14.4" without
reproducing the text. Courts, engineers, and expert witnesses treat these references as
unambiguous. This is also consistent with how standards are designed to be cited.

**The "ChatGPT reproduces it anyway" argument is not a legal defence.**
The reasoning that "LLMs return proprietary text, so reproducing it commercially is
safe" is structurally equivalent to claiming jaywalking is safe because others jaywalk.
OpenAI and Google have nine-figure legal budgets and global operations; a NZ startup
storing commercial clause text without a licence is a qualitatively different
enforcement target. Standards bodies do not need to win a copyright suit — an interim
injunction during pre-revenue stage is product death.

**Internal-only preserves the opacity of the moat.**
The Standards Knowledge Store's value is not in the content per se but in the curated
applicability logic that determines which clauses apply to which scenarios. Making that
logic visible via a public query interface commoditises it on day one. Embedding it
inside skeleton generation and Pre-Review checks keeps it opaque to competitors who can
see outputs but cannot reverse-engineer coverage.

**Alignment with positioning and strategic bets.**
Positioning explicitly lists "chatbot" as an anti-positioning forbidden form. A public
standards interface is a chatbot. Internal-only use is consistent with Bet 6
(staying invisible to incumbents while the moat matures) and Bet 4 (Switzerland-neutral
quality layer, not an AI assistant).

## Consequences

**Positive:**
- Reduces IP exposure to the minimum achievable without abandoning standards grounding.
- Preserves moat opacity — competitors see outputs, not the knowledge architecture.
- Consistent with professional engineering practice — citation-only outputs are not a
  product quality compromise.
- Aligns with positioning (not a chatbot) and Bet 6 (stealth during beachhead phase).

**Negative:**
- Junior engineers using Redline features may encounter clause references for standards
  they do not have immediate access to. Mitigation: include a "where to find this
  standard" link or employer-library reference alongside every clause reference. This
  is a UX responsibility, not an architecture change.
- The citation-only design does not resolve the formal licensing question for internal
  use. Direct enquiries to Standards NZ, Standards Australia, NZGS, and ACENZ are
  required before any standards content enters a production system (see P-026).
- Public-facing Product-Led SEO tools drawing on the Standards Knowledge Store are
  deferred until the licensing review resolves and KR1 is validated (P-019, P-026).

## References

- `docs/knowledge/geotechnical/standards-and-codes/nz-au-standards-ip-classification.md`
  — Graeme's domain advisory (2026-04-19)
- `docs/product/strategy/positioning.md` — Anti-positioning (chatbot forbidden form)
- `docs/product/strategy/strategic-bets.md` — Bet 3 (Standards Knowledge Store moat),
  Bet 4 (Switzerland-neutral), Bet 6 (new-market disruption stealth)
- `docs/product/strategy/decisions/parked-decisions.md` — P-019 (Product-Led SEO),
  P-026 (formal licensing enquiries)
- ADR-003 — Facade primitives-only boundary (related: what passes through internal
  boundaries)
