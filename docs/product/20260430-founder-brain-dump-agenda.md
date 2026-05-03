# Founder Brain Dump Agenda -- 30 April 2026

Source: [Redline NotebookLM](https://notebooklm.google.com/notebook/9ef1f417-4a48-416e-8881-49473ca82392)
-- 20260430 Redline Brain Dump Part 1 & Part 2

---

## 1. Marketing & Positioning

### 1.1 The "No-AI" Marketing Strategy [John, Ron]

The founder proposes never using the word "AI" on the website or in pitches.
The term has become an overloaded buzzword that triggers scepticism. Instead,
describe the product as a **quality layer for engineering documents created by
humans and machines**. "Machines" replaces "AI" deliberately.

**Discussion points:**

- Is this a genuine differentiator or does it hurt discoverability (SEO, search ads)?
- Draft alternative taglines that avoid "AI" but communicate the value.
- Does "machines" land with engineering CEOs, or is a different term needed?

> **RESOLVED (2026-04-30).** Adopted three-layer AI Language Policy: AI is banned
> from positioning layer (tagline, hero, pitch), permitted factually in explanatory
> layer, and used for discoverability in discovery layer (SEO, blog, FAQ). "Machines"
> dropped entirely -- wrong mental image for engineers. Updated in
> `docs/product/strategy/positioning.md` (AI Language Policy section).

### 1.2 CEO Priority Alignment [Ron]

Before building further, identify the **top three priorities** of a geotechnical
engineering firm's CEO. If the quality layer does not serve one of those three,
pivot fast. The "burrito analogy": if they don't want a burrito, no discount
will help.

**Discussion points:**

- What are our current hypotheses for the top-three CEO priorities?
- How do we validate them before investing further?

> **RESOLVED (2026-04-30).** Ron + Graeme aligned on CEO priority order:
> (1) Financial Performance, (2) Talent, (3) Liability. "Efficiency" retired as
> a selling term -- replaced with specific consequences (capacity, write-off
> reduction, leverage). Context-dependent by firm size (Tier 3: financial firmly #1;
> Tier 1: talent can overtake). Supporting tagline revised from "catches what a
> senior reviewer would catch" (confrontational to TD gatekeeper) to "handles the
> routine checks so your senior reviewers can focus on the judgment that matters."
> Updated in `docs/product/strategy/positioning.md` (CEO Priority Hierarchy +
> Positioning Language Sensitivity sections).

### 1.3 Discovery Research Prep [Founder, Ron]

Two sources proposed for pre-meeting research:

1. **Deep research** (Gemini / online) -- scan forums and public sources to compile
   what engineering CEOs care about.
2. **Ground Engineering magazine archive** (15 years) -- mine for implicit and
   explicit signals about CEO concerns. This is proprietary data, not available
   to competitors via deep research.

**Discussion points:**

- Who runs the deep research query? (Founder or agent?)
- Who mines Ground Engineering? (Linda to index, Graeme to interpret?)
- Deliverable: a short list of candidate CEO pain points to test in interviews.

### 1.4 Segment by Company Size [Ron, Mark]

Break the high-level problem statements (liability, efficiency) down by firm
size. Small/medium firms and large firms likely have different pain hierarchies.
Understanding the split clarifies what is in and out of scope.

**Discussion points:**

- Define the size buckets (headcount? revenue? project type?).
- Are we targeting SMEs, large firms, or both?

> **RESOLVED (2026-05-03).** Three tiers defined by headcount: Tier 3 (5–50 staff,
> small/niche firms), Tier 2 (50–500 staff, mid-size firms), Tier 1 (500+ staff,
> large infrastructure firms). Beachhead is Tier 3 — they cannot build, cannot
> afford bespoke, and have the highest pain-to-resource ratio. Tier 2 follows via
> bowling-pin expansion after Tier 3 dominance. Tier 1 is explicitly out of scope
> (they build their own tools). CEO priority hierarchy is context-dependent by tier:
> Tier 3 = Financial Performance > Liability > Talent; Tier 2 = Financial
> Performance > Talent > Liability; Tier 1 = Talent > Financial Performance >
> Liability. Full analysis in `docs/research/20260503-firm-size-segmentation.md`.
> Next step: Mark to frame tier-specific problem statements linked to the beachhead
> bet (Bet 1). KR2 discovery conversations should filter by firm tier and probe
> willingness-to-pay at the Tier 3 price point.

### 1.5 CEO Outreach Journey [John, Founder]

Build a structured LinkedIn outreach sequence: contact decision-makers, run
a discovery call, offer a one-week trial, collect feedback. "Get out of the
building."

**Discussion points:**

- Draft the outreach sequence and touchpoints.
- What does the one-week trial look like concretely?
- How do we track commitment and feedback loops?

---

## 2. Product Scope & Engineering Use Cases

### 2.1 "Before the Fact" vs. "After the Fact" [Mark, Graeme]

A civil engineer (BMS specialist) uses Gemini to check designs against
standards. This reveals two distinct use cases for the standards engine:

- **Before the fact** -- awareness of relevant standards while designing new
  infrastructure.
- **After the fact** -- verifying or expanding existing infrastructure (e.g. a
  dam, retaining wall) and checking compliance to suggest improvements or write
  a report.

**Discussion points:**

- Are these truly separate products or modes of the same engine?
- Which use case do we tackle first?
- What project-type taxonomy do we need (new build, expansion, demolition,
  maintenance)?

### 2.2 Practice of Engineering vs. Business of Engineering [Ron, Graeme]

Two layers of value:

- **Practice** -- physical equations, engineering theory, calculation checks.
- **Business** -- standards compliance for insurance, liability, and legal
  protection. A design can work physically but still expose the firm to liability
  if it doesn't comply with standards.

**Discussion points:**

- Should we position the quality layer squarely in the "business of engineering"
  lane?
- Does this framing resonate with CEOs?
- Where does it leave calculation-checking as a future feature?

---

## 3. AI Engineering & Agent System

### 3.1 LLM Data Extraction Sweet Spot [Founder]

From hands-on experience: extracting 25-30 parameters per query works reliably;
50+ causes timeouts, sparse results, or hallucinations. Clean data matters as
much for LLM extraction as for traditional ML/statistics.

**Discussion points:**

- Document the current extraction guidelines as a skill or codified rule.
- Where does this knowledge live? (rag-prompting skill? A new extraction skill?)

### 3.2 RAG Query Guidelines & Reflection [Founder, Mark]

The RAG system (NotebookLM) has limitations. Proposed improvements:

- Batch queries thematically; one document at a time.
- Diversify the sample of documents to test consistency.
- Create a "reflection page" where agents experiment with query hypotheses,
  track retrieval rate, and iteratively improve.

**Discussion points:**

- Update the `rag-prompting` skill with the batch/sample guidelines.
- Design the reflection mechanism -- manual first, then semi-automatic.

### 3.3 Handcrafted Skills via Onboarding [Founder, Harriet]

Generic prompt-based skills underperform for procedures and ceremonies.
A better approach: **onboard the agent step by step** down the happy path,
then have it document the process as a new skill. Test with a second document
to validate generalisability.

**Discussion points:**

- Formalise this as a meta-skill or an extension of `writing-skills`?
- Which procedures are next in line for this treatment?

### 3.4 Automatic Agent Reflection [Founder, Harriet]

After long or error-prone processes, agents should reflect on root causes and
update their own skills, instructions, or job descriptions. Start
semi-automatic (user triggers reflection), then move to fully automatic
(triggered after gates or long processes).

**Discussion points:**

- What does "semi-automatic reflection" look like concretely? A ceremony?
  A hook?
- How do we prevent drift (agents updating skills in harmful ways)?
- Prototype: pick one agent and one process for a reflection pilot.

### 3.5 Systematic Creativity Skill [Founder]

A book , "Inside the Box: A Proven System of Creativity for Breakthrough Results", lays out
Systematic Inventive Thinking (SIT,  innovation principles (subtraction, addition, multiplication, etc.) applied
to existing products. Examples: multi-blade razors (addition), scent-only
detergent (subtraction), blank-key keyboards (subtraction).

Proposal: extract principles and examples into a creativity skill for agents.
Probably most useful **after** a successful product exists, but could also be
applied to competitors' products.

**Discussion points:**

- Identify the book and extract the framework.
- Is this a priority now or a backlog item?
- If backlog, park it as a future-skill ticket.

---

## Suggested Discussion Order

| Priority | Item                                     | Key agents       | Time estimate |
| -------- | ---------------------------------------- | ---------------- | ------------- |
| 1        | 1.2 CEO Priority Alignment               | Ron              | 15 min        |
| 2        | 2.2 Practice vs. Business of Engineering | Ron, Graeme      | 15 min        |
| 3        | 2.1 Before vs. After the Fact            | Mark, Graeme     | 15 min        |
| 4        | 1.1 "No-AI" Marketing Strategy           | John, Ron        | 10 min        |
| 5        | 1.3 Discovery Research Prep              | Founder, Ron     | 10 min        |
| 6        | 1.4 Segment by Company Size              | Ron, Mark        | 10 min        |
| 7        | 1.5 CEO Outreach Journey                 | John             | 10 min        |
| 8        | 3.1-3.2 Extraction & RAG Guidelines      | Founder          | 10 min        |
| 9        | 3.3-3.4 Onboarding & Reflection          | Founder, Harriet | 10 min        |
| 10       | 3.5 Creativity Skill                     | Founder          | 5 min         |
