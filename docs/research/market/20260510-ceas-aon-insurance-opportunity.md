# CEAS/Aon Insurance Opportunity -- Market Signal and Engagement Plan

**Date**: 2026-05-10
**Updated**: 2026-05-14 (post-webinar debrief)
**Source**: CEAS Indemnity Matters Issue 88 (April 2026); CEAS/Aon webinar (14 May 2026, recorded and transcribed)
**Status**: Webinar complete. Coffee meeting with Christine Crook: OFF (see below). Full intelligence: `docs/research/20260514-ceas-aon-webinar-findings.md`.

---

## What is CEAS?

CEAS (Consulting Engineers Advancement Society) is a New Zealand professional body
that partners with Aon, one of the world's largest insurance brokers, to provide
Professional Indemnity (PI) insurance to consulting engineering firms. *[Source:
newsletter directory, page 1.]* How many NZ engineering firms use the CEAS scheme is
not stated in the newsletter -- the claim that "most" small-to-mid firms are covered
through CEAS is an assumption, not a verified fact.

As the PI scheme administrator and broker, Aon handles renewals and processes claims
for CEAS member firms. *[Inference from their role -- not explicitly stated in the
newsletter.]*  This means they have visibility into what types of failures lead to
claims -- but whether they share that data openly in a coffee conversation is unknown.

## What happened

Two public-domain signals emerged in early 2026:

### 1. The CEAS Newsletter (Issue 88, April 2026)

The newsletter -- sent to every CEAS member firm in NZ -- contained a section called
"Professionals and AI" that cited two cautionary tales:

- **Deloitte** (accountants) had to partially refund a $440,000 report to the Australian
  government after admitting they used generative AI to produce it and it contained
  errors. A senator called it "a human intelligence problem."
- **A lawyer in Western Australia** was referred to the legal regulator after submitting
  AI-generated court documents containing citations to cases that do not exist. This was
  "one of more than 20 cases so far in Australia" with similar problems.

The newsletter then directly asked NZ consulting engineers:

> "How open are you with your clientele about your use of AI? And are your reports
> factually correct?"

This question comes from the engineers' own insurance provider. It is not a tech blog
or a LinkedIn opinion piece -- it is the people who underwrite their professional
liability asking whether their reports can be trusted.

### 2. The CEAS/Aon Webinar

CEAS/Aon is running a free lunchtime webinar covering four insurance types:
Professional Indemnity, Statutory Liability, Cyber Liability, and Management
Liability. The webinar focuses on typical risk scenarios for NZ engineering practices.

## Why this matters for Redline

### The insurance angle, explained simply

When an engineering firm produces a report with errors, and a client or third party
suffers a loss because of those errors, the firm's Professional Indemnity (PI) insurance
is what covers the legal costs and damages. PI insurance is not optional -- clients
require it in contracts, and firms cannot operate without it.

Every year, firms renew their PI cover. *[Standard insurance industry practice --
not stated explicitly in the newsletter.]* Whether renewals currently include
specific QA-related questions is unknown -- that is what Question 1 in the coffee
meeting is designed to find out.

The claim that "most small firms answer with 'our seniors review everything'" comes
from internal persona research (the Anna persona), not from the newsletter or any
primary research with insurers. It is a working assumption.

The newsletter signals that the insurance industry is beginning to pay attention to AI
usage in professional reports -- but "starting to notice" is our interpretation of the
newsletter's tone. What the newsletter actually does is reprint two cautionary tales
from other professions and ask engineers a question. It does not state that Aon has
changed its underwriting approach.

### What "insurance bifurcation" means -- and why it's still a hypothesis

"Bifurcation" means the insurance market splitting into two camps. Our current working
hypothesis (sourced from a competitive intelligence session in April 2026, not from
primary research with any insurer) is that this is beginning to happen in the AI space:

- **Camp A** -- Some insurers may offer "affirmative AI policies" that explicitly cover
  AI-related risks, but with conditions: the firm must demonstrate controls to catch
  AI errors.

- **Camp B** -- Other insurers may insert "absolute exclusion clauses": if an error was
  caused by AI, we do not cover it.

