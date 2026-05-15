# CEAS/Aon Webinar Findings — Insurance for Consulting Engineers

**Date**: 2026-05-14
**Event**: CEAS/Aon "Insurance for Consulting Engineers" webinar (4th in series)
**Format**: Two-part — presentation (recorded, to be posted in CAS members area) + Q&A
**Attendees**: ~100 NZ civil engineering firms; audience mics muted throughout

---

## IMPORTANT — Recording and Attribution Rules

The host (Michelle, CAS) stated explicitly at the opening:

> "We do ask that there's no recordings or AI notetakers in these webinars to allow
> for free conversation and discussion in the Q&A."

She also confirmed only the presentation portion would be recorded for the members
area — the Q&A was not intended to be on record.

This session was recorded and transcribed internally. The following rules apply
to all use of this intelligence:

- **Never cite this webinar as an external source.**
- **Never attribute quotations to named individuals in any published or external document.**
- **Never reference the recording or this transcript in any outreach to CAS, Aon, or
  Craig Lewis.**
- All arguments drawn from webinar intelligence must stand independently — grounded
  in structure and domain knowledge, not in what was said in a private Q&A session.

---

## Presenters

| Name | Role |
|---|---|
| Michelle | CAS host and moderator |
| Christine Crook | Aon, specialist in PI and liability insurance for professional service firms; 20+ years with CAS |
| Craig Lewis | CAS Chair; joined for Q&A session |
| Gaynor Roberts | Aon Claims Manager; joined for Q&A session |

**Structural note**: Aon is the broker — they administer the CAS PI scheme and handle
renewals and claims. **NZI (New Zealand Insurance) is the actual underwriter.** Any
underwriting change — such as favorable premium treatment for documented AI QA — would
be decided by NZI, not Aon. Craig referenced NZI explicitly when answering Q10.

---

## Q&A Findings

### Q5 — QA processes as a renewal factor

**Question (submitted by the user)**: "For small firms, how do PI renewal conversations
typically address the firm's internal QA processes — is that a factor in underwriting,
or is it mostly about claims history?"

**Christine Crook**: Yes, internal QA measures are definitely extracted at renewal. Aon
asks firms to outline their basic QA processes. This information is a factor in
underwriting alongside claims history.

**Craig Lewis**: This has been in CAS renewal documentation for six to eight years.
It was introduced to drive discipline around scope definition, standard contract
conditions, limiting liability, and internal review processes. Firms are asked to
outline basic QA measures. Craig noted that firms "easy copy last year's answer without
reviewing" — an implicit acknowledgment that the question has become a checkbox in
practice.

**Strategic read**: Confirmed — QA is an established, multi-year factor in PI renewal.
It is not new and it is not edge-case. However, the question was designed for the
commercial QA layer (scope, contracts, sign-off procedures) and has no mechanism to
detect technical content verification failures. See Graeme's structural finding below.

---

### Q6 — AI claims in engineering reports

**Question**: "Are you seeing PI claims where AI-generated content in engineering
reports was a contributing factor, or is it still theoretical?"

**Gaynor Roberts**: "Not seeing it on the engineers book — but we're expecting to."
Lawyers are currently the most frequent target because AI fabricates case law. Gaynor
said this is a pattern across all insurance schemes, not just engineering.

**Craig Lewis**: Used the "bright, very keen young graduate" framing — originally
attributed to "Jim Dobby" from CAS roadshows. The principle: using AI does not
transfer responsibility. The buck stops with whoever signs the producer statements.
It does not absolve you from checking AI output and weeding out hallucinations.

**Strategic read**: AI engineering claims are expected, not yet observed. The claims
manager confirmed it publicly. Redline's positioning as "ahead of the wave" is
structurally accurate as of May 2026.

**Graeme's domain challenge to the grad analogy**: The "check AI like you'd check a
grad's work" framing is useful as a cultural prompt but misleading as a practical
standard. A graduate's mistakes stay within the domain of plausible engineering — a
miscalculated factor of safety, a misapplied load combination. AI can fabricate a
reference to a standard that does not exist, generate unenforceable baseline language,
or produce absolute statements that look polished but create warranty exposure. These
are categorically different failure modes. The framing undersells the required standard
of checking: verification, not just review.

---

### Q10 — Favorable underwriting for AI QA processes

**Question**: "Would firms with systematic AI QA processes get more favorable
underwriting treatment?"

**Craig Lewis**: "Would have to be a fairly good argument put forward." Not a no — but
emphatically not a yes. He specifically referenced NZI as the decision-maker.

**Christine Crook**: "AI is an emerging risk — it's understanding it as a tool and
benefit but also understanding the risk profile. It's part of the evolution of risk
management and how underwriters approach that." Careful hedge, not a commitment.

**Strategic read**: The bifurcation thesis — that firms with documented AI QA will
receive premium benefits — is still unconfirmed with any NZ underwriter. The question
is now alive in the insurance community (Craig did not say it was implausible), but
the underwriting market has not formalised the requirement. The path to confirmation
runs through NZI, not Aon.

---

### Newsletter follow-up (not a direct question — contextual exchange)

Craig confirmed that CAS received member responses to the April newsletter AI question:
"How open are you with your clientele about your use of AI?"

CAS board meeting was scheduled for the week of 19 May 2026. Craig: "If there's
anything of interest that has come in, we'll get that out in Indemnity Matters in the
future."

**Action**: Watch for the next Indemnity Matters issue. The member responses are
primary market research — what NZ consulting engineers actually said about their AI
usage — and will be published in full for CAS members.

---

## Graeme's Structural Finding (domain-validated)

