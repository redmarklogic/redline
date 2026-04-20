# Professional Assessment: AI-Drafted GBR Liability Exposure in DSC Disputes

**Sub-domain**: contracts-and-risk
**Last verified**: 2026-04-20
**Confidence**: cross-referenced
**Sources**: Geotechnical Baseline Reports (GBR) notebook, Risk Assessment in Engineering notebook

## Summary

This assessment identifies the three most dangerous content errors an AI could introduce
into a Geotechnical Baseline Report (GBR), explains why each is catastrophic in a Differing
Site Conditions (DSC) dispute, and defines what a defensible human-review audit trail must
capture. A GBR is a binding contract document that establishes a single, assumed set of
subsurface conditions (the "baseline") to allocate financial risk between the project owner
and the contractor. A DSC claim allows a contractor to seek additional time and money when
actual ground conditions are materially worse than the stated baseline. The signing
engineer's professional indemnity insurance only covers negligence, not guarantees or
warranties — so AI-generated language that implies certainty can void coverage entirely.

---

## 1. The Three Most Dangerous AI-Introduced Errors in a GBR

### 1.1 Ambiguous Baseline Language

**What the error looks like.** AI language models are trained to produce hedged, conversational
text. They naturally generate qualifiers — words like "may," "can," "might," "up to," "could,"
"should," "some," and "few." In a GBR, every one of these words is fatal to enforceability
[Source: GBR notebook, citations 29, 30].

A GBR baseline must be a single, measurable, enforceable threshold. It is the contractual
line that separates "owner pays" from "contractor pays." If the baseline is ambiguous, no
Dispute Review Board (DRB) or court can determine whether the actual ground exceeded it.

**Concrete example of the danger.**

- AI phrasing (indefensible): *"Some shear zones may yield up to 250 gpm initial inflow,
  but the flows should dissipate."* [Source: GBR notebook, citations 25, 31]
- Engineer phrasing (defensible): *"Three shear zones are anticipated to each yield
  250 gpm... each is anticipated to yield no more than 60 gpm after one month."*
  [Source: GBR notebook, citations 25, 31]

**Why this is dangerous in a DSC dispute.** If the owner's GBR uses the first phrasing,
the contractor will argue — successfully — that "some" and "may" and "should" are not
enforceable thresholds. The owner will lose the DSC dispute because the baseline is too
ambiguous to enforce a contractual boundary [Source: GBR notebook, citations 29, 30].
The AI has effectively gifted the contractor an uncontestable claim.

This is the single most AI-specific risk. An AI generating "plausible text" rather than
definitive, measurable boundary conditions exposes the design engineer to massive
professional liability [Source: GBR notebook, citations 32, 33]. A GBR is a legal
risk-allocation instrument that happens to look like an engineering report. The AI does
not understand this distinction.

### 1.2 Conflating Ground Properties with Ground Behaviour

**What the error looks like.** An AI will naturally describe the ground in terms of its
intrinsic physical properties — soil type, grain size, strength values — because that is
what the Geotechnical Data Report (GDR) contains. However, a GBR must baseline how the
ground will behave when excavated, not merely what it is [Source: GBR notebook, citations
20, 21].

Ground behaviour is the engineering judgment dimension: how will this material react when
exposed to air, water, vibration, or the contractor's specific equipment? The DSC threshold
is often crossed not because the soil type changed, but because the behaviour was
unexpectedly adverse [Source: GBR notebook, citation 22].

**Concrete example of the danger.** On one major tunnel project, the GBR specifically warned
that shale would appear massive and durable but would "slake" (deteriorate and crumble over
time when exposed to air or water). When the contractor chose a cheaper support method and
the tunnel walls began to collapse, the owner successfully defeated the DSC claim and forced
the contractor to bear the cost — entirely because the behavioural baseline had been written
with engineering judgment, not merely data [Source: GBR notebook, citation 23].

An AI relying only on rock strength data would have missed the time-dependent behavioural
risk entirely [Source: GBR notebook, citation 23].

**Why this is dangerous in a DSC dispute.** If the AI baselines a clay or rock solely by its
laboratory-measured strength but fails to baseline its field behaviour (slaking, squeezing,
swelling, running, flowing), the contractor will encounter adverse behaviour that is
technically consistent with the stated soil type but commercially devastating. They will
claim — often successfully — that the behaviour constitutes a differing site condition
because the GBR did not warn them.

