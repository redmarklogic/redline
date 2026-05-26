# Guiding Policy: Software Delivery in the AI Era

*Sources: DORA 2024 State of DevOps Report; DORA 2025 State of AI-assisted Software Development; DORA AI Capabilities Model (November 2025); DORA Balancing AI Tensions (March 2026); DORA Impact of Generative AI in Software Development (2025).*
*Framework applied: Rumelt (2011). Good Strategy Bad Strategy - guiding policy as the bridge between diagnosis and coherent action.*
*See also: [accelerate_problem_diagnosis_in_ai_era.md](./accelerate_problem_diagnosis_in_ai_era.md) for the six AI-era diagnoses this policy responds to.*
*See also: [accelerate_guiding_policy_pre_ai_era.md](./accelerate_guiding_policy_pre_ai_era.md) for the 2018 baseline policy this extends.*

---

## What Is a Guiding Policy?

In Rumelt's strategy kernel[^kernel], the guiding policy is the bridge between diagnosis and coherent action. It is not a goal. It is not a plan. It is an **overall approach** chosen to cope with the obstacles named in the diagnosis. It rules out as much as it focuses on - closing off a wide range of possible responses so that energy can concentrate on what actually works.

The AI-era guiding policy is answering the question: *Given that AI adoption is degrading system stability, amplifying existing dysfunction, inflating batch sizes, and creating a false sense of individual productivity - what is the overall approach that will produce real improvement?*

---

## The Overarching Policy Direction

The AI-era guiding policy can be stated in one sentence:

> **Stop treating AI adoption as the strategy. Build the organisational system - the architecture, platform, practices, and measurement framework - that allows AI to amplify strengths rather than accelerate weaknesses, and measure success by system-level DORA[^dora] outcomes, not individual productivity perceptions.**

This extends rather than replaces the pre-AI *Accelerate* policy. The 24 capabilities identified by *Accelerate*[^accelerate] remain valid and necessary. What the AI era adds is a new layer: **the organisational preconditions without which AI investment produces instability rather than improvement.**

The guiding policy rules out: treating AI tool adoption as a productivity programme, measuring AI success by individual output metrics, scaling AI before the foundational system is healthy, and allowing AI to bypass the small batch discipline that *Accelerate* identified as critical.

---

## The Five Foundational Principles of the AI-Era Policy

### 1. Platform-first: build the system AI needs before scaling AI

AI tools are only as effective as the organisational system they operate within. The DORA research is explicit: organisations with high-quality internal developer platforms[^idp], strong APIs, clear workflows, and strong testing practices see AI act as a powerful collaborator. Organisations without those foundations see AI generate technical debt faster.

The policy direction is **not** "adopt AI then fix the system." It is: **fix the system first, then scale AI adoption.**

This means:
- Invest in internal developer platforms before scaling AI tooling
- Ensure APIs, documentation, and codebases are legible to AI before using AI against them
- Treat platform engineering[^platform] as the prerequisite capability for AI ROI, not a nice-to-have

### 2. Verify proportionally to what you generate

AI dramatically increases code generation speed. Without a corresponding increase in verification capacity, throughput metrics improve while quality and stability degrade - the pattern the DORA 2024 data shows in organisations with high AI adoption.

The policy direction is: **invest in verification infrastructure at the same rate you invest in generation tooling.**

This means:
- Test automation coverage must grow as AI code generation grows - AI-generated code requires more testing, not less, because AI cannot reliably signal its own uncertainty
- Automated code review tooling (linting, static analysis, security scanning) must run on every AI-generated contribution
- Change failure rate and time to restore service are the primary success metrics - not lines of code generated or PR throughput

### 3. Enforce small batches structurally - the tooling creates pressure in the opposite direction

*Accelerate* identified working in small batches as one of the highest-leverage capabilities in software delivery. AI creates structural pressure against this: it makes large pull requests easy to generate, so the default behaviour shifts toward larger changes.

The policy direction is: **treat small batch size as a non-negotiable structural constraint, not a cultural preference.**

This means:
- Enforce PR size limits as a process control, not a guideline
- Decompose AI-generated output before it is submitted for review - the author's job is not done when AI produces the code; it is done when the code is in reviewable units
- Measure batch size as a leading indicator of stability risk, not just a hygiene preference

