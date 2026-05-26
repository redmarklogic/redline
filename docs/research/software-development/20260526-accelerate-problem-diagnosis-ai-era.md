# Problem Diagnosis: Software Delivery in the AI Era

*Sources: DORA 2024 State of DevOps Report; DORA 2025 State of AI-assisted Software Development Report; DORA Impact of Generative AI in Software Development (2025); DORA Balancing AI Tensions (March 2026); DORA AI Capabilities Model (November 2025).*
*Framework applied: Rumelt (2011). Good Strategy Bad Strategy - diagnostic principles.*
*See also: [accelerate_problem_diagnosis_pre_ai_era.md](./accelerate_problem_diagnosis_pre_ai_era.md) for the 2018 baseline.*

---

## What Changed - And What Didn't

The 2018 *Accelerate*[^accelerate] research diagnosed six structural root causes of poor software delivery performance. None of those causes have been eliminated. What AI has done is **restructure the priority ordering and introduce new failure modes that did not exist before**.

As of 2025–2026, 90% of technology professionals use AI at work. Over 80% believe it has increased their individual productivity. Yet the DORA[^dora] data shows that higher AI adoption is simultaneously associated with:

- Increased software delivery **throughput**
- Increased software delivery **instability**

This is not a paradox - it is a **diagnostic signal**. AI is not solving the delivery problem. It is amplifying it in new directions.

The 2025 DORA research frames AI's primary role precisely: **AI is an amplifier. It magnifies an organisation's existing strengths - and its existing dysfunctions.**

> "If an organisation has a high-quality internal platform, strong APIs, clear workflows, and strong testing practices, AI acts as a powerful collaborator. However, if a team suffers from fragmented tooling, siloed data, or fragile infrastructure, AI will simply help them generate technical debt faster."
> - DORA, *Balancing AI Tensions*, March 2026

The diagnostic task for 2025–2026 is therefore twofold: understand which pre-AI problems are now **accelerated**, and identify the genuinely **new** structural failures that AI has introduced.

---

## What the Research Was Solving For (Presenting Symptoms)

The symptoms visible to most organisations in 2025:

- Productivity feels higher but system stability is degrading
- Code review is slower and more cognitively demanding despite faster code generation
- Deployments are increasing in frequency but failing more often
- Junior engineers appear productive but senior engineers are concerned about codebase health
- AI tools are adopted widely but measurable organisational performance improvements are elusive
- Burnout persists despite the "productivity gains" AI was supposed to provide

**These are results, not causes.** The diagnoses below identify the structural forces producing them.

---

## Diagnosis 1: The "Verification Tax" Is Eroding the Productivity Gain

### The result being observed

Developers report feeling more productive. Individual output (code volume, PR throughput) increases. Yet change failure rates rise and system stability degrades. Lead times for complex work do not improve proportionally.

### The structural cause

AI generates code faster than humans can verify it correctly. This creates a **hidden verification tax**: time saved during creation is re-allocated to auditing. The DORA research on 1,110 Google engineers (Q3 2025) found this pattern universal across all AI use cases - code generation, code review, testing, debugging, documentation.

The verification tax is asymmetric in two ways:

1. **Author vs. reviewer imbalance:** AI lets an author generate a massive changelist quickly. The reviewer still audits every line manually. Reviewer cognitive load increases faster than author throughput. One engineer's observation: *"Reviewing [another's] code is so much harder than writing it. AI tools are increasing the rate at which people can churn out code that needs to be reviewed."*

2. **AI cannot signal its own uncertainty:** AI tools cannot reliably flag when they are hallucinating or producing incorrect output. Engineers must treat every interaction as potentially deceptive. 30% of developers (2025 DORA) report little to no trust in AI-generated code.

The net result: **throughput metrics improve while quality and stability metrics degrade.** This is the signature of a system where local output is increasing but global outcomes are worsening.

### The diagnostic insight

The problem is not AI adoption itself - it is that organisations are **measuring creation speed without measuring verification cost**. They are optimising for the visible gain (code generated faster) while the hidden cost (review burden, defect rate, rework) accumulates invisibly.

This is the same measurement dysfunction diagnosed in *Accelerate* - optimising local outputs rather than global outcomes - but AI has made it faster and more damaging.