This error is particularly insidious because an AI will produce a document that looks
technically correct — all the soil properties are accurately stated — but is professionally
negligent because the engineering judgment about behaviour is absent.

### 1.3 Copying Raw Data Instead of Constructability Baselines

**What the error looks like.** An AI will default to copying or summarising raw data from the
GDR — permeability values (how fast water moves through soil or rock), strength test results,
or borehole descriptions — and present them as baselines. However, raw data is not a
construction baseline [Source: GBR notebook, citations 15, 16].

A defensible GBR translates raw data into measurable construction parameters: inflow rates
in gallons or litres per minute at specified locations [Source: GBR notebook, citations 17,
18], the anticipated number, size, and strength of boulders [Source: GBR notebook, citations
11, 12], or percentage distributions of rock strength rather than broad ranges [Source: GBR
notebook, citations 25, 26].

**Concrete example of the danger: groundwater.** On the Dearborn CSO Tunnel project, the GBR
failed to properly baseline vertical shear zones and the resulting groundwater inflows. The
actual inflows exceeded pumping capacity. The shaft grouting required to stop the water
exceeded the entire contract's grout quantity before the shaft even reached tunnel depth. The
project was deemed a DSC and ultimately terminated [Source: GBR notebook, citation 19].

**Concrete example of the danger: rock strength.** On the Cowles Mountain Water Tunnel, the
GBR underestimated the percentage of very strong rock. The resulting tool wear and slow
advance rates led to a successful DSC claim due to massive schedule delays [Source: GBR
notebook, citation 28]. If an AI had baselined rock strength as a broad range (e.g., "6,000
to 25,000 psi") without specifying a definitive contractual average or percentage
distribution, it would have created a legal "battle zone" [Source: GBR notebook, citations
25, 26] — the contractor bids on the lowest strength and claims a DSC when they encounter
the harder rock [Source: GBR notebook, citation 27].

**Why this is dangerous in a DSC dispute.** The contractor's claim will succeed because the
baseline was expressed in terms the contractor cannot measure or act upon during
construction. Permeability is a laboratory property; inflow rate is what the contractor
experiences at the face. If the GBR states permeability instead of inflow rate, the
contractor has no contractual threshold to bid against, and no measurable line to defend
in a dispute.

---

## 2. Defensible Human-Review Audit Trail for AI-Drafted GBRs

If AI is used to draft any part of a GBR, the human-review record must demonstrate five
things to survive a DSC claim. Each of these is grounded in industry guidance literature.

### 2.1 Documented Rationale for Every Deviation from the GDR

The GBR must explain how each baseline relates to the factual data in the GDR [Source: GBR
notebook, citations 10, 11]. Where baselines deviate from the GDR dataset — as they
frequently should, because a GBR is a risk-allocation tool, not a data summary — the
reasons for those deviations must be documented [Source: GBR notebook, citations 12, 13].

Where baselines deviate from the factual data at the request of one of the contracting
parties, it is also recommended that a record is maintained to allow transparency should a
claim be raised [Source: GBR notebook, citation 16].

**What to record:** For each baseline parameter, the audit trail must document: (a) what the
GDR data showed, (b) what the baseline was set at, (c) why the engineer chose that value,
and (d) which party requested or accepted the deviation.

### 2.2 Independent "Fresh Eyes" Cross-Reference Review

The ultimate quality assurance check is engaging the "fresh eyes" of independent reviewers
in a page-turning process that incorporates the general conditions, technical
specifications, drawings, GDR, and GBR [Source: GBR notebook, citations 17, 18].

This cross-referencing review must occur immediately prior to issuing the bid documents
[Source: GBR notebook, citations 17, 18]. Because GBR statements are subject to "intense
scrutiny, interpretation, and possible misinterpretation in the evaluation of potential DSC
claims," this independent compatibility check must be formally recorded [Source: GBR
notebook, citations 17, 18].

**What to record:** The identity of the independent reviewers, the date of the page-turning
review, which contract documents were cross-referenced, and any contradictions identified
and resolved.

### 2.3 Documented Reviewer Competency

The literature strictly defines who is qualified to review a GBR. Owners must retain
reviewers based on "demonstrated qualifications and experience in the preparation and review
of such documents" [Source: GBR notebook, citation 19].

Critically, it is strongly recommended that owners retain individuals with substantial
experience not only in local geology but specifically in "the use of GBRs in previous
project administration and dispute adjudication" [Source: GBR notebook, citations 20, 21,
22].