**This has not been confirmed with any NZ insurer.** It is a directional hypothesis
based on what is happening in insurance markets globally and in adjacent industries.
The CEAS newsletter reinforces the hypothesis -- the insurer is asking engineers about
AI usage and report accuracy -- but asking questions is not the same as having changed
policy terms.

**The coffee meeting with Aon exists specifically to test this hypothesis.** Question 4
("would a systematic QA layer change any underwriting conversation?") is designed to
find out whether bifurcation is real in the NZ engineering market or is still
theoretical.

If the thesis is correct, engineering firms that use AI without documented QA controls
face a meaningful insurance risk: higher premiums, exclusion from coverage, or having
to hide their AI usage and hope nobody finds out.

**This is what Redline is designed to do.** Redline's Pre-Review product checks
engineering reports against firm standards and domain requirements before senior review.
It creates a documented audit trail -- a record of what was checked, what was flagged,
and what the engineer did about it.

The positioning line we have been developing is: **"Redline gives you the audit trail
your insurer will ask for."** *[Internal strategy -- partially validated by webinar,
not yet confirmed by underwriter.]*

The webinar confirmed that QA processes are a factor in renewal underwriting and have
been for six to eight years. However, the renewal QA question was designed for the
*commercial* QA layer (scope discipline, contract conditions, senior sign-off) -- not
for the *technical content verification* layer where AI failure modes actually live.
The positioning line is directionally correct but must not be stated as a current
underwriting requirement. The correct frame: Redline creates the audit trail for the
technical content check the renewal QA question has never had -- and won't need to ask
for if it's already there. The coffee meeting with Aon is no longer the designed test
(see below); the conversation with NZI (the actual underwriter) is the test that
matters.

### Additional signals from the newsletter

- **PS4 Practice Advisory**: Building Consent Authorities raised concerns about altered
  Producer Statements (a type of professional certification document). *[Fact from
  newsletter, page 3.]* Graeme confirmed (advisory session, 2026-05-10) that this maps
  structurally to a common quality failure in geotechnical reports -- conclusions that
  exceed the scope of the investigation without proper qualifications. Whether Pre-Review
  would catch this type of failure is a product design question, not yet validated with
  users.

- **$60,000 Disputes Tribunal**: Since January 2026, the NZ Disputes Tribunal can
  consider claims up to $60,000 (doubled from $30,000). Engineers cannot be represented
  by a lawyer in the Tribunal, and decisions are based on "fairness" not contract terms.
  *[All facts from newsletter, page 4.]* The newsletter explicitly mentions the
  "blowback" risk: a $5,000 fee claim could trigger a counterclaim. *[Direct quote
  paraphrased from newsletter.]* The inference that this raises the urgency of report
  QA is ours, not the newsletter's.

- **1979 case study reprinted**: CEAS republished a 47-year-old case study about an
  engineer who reported favourably on a site based on three hand-auger holes and failed
  to qualify the limitations of the investigation. He was sued when unexpected fill was
  found elsewhere on the site. *[Fact from newsletter, page 5.]* The interpretation --
  that CEAS reprinted this because they see a connection to the AI quality problem --
  is ours. The newsletter does not explicitly make that link. CEAS may simply reprint
  old case studies routinely for educational value.

## The engagement plan

### Step 1: Webinar — COMPLETE (2026-05-14)

Attended. The webinar ran as planned — presentation from Christine Crook (Aon,
specialist in PI and liability for professional service firms), Q&A with Craig Lewis
(CAS Chair) and Gaynor Roberts (Aon Claims Manager). Approximately 100 attendees from
NZ civil engineering firms.

Key intelligence extracted — full record at
`docs/research/20260514-ceas-aon-webinar-findings.md`. Summary of findings
most relevant to the engagement plan:

**Q5 (QA as renewal factor)**: Confirmed by both Christine and Craig.
QA has been in CAS renewal documentation for 6--8 years, originally to drive discipline
around scope, conditions, and internal review. Firms are asked to "outline basic QA
measures." Craig acknowledged firms can "easy copy last year's answer" -- i.e., it
has become a checkbox, not an audit.