**Leverage:** Rebalance the process to shift AI's role earlier (author-side review automation, pre-commit validation) and enforce small batch sizes. Large AI-generated PRs are the mechanism by which individual velocity gains convert into system instability.

---

## Diagnosis 2: AI Is an Amplifier of Existing Dysfunctions - Not a Remedy for Them

### The result being observed

Organisations with poor architecture, fragmented tooling, siloed data, or weak testing practices adopt AI and see their problems worsen rather than improve. Technical debt accumulates faster. Deployments become more chaotic. Teams feel busier but progress less.

### The structural cause

AI does not have an opinion about architecture. It generates code within the constraints of the system it is given access to. If the underlying system is tightly coupled, AI helps engineers generate more tightly coupled code faster. If documentation is absent, AI generates code against an undocumented system and produces confidently wrong outputs.

The 2025 DORA research is explicit: AI magnifies existing strengths *and* existing weaknesses. The 2024 DORA report found that AI adoption **negatively impacts software delivery stability and throughput** at the system level, while positively impacting individual productivity. The gap between individual and system outcomes is the diagnostic signal.

### The diagnostic insight

Organisations treating AI as the *cause* of their current delivery capability - rather than as an amplifier of it - will continue to be confused by this pattern. The correct framing is: **AI reveals what was already true about your organisation, at higher speed and higher volume.**

The pre-AI bottlenecks diagnosed by *Accelerate* - coupling, bureaucratic process, pathological culture[^westrum], flawed measurement - are not removed by AI. They are surfaced faster and more visibly.

**Leverage:** Before scaling AI adoption, diagnose the organisational system AI will amplify. Fix coupling, testing coverage, and information access first. Scaling AI into a broken system accelerates the breakdown.

---

## Diagnosis 3: The Batch Size Problem Has Returned in a New Form

### The result being observed

Deployment frequency increases. Change failure rates also increase. Teams are shipping more often and breaking more often simultaneously.

### The structural cause

AI dramatically lowers the activation energy for generating code. The result is that **batch sizes grow** - individual PRs and changelists become larger because AI can produce them faster. Large batches are slower to review, harder to test in isolation, and more likely to cause system instability when merged.

*Accelerate* identified working in small batches as one of the highest-leverage capabilities for high-performing teams. AI has created structural pressure in the opposite direction: it makes large batches easy to generate, which is a capability trap.

The DORA Gen AI Impact report quantifies this: *"A 25% increase in AI adoption is associated with a 1.5% decrease in delivery throughput and a 7.2% decrease in delivery stability."* The mechanism is batch size inflation.

### The diagnostic insight

The small batch discipline that was a learned cultural practice in high-performing pre-AI teams is now under **active pressure from the tooling itself**. AI has created an environment where the path of least resistance is larger batches.

This is a new form of the old architecture problem: the structure of the tooling shapes the structure of the work, whether you plan for it or not.

**Leverage:** Enforce small batch sizes as a *mandatory* structural constraint on AI-assisted development, not a preference. The discipline of decomposing AI-generated output into reviewable, testable units is the critical countermeasure. This is a process architecture decision, not a personal responsibility.

---

## Diagnosis 4: The "Valuable Work Paradox" - AI Speeds Up What Developers Enjoy, Not What Burdens Them

### The result being observed

Developers using AI extensively report higher job satisfaction and more time in flow states. Yet the same research shows they spend less time on **valuable** work, while time spent on bureaucracy, meetings, and toilsome tasks remains unchanged.

### The structural cause

DORA names this the **"vacuum hypothesis"**: AI successfully accelerates the tasks developers find engaging - creative coding, problem-solving, exploration. It has not automated the drudgery: approval processes, bureaucratic coordination, meetings, compliance overhead.

The result is that AI creates a productivity illusion. Individual engineers feel more effective because their enjoyable work goes faster. But the organisational weight - the bureaucratic and coordination overhead that *Accelerate* diagnosed as a structural bottleneck - is untouched.

### The diagnostic insight

Applying Rumelt's diagnostic check[^rumelt]: the presenting symptom is that developers feel better but organisational delivery performance does not proportionally improve. The root cause is that **AI is targeting the wrong bottleneck**. The bottleneck was never creative coding time - it was coordination overhead, approval latency, and process drag. AI accelerates what was already fluid and leaves the actual constraints in place.