**What to record:** The qualifications and GBR-specific experience of every reviewer who
signed off on the document. Junior engineers or non-specialists cannot be the review gate
for an AI-drafted GBR.

### 2.4 Multi-Disciplinary Review Cycles

A GBR is a legal and commercial document, not just a technical one [Source: GBR notebook,
citation 23]. GBR drafts must be subject to cycles of review by the writers, the employer's
legal staff, and risk managers, who will focus on making statements legally sound and not
vulnerable to challenge [Source: GBR notebook, citation 24].

**What to record:** That construction specialists reviewed the means-and-methods baselines,
designers reviewed for contract compatibility, and legal/commercial teams reviewed for risk
allocation [Source: GBR notebook, citations 25, 26]. Each review cycle must be separately
documented with findings and resolutions.

### 2.5 Owner's Informed Consent on Risk Allocation

The audit trail must show that meetings were conducted with the owner to discuss the
consequences of where the baselines are set [Source: GBR notebook, citation 27]. Owners
should participate in and contribute to the setting of the baselines and should understand
the consequences of the levels at which the baselines are set [Source: GBR notebook,
citations 28, 29].

The design team must document that they explained to the owner the "potential consequences
of establishing conservative baselines (i.e., baselines set higher than the data and
reasonableness would suggest)" [Source: GBR notebook, citations 27, 30]. The owner's active,
informed acceptance of the resulting risk profile and bid price implications must be recorded
[Source: GBR notebook, citations 30, 31].

**What to record:** Meeting minutes showing the owner was briefed on baseline choices, their
financial implications, and their informed acceptance of the resulting risk allocation.

---

## 3. Additional Professional Observations on AI-Drafted High-Stakes Documents

### 3.1 The PLI Coverage Gap

Professional Liability Insurance (PLI) — also known as Errors and Omissions (E&O) insurance
— covers claims based on negligence, not breach of warranty [Source: Risk Assessment
notebook, citations 5, 6]. PLI policies explicitly exclude coverage for express warranties,
guarantees, and penalty clauses [Source: Risk Assessment notebook, citation 7].

If an AI generates language that implies a 100% success rate or guarantees a specific
outcome, the engineer effectively offers an uninsured warranty, voiding their PLI coverage
for those specific claims [Source: Risk Assessment notebook, citations 2, 5].

In AI-generated text, the risk of inadvertently inserting "taboo" absolute words — "ensure,"
"guarantee," "certify," "all," or "safe" — is significant [Source: Risk Assessment notebook,
citations 2, 3, 4]. These words elevate the engineer's legal standard of care from
negligence (doing what a reasonable professional would do under similar circumstances) to
strict liability (guaranteeing a specific result) [Source: Risk Assessment notebook,
citation 2].

This is not a hypothetical risk. AI language models are optimised to sound confident and
authoritative. A model drafting a GBR clause will naturally tend toward absolute statements
that void the signing engineer's insurance protection.

### 3.2 The Signing Engineer's Personal Accountability

Under the professional Code of Ethics, an engineer must not sign or seal plans,
specifications, or reports unless the documents were actually prepared by them or prepared
under their direct supervision [Source: Risk Assessment notebook, citation 8]. Engineers
must accept personal responsibility for their professional acts and cannot use a corporation
or non-engineer entity as a "cloak" for unethical acts [Source: Risk Assessment notebook,
citation 9].

An AI tool is a non-engineer entity. If the signing CPEng cannot demonstrate that they
exercised direct supervision over every material statement in the GBR, they are exposed to
both professional misconduct proceedings and uninsured personal liability.

### 3.3 The "Distance from Fundamental Reasoning" Problem

The research context notes that insurers warn AI "distances staff from fundamental
reasoning." From my 25 years of experience, this is the deepest risk. A GBR is not a
document that can be produced by assembling correct facts. It requires the engineer to
inhabit a constructability mindset — to visualise what will happen when a specific piece
of equipment meets a specific stratum under specific groundwater conditions, and to set
the contractual boundary at the point where the risk shifts fairly between the parties.

An AI cannot do this. It has no experience of ground conditions. It has never stood at a
tunnel face wondering whether the clay is going to squeeze or run. It cannot assess whether
the owner should carry the risk of 200 gpm inflow or 500 gpm inflow, because it does not
understand the financial consequences of that choice on contractor pricing.

