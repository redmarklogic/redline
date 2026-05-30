# Qmd Narrative Design — Detailed Reference

## Procedure

Apply this skill whenever generating or reviewing a Quarto `.qmd` document for an external audience — a client presentation (`revealjs`), a technical report (`html`/`pdf`/`typst`), or a client memo. Start by asking clarifying questions, then structure content using the Hook-Problem-Insight-Proof-Action arc with audience-aware density.

**Related skills:**

- Pre-flight data quality: `.agents/skills/eda-interpreting-data/SKILL.md`
- Plot construction: `.agents/skills/eda-visual-design/SKILL.md`
- Table rendering: `.agents/skills/qmd-tables/SKILL.md`
- Mermaid diagrams: `.agents/skills/mermaid-diagrams/SKILL.md`

---

### 2.1 Story Arc — Hook → Problem → Insight → Proof → Action

Every document follows this five-beat structure. The beats may map to slides,
sections, or paragraphs depending on mode, but the sequence is fixed.

| Beat        | Purpose                        | What to generate                                                                    |
| ----------- | ------------------------------ | ----------------------------------------------------------------------------------- |
| **Hook**    | Capture attention immediately  | An opening question, surprising fact, or consequence that matters to*this* audience |
| **Problem** | Establish the gap or challenge | State what is unknown, broken, or at risk — in terms the audience recognises        |
| **Insight** | Deliver the key message        | A single, direct claim. This is the answer to question 2 above.                     |
| **Proof**   | Substantiate the insight       | Data, figures, models — the minimum evidence needed to make the claim credible      |
| **Action**  | Close with a directive         | What the audience should do, decide, or read next                                   |

The Hook must earn the audience's attention in the first 30 seconds of a talk or
the first paragraph of a report. Do not open with project background, scope
statements, or methodology. Open with consequence.

### 2.2 One Key Message — Enforce It

Identify the single key message (from clarifying question 2) before generating
any content. Every slide, section, and figure must either advance that message or
be cut. If two elements make the same point, keep the more precise one and remove
the other.

Do not end a document with no obvious conclusion. The Action beat is mandatory.

### 2.3 Know the Audience — Match Depth to Level

| Audience level           | What to include                                                                          | What to omit                                          |
| ------------------------ | ---------------------------------------------------------------------------------------- | ----------------------------------------------------- |
| **General**              | Define every technical term on first use. Use analogies. Show consequences, not methods. | Methodology detail, model equations, parameter tables |
| **Technically informed** | Define domain-specific acronyms. Show methods briefly. Key results in full.              | Step-by-step derivations, raw data tables             |
| **Highly specialised**   | Assume shared vocabulary. Show methods and uncertainty fully.                            | Introductory analogies, definition slides             |

Never use jargon without definition for a general audience. Never over-explain to
a specialised audience — it implies the reader cannot follow without hand-holding.

### 2.4 Writing Quality: Simplicity and Precision

Apply these rules to every sentence generated — in slide bullets, speaker notes,
report prose, and captions.

- **Strip each sentence to its cleanest form.** Remove every word that does not
  change the meaning. "During the course of the analysis it was observed that…"
  → "Analysis showed…"
- **Use active voice.** "The committee decided" not "The decision was made by the
  committee."
- **Use strong, specific verbs and nouns.** "Analysed" not "performed an analysis
  of." "Concentration exceeded 50 mg/L" not "concentration was high."