This is structurally analogous to the International Harvester failure[^harvester]: investing in equipment (AI tools) while the real problem (work organisation and process) remains unaddressed.

**Leverage:** Diagnose where the actual delays occur in your delivery pipeline - not where developers feel busy, but where work waits. Apply AI and automation to coordination overhead, not just creative coding. The highest-leverage application of AI may be in automating approvals, surfacing bottlenecks, and reducing review latency, not in accelerating code generation.

---

## Diagnosis 5: The Expertise Paradox - AI Creates False Confidence in Shallow Knowledge

### The result being observed

Junior developers work in unfamiliar domains without needing to develop the foundational understanding that domain requires. Architectural decisions get made without the expertise to evaluate AI's suggestions. Codebases accumulate "confident but wrong" design choices.

### The structural cause

AI lowers the barrier to starting in unfamiliar domains by generating plausible-looking code. This is a surface benefit but carries a hidden structural cost: it **bypasses the productive struggle** that builds genuine expertise.

When developers lack the expertise to evaluate AI's architectural suggestions, they cannot detect when AI is wrong or when a technically correct suggestion is strategically poor for their specific system. AI validates the user's assumptions regardless of their architectural merit because it has no knowledge of the organisation's specific constraints, history, or strategy.

The DORA research identifies this as **skill degradation risk**: *"AI tools increase my productivity, they write code faster than I could, but the code is (currently) lower quality than I could write myself."* The concern is not just current quality - it is that the people responsible for maintaining and extending the system are not developing the understanding needed to do so.

### The diagnostic insight

This is a generational compounding problem, not just a current quality problem. If junior engineers never build the deep foundational expertise that comes from struggling through problems manually, the organisation's senior engineering capability will not be replenished. In five years, the senior engineers who can evaluate AI output critically will retire, and their replacements will have been trained on AI-assisted shortcuts.

**Leverage:** Actively preserve time and structured space for deep learning. Pair junior engineers with senior mentors specifically for AI-generated architectural decisions. Require manual coding for complex system components not as a punishment but as a capability-building practice. The cost of this investment is visible; the cost of not making it is invisible until it is too late.

---

## Diagnosis 6: Unstable Organisational Priorities Are the Most Resistant Cause of Burnout

### The result being observed

Burnout persists or worsens in some organisations despite AI adoption. Developer satisfaction improvements from AI are real but fragile. Teams report feeling more productive yet also more anxious.

### The structural cause

The 2024 DORA report identified **unstable organisational priorities**[^unstable] as a distinct and particularly damaging driver of developer burnout - one that is *"highly resistant to mitigation and persists even in environments with strong leaders and high-quality documentation."*

This is a different mechanism than the six burnout causes identified in *Accelerate* (work overload, lack of control, insufficient rewards, breakdown of community, absence of fairness, value conflicts). Unstable priorities operate upstream of all of those: when strategic direction shifts frequently, all six burnout drivers are activated simultaneously. Work that felt meaningful becomes wasted. Autonomy disappears as priorities reset. Community breaks down as teams are reorganised around new objectives.

In the AI era, this problem is intensified because organisations are making rapid strategic pivots around AI tooling, AI strategy, and AI-first product directions - often faster than delivery teams can absorb.

### The diagnostic insight

The "elephant in the elevator" here is that many organisations believe they are responding appropriately to a fast-moving AI landscape by pivoting frequently. The data says otherwise: **constant priority shifts are among the highest-damage variables in software delivery performance**, and no amount of AI tooling, good leadership, or documentation can compensate for them.

**Leverage:** Diagnose whether your organisation's delivery problems are caused by capability gaps or by priority instability. If it is the latter, fixing the capability (with more AI tools, better practices, stronger leaders) will not help. The only fix is strategic stability - making fewer, clearer choices and holding them for long enough for delivery systems to align.

---

## What Organisations Are Still Not Naming

Applying the Rumelt "elephant in the elevator"[^elephant] test - *what is the central obstacle everyone knows exists but no one names in the plan?* - to the AI era surfaces four recurring avoidances. Each one has supporting evidence. Each one goes unnamed in most AI strategies.