This is the most strategically significant insight from the webinar.

**The commercial/technical QA structural gap:**

NZ engineering QA practice operates in two structurally separate layers:

1. **Commercial QA layer**: Scope definition, standard contract conditions, LOE (Letter
   of Engagement), liability caps, upfront client conversations, senior sign-off on
   delivery. This is the layer the CAS renewal question was designed to probe, starting
   six to eight years ago.

2. **Technical content verification layer**: Checking whether the report's technical
   content — AI-generated or otherwise — is correct, internally consistent, correctly
   sourced, and free of category errors, warranty language drift, or hallucinated
   references.

**The renewal QA question cannot detect technical content verification failures.** It
was not designed to. A firm can answer every CAS renewal question correctly — excellent
commercial QA — and still submit a report that contains an AI-generated sentence citing
a standard that does not exist, or asserting ground behaviour in absolute terms that
create warranty exposure under the PI policy.

**Redline sits in the gap between the question that has been asked for six years and the
question that is about to be asked.** Not "do you have a QA process" but "can you
demonstrate what your AI-assisted QA actually checked, and when."

This structural finding is grounded in how the renewal question was described by Craig
Lewis (confirmed) and in Graeme's professional assessment of large-firm vs small-firm
QA practices across NZ consultancies.

---

## Warranty Language Risk (additional domain finding)

AI-generated text tends toward confident, declarative prose. That register can drift
into warranty language — e.g. "the ground will not liquefy under the design seismic
event" rather than "based on the investigation data and engineering judgement, the
risk of liquefaction is assessed as low."

Standard NZ PI policies contain warranty exclusions. A sentence that functions as an
express warranty can render the policy unresponsive to a claim arising from breach of
that warranty — even if the engineer was not negligent in the ordinary sense.

**The failure mode**: the AI writes confidently, the sentence looks professionally
polished, and the senior reviewer is checking for technical soundness rather than for
legal language register. The warranty language slips through.

**Applicable to Redline**: A technical content pre-review that flags absolute-language
constructions is a named, addressable check. Redline surfaces the flag; the engineer
resolves it. Redline must never assert that a particular sentence does constitute a
warranty — that is a legal judgment outside the product scope.

This failure mode is grounded in standard PI policy terms (warranty exclusions) and in
Graeme's assessment of how AI-generated engineering prose registers. It has not been
confirmed as a live claims pattern in NZ engineering as of May 2026.

---

## Confirmed Facts vs Unconfirmed Hypotheses

### Confirmed

| Fact | Source |
|---|---|
| QA processes are a factor in CAS/Aon PI renewal underwriting | Christine Crook (Aon) + Craig Lewis (CAS) at webinar |
| QA has been in renewal docs for 6--8 years | Craig Lewis (CAS) at webinar |
| Original intent was to drive commercial discipline (scope, conditions, review) | Craig Lewis (CAS) at webinar |
| AI claims have not yet appeared on the engineering book | Gaynor Roberts (Aon Claims Manager) at webinar |
| AI claims are expected on the engineering book | Gaynor Roberts (Aon Claims Manager) at webinar |
| NZI is the actual underwriter; Aon is the broker | Craig Lewis (CAS) at webinar |
| CAS received member responses to April newsletter AI question | Craig Lewis (CAS) at webinar |
| The commercial QA layer and technical verification layer are structurally separate in NZ engineering practice | Graeme (Redline domain expert), cross-referenced with Risk Assessment in Engineering notebook and Geotechnical Report Workflows notebook |
| Standard NZ PI policies contain warranty exclusions | Graeme (Redline domain expert), cross-referenced with Risk Assessment in Engineering notebook |

### Not Confirmed

| Hypothesis | Status |
|---|---|
| NZI will grant premium relief for documented technical content QA | Unconfirmed — requires direct conversation with NZI; no path established |
| NZ PI market is bifurcating (affirmative AI policies vs exclusion clauses) | Unconfirmed — directional signals exist, no NZ underwriter has stated policy |
| PI policy warranty exclusions have been triggered by AI-generated engineering language in a live claim | Structural risk grounded in policy terms; no confirmed NZ case as of May 2026 |
| What NZ member firms said in response to the April AI newsletter question | Unknown until next Indemnity Matters publication |

---

## Indemnity Matters Access Strategy

The user currently accesses Indemnity Matters through their employer. Access ends
post-June 1 (departure date).

**Strategy**: Email Craig Lewis directly this week (before the CAS board meeting of
19 May 2026) as a founder introduction. Purpose: establish a personal or founder
relationship with CAS for ongoing Indemnity Matters access. Frame as a founder building
a quality layer for geotechnical reports, seeking to maintain connection with the
professional community after leaving a large firm.

**Rules for this outreach**:
- Do not reference the webinar recording or this transcript
- Do not mention that the user attended and recorded the Q&A
- The webinar is a legitimate public event — attendance can be mentioned as context
- Do not pitch Redline as a product in the introduction email
- Four sentences maximum

---

## Strategic Summary

The webinar produced a named, structurally validated product territory:

> The CAS/Aon renewal QA question has existed for six to eight years. It was designed
> to detect the absence of commercial QA. It cannot detect technical content
> verification failures — and that is exactly where AI-assisted report writing
> introduces new risk. No existing mechanism in NZ engineering practice bridges this
> gap. Redline does.

This argument is grounded in the insurer's own framework. It does not require Redline
to claim a current underwriting requirement — it only requires explaining why the
existing requirement, taken seriously, is insufficient for the AI era.

Full knowledge-store record: `docs/knowledge/geotechnical/contracts-and-risk/ai-signing-liability-and-qa-underwriting.md`
