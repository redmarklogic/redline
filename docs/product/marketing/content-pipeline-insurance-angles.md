# Content Pipeline — Insurance Angles

**Owner**: John (Head of Marketing)
**Date**: 2026-05-14
**Source intelligence**: CEAS/Aon webinar (14 May 2026) + Graeme domain validation +
Indemnity Matters Issue 88 (April 2026)
**Status**: Draft — 4 gems identified, none published

---

## Attribution Constraints (binding for all four gems)

1. **Do not cite the webinar as a source.** The host explicitly requested no recordings
   or AI notetakers. The Q&A was not intended to be on record. No external document
   may reference the webinar, the Q&A session, or what was said in it.
2. **Do not attribute statements to Christine Crook, Craig Lewis, or Gaynor Roberts by
   name in any published content.** Their names may appear in internal documents only.
3. **All arguments must stand independently** — grounded in structure, domain knowledge,
   and publicly available sources (Indemnity Matters newsletter, PI policy terms,
   standard engineering QA practice). If an argument cannot stand without the webinar
   as a source, do not publish it.

---

## Graeme Review Gate

- **Gem 1** and **Gem 2** require Graeme sign-off before any draft goes external.
  Both make domain-specific claims about engineering QA and PI policy structure.
- **Gem 3** requires Graeme review of any specific engineering examples used in the
  post. The structural argument does not require Graeme review, but examples do.
- **Gem 4** requires no Graeme review for the framing, but any engineering-specific
  content must go through Graeme before publication.

---

## Gem 1 — Publish First

**Working title**: "The question your PI insurer has asked for eight years — and what
it still can't see"

**Big 5 category**: Problems

**Target reader**: Small-firm principal or Technical Director who has just renewed PI
insurance and answered the QA question without thinking hard about it.

**Core argument**:

NZ PI renewal documentation has included a QA question for six to eight years. Firms
are asked to outline their basic QA measures. The question was introduced to drive
commercial discipline: scope definition, standard contract conditions, limiting
liability. It is a process-existence check.

That question has no access to the content of the reports the firm produces. It cannot
detect whether an AI-generated sentence in a GBR cites a standard that does not exist,
whether the baseline language is unenforceable, or whether the text has drifted into
warranty-territory phrasing. These failure modes are invisible to the commercial QA
layer the renewal question was designed to probe.

The question the renewal form has not yet asked — but that the AI era is making
necessary — is: "Can you demonstrate what your technical content review actually
checked, and when, before the signing engineer signed?"

**Why this gem is most valuable**:

The argument is counter-intuitive (the insurer's question doesn't do what you think it
does), highly specific, and addresses a fear the audience already has (AI risk and PI
exposure). It does not require over-claiming — the structural argument is factual. It
opens naturally to what Redline does. It is the highest-traffic Big 5 category
("Problems" — naming a problem the reader didn't know they had). Graeme has validated
the structural distinction.

**Publication order**: First.

**Key constraint**: Must not claim the technical audit trail is currently required by
insurers. The framing is "the question the renewal form has never had" — not "the
question your insurer is now asking."

---

## Gem 2

**Working title**: "AI writes confidently. Confident language can void your PI cover."

**Big 5 category**: Problems (conversion-critical variant — reframes a risk they
thought they already understood)

**Target reader**: Senior engineer or firm principal who is already using AI and
feels comfortable. This piece reframes the risk from "AI might get the facts wrong"
(which they know) to "AI's writing style — not just its facts — may create a legal
liability your policy won't cover."

**Core argument**:

AI-generated text tends toward confident, declarative prose. That register can drift
into warranty language. A sentence such as "the ground will not liquefy under the
design seismic event" is not a hedged professional opinion — it is an express warranty.
Standard NZ PI policies contain warranty exclusions: they do not cover liability for
contractual guarantees of outcome.

The failure mode is invisible to standard senior review, which checks technical
soundness, not legal language register. The sentence looks professionally polished. It
reads like a confident expert conclusion. It passes a plausibility check. It may void
coverage if a claim arises.

The grad analogy commonly used for AI oversight — "treat it like a junior engineer's
work" — does not address this. A graduate's confident language still reads like a
graduate's attempt at precision. AI produces a sentence indistinguishable from
carefully crafted expert prose. The reviewer's instinct is: this is fine. That
instinct is the problem.

**Why this gem is valuable**:

The angle is novel. It does not appear in any NZ engineering content marketing. It
reframes the risk from content accuracy (well understood) to language register (not
yet on the audience's radar). It is highly shareable among principals who pride
themselves on technical accuracy but have not thought about the language register
problem.

**Graeme review gate**: Mandatory before any draft goes external. The claim about
warranty exclusions in NZ PI policies must be verified by Graeme and referenced to a
specific policy provision or industry guidance. The language examples must use
hypothetical sentences, not actual clauses from any specific report.

**Publication order**: Second.

---

## Gem 3

**Working title**: "The 'treat it like a junior engineer' rule for AI — and why it's
missing the point"

**Big 5 category**: Best of (how-to variant — "here's the right framing, and why it
matters more than the one everyone uses")

**Target reader**: Any engineering professional who has heard the grad analogy and
accepted it as sufficient guidance.

**Core argument**:

The "treat AI like a bright, very keen young graduate" rule is now in broad circulation
in the NZ engineering profession. It is useful as a cultural prompt. It is incomplete
as a practical standard.

The analogy gets one thing right: using AI does not transfer responsibility. The
professional who signs the report is still responsible for its content. That principle
is correct.

The analogy gets one important thing wrong. A graduate's mistakes stay within the
domain of plausible engineering. They misapply a formula. They forget a load
combination. They use the wrong bearing capacity factor. These errors are visible on a
technical review — they look like mistakes.

AI can produce a sentence that looks like a carefully crafted expert conclusion and
contains a failure mode a technical review would not detect: a citation to a standard
that does not exist, a statement about ground behaviour phrased as an engineering
certainty, a clause that functions as a warranty rather than a qualified professional
opinion. The sentence does not look like a mistake. It looks authoritative. That is
what makes it dangerous.

Checking AI like you check a graduate's work is necessary. It is not sufficient.
The standard of care needed for AI output is verification — independently confirming
every material citation, every absolute statement, every load-bearing claim — not just
review.

**Attribution note**: The grad analogy is in public circulation in the NZ engineering
profession. This post does not need to cite a specific source. The argument stands
independently. Do not reference the webinar, the Q&A, or any named speaker.

**Graeme review gate**: Required for any specific engineering examples used to illustrate
the failure mode categories. The structural argument does not require Graeme review.

**Publication order**: Third.

---

## Gem 4 — Publish Last

**Working title**: "Insurers aren't seeing AI claims in engineering yet. Here's what
they said is coming."

**Big 5 category**: Discovery / SEO anchor

**Target reader**: Engineer or principal searching for "AI insurance engineering" or
"engineering PI insurance AI."

**Core argument**:

The insurance industry's claims data for engineering firms does not yet show AI as a
contributing factor. This is publicly observable — the AI claims pattern currently
documented in professional liability literature is concentrated in legal services
(fabricated case law), not engineering.

This is not because engineering is safe from AI-related claims. It is because the
AI failure modes in engineering — hallucinated standard references, warranty language
drift, scope-exceeding conclusions — have not yet propagated into formal claims. The
claims curve for legal services preceded engineering by approximately 12--18 months.

The insurance industry itself is signalling this expectation. The commentary in
Indemnity Matters (CEAS, April 2026) is the clearest public-domain signal from a NZ
professional indemnity insurer that engineering is next.

**Why this gem is less sharp than gems 1--3**:

The insight is directional ("expecting to") rather than definitive. It does not name a
structural gap or reframe a specific risk. It positions Redline as informed and ahead
of the wave — which has value for thought leadership but lower conversion potential
than the structural arguments in gems 1 and 2.

**Attribution**: The Indemnity Matters newsletter (April 2026) is a public document and
can be cited as a source. No webinar citation required. The argument works off the
newsletter alone.

**Publication order**: Fourth.

---

## Recommended Sequence

| Order | Gem | Big 5 | Est. conversion potential | Graeme gate |
|---|---|---|---|---|
| 1 | The question your insurer can't see | Problems | High | Required |
| 2 | Confident language voids PI cover | Problems | High | Required (mandatory) |
| 3 | The grad analogy is incomplete | Best of | Medium | Required for examples |
| 4 | Insurers aren't seeing it yet | Discovery | Low--medium | Not required |

**Sequence rationale**: Lead with the structural argument (Gem 1) because it is the
most defensible, counter-intuitive, and directly opens the Redline value proposition.
Follow with the warranty language angle (Gem 2) while the structural argument is still
resonating. The grad analogy rebuttal (Gem 3) can be scheduled when there is a topical
hook (e.g. after CAS publishes the member survey findings in the next Indemnity
Matters). Gem 4 is the search-anchor piece — it can run anytime but has the lowest
conversion ceiling.

**Before publishing Gem 1**: Confirm with Ron that "the question the insurer has
never asked" framing does not overclaim the current state of underwriting requirements.