- **AI adoption is degrading system stability in most organisations.**

    This is not an opinion - it is the finding of the 2024 DORA State of DevOps Report, the largest annual survey of software delivery practices globally (thousands of respondents across industries and geographies).

    - *Evidence:* A 25% increase in AI adoption is associated with a 1.5% decrease in delivery throughput *and* a 7.2% decrease in delivery stability. Organisations adopting AI more heavily are, on average, shipping less reliably - not more.
    - *Corroborating finding:* DORA research on 1,110 Google engineers (Q3 2025) - individual productivity perceptions improve, but change failure rates rise.
    - *Why it goes unspoken:* Admitting it contradicts the investment narrative most organisations have already committed to publicly. If you have announced an "AI-first engineering strategy," this finding is uncomfortable to say out loud.

- **Batch sizes are growing because AI makes large PRs easy - and this is structural, not an individual discipline failure.**

    A pull request (PR) is a unit of code change submitted for review before it is merged into the main codebase. *Accelerate* identified working in small PRs as one of the highest-leverage practices for high-performing teams: small changes are easier to review, easier to test, and less likely to cause system failures when deployed.

    - *What AI changed:* Code generation dramatically lowers the effort to produce a large PR - what once took three days of writing can now be generated in an afternoon. PRs are getting bigger.
    - *Evidence:* The DORA Gen AI Impact report links batch size inflation directly to the stability decline - larger batches are harder to review correctly, more likely to contain undetected defects, and more damaging when they fail in production.
    - *Why it goes unaddressed:* Fixing it requires process constraints - mandatory PR size limits - that visibly slow individual output metrics. In an environment where "AI productivity" is measured by code generation speed, slowing individual throughput for system health is a hard sell.

- **The expertise organisations are losing to AI shortcuts cannot be recovered quickly.**

    The DORA 2025 research found that developers using AI tools extensively report lower confidence in their own ability to evaluate the code AI produces - an effect particularly acute for junior engineers.

    - *From the research:* *"AI tools increase my productivity, they write code faster than I could, but the code is (currently) lower quality than I could write myself."*
    - *The structural concern:* Deep engineering expertise - the ability to recognise that AI-generated code is architecturally wrong despite being technically correct - is built through years of struggling through problems manually. AI shortcuts bypass that struggle, producing surface fluency without deep understanding.
    - *The generational risk:* In five to ten years, the senior engineers who can evaluate AI output critically will retire. Their replacements will have been trained on AI-assisted shortcuts rather than first-principles problem solving.
    - *Why it goes unspoken:* Naming it requires challenging both the AI tooling investment and the way organisations develop their people - two things currently moving in opposite directions.

- **Unstable priorities cause more delivery damage than any technical failure - and the instability is a leadership choice.**

    The 2024 DORA report identified unstable organisational priorities as the burnout driver most resistant to mitigation - persisting even in teams with strong leaders, good documentation, and high-quality practices in place.

    - *The mechanism:* Frequent strategic pivots simultaneously activate all six of the structural burnout causes identified in *Accelerate* (see [^unstable] for detail). No technical fix and no AI tool addresses this.
    - *The only remedy:* Leaders making fewer, clearer strategic choices and holding them for long enough for delivery teams to actually execute against them.
    - *Why it goes unspoken:* Naming it requires leadership to accept direct accountability for delivery dysfunction - acknowledging that the pivoting which feels like responsive leadership from the top looks like chaos and wasted work from the teams doing the building.

Strategies that do not name these will not address them.

---

## Summary: The AI-Era Diagnostic Map

| Diagnosis | Root cause classified as | Leverage point |
|---|---|---|
| **Verification tax eroding productivity gains** | Creation-speed metric without verification-cost metric | Measure review burden; shift AI to author-side validation; enforce small batches |
| **AI amplifies existing dysfunction** | Organisational weaknesses accelerated, not remedied | Fix architecture, testing, and information access *before* scaling AI adoption |
| **Batch size inflation → instability** | AI lowers activation energy for large PRs; structural pressure against small batches | Enforce small batch sizes as a mandatory process constraint, not a preference |
| **Valuable work paradox** | AI targets enjoyable coding tasks, not coordination bottlenecks | Diagnose actual wait times; apply AI to bureaucratic overhead, not just creative coding |
| **Expertise paradox / skill degradation** | AI bypasses productive struggle; shallow confidence in unfamiliar domains | Structured mentoring, mandatory manual coding for complex components |
| **Priority instability as dominant burnout driver** | Frequent strategic pivots override all other mitigations | Fewer, clearer strategic choices held for longer; accept that instability is a leadership decision |