**Q6 (AI claims in engineering)**: Gaynor Roberts: "Not seeing it on the engineers
book -- but we're expecting to." Lawyers are the current primary target (fabricated
case law). Craig's framing: "Treat AI like a bright, very keen young graduate. The buck
stops with whoever's signing the producer statements."

**Q10 (favorable underwriting for AI QA processes)**: Craig: "Would have to be a
fairly good argument put forward." Christine: "AI is an emerging risk -- part of the
evolution of how underwriters approach risk management." Both pointed to NZI (the
actual underwriter, not Aon) as the decision-maker for any underwriting change.

**Key structural intelligence (Graeme-validated)**: The CAS renewal QA question
operates at the commercial layer (scope, conditions, contracts). The technical content
verification layer -- whether AI-generated report text was verified for hallucinations,
category errors, and warranty language drift -- is structurally invisible to the
renewal question. No existing NZ mechanism bridges this gap. This is the defensible
product territory.

### Step 2: Coffee meeting with Christine Crook -- OFF

Decision date: 2026-05-14.

Reason: Christine's role is at Aon, the broker -- not NZI, the underwriter.
Favorable underwriting treatment for AI QA (the core hypothesis to test) would be
decided by NZI, not Aon. Christine's answer to Q10 was a carefully hedged response
pointing to NZI. A coffee meeting at this stage would not produce the intelligence
needed to confirm or refute the bifurcation thesis -- Christine does not hold a firm
underwriting position and explicitly deferred to NZI on the core question.

The conversation that matters is with NZI. That conversation requires case data and
a validated risk-reduction argument, neither of which exists at the current stage.

### Step 3: Craig Lewis relationship -- active, post-June

Craig Lewis is the CAS Chair and the most strategically relevant contact from the
webinar. Two purposes:

1. **Indemnity Matters access**: The user loses institutional access to Indemnity
   Matters upon leaving their current employer (post-June 1). A personal or founder
   subscription via a relationship with Craig is the access strategy.

2. **Member survey intelligence**: Craig confirmed at the webinar that CAS received
   member responses to the April newsletter AI question ("How open are you with your
   clientele about your use of AI?") and is discussing at a board meeting the week of
   May 19. Findings will appear in a future Indemnity Matters. This is primary market
   research. Watch for the issue.

**Action**: Email Craig Lewis this week (before the board meeting) as a founder
introduction. Four sentences maximum. Do not mention the webinar recording. Keep it
clean: building a quality layer for geotechnical reports, losing institutional access
to Indemnity Matters after June 1, would like to discuss a personal subscription or
founding relationship with CAS.

### Five questions for the coffee meeting (priority order)

1. **"When a small firm renews PI cover, what QA-related questions does your team ask?
   What do firms typically answer?"**
   Why: Validates whether "we use a systematic QA layer" would actually matter during
   renewal, or whether underwriters only care about claims history.

2. **"You asked engineers in the April newsletter about AI usage and report accuracy.
   What kind of responses are you getting? Are firms disclosing AI usage?"**
   Why: Tells me whether firms are openly using AI or hiding it. If they are hiding it,
   the audit trail becomes even more valuable -- it gives firms something to show
   instead of something to hide.

3. **"Are you seeing claims where AI-generated content in engineering reports was a
   contributing factor? Or is that still theoretical?"**
   Why: Grounds the Deloitte and lawyer examples in engineering-specific reality. If the
   answer is "not yet in engineering," I know I am ahead of the wave but should not
   overstate the urgency.

4. **"If a firm could show a systematic, documented pre-review QA layer -- not replacing
   senior review, but catching routine stuff before it -- would that change any
   underwriting conversation?"**
   Why: This is the critical question. If yes, the insurance GTM angle is validated. If
   no, the insurance positioning is marketing copy, not a conversion driver.

5. **"What's the most common type of claim you see from small geotechnical firms?"**
   Why: Validates Graeme's assessment that scope-limitation failures (conclusions that
   exceed the scope of the investigation) are a dominant claim pattern.