### 4. Direct AI at bottlenecks, not flow states

DORA identified the "valuable work paradox"[^paradox]: AI successfully accelerates the tasks developers find engaging - creative coding, exploration, problem-solving - while leaving bureaucratic overhead, approval latency, and coordination drag entirely unaddressed. The result is that individual satisfaction improves while organisational delivery performance does not proportionally follow.

The policy direction is: **diagnose where work waits, then apply AI and automation to those bottlenecks - not to what already flows.**

This means:
- Map the value stream[^valuestream] before deploying AI; identify where work queues, not where developers feel busy
- Apply AI and automation to approval processes, documentation generation, incident triage, and review latency - the parts of the pipeline that *Accelerate* identified as bureaucratic drag
- Resist the pull to optimise developer experience (DX) metrics at the expense of delivery system metrics

### 5. Preserve expertise intentionally

AI creates a generational compounding risk: developers who never struggle through problems manually develop surface fluency without deep understanding. The expertise required to evaluate whether AI-generated code is architecturally correct - not just technically valid - is built through the productive struggle that AI shortcuts bypass.

The policy direction is: **build explicit, protected practices for expertise development that AI tooling does not erode.**

This means:
- Pair junior engineers with senior engineers specifically for architectural review of AI-generated code - not as a gatekeeping step but as a learning mechanism
- Require manual implementation for complex system components as a capability-building practice
- Recognise that the cost of this investment is visible and immediate; the cost of not making it is invisible until the pipeline of senior engineers capable of evaluating AI output is exhausted

---

## What the Policy Rules Out

These are explicit rejections - approaches that the DORA 2024–2026 research shows either fail to improve system-level outcomes or actively worsen them.

| Ruled out | Why |
|---|---|
| **AI adoption as a productivity programme** | Individual productivity perceptions improve; system stability degrades. These are not the same thing. Programmes measured by individual metrics will optimise for the wrong outcome. |
| **Individual AI productivity metrics as success measures** | Lines of code generated, PR throughput, and "time saved" are local outputs. DORA outcomes (deployment frequency, lead time, change failure rate, MTTR) are system outcomes. The former can improve while the latter degrades. |
| **Scaling AI before fixing architecture and testing** | AI amplifies whatever it operates within. Tightly coupled architectures with poor test coverage generate more tightly coupled code and more undetected defects, faster. |
| **Using AI to bypass the small batch discipline** | Large AI-generated PRs are the primary mechanism by which individual velocity gains convert into system instability. This is measurable and documented in the DORA Gen AI Impact data. |
| **Treating AI-generated code as lower-risk than human-generated code** | AI cannot reliably signal its own uncertainty. 30% of developers (DORA 2025) report little to no trust in AI-generated code - but the review burden to justify that trust is higher, not lower. |
| **Replacing the productive struggle of learning with AI shortcuts for junior engineers** | Expertise cannot be rented from AI. The organisational capacity to evaluate and correct AI output depends on engineers who developed understanding through deliberate practice. |
| **Pivoting AI strategy faster than delivery systems can absorb** | Unstable priorities[^unstable] are the burnout driver most resistant to mitigation. Frequent AI strategy pivots activate all six burnout causes simultaneously. |

---

## What the Policy Focuses On

### Platform engineering as the primary AI enabler

The DORA AI Capabilities Model identifies the internal developer platform as the highest-leverage investment for AI-assisted delivery. A platform is the shared infrastructure - tooling, APIs, deployment pipelines, documentation, security libraries - that makes doing the right thing easy for every team.

Platforms matter for AI specifically because:
- AI tools work better when codebases, APIs, and documentation are consistently structured and machine-readable
- Without a platform, AI adoption is fragmented - each team builds its own AI workflow, creating inconsistency, security gaps, and incompatible practices
- Platform engineering creates the guardrails that allow teams to use AI freely without introducing systemic risk

The DORA research finds that high-performing AI-era organisations invest in platforms *before* scaling AI tooling - not after.

### Verification infrastructure at parity with generation tooling

High-performing AI-era organisations treat test automation and automated code quality tooling as the primary safeguard against AI-generated defects. The policy is:

- Every AI-generated code contribution passes through the same automated test suite as human-written code - with no exceptions for speed or convenience
- Static analysis, security scanning, and dependency review run automatically on every contribution
- Test coverage is treated as a hard constraint on AI code generation: if the tests do not exist to catch AI errors, the AI is operating without a safety net

This is the AI-era extension of *Accelerate*'s "build quality in" principle. The mechanism changes (AI introduces new failure modes) but the policy is the same: quality cannot be inspected in at the end; it must be built in continuously.

### DORA outcomes as the non-negotiable measurement framework

The policy rejects individual AI productivity metrics as success measures. The four DORA metrics remain the definitive measurement framework:

| Metric | What it measures | Why AI adoption makes it more important |
|---|---|---|
| **Deployment frequency** | How often the organisation ships to production | AI pressure to ship more often must be accompanied by the practices that keep high frequency safe |
| **Lead time for changes** | Time from code commit to production | AI that accelerates coding but not review, approval, or testing does not improve this metric |
| **Change failure rate** | Percentage of deployments requiring rollback or hotfix | The primary signal that AI-generated code is introducing instability |
| **Time to restore service (MTTR)** | How fast the organisation recovers from failures | AI that inflates batch sizes makes failures harder to diagnose and recover from |

Organisations that measure AI success by individual productivity and ignore these four metrics will optimise for the wrong outcome.

### Agentic AI as an emerging practice requiring structural guardrails

The DORA AI Capabilities Model (November 2025) identifies **agentic AI**[^agentic] - AI systems that take actions autonomously rather than just generating suggestions - as an emerging capability that high-performing organisations are beginning to adopt for specific pipeline stages (automated testing, incident triage, dependency updates, documentation generation).

The policy direction is: **deploy agentic AI in bounded, auditable contexts with clear human override mechanisms** - not as a general-purpose autonomous actor across the delivery system.

### Transformational leadership focused on system health, not AI adoption speed

Leadership in the AI era creates the conditions for teams to use AI effectively - which means creating the conditions for platform investment, verification discipline, small batch enforcement, and expertise preservation. None of these are natural outcomes of competitive pressure toward rapid AI adoption.

The DORA research confirms that leadership impacts performance indirectly. Leaders who pressure teams for faster AI adoption without investing in the system those teams operate within will see the same outcome as pre-AI leaders who pressured for speed without investing in architecture: instability and burnout.

---

## DORA's AI Capabilities: The Policy's Instrument Panel

The DORA AI Capabilities Model (November 2025) identifies the specific capabilities that predict positive AI-era outcomes. These build on and extend the original 24 *Accelerate* capabilities.

### Foundation capabilities (inherited from *Accelerate* - required before AI adds value)
1. Loosely coupled architecture
2. Continuous integration with trunk-based development
3. Comprehensive test automation
4. Deployment automation and pipeline
5. Lightweight change approval (peer review, not CABs)
6. Generative organisational culture (Westrum)

### New AI-era capabilities
7. **Internal developer platform** - shared infrastructure enabling consistent, safe AI use across teams
8. **AI-assisted code generation with batch size controls** - AI generation paired with mandatory decomposition before review
9. **AI-assisted code review** - automated pre-review (linting, security scanning, test coverage checks) before human review
10. **Verification infrastructure scaling** - test automation investment growing proportionally to AI code generation volume
11. **Documentation practices for AI legibility** - codebases, APIs, and architecture documented in ways AI tools can use effectively
12. **Agentic AI in bounded pipeline contexts** - autonomous AI for specific, auditable tasks (dependency updates, test generation, incident triage) with human override
13. **AI-aware measurement framework** - DORA outcomes tracked separately from individual AI productivity perceptions, with explicit monitoring of change failure rate as the primary AI stability signal
14. **Expertise preservation practices** - structured mentoring, deliberate manual practice for complex components, senior review of AI architectural decisions

**The highest-leverage AI-era capability:** Internal developer platform. It determines whether AI tooling is deployed consistently and safely across teams, or whether each team builds its own fragmented AI workflow that creates systemic risk.

---

## How the Policy Connects to the AI-Era Diagnoses

Each diagnostic finding maps directly to a policy response:

| AI-era diagnosis (root cause) | Guiding policy response |
|---|---|
| Verification tax eroding productivity gains | Invest in verification infrastructure at parity with generation; measure change failure rate as the primary success signal |
| AI amplifies existing dysfunction | Fix architecture, testing, and platform *before* scaling AI; the amplifier cannot be fixed after it has amplified |
| Batch size inflation → instability | Enforce small batches as a structural process constraint; decompose AI-generated output before review |
| Valuable work paradox (AI targets flow, not bottlenecks) | Map value stream bottlenecks first; direct AI at queues and approval latency, not creative coding time |
| Expertise paradox / skill degradation | Protect deliberate practice time; pair junior engineers with seniors for architectural review of AI output |
| Priority instability as dominant burnout driver | Fewer, clearer AI strategy choices held for longer; measure and report on DORA outcomes to make instability's cost visible |

---

## What This Policy Is Not

- It is **not anti-AI**. The policy is not to slow down AI adoption. It is to build the organisational system that allows AI adoption to produce system-level improvement rather than individual-level perception improvement.
- It is **not a replacement for the *Accelerate* policy**. The 24 capabilities and five principles of *Accelerate* remain valid. This policy layer sits above them, addressing the specific failure modes AI introduces.
- It is **not a tool recommendation**. Which AI coding assistant, which platform tooling, which agentic framework - these are coherent actions, not guiding policy. The policy is direction; the tools are implementation details.
- It is **not static**. The DORA AI Capabilities Model is explicitly described as an evolving framework. The specific capabilities and their relative leverage will shift as AI technology and adoption patterns mature. The measurement framework - DORA outcomes - is the stable anchor. The specific capabilities are the current best understanding of what drives those outcomes.
- It is **not complete by itself**. A guiding policy without coherent actions is just direction. The capabilities become actionable only when translated into specific investments, sequenced decisions, and measurable milestones for a specific organisation.

---

## Appendix: Verification Platform Examples

*This appendix provides concrete tool examples for the verification infrastructure capability described in Principle 2. These are coherent action examples, not policy prescriptions - specific tool choices are implementation details that change as the ecosystem matures.*

*Sources: DORA Balancing AI Tensions (March 2026); DORA AI-accessible internal data capability (January 2026); DORA Test automation capability.*

---

### 1. Static Analysis - catches defects before code runs

Tools that scan code for quality issues, security vulnerabilities, and style violations automatically on every commit or pull request.

| Tool | What it does |
|---|---|
| **SonarQube / SonarCloud** | Code quality + security analysis; vendor has an explicit "AI code" solution targeting AI-generated output |
| **Semgrep** | Open-source pattern-based static analysis; widely used for enforcing security rules on every PR |
| **CodeClimate** | Code quality trends + maintainability scoring tracked over time |
| **GitHub Advanced Security (CodeQL)** | Semantic code analysis built into GitHub PR workflows |
| **Qodana** (JetBrains) | IDE-grade inspections running in CI |

### 2. Security Scanning - shift left on security

| Tool | What it does |
|---|---|
| **Snyk** | Dependency vulnerability scanning + SAST (code-level security analysis) |
| **Checkmarx / Veracode** | Enterprise SAST/DAST scanning |
| **Wiz** | Cloud security scanning; DORA specifically cited their "rules files for safer vibe coding" in Balancing AI Tensions |
| **Socket.dev** | Supply chain / dependency trust analysis |

### 3. AI-Assisted Pre-Review Automation

DORA (Balancing AI Tensions, March 2026) explicitly recommends: *"Shift automation and AI to the author during the writing phase - use agents to enforce organisational standards before human review is required."* These tools operationalise that recommendation.

| Tool | What it does |
|---|---|
| **GitHub Copilot code review** | AI-generated review comments surfaced before human reviewers see the PR |
| **CodeRabbit** | AI PR reviewer; summarises changes, flags issues, comments before human review |
| **Qodo (formerly CodiumAI)** | Generates tests from code + reviews PRs for correctness |
| **Reviewpad** | Configurable automated PR rules (label, route, block large PRs) |

### 4. Test Generation - automating creation of the verification layer