- **Eliminate clutter.** Cut: qualifiers without content ("very", "quite", "somewhat"),
  tautologies ("past history", "future plans"), filler transitions ("It should be
  noted that", "In order to").
- **Do not show off.** Complex vocabulary and long sentences do not demonstrate
  expertise — they obstruct the message. Clarity signals confidence.
- **Expand every acronym on first use.** Write "Greenhouse Gas (GHG)" on first
  mention, then "GHG" thereafter. Do not assume shared knowledge of Three-Letter
  Acronyms (TLAs). Avoid management speak and corporate jargon entirely.

### 2.5 Paragraph Structure (Reports)

- Every paragraph explores one idea. Start a new paragraph when introducing a new point.
- Begin each paragraph with a topic sentence that states the paragraph's subject.
  The remaining sentences elaborate, support, or qualify that subject.
- Do not mix argument, evidence, and conclusion within the same paragraph. If a
  paragraph contains all three, split it into two.

### 2.6 Mechanical Grammar Rules

Apply consistently in all generated prose:

- Use the **serial (Oxford) comma** in all lists of three or more: "methane,
  nitrous oxide, and carbon dioxide."
- Do not join independent clauses with a comma alone (comma splice). Use a
  semicolon, a full stop, or a comma with a coordinating conjunction.
- Ensure opening participial phrases refer to the grammatical subject of the
  sentence. "Walking down the hall, I heard the alarm" — not "Walking down the
  hall, the alarm sounded."

### 2.7 Use Computed Values — Never Hard-code Numbers in Narrative

Every statistic cited in prose (median, total, percentage, sample size) must be
read from a computed variable in the same document, not typed manually. Hard-coded
numbers become silently stale when data changes.

### 2.8 Unicode Symbols in QMD Prose — Use the Character Directly

In QMD prose, always write the actual Unicode character. Never write `\uXXXX` —
these are Python string escapes, not Markdown; Pandoc renders them verbatim
(e.g. `\u2014` appears as `\u2014`, not `—`). Inside `print()` calls in code
cells, `\uXXXX` escapes are correct and preferred.

| Symbol            | Wrong in prose | Right in prose |
| ----------------- | -------------- | -------------- |
| Em dash —         | `\u2014`       | `—`            |
| En dash –         | `\u2013`       | `–`            |
| Superscript ²     | `\u00b2`       | `²`            |
| Subscript ₂ (CO₂) | `\u2082`       | `₂`            |
| Degree °          | `\u00b0`       | `°`            |
| Multiplication ×  | `\u00d7`       | `×`            |
| Micro µ           | `\u00b5`       | `µ`            |

---

### 3.1 Structure

- Generate an **agenda/outline slide** at the start and a **summary slide** at
  the end. The summary restates the key message and the action in two to four
  bullet points. Do not introduce new content.
- Target **one slide per 1.5–2 minutes** of talk time. For a 20-minute talk,
  aim for up to 10 slides. For a 30-minute talk, up to 15 slides.
- If a slide cannot be explained in under 2 minutes, split it.

### 3.2 Slide Composition

- **Maximum ~5 short phrases per slide face.** Use fragments, not full sentences.
  The presenter speaks the full thought; the slide shows the scaffold.
- **Prefer a figure or diagram over a bullet list.** When the point can be shown
  visually, generate a figure placeholder and one short label — not a bulleted
  description of what the figure would show.
- **One message per slide.** The slide title states the conclusion, not the topic.
  "Methane flux peaks in summer" not "Seasonal methane flux."
- **Put detail in speaker notes, not on the slide face.** Any content that requires
  more than a phrase belongs in `::: {.notes}`.
- **Formatting constraints.** Do not use underlines or ALL CAPS on slide faces.
  Use bold and italics sparingly — at most one emphasised phrase per slide. Do not
  rely on colour alone to convey meaning.

### 3.3 Speaker Notes

Speaker notes must contain the full spoken version of the slide. Generate them
for every content slide using this structure:

1. **Transition sentence** — connects this slide to the previous one.
2. **Main talking points** — in full sentences, matching the slide bullets but
   expanded with numbers, context, and nuance.
3. **Cue for the next slide** — a one-sentence bridge.

Never leave a speaker notes block empty on a content slide.

### 3.4 Incremental Builds (Fragments)

Use `::: {.fragment}` to introduce content step by step when:

- A list has more than three items.
- A diagram has multiple stages introduced sequentially.
- A comparison table is being built up element by element.

Do not use fragments decoratively. Each fragment reveal must correspond to a
spoken turn — something the presenter actively discusses before advancing.

### 3.5 Slide Anti-Patterns

| Anti-pattern                           | Why it fails                         | Fix                                                                                     |
| -------------------------------------- | ------------------------------------ | --------------------------------------------------------------------------------------- |
| Full sentences on the slide face       | Audience reads instead of listening  | Replace with short phrases; move full prose to speaker notes                            |
| Code blocks or equations on slide face | Audience cannot absorb them at pace  | Simplify to a diagram or a verbal description; reference the full version in the report |
| Six or more bullet points              | Cognitive overload                   | Split the slide                                                                         |
| Unvalidated last-minute results        | Risk of presenting wrong numbers     | Only embed results from committed, reviewed analysis                                    |
| Bullet list where a figure would work  | Slower to read, harder to remember   | Generate a figure placeholder                                                           |
| Decorative animations                  | Visual noise                         | Only animate when each reveal is a distinct spoken beat                                 |
| Unexpanded acronyms                    | Audience loses the thread            | Expand every acronym on first use; avoid TLAs and jargon                                |
| Underlines or ALL CAPS                 | Clashes with brand; looks aggressive | Use bold sparingly; no underlines or ALL CAPS                                           |

### 3.6 Presentation Contexts

Choose the structural template that matches the presentation type (clarifying
question 4). The shared principles (Rules 2.1–2.7) and slide composition rules
(Rules 3.1–3.5) apply regardless of context.

#### Client Progress Update

Adapt the HPIPA arc for status-driven communication:

| Beat        | Adaptation                                                         |
| ----------- | ------------------------------------------------------------------ |
| **Hook**    | Why this update matters now — a deadline, decision, or risk        |
| **Problem** | Current blockers, risks, or scope changes requiring attention      |
| **Insight** | Progress summary against milestones                                |
| **Proof**   | Deliverables completed, data collected, metrics                    |
| **Action**  | Decisions needed from the client, next steps with owners and dates |

End with a clear **next steps** slide listing actions, owners, and due dates.

#### Conference / Technical

Use the traditional academic structure:

1. **Purpose** — problem statement and why it matters
2. **Outline** — brief agenda (one slide)
3. **Background** — prior work and context (keep brief)
4. **Methods** — approach, models, data sources
5. **Results / Analysis** — key findings with figures
6. **Discussion / Summary** — interpretation, limitations, implications
7. **Future Work** — open questions and next steps

For conference talks, bias toward figures over text. Audiences retain visuals
better than bullet points in technical settings.

#### General Briefing (Default)

Use the standard HPIPA arc (Rule 2.1) without modification.

---

### 4.1 Structure

- Use the Hook → Problem → Insight → Proof → Action arc at the **section level**.
  The executive summary or abstract delivers all five beats in compressed form.
- Every section begins with a **topic sentence** that states what the section
  establishes. Do not open a section with data or methodology before stating what
  question is being answered.
- Long reports must include an **executive summary** (one page maximum) that
  contains: the key message, the top two or three supporting findings, and the
  recommended action. A reader who reads only the executive summary must understand
  what to do.

### 4.2 Progressive Disclosure

- State conclusions before evidence. "Methane flux was highest in summer (Figure 3)."
  Not "Figure 3 shows the seasonal pattern. From this it can be seen that methane flux
  was highest in summer."
- Place **detailed methodology, derivations, and raw data tables in an appendix**.
  Reference them from the main body but do not interrupt the narrative with them.
- Use **callout boxes** (`::: {.callout-note}`, `::: {.callout-important}`) to
  surface actionable findings inline without breaking the flow of the argument.
- If a sequence must render as a numbered list, write it as a real Markdown list with
  one item per line; do not compress it into a single paragraph like "1. ... 2. ...".
- Apply the same rule to unordered (bullet) lists. Never compress a bullet list into
  a single paragraph like "- Item A - Item B - Item C". Each bullet item must be on
  its own line, preceded by a `-` or `*` without any inline `-` separators between items.

### 4.3 Figures and Tables in Reports

- Every figure and table must be preceded by a sentence that states what it shows
  and why it matters — before the reader's eye reaches the visual.
- Every figure and table must be followed by a sentence that states what the result
  means for the key message.
- Do not let a figure or table stand alone between two unrelated paragraphs.

### 4.4 Tone

- Use the same register throughout. Do not shift from objective technical reporting
  into advocacy, personal narrative, or hedged speculation within the same section.
- Write for the audience level established in the clarifying questions. Do not
  adjust register mid-document based on topic difficulty.
- Match the key message's evidence level. A strong claim requires quantified proof.
  A hedged claim ("suggests", "indicates") requires at least directional evidence.
  Do not claim more than the data supports.

---

### Before Generating

- [ ] Audience level established — general, informed, or specialised (Rule 1)
- [ ] Single key message identified in one sentence (Rule 2.2)
- [ ] Format and length constraint known (Rule 1)
- [ ] Presentation context identified — progress update, conference, or general (Rule 1, presentations only)

### Story Arc

- [ ] Hook opens with consequence, not background (Rule 2.1)
- [ ] Problem stated in terms the audience recognises (Rule 2.1)
- [ ] Insight is a single, direct claim (Rule 2.1)
- [ ] Proof is the minimum evidence needed to make the claim credible (Rule 2.1)
- [ ] Action beat present — audience knows what to do next (Rule 2.1)

### Writing Quality

- [ ] Every sentence stripped to its cleanest form (Rule 2.4)
- [ ] Active voice throughout (Rule 2.4)
- [ ] No clutter: qualifiers without content removed (Rule 2.4)
- [ ] Serial comma applied in all three-or-more lists (Rule 2.6)
- [ ] No comma splices (Rule 2.6)
- [ ] All cited statistics are computed values, not hard-coded (Rule 2.7)
- [ ] All acronyms expanded on first use (Rule 2.4)

### Presentation Only

- [ ] Slide count matches talk duration at 1.5–2 min per slide (Rule 3.1)
- [ ] Agenda slide and summary slide present (Rule 3.1)
- [ ] Maximum ~5 short phrases per slide face (Rule 3.2)
- [ ] Slide title states the conclusion, not the topic (Rule 3.2)
- [ ] Speaker notes present for every content slide (Rule 3.3)
- [ ] Fragments used only for sequentially introduced content (Rule 3.4)
- [ ] No full sentences, code blocks, or equations on the slide face (Rule 3.5)
- [ ] Matching structure template applied for presentation context (Rule 3.6)
- [ ] No underlines or ALL CAPS on slide faces (Rule 3.2)
- [ ] Brand palette applied where colour is used (Addendum A)

### Report Only

- [ ] Executive summary delivers all five arc beats in one page (Rule 4.1)
- [ ] Each section opens with a topic sentence stating the question it answers (Rule 4.1)
- [ ] Conclusions stated before evidence in every paragraph (Rule 4.2)
- [ ] Methodology/raw data in appendix, not main body (Rule 4.2)
- [ ] Numbered and unordered lists each have one item per line — no compressed inline lists (Rule 4.2)
- [ ] No `\uXXXX` escape sequences in QMD prose — actual Unicode characters used directly (Rule 2.8)
- [ ] Every figure and table preceded and followed by interpretive prose (Rule 4.3)
- [ ] Consistent register throughout — no mid-document tone shift (Rule 4.4)