### What NOT to say

- **Do not pitch Redline as a product.** No demo, no feature list, no "we are launching
  in June." I am gathering intelligence, not selling.
- **Do not reveal the insurance bifurcation thesis.** Do not say "we think insurers will
  start requiring audit trails." That telegraphs the GTM strategy.
- **Do not reveal the audit trail positioning line.** "Redline gives you the audit trail
  your insurer will ask for" is a GTM weapon. Do not hand it to the other side of the
  table.
- **Do not ask for endorsement or partnership.** Too early. Partnerships are diluting
  before product-market fit.
- **Do not name specific firms or specific engineers.** My credibility comes from
  the literature and 3.5 years of observation, not from naming former colleagues or
  clients.

### What success looks like

The meeting is successful if I walk away knowing:

1. Whether the insurance bifurcation is happening in NZ engineering specifically, or is
   still theoretical
2. At least one concrete data point about what Aon actually asks small firms during PI
   renewal
3. Whether "systematic QA layer" is a concept that means anything to an underwriter
4. A warm enough relationship that I could email six months later and say "I launched,
   here is what we built, can I show you?"

The meeting is a failure if I spend the time pitching, or if the Aon person leaves
thinking "that person was trying to sell me something."

### Longer-term possibility (not for this meeting)

If the insurance bifurcation thesis validates during the second half of 2026 -- if real
evidence emerges that insurers are differentiating based on AI QA practices -- then Aon
becomes a potential validator. The specific play: Aon confirms (publicly or privately)
that firms with systematic AI QA processes get more favourable underwriting treatment.
That confirmation would be the most powerful marketing asset Redline could have, worth
more than any paid campaign.

But that is a future conversation, conditional on Redline having a launched product and
demonstrable value. File it. Do not raise it over coffee.

## Content opportunity from the newsletter

John (marketing) identified a Big 5 "Problems" blog post opportunity based on the
newsletter:

- **Working title**: "Your Insurer Just Asked If Your AI Reports Are Factually Correct.
  What's Your Answer?"
- **Hook**: The CEAS/Aon question itself -- devastating because it cannot be dismissed
  as startup marketing
- **Structure**: Insurer's question --> Deloitte and lawyer cases --> why engineering
  may carry similar or higher risk *[hypothesis -- requires Graeme sign-off before
  publishing]* --> the pattern (generic AI, no domain checks) --> a constructive
  question (not a pitch)
- **Timing**: Publish by early June, before the CEAS Conference (22-23 July in
  Christchurch). *[Conference dates are fact from newsletter, page 1.]* Whether the
  conference actually amplifies the content is an assumption -- it depends on attendees
  seeing and engaging with the post.
- **Spin-offs**: A "Versus" piece (AI that writes vs AI that checks), a LinkedIn
  series (3 posts), a pricing anchor post

The blog post requires Graeme's sign-off on any domain-technical claims before
publishing.

## Webinar Debrief — 14 May 2026

**Status**: Complete. Video uploaded to NotebookLM (notebook `12dc5e06-4f77-4577-abca-758017e26675`).

**CRITICAL CONSTRAINT — No public use of webinar material.** The webinar host
explicitly stated at the opening: *"We do ask that there's no recordings or AI notetakers
in these webinars to allow for free conversation and discussion in the Q&A."* The video
exists for private internal intelligence only. No quotes, paraphrases, or references to
the webinar Q&A may appear in any public content (blog posts, LinkedIn, website).
The presentation content may only be referenced if independently corroborated from
public sources (e.g., the newsletter, public insurance documentation).

**Presenters identified:**
- **Christine Crook** (AON) — specialist in liability insurance and companion policies for
  professional service firms, 20+ years of involvement with CAS. Primary presenter.
- **Gaynor Roberts** (AON) — Claims Manager. Answered the AI claims question.
- **Craig Lewis** (Chair of CAS; Lewis Bradford Consulting Engineers) — Co-host for Q&A.
- **Michelle** — Host (likely Michelle Grant, LGE Consulting Ltd, based on attendee list).