| Tool | What it does |
|---|---|
| **Qodo / CodiumAI** | Generates unit tests from existing code |
| **Diffblue Cover** | Automatically writes JUnit tests for Java codebases |
| **GitHub Copilot** (test mode) | Test generation from prompts or function signatures |

### 5. Batch Size Enforcement - structural controls on PR size

DORA identifies working in small batches as a "critical countermeasure" to AI-inflated PRs. These tools enforce it structurally rather than relying on cultural norms.

| Tool | What it does |
|---|---|
| **Danger.js / Danger.rb** | Scriptable PR automation; can fail a PR build if the diff exceeds a configurable line count |
| **Reviewpad** | Rule-based PR management including size gates and routing |
| **Custom GitHub Actions** | `git diff --stat` threshold checks as a required status check |

### 6. Context Engineering / AI-Accessible Internal Data

DORA identifies giving AI access to your organisation's specific codebase, documentation, and standards as a key multiplier for AI code quality - its January 2026 capability page describes this as the bridge between "using AI" and "getting value from AI."

| Tool | What it does |
|---|---|
| **Sourcegraph Cody** | Codebase-aware AI assistant using retrieval-augmented generation against your entire repo |
| **GitHub Copilot Enterprise** | Indexes your organisation's codebase for context-aware suggestions grounded in internal patterns |
| **MCP servers** (Model Context Protocol) | Connect AI tools to internal APIs, documentation, and metrics - DORA cites this as the emerging standard pattern |
| **RAG pipelines** (LangChain, LlamaIndex) | Custom retrieval-augmented generation against internal documentation |

### 7. Production Feedback Loops - monitoring as verification

These complete the verification loop by feeding real production signals back into the delivery process.

| Tool | What it does |
|---|---|
| **Datadog / New Relic / Dynatrace** | Application performance monitoring; alerts on degrading DORA outcomes (MTTR, error rate) |
| **Honeycomb** | Observability for distributed systems; particularly useful for diagnosing AI-generated code failures |
| **Grafana** | Open-source metrics and alerting dashboards |
| **Dependabot / Renovate** | Automated dependency update PRs - an example of agentic AI in a bounded, auditable context |

---

### The DORA-Recommended Stack Shape

DORA does not prescribe specific tools but describes the *shape* of what verification infrastructure requires:

1. **Author-side** - static analysis and AI pre-review run before the PR is opened, not after
2. **Pipeline-side** - full test suite and security scan on every commit, with results visible within ten minutes (DORA's explicit target)
3. **PR gate** - batch size check and AI review summary before human review starts
4. **Context layer** - AI tools grounded in internal codebase and standards, not just generic training data

The DORA Balancing AI Tensions paper (March 2026) states: *"Investing in robust test automation for faster feedback may provide a better return on investment than optimising manual review."* Verification infrastructure is not a cost centre against AI - it is the capability that determines whether AI adoption improves or degrades DORA outcomes.

---

## Footnotes

[^kernel]: **Rumelt's strategy kernel** - the three-part structure Richard Rumelt describes in *Good Strategy Bad Strategy* (2011) as the minimum components of any real strategy.

    - **Diagnosis** - identifies the nature of the challenge; names the specific obstacle causing failure rather than just describing symptoms.
    - **Guiding policy** - the overall approach chosen to cope with that obstacle; rules out wide ranges of alternatives as much as it points in a direction.
    - **Coherent actions** - the specific steps, resource allocations, and changes that implement the guiding policy.

    Rumelt's argument: most "strategies" are actually just goal lists with no theory of why things are currently failing or how the chosen approach will address it. The kernel is the minimum structure that separates genuine strategy from wishful thinking.

[^dora]: **DORA - DevOps Research and Assessment** - a research programme originally founded by Nicole Forsgren, Jez Humble, and Gene Kim, part of Google Cloud since 2018.

    - **What it produces:** The annual *State of DevOps Report* - the longest-running and largest survey-based study of software delivery practices globally.
    - **The four DORA metrics:** Deployment frequency, lead time for changes, time to restore service (MTTR), and change failure rate - the definitive system-level measures of software delivery performance.
    - **Why they are system-level:** They measure what the whole delivery system produces, not what individuals output. Individual productivity can increase while all four DORA metrics degrade simultaneously - this is the pattern the 2024 DORA data shows in high-AI-adoption organisations.

[^accelerate]: ***Accelerate: The Science of Lean Software and DevOps*** (2018) - Nicole Forsgren, Jez Humble, and Gene Kim.

    - **What it established:** The empirical research foundation for software delivery performance. Four years of survey data identifying the 24 capabilities that predict high performance.
    - **Its relationship to the AI-era policy:** The 24 *Accelerate* capabilities are the *foundation* this policy builds on - not the ceiling. AI adoption without first achieving the *Accelerate* foundation produces worse outcomes than not adopting AI at all.

[^idp]: **Internal Developer Platform (IDP)** - the shared internal infrastructure that a platform engineering team builds and maintains for delivery teams to use.

    - **What it includes:** Deployment pipelines, testing infrastructure, security scanning, API standards, documentation frameworks, approved toolchains, and shared libraries.
    - **What it is not:** A portal or a set of guidelines. An IDP is operational infrastructure - teams use it to build and ship software rather than configuring their own from scratch.
    - **Why it matters for AI:** AI tools work best when codebases, APIs, and workflows are consistently structured. A platform creates that consistency across teams. Without it, each team's AI workflow diverges, creating incompatible practices, security gaps, and inconsistent quality.

[^platform]: **Platform engineering** - the discipline of building and maintaining the internal developer platform.

    - **The role:** Platform engineers are not embedded in delivery teams - they build the shared infrastructure that all delivery teams use.
    - **The value proposition:** Encode good practices (security, testing, deployment standards) into infrastructure rather than relying on each team to independently discover and apply them correctly.
    - **DORA's finding:** Platform engineering is the highest-leverage investment for organisations wanting AI to add value at system level rather than just individual level.

[^paradox]: **The valuable work paradox** - named by DORA in the 2025 research.

    - **The finding:** AI successfully accelerates the tasks developers find engaging (creative coding, problem-solving, exploration). It has not automated the drudgery: approval processes, bureaucratic coordination, meetings, compliance overhead.
    - **The result:** Individual job satisfaction improves. Organisational delivery bottlenecks remain exactly where they were.
    - **Why it matters strategically:** Organisations measuring AI success by developer satisfaction will believe AI is working. Organisations measuring by DORA outcomes will see that the actual constraints are untouched.

[^valuestream]: **Value stream** - the sequence of steps that takes a customer need from idea through development to working software in production.

    - **Value stream mapping:** A technique borrowed from Lean manufacturing that traces every step in that sequence and identifies which steps add value, which add delay, and where work queues.
    - **Why it matters for AI:** Without mapping the value stream, organisations apply AI where developers feel busy rather than where work actually waits. The bottleneck is almost never creative coding time - it is coordination, approval, and integration latency.

[^unstable]: **Unstable organisational priorities** - identified by DORA 2024 as the burnout driver most resistant to mitigation.

    - **What it looks like:** Strategic direction changes faster than delivery teams can execute against it - pivoting from one AI strategy to another, reorganising teams around new AI initiatives before the previous ones shipped, cancelling work mid-flight as AI tooling decisions change.
    - **Why it is uniquely damaging:** It simultaneously activates all six structural burnout causes from *Accelerate* (overload, loss of control, insufficient rewards, breakdown of community, absence of fairness, value conflicts). No technical or managerial intervention can compensate for it while the instability continues.
    - **The lever:** The pace of strategic pivots is a leadership choice. Naming it as the cause is the prerequisite for addressing it.

[^agentic]: **Agentic AI** - AI systems that do not just generate suggestions for a human to accept or reject, but take actions autonomously as part of a workflow.

    - **Examples in software delivery:** An AI agent that automatically opens a pull request when it detects a failing dependency; an agent that generates a draft incident report when an alert fires; an agent that proposes and applies a test for a new code path.
    - **The opportunity:** Agentic AI can address the bottlenecks that generative AI cannot - the approval latency, coordination overhead, and documentation drag that the valuable work paradox leaves untouched.
    - **The risk:** Agentic AI operating without clear boundaries and human override mechanisms introduces a new class of risk - actions taken autonomously that are difficult to audit, reverse, or attribute. The policy is bounded deployment with audit trails, not open-ended autonomy.