The danger is that an AI draft will look professional and comprehensive — all the right
headings, all the right data — while being professionally negligent because the engineering
judgment that converts data into defensible baselines is entirely absent.

### 3.4 Template and Boilerplate Risks

The literature warns against over-reliance on template disclaimers or boilerplate text
[Source: Risk Assessment notebook, citation 1]. Limitations and assumptions must be written
specifically for the context of the actual services provided, not copied from a standard
template [Source: Risk Assessment notebook, citation 1].

An AI trained on previous GBRs will naturally reproduce template language. This creates a
false sense of protection — the disclaimers look correct but may not match the actual
scope, site conditions, or contractual context of the project at hand.

---

## Standards Referenced

| Standard / Guideline | Relevance |
|---|---|
| ASCE GBR Guidelines | GBR preparation, baseline setting, DSC framework |
| CIRIA C807 | UK/international GBR guidance, risk allocation |
| FIDIC Emerald Book | Contractual framework for underground works |
| NZTS Guide | NZ-specific GBR/GIR guidance |
| Engineering NZ Code of Ethics | CPEng obligations, signing requirements |

## Open Questions

1. **Insurer position on AI-assisted GBRs specifically.** The notebooks confirm the general
   PLI exclusion for warranties and guarantees, and the competitive intelligence notes insurer
   bifurcation on AI coverage. But no notebook source provides specific policy language from
   NZ/AU professional indemnity insurers on AI-drafted contract documents. This is a gap that
   should be filled by direct engagement with the firm's PI broker.

2. **Regulatory body guidance on AI in CPEng work.** The notebooks confirm that Engineering NZ
   prohibits relying solely on AI for safety assessments or code compliance. But the specific
   regulatory guidance on AI use in non-safety contractual documents (like GBRs) is not yet
   documented. This may require a direct inquiry to Engineering NZ.

3. **Case law on AI-generated contract documents.** No notebook source contains case law
   specifically involving AI-generated engineering contract documents. As of April 2026, this
   body of law likely does not yet exist, but it will emerge. The first DSC dispute involving
   an AI-drafted GBR will set significant precedent.

4. **Hazardous materials and contamination baselines.** The GBR notebook documents cases where
   hydrogen sulfide gas was missed in GBRs, leading to project termination [Source: GBR
   notebook, citation 23]. An AI's ability to detect trace chemical anomalies in GDR data is
   an additional risk area not fully explored in this assessment.

## Glossary

| Term | Definition |
|---|---|
| GBR (Geotechnical Baseline Report) | A binding contract document that establishes a single, assumed set of subsurface conditions to allocate financial risk between the project owner and the contractor. |
| DSC (Differing Site Conditions) | A contractual clause allowing a contractor to claim additional time and money if actual ground conditions are materially worse than the GBR baseline. |
| GDR (Geotechnical Data Report) | A separate document containing purely factual, uninterpreted raw site investigation data such as boring logs and laboratory test results. |
| CPEng (Chartered Professional Engineer) | A professional registration under Engineering NZ indicating competence to practise independently. The CPEng retains personal liability for documents they sign. |
| PLI (Professional Liability Insurance) | Also called Errors and Omissions (E&O) insurance. Covers claims based on negligence but excludes express warranties, guarantees, and penalty clauses. |
| DRB (Dispute Review Board) | An independent panel that adjudicates disputes between owner and contractor during construction. |
| UCS (Unconfined Compressive Strength) | A laboratory measure of rock strength, expressed in psi or MPa. |
| TBM (Tunnel Boring Machine) | Large machine used to excavate tunnels. Performance and tool wear are directly affected by ground conditions. |
| Slaking | Deterioration and crumbling of rock when exposed to air or water over time — a behavioural property that laboratory strength tests do not capture. |
| Strict liability | A legal standard where the engineer guarantees a specific outcome, as opposed to negligence (doing what a reasonable professional would do). PLI does not cover strict liability. |

## Sources Consulted

| Notebook | Queries asked | Key citations returned |
|---|---|---|
| Geotechnical Baseline Reports (GBR) | 2 | ASCE GBR Guidelines, CIRIA C807, FIDIC Emerald Book, NZTS Guide; case studies from Dearborn CSO Tunnel, Cowles Mountain Water Tunnel, Western Regional Conveyance Tunnel, Detroit River Outfall Tunnel |
| Risk Assessment in Engineering | 1 | Professional Code of Ethics (signing requirements), PLI coverage exclusions, template/boilerplate risks, QA/QC frameworks |