---

## The Shift in the Diagnostic Frame Since 2018

| Pre-AI diagnosis (Accelerate, 2018) | AI-era diagnosis (DORA 2024–2026) |
|---|---|
| Speed and stability trade off against each other | Speed increases, stability degrades - simultaneously - due to batch size and verification collapse |
| Measurement frameworks drive dysfunction | Measurement dysfunction is amplified: AI inflates all output-based metrics faster |
| Architecture is the primary scalability constraint | Architecture remains the constraint; AI makes bad architecture generate more debt faster |
| Culture determines information flow and safety | Culture still matters, but AI introduces new trust and transparency dimensions |
| Change Advisory Boards (CABs) and process gates are risk management theater | Still true, but the more urgent gate problem is batch size and review capacity |
| Burnout is caused by six organisational conditions | Burnout is now additionally driven by priority instability, which is uniquely resistant to mitigation |

---

## Sources

- DORA (2024). *Accelerate State of DevOps Report 2024*. Google Cloud. [dora.dev/research/2024](https://dora.dev/research/2024/)
- DORA (2025). *State of AI-assisted Software Development*. Google Cloud. [dora.dev/research/2025](https://dora.dev/research/2025/)
- DORA (2025). *Impact of Generative AI in Software Development*. Google Cloud. [dora.dev/ai/gen-ai-report](https://dora.dev/ai/gen-ai-report/)
- DORA (2025). *AI Capabilities Model*. Google Cloud. [dora.dev/ai/capabilities-model/report](https://dora.dev/ai/capabilities-model/report/)
- Baolin, J. & Harvey, N. (March 2026). *Balancing AI tensions: Moving from AI adoption to effective SDLC use*. DORA. [dora.dev/insights/balancing-ai-tensions](https://dora.dev/insights/balancing-ai-tensions/)
- D'Angelo, S. et al. (August 2025). *Choosing measurement frameworks to fit your organisational goals*. DORA. [dora.dev/research/2025/measurement-frameworks](https://dora.dev/research/2025/measurement-frameworks/)

---

## Footnotes

[^accelerate]: ***Accelerate: The Science of Lean Software and DevOps*** (2018), Nicole Forsgren, Jez Humble & Gene Kim.

    - **What it is:** A research-based book drawing on four years of survey data from the DORA State of DevOps programme to identify what separates high-performing software delivery organisations from low performers.
    - **Key contribution:** Introduced the four DORA metrics - deployment frequency, lead time for changes, time to restore service, and change failure rate - as the definitive measures of software delivery performance.
    - **What it identified:** 24 specific technical, cultural, and managerial capabilities that statistically predict those outcomes.
    - **What references to it mean here:** All references to *Accelerate* diagnoses in this document refer to the structural findings from that 2018 research, used as the pre-AI baseline against which AI-era changes are compared.

[^dora]: **DORA - DevOps Research and Assessment.**

    - **What it is:** A research programme originally founded by Forsgren, Humble, and Kim, part of Google Cloud since 2018.
    - **What it produces:** The annual *State of DevOps Report* - the longest-running and largest survey-based study of software delivery practices globally, covering thousands of respondents across industries and countries each year.
    - **What it tracks:** How technology capabilities, practices, and organisational factors affect software delivery performance and business outcomes.
    - **Why it matters here:** The 2024 and 2025 DORA reports are the primary empirical sources for this document. When the document cites DORA findings, it is citing large-sample survey research - not anecdote or consulting opinion.

[^westrum]: **Pathological culture** - Ron Westrum's term from his typology of organisational information-flow cultures (1988, extended 2004).

    Westrum identified three types of organisation based on how they handle information:

    - **Pathological (power-oriented):** Information is hoarded or distorted for political advantage. Messengers who bring bad news are punished. Blame lands on individuals. Failure is covered up.
    - **Bureaucratic (rule-oriented):** Departments protect their turf and filter information through hierarchy. Things are done by the book - their book.
    - **Generative (performance-oriented):** Information flows freely to whoever needs it. Risks are shared. Failure is treated as a signal to investigate the system, not to blame a person.

    *Accelerate* found that generative culture is a strong predictor of software delivery performance - and that culture is a *system property*, meaning it can be changed by changing the system, not by exhorting individuals to behave better.

[^rumelt]: **Rumelt's diagnostic check** - from Richard Rumelt's *Good Strategy Bad Strategy* (2011).

    The check asks whether a plan has correctly identified the specific obstacle causing poor performance, rather than simply describing desired outcomes. Three steps:

    - **Name the actual obstacle** - not the goal, not the symptom, but the specific structural force causing the failure.
    - **Explain the mechanism** - describe how the obstacle produces the observed failure, so the connection is visible and testable.
    - **Identify the leverage point** - which aspect of the obstacle, if addressed, would produce the most improvement for the least effort?

    Rumelt's core argument: most "strategies" skip the diagnosis entirely and jump from symptoms to action plans. A plan that fails this check is not a strategy - it is a wish list with a budget.

[^elephant]: **"Elephant in the elevator"** - Richard Rumelt's phrase from *Good Strategy Bad Strategy* (2011).

    - **What it means:** The central, obvious problem that everyone in an organisation knows exists but that never appears in the strategy document. Like an elephant somehow in the elevator - visible, unavoidable, requiring everyone to contort around it - but politely unacknowledged.
    - **The diagnostic test:** Read the strategy document and ask whether the real obstacle is named, or whether the document describes goals and initiatives while talking around it.
    - **What absence signals:** If the elephant is not in the document, the organisation has chosen not to confront the hardest part of its situation. That is itself a diagnostic finding - not a neutral omission.

[^harvester]: **International Harvester (1979) - the canonical example of diagnosis failure.**

    - **What it was:** One of America's largest industrial conglomerates - manufacturing farm equipment, trucks, and construction machinery.
    - **The situation:** Years of declining profitability, with margins running at roughly half of direct competitors.
    - **What the plan said:** Increase market share in each division and cut costs across the board. Described desired outcomes. Never asked *why* performance was poor.
    - **What the plan ignored:** Harvester had the worst labour relations in American industry and grossly inefficient work organisation - visible to anyone on the factory floor, absent from every boardroom document.
    - **What happened:** Rather than diagnose and address the root cause, the company invested in expansion. In 1979–1980, a six-month strike exposed the dysfunction completely: $3 billion in losses, 35 of 42 plants closed, eventual collapse.
    - **Rumelt's lesson:** Confusing the obstacle (broken labour relations and work organisation) with the goal (higher margins) produces plans that cannot succeed regardless of how well they are executed.
    - **The AI-era parallel:** Organisations that diagnose their delivery problem as "not enough code velocity" and invest in AI code generation tools - while leaving the actual bottlenecks (coordination overhead, approval latency, architectural coupling) entirely unaddressed.

[^unstable]: **Unstable organisational priorities** - identified by DORA 2024 as the burnout driver most resistant to mitigation.

    - **What it looks like in practice:** A team is mid-way through building feature A when leadership announces a pivot to initiative B, which is replaced by initiative C three months later. Work is abandoned before it ships. Systems are built to requirements that no longer apply. Teams are reorganised to serve new objectives before delivering against the previous ones.
    - **How DORA distinguishes it from normal reprioritisation:** By its *frequency*, its *pace relative to delivery cycles*, and its *resistance to mitigation* - even excellent management, good documentation, and strong culture cannot compensate for it.
    - **The mechanism - six burnout drivers activated simultaneously** (from *Accelerate*):
        - *Work overload* - everyone is working on too many things at once
        - *Loss of control* - direction changes are outside the team's influence
        - *Insufficient rewards* - work is cancelled before it creates value
        - *Breakdown of community* - teams are restructured repeatedly
        - *Absence of fairness* - decisions feel arbitrary
        - *Value conflicts* - engineers are asked to discard work they know has value
    - **Why it is classified as a leadership decision:** The pace of strategic pivots is within leadership's control - unlike market conditions or technical debt. Organisations that name this can address it. Organisations that avoid naming it cannot.