**Format:** ~100 attendees, audience mics muted. Part 1: presentation by Christine Crook.
Part 2: live Q&A, questions read by Michelle from the online forum.

**Key Q&A findings relevant to Redline (internal use only):**

1. **QA IS a factor in PI underwriting (Q5 confirmed).** Christine Crook: *"Yes, it is
   definitely a factor in underwriting... we do try and extract some of those questions
   from you at renewal time as well."* Craig Lewis added it has been part of renewal
   documentation for 6-8 years. **This validates the bifurcation hypothesis directionally.**
   QA documentation is asked about at renewal — not just claims history.

2. **No AI claims in engineering yet, but expected (Q6).** Gaynor Roberts (Claims Manager):
   *"No, we're not [seeing AI claims], but we're expecting to... we haven't seen any AI
   claims [even across other schemes]. The most frequent claims would be against lawyers."*
   **Signal: Redline is ahead of the wave.** The urgency is real but not yet a claims
   reality in the engineering book.

3. **AI QA favorable treatment — deflected, not denied (Q10).** Craig Lewis: *"I think
   that would be something that NZI would need to consider... would have to be a fairly
   good argument put forward."* Christine Crook: *"AI is really an emerging risk... it's
   part of the evolution around risk management."* This is the public-stage non-answer
   Ron predicted. The coffee meeting remains the path to a candid answer.

4. **Craig Lewis is the coffee meeting target.** As CAS Chair and practising engineer
   (Lewis Bradford Consulting Engineers), he is both the Q&A co-host and a practitioner.
   The post-webinar email is to Christine Crook (AON) per the original plan, but Craig
   Lewis is a secondary warm contact who can validate the practitioner side of Q4.

5. **Newsletter follow-up signal.** Craig Lewis said: *"There was a follow-up [asking]
   about the responses coming in after the April newsletter. We have a board meeting
   next week, so we'll follow up."* The AI disclosure question from Issue 88 is
   generating member responses. This confirms it is live and unresolved in the community.

**Questions asked in the public webinar that were reserved for coffee:**
- Q5 (QA at renewal): Asked publicly. Received a confirming answer — bifurcation is real.
  Do not re-ask verbatim in the coffee meeting. Reframe as: *"How does that documentation
  actually look? Is 'we use seniors to review everything' still sufficient, or are
  underwriters looking for something more systematic?"*
- Q10 (AI QA favorable treatment): Asked publicly. Received the expected deflection.
  In the coffee meeting, reframe as: *"When a firm has a written QA checklist with a
  sign-off trail — not just 'seniors review everything' — does that show up anywhere
  in the renewal conversation, or is it essentially invisible to underwriting?"*

**Coffee meeting — revised approach:**
- Email hook: *"I was at your webinar last week — thank you for a genuinely informative
  session. I had a follow-up I didn't want to ask in the group setting."*
- Questions 1, 2, 3, and 5 from the original plan remain valid (not asked publicly).
- Questions 4 and 10 reframed as above.
- Do not contact before June 2 (company launch date).

**See full intelligence extract:** `docs/research/20260514-ceas-aon-webinar-intelligence-extract.md`

---

## Key dates

| Date | Event |
|---|---|
| 14 May 2026 | CEAS/Aon webinar — COMPLETE. Video in NotebookLM. See debrief above. |
| June 2 | Company officially launches (first day on Redline) |
| Early June | Email Christine Crook, request coffee meeting (post-webinar framing) |
| Early June | Publish Big 5 "Problems" blog post (before conference — newsletter sources only, no webinar material) |
| 22-23 July | CEAS Members' Conference, Te Pae Christchurch (evaluate attending as individual, not sponsor) |

## Provenance

- Newsletter analysis: Ron (strategy), 2026-05-10
- Domain validation (PS4/GBR mapping): Graeme (geotechnical), 2026-05-10
- Persona impact ($60k Tribunal): Mark (product), 2026-05-10
- Content brief: John (marketing), 2026-05-10
- Engagement plan: Ron (strategy), 2026-05-10
- Webinar debrief: Founder + Ron (strategy), 2026-05-14
