# Coherent Actions: Accelerate in the AI Era

*Sources: DORA (2025). State of AI-assisted Software Development. Google Cloud. | DORA (2025). AI Capabilities Model. Google Cloud. | DORA (2026, March). Balancing AI tensions: Moving from AI adoption to effective SDLC use. dora.dev. | DORA (2025). Impact of Generative AI in Software Development. Google Cloud.*
*Framework applied: Rumelt (2011). Good Strategy Bad Strategy - coherent actions as the specific, mutually reinforcing decisions that implement the guiding policy.*
*See also: [accelerate_problem_diagnosis_in_ai_era.md](./accelerate_problem_diagnosis_in_ai_era.md)*
*See also: [accelerate_guiding_policy_in_ai_era.md](./accelerate_guiding_policy_in_ai_era.md)*
*See also: [accelerate_coherent_actions_pre_ai_era.md](./accelerate_coherent_actions_pre_ai_era.md)*

---

## What Are Coherent Actions?

In Rumelt's strategy kernel[^kernel], coherent actions are the third element: the specific resource allocations, decisions, and changes that implement the guiding policy. They are not a project portfolio or a list of AI tooling to adopt. They are mutually reinforcing: each makes the others more effective.

This document extracts the coherent actions the DORA AI-era research actually prescribes - the specific things the research says teams and leaders should do, including the numerical thresholds it names. These are not interpretations; they are what the research directly recommends.

---

## Establish Performance Targets That Survive AI Inflation

DORA's four throughput and stability metrics[^dora-metrics] remain the anchor in the AI era. The AI-era problem is not that these targets change - it is that inputs to them must be interpreted differently. The 2025 DORA research found that a 25% increase in AI adoption is associated with a 1.5% decrease in delivery throughput and a 7% decrease in delivery stability. Higher adoption correlates with more throughput and more instability simultaneously.

| Metric | High performer baseline | AI-era interpretation |
|---|---|---|
| **Deployment frequency** | Multiple times per day, on demand | Still valid; now requires batch-size discipline to prevent AI-generated mass deployments from masking instability |
| **Lead time for changes** | Less than one hour from commit to production | Context engineering and AI-accessible internal data directly reduce lead time; the bottleneck shifts from writing to verifying |
| **Time to restore service (MTTR)** | Less than one hour | AI-assisted incident response can reduce MTTR, but only if monitoring and runbooks are high-quality inputs |
| **Change failure rate** | 0–15% | The primary risk in the AI era: AI inflates throughput while stability degrades; this metric catches the gap |

Individual output metrics - lines of code accepted, PR count, commit frequency - are explicitly rejected by the 2025 DORA research as measures of team performance. AI can inflate all three without delivering any corresponding increase in user value.

---

## Measurement

### Measure effective throughput, not raw output

Raw PR count or commit frequency is insufficient in the AI era because AI-generated boilerplate inflates activity without delivering value. The replacement: **effective throughput**, defined as PR merge frequency minus rework.

DORA-derived thresholds:

| Performance tier | Effective throughput profile |
|---|---|
| **High** | High merge frequency, rework rate **less than 10%** |
| **Medium** | High merge frequency, moderate rework |
| **Low** | Low merge frequency, or high merge frequency with rework **greater than 25%** |

Tracking rework directly - PRs opened to fix or revert other PRs - makes the difference between velocity and "rework masquerading as velocity" visible in the data.

### Measure human-in-the-loop rate

The percentage of PRs that received meaningful human review, as distinct from auto-approval or rubber-stamping. The 2025 DORA report found that 30% of developers report little to no trust in AI-generated code. The structural risk is that reviewers trust AI output and approve without deep reading - producing a metric that registers as "reviewed" while the actual verification did not occur.

Proxy signal recommended by DORA research: a **500-line PR approved in less than 2 minutes** is a reliable heuristic for rubber-stamp review - it is not physically possible to read 500 lines in that window. Flag this automatically. Additional signal: whether the reviewer has prior commits in the affected files (existing familiarity reduces review risk) and whether the review contains inline comments (evidence that the reviewer engaged with the code rather than scrolling to approve).

### Track the three-way AI risk signal

DORA identifies a compound risk dimension that three individual signals cannot capture alone. Each dimension independently is low-signal; combined, they identify the highest-risk PRs:

1. **Authorship** - who wrote the code: human, AI with human steering, or autonomous AI (bot account or fully agent-generated)
2. **Review** - who checked it before merge: dual human reviewers, one human reviewer, one human and one AI reviewer, or self-merged
3. **Contributor history** - whether the author has prior commits in the affected files of that codebase

The highest-risk scenario: fully AI-authored, self-merged PR, from an author with no prior commits in that codebase. Teams should build automated tooling to surface this signal before merge, not after.

### Replace output dashboards with Value Stream Management signals

DORA recommends tracking downstream quality signals rather than upstream activity counts:

- Code review turnaround times
- Failed deployment recovery time
- Deployment rework rates
- Production incidents

These reveal where the value stream is queueing. DORA also names three measurement frameworks suitable for the AI era: **SEQ** (speed, ease, quality - Google's developer productivity measure), **SPACE** (Satisfaction, Performance, Activity, Communication/Collaboration, Efficiency), and **HEART** (Happiness, Engagement, Adoption, Retention, Task success). Choose the framework that maps to your specific organisational goals; do not choose a single metric.

---

## Continuous Delivery

### Version-control prompts alongside code

DORA's 2025 AI Capabilities Model[^ai-caps] adds a fifth asset class to version control: prompts. The existing four - application code, application configuration, system configuration, build and configuration scripts - apply unchanged. Prompts must receive identical treatment: stored in version control, reviewed, tested, and auditable. An AI-assisted pipeline that uses unversioned prompts is not a reliable pipeline.

*→ See [Addendum: Version-controlling prompts](#addendum-version-controlling-prompts) at the end of this document for detailed guidance on file formats, repository structure, content guidelines, do/don't, and the team knowledge accumulation effect.*

### Apply batch-size discipline specifically to AI-generated changes

DORA's working-in-small-batches capability page[^small-batches] adds a specific AI note: AI tools are optimised for generating large, complete features - the opposite of what safe delivery requires[^safe-delivery]. The explicit rule:

- Features complete in **hours to a couple of days** - not weeks
- Individual tasks in **one day to one week** at most
- Avoid AI-generated massive pull requests: the cognitive load required to review a small chunk of machine-generated code is **higher per line** than reviewing human-written code, not lower

Flag PRs over 1,000 lines as requiring escalated review attention; the review load per line rises non-linearly with AI-generated content because reviewers cannot use familiarity and authorial intent to assist comprehension.

Use dark launching[^dark-launching] and feature toggles[^feature-toggles] to check small batches to trunk for features not yet user-visible, rather than accumulating changes on long-lived branches until the feature is complete.

### Require spec-driven development before AI code generation

Before generating code with AI, developers must draft a written plan - a specification in a markdown file - that covers the intent, the affected components, and the design decisions made. This document is committed with the pull request.

Two effects:

1. The spec becomes context the AI receives, grounding its output in the team's actual system rather than generic patterns
2. The spec creates an audit trail of human intent that reviewers can use to verify that what AI generated matches what was planned

Enforce this with a CI/CD pre-commit hook that checks for the presence of the spec file on AI-associated PRs. A team that cannot articulate a spec before generating code is in the "vibe coding" failure mode - building systems they cannot fully explain or validate.

### Deploy AI feedback to the author side, not the reviewer side

DORA (March 2026) is specific: AI-generated feedback on code should be delivered to the **author** during the writing phase, not to the reviewer during review. This is categorically more efficient:

- The author has the context to act on the feedback immediately
- The reviewer inherits a pre-screened change, reducing cognitive load
- Shifting AI feedback to the reviewer means the reviewer audits AI-against-AI output without the grounding that the author had

Implement AI pre-review in the IDE and as an author-side CI step. Do not position AI review as a reviewer tool.

---

## Verification Infrastructure

This section addresses P7 from the AI-era diagnosis: the shift of the primary bottleneck from code *writing* to code *verification*[^diagnosis].

### Build context-aware review agents

Rather than using AI to generate more code, teams should build **context-aware review agents** - automated systems that enforce organisational standards before human review begins. DORA (March 2026) names these as a direct countermeasure to the reviewer cognitive load problem.

The implementation pattern: deploy multiple sub-agents in parallel, each using a lower-powered model, each checking a narrow specific concern - security patterns, API standards, UI alignment, test coverage, style guide compliance. Narrow scope prevents hallucination accumulation and makes agent failures isolatable.

### Move from prompt engineering to context engineering

DORA names context engineering as the discipline that separates teams that extract value from AI from teams that adopt AI without commensurate benefit:

- **Prompt engineering** is a single command
- **Context engineering** is the system that automatically gathers relevant information - API docs, company policies, compliant code snippets, architectural decision records - and provides it as structured input to every AI interaction

Two implementation patterns:

1. **Retrieval-augmented generation (RAG):** a precise method for finding and providing only the most relevant, up-to-date information for the current request - not the entire documentation corpus
2. **Model Context Protocol (MCP) server:** intelligently selects, structures, and feeds only the most relevant context to the AI, rather than raw documents

Avoid feeding large raw documents into the AI's context window. This approach leads to hallucinations - outputs that sound confident but are factually false. Provide only the most specific context for the current request ("context harvesting").

### Curate AI training context from gold-standard repositories only

If using AI tools indexed against internal code, curate the corpus deliberately:

- Index only active, well-maintained repositories - not deprecated projects, archived codebases, or known-problematic legacy code
- An AI trained on deprecated patterns will replicate deprecated patterns at machine speed
- Build a specific "curriculum" of gold-standard repositories and enforce it

This is the internal-data equivalent of the pre-AI-era principle that test ownership determines test quality: AI context quality determines AI output quality.

### Implement least-privilege access for AI data retrieval

When connecting AI tools to internal data sources, implement access controls specifically:

- The retrieval mechanism must operate with **the user's own credentials**, not a shared service account or elevated permissions
- Never connect AI tools to internal data using a "super-user mode"
- Access violations should be logged and surfaced in review metrics

DORA identifies this as a primary security pitfall of AI-accessible internal data implementations.

---

## Architecture

### Build and operate a quality internal platform

DORA's 2025 AI Capabilities Model identifies a quality internal platform[^ai-caps] as one of seven capabilities that amplify the benefit of AI adoption. AI is an amplifier - it magnifies existing strengths and existing dysfunctions. A fragmented, poorly-abstracted internal platform becomes the substrate on which AI generates technical debt faster.

A quality internal platform, as measured by DORA, demonstrates these properties:

- Behaves predictably and as expected
- Effectively abstracts away infrastructure complexity
- Gives clear feedback on the outcome of every task
- Helps teams build and run reliable and secure applications
- Guides teams through required processes (code reviews, security sign-offs) without creating toil
- Is easy to use and provides the tools teams need to work independently
- Has a dedicated platform team that acts on feedback

The platform is the primary mechanism for reducing tool sprawl - the proliferation of disconnected AI tools that creates decision-making overhead and disrupts developer flow. Rather than asking "how do we add AI into individual tools?", the question is "how do we support the full developer journey holistically?"

### Maintain architectural decision records grounded in the domain

DORA research identifies a specific failure mode in AI-assisted architecture: AI produces documentation that sounds plausible but is not grounded in the actual system. This "fabricated documentation" pattern - including hallucinated Jira URLs, invented API specifications, and architectural recommendations that ignore actual constraints - is prevented by maintaining **Architectural Decision Records (ADRs)**:

- Document what alternatives were considered and why specific choices were made
- Store ADRs in version control alongside the code they describe
- Provide ADRs as part of the context engineering input for AI architectural work
- Require ADR creation or update as a condition of architectural PRs

ADRs serve two functions: they ground the AI in domain reality, and they give reviewers a human-authored source of truth against which to validate AI-generated architectural suggestions.

### Build healthy data ecosystems as an AI prerequisite

Connecting AI to poor-quality internal data produces poor-quality outputs at machine speed. DORA identifies data quality as a prerequisite for AI effectiveness, not a secondary concern:

- If a specific internal data point is needed, it must be retrievable in **under one hour of searching**
- Siloed data that cannot be accessed by the team cannot be used by AI either - AI-accessibility exposes data quality problems that were previously tolerable
- Pilot AI-accessible data with a single, high-value source (e.g., one service's API documentation) and use AI to help clean and structure it before scaling

**What "internal data" means in practice.** Internal data is the proprietary information that gives AI context your organisation's actual system rather than a generic approximation of it. It includes: internal codebases and architectural diagrams (so AI understands your structure, not a hypothetical one); API documentation and style guides (so generated code conforms to your standards); wikis, runbooks, and onboarding guides (so AI can answer "how does this service work?" rather than hallucinating an answer); operational metrics and incident logs (so AI-assisted debugging starts from real signals); and Architectural Decision Records (so AI recommendations are grounded in constraints the team has already evaluated and decided). Without these, the AI operates on the same generic knowledge any stranger to your codebase would have.

**Symptoms of a poor data ecosystem versus a good one.** A poor ecosystem is visible in specific failure modes: AI recommends deprecated patterns because it was indexed against old repositories; AI invents plausible-sounding but non-existent API endpoints because the real API is not documented; onboarding takes weeks because tribal knowledge is in individuals' heads and inaccessible to AI; and engineers spend significant time correcting AI output that confidently contradicts internal standards no external model could know. A healthy ecosystem produces the opposite: AI code suggestions reference the team's actual coding conventions without prompting; new contributors can get substantive answers from AI about unfamiliar parts of the codebase because documentation exists and is indexed; and AI-generated PRs require fewer review corrections because the model was given the right constraints before it generated.

---

## Lean Management and Process

### Enforce small batches specifically as an AI safety net

DORA is explicit (December 2025 update to the working-in-small-batches capability): working in small batches acts as a **critical safety net for AI adoption**. Higher AI adoption is associated with increased software delivery instability; small batches are the primary structural countermeasure.

The anti-pattern DORA names: AI tools are optimised for generating large, complete features. The temptation is to generate a massive pull request representing a complete feature and submit it for review. This trades individual efficiency for team verification overhead, and DORA finds the trade is consistently negative.

The enforcement mechanism: project timelines must explicitly account for the discrepancy between rapid AI prototyping and the effort required for production-grade quality. Do not reduce estimates before closing this gap.

### Adjust estimation to account for the prototype-to-production gap

DORA (March 2026) names a specific structural problem: while a prototype can be built almost instantly with AI, the final stretch - precision, edge-case handling, integration with internal systems - can take more effort than if the project had been built manually from the start.

Teams must:

- Explicitly estimate the production-integration phase separately from the prototype phase
- Not reduce project timelines because AI reduced initial prototyping time
- Actively track where prototype-to-production gap is consuming the throughput gain

### Do not punish teams for slower throughput during verification quality gates

DORA (March 2026) identifies a specific leadership failure mode: penalising teams for slower raw throughput when the slowdown is caused by necessary verification and quality gating. This creates pressure to rubber-stamp AI output, which accelerates technical debt accumulation and instability.

Leaders must be explicit that meaningful verification time is not waste - it is the activity that prevents the verification bottleneck from turning into a production incident.

### Track review load per reviewer

AI-assisted development transfers cognitive burden from authors to reviewers. Track review load per reviewer explicitly - total PRs reviewed per person per month - to surface reviewer fatigue before it manifests as rubber-stamping. The bottleneck has shifted from writing to reviewing; tooling and WIP limits must follow.

---

## Culture

### Publish a clear, communicated AI stance

DORA's AI Capabilities Model identifies **clear and communicated AI stance**[^ai-caps] as one of the seven amplifying capabilities. The specific components:

- **Mandatory or optional training** on how to use AI tools: the absence of training signals that the organisation has not formed a position
- **Brown bag sessions, peer demos, or informal walkthroughs** on AI use: DORA measures frequency; high-performing teams hold these regularly
- **Explicit policy on which AI tools are allowed**: teams must know which tools they can use without individual approval
- **Explicit policy on when vibe coding is acceptable and when human domain-expert review is mandatory**: the absence of this policy is the primary source of the invisible-AI-risk failure mode

The policy must be specific enough that an engineer can determine without asking their manager whether a given use of AI requires additional review.

### Pair junior engineers with senior mentors for AI architectural review

DORA (March 2026) names a specific practice for preventing the expertise paradox[^diagnosis] from degrading team capability over time:

- Engineering leaders actively pair junior engineers with senior mentors specifically to review AI-generated architectural decisions
- This is not general mentorship; it is domain-expertise transfer for the specific task of validating AI output
- Encourage manual coding for complex system components to ensure foundational understanding is built - not as a permanent constraint, but as a deliberate investment in the productive struggle that builds expertise

The failure mode this prevents: an engineer develops false confidence by successfully using AI in an unfamiliar domain, without developing the expertise to know when the AI's architectural decisions are wrong. DORA names this "the blind leading the blind."

### Build an AI community of practice

DORA recommends a structured mechanism for sharing AI learning across the organisation:

- Establish a **generative AI community of practice** with explicit membership, meeting cadence, and shared documentation of what is working and what is not
- Base sharing on experiments conducted by teams, not vendor briefings or conference talks
- Document failures alongside successes - in a Westrum generative culture, AI failure modes are shared rather than hidden

The community of practice is the mechanism through which AI-related knowledge scales across teams that have not yet encountered a given failure mode.

### Establish a baseline before introducing AI tooling

DORA's guide explicitly prescribes sequencing: **establish a DORA Quick Check baseline before introducing AI**, not after. Without a baseline, the team cannot distinguish between AI-driven improvement and baseline variation, cannot measure the J-curve productivity dip during adoption, and cannot make an evidence-based case for continued investment.

Measure: deployment frequency, lead time, MTTR, change failure rate. Bookmark the Quick Check result. Re-measure at fixed intervals after AI introduction.

---

## Transformational Leadership

### Communicate a clear AI strategy with role-level specificity

DORA research found that 90% of technology professionals now use AI at work. The absence of a communicated organisational AI strategy does not prevent adoption - it prevents coherent adoption. The strategy must be specific enough to answer:

- Which AI tools are approved for which use cases
- When is AI-generated code acceptable without additional review, and when is mandatory human domain-expert review required
- How will the organisation measure the impact of AI adoption (and therefore when to adjust the approach)

Generic AI strategies - "we embrace AI" or "use AI responsibly" - provide no decision-making guidance at the team level.

### Accept and communicate the J-curve

DORA names the **J-curve effect** as a predictable pattern in AI adoption: productivity dips initially as teams invest time in learning, adjusting processes, and facing unforeseen challenges. Leaders who do not communicate this expectation create pressure to demonstrate immediate productivity gains, which drives teams toward superficial adoption - adopting AI for visible output metrics without building the underlying capabilities that make AI effective.

Specific leadership actions:

- Communicate the expected productivity dip before it occurs
- Do not punish teams for initial throughput decline during genuine AI capability building
- Define the indicators that distinguish productive capability-building from stalled adoption

### Track the team's AI skill development, not just AI tool usage

DORA research identifies skill degradation as a structural risk of AI adoption - specifically, that AI tools can allow engineers to produce output in unfamiliar domains without developing the foundational understanding needed to evaluate that output. Leaders must track both:

- AI **tool adoption rate** (the shallow signal)
- Team **capability development** in the domains AI is being used to assist (the signal that matters)

A team that generates AI architectural decisions for a domain no one on the team understands has not become more capable - it has become more fragile.

### Actively invest in the quality internal platform as an AI prerequisite

Leaders must treat internal platform quality as a prerequisite for effective AI adoption, not a separate infrastructure concern. DORA's research shows that AI amplifies existing strengths and dysfunctions. A team operating on a fragmented, poorly-abstracted platform will generate technical debt faster with AI - not less. Platform investment before or concurrent with AI adoption is not optionality; it is the condition under which AI delivers positive returns.

---

## How the Actions Connect to the AI-Era Diagnoses

| AI-era diagnosis | Actions that address it |
|---|---|
| **P6: AI amplifies existing dysfunctions** | Quality internal platform; clear AI stance; Westrum generative culture; leaders communicate J-curve |
| **P7: Verification bottleneck shift** | Context-aware review agents; AI feedback to author side not reviewer; review load tracking; human-in-the-loop measurement |
| **P8: Invisible AI risk** | Three-way risk signal (authorship × review × contributor history); rubber-stamp detection; spec-driven development |
| **P9: Rework masquerading as velocity** | Effective throughput metric (merge frequency minus rework); high/medium/low rework thresholds; replace output dashboards with VSM signals |
| **P10: Deskilling and false expertise** | Spec-driven development; junior/senior pairing for AI architectural review; manual coding for complex components; ADRs |
| **P11: Signal reliability in flux** | Explicit measurement frameworks (SEQ/SPACE/HEART); DORA baseline before adoption; version-controlled prompts; audit-trail specs |

---

## What This Document Is Not

- **Not the guiding policy.** The guiding policy - verify AI output with the same rigour applied to human output; engineer context rather than accept defaults; treat AI as amplifier not author - is the layer above. This document implements it with specific DORA-prescribed actions.
- **Not sequenced by default.** The diagnosis-to-action table above identifies causal links. Use it to find the action that unblocks the most others in your specific context.
- **Not a technology buying guide.** DORA does not recommend specific AI tools. The actions above apply regardless of which AI assistant, code generation tool, or review platform your team uses. The architectural patterns (RAG, MCP, context engineering) apply across providers.
- **Not the pre-AI-era version.** The pre-AI prescriptions from *Accelerate* (2018) - trunk-based development, full pipeline automation, CAB elimination, security shifting left - remain valid and are prerequisite conditions for the AI-era actions above. A team that has not implemented continuous delivery cannot safely operate AI-assisted development. See `accelerate_coherent_actions_pre_ai_era.md` for those foundations.

---

## Addendum: Version-controlling Prompts

*Expands [Version-control prompts alongside code](#version-control-prompts-alongside-code) in the Continuous Delivery section above.*

### Why this is new and why it matters

In pre-AI delivery, the pipeline's behaviour was determined entirely by code and configuration - both already in version control. Now, a third determinant exists: the prompts and agent instruction files that shape what AI tools generate, how AI assistants respond, and what constraints they operate under. If those prompts live only in an individual developer's IDE settings, a SaaS tool's cloud configuration, or an undocumented mental model of "how to talk to the model", the pipeline has a hidden, unreviewed, unversioned input. Two developers working on the same codebase will get different AI behaviour, and no audit trail exists when a prompt change causes a regression.

DORA's version control capability page (updated January 2026) is explicit: teams should "version AI prompts to share knowledge and create audit trails, as well as agent configuration files to establish team norms and guardrails for AI assistants." The security literature reinforces the risk: between 25% and 70% of working coding outputs from leading models contain vulnerabilities (BaxBench, 2025). Research on prompt engineering for secure code generation found that simply adding the word "secure" to a prompt reduced vulnerability density by 28–43% across GPT-3/3.5/4. A prompt that says "you are a developer who is very security-aware and avoids weaknesses in the code" reduced vulnerable output by 47–56% on average (Wiz/research, 2025). Those are not facts that should live in one engineer's muscle memory; they are team policy, and team policy belongs in version control.

### What to version-control

Every AI tool in common use has a supported convention for storing persistent instructions:

| Tool | Convention file |
|---|---|
| GitHub Copilot | `.github/copilot-instructions.md` (repository custom instructions) |
| Claude Code | `CLAUDE.md` (project root or subdirectory) |
| Gemini CLI | `GEMINI.md` (hierarchical - global, workspace, and directory-scoped) |
| OpenAI Codex | `AGENTS.md` |
| Cursor | `.cursor/rules/` (scoped rule files per directory) |
| Windsurf / Cline | Rules files in the project root |
| Aider | Conventions file (`.aider.conf.yml` or inline) |

In addition to these tool-specific convention files, version-control:

- **Prompt templates** used in automated pipelines - the system prompts and few-shot examples for any AI step in CI/CD
- **Agent task definitions** for agentic workflows - the goals, constraints, and tool permissions given to autonomous agents
- **Spec files** written before code generation (see [spec-driven development](#require-spec-driven-development-before-ai-code-generation) above) - these are the human intent record attached to AI-generated PRs

### Practical structure in a repository

A usable convention for teams that use multiple AI tools:

```
.agents/
  AGENTS.md          # OpenAI Codex / Copilot agent configuration
  instructions/      # Custom instruction files by topic or language
    python.md
    security.md
    api-standards.md
CLAUDE.md            # Claude Code project context (project root)
GEMINI.md            # Gemini CLI context (project root)
.github/
  copilot-instructions.md  # GitHub Copilot repository instructions
prompts/
  pipeline/          # System prompts for automated CI/CD AI steps
    pr-review.md
    security-scan.md
```

Gemini CLI supports a hierarchical system - it loads `GEMINI.md` from the project root, then from subdirectories as the AI accesses files within them. This means a service under `services/payments/` can have its own `GEMINI.md` with payment-domain-specific constraints, loaded only when the AI works in that directory. The same pattern applies to Cursor's `.cursor/rules/` scoped rules. Structure your convention files to match the information scoping of your codebase: organisation-wide rules in the root, service-specific rules at the service level.

### What to put in these files

A well-formed convention file covers four categories:

1. **Coding style and standards** - indentation, naming conventions, import ordering, preferred idioms for the language and framework in use
2. **Security constraints** - explicit instructions not to hard-code secrets, always validate inputs, use parameterised queries, prefer approved libraries for auth and crypto, follow OWASP Top 10 mitigations; research shows these direct instructions substantially reduce vulnerability density
3. **Architecture and API standards** - which internal APIs to use (not invent), which deprecated patterns to avoid, approved libraries vs. prohibited ones
4. **Scope and permission limits for agents** - for agentic workflows, explicit instructions on what the agent is and is not permitted to do: "do not create new files outside the src/ directory"; "do not modify migrations without explicit instruction"; "do not call external APIs not already in use"

Keep each file under 500 lines. Beyond that length, the model's attention dilutes, and atomic rules become muddled. Break large convention files into scoped sub-files imported by reference.

### Do and don't

**Do:**
- Commit convention files with the first PR that uses any AI tool on that codebase - not retroactively after a problem occurs
- Review changes to convention files in pull requests, the same way you review any other configuration change; a change to `CLAUDE.md` changes the behaviour of every developer's AI on that repository
- Include security-oriented language explicitly; research consistently shows it reduces vulnerability density even in models that know security principles - the instruction activates more cautious generation behaviour
- Scope rules to the directory level where they are relevant; broad rules applied everywhere become noise that the model ignores
- Test convention file changes by verifying that AI output changes as expected before merging - treat them as tested configuration, not documentation

**Don't:**
- Store convention files only in IDE cloud sync settings, a team wiki, or an individual's dotfiles; if it is not in the repository, it is not the team's convention - it is one person's
- Let convention files become stale; an outdated `CLAUDE.md` that references deprecated APIs or obsolete patterns actively teaches the AI to produce wrong output
- Write vague instructions like "follow best practices" or "be careful with security"; these are not actionable and do not change model behaviour; name the specific practices and the specific weaknesses to avoid
- Rely on convention files alone as a security control; they reduce risk but do not eliminate it; automated SAST scanning, dependency analysis, and secrets detection remain necessary

### The team knowledge accumulation effect

The deeper value of convention files in version control is compounding: each time the team discovers that the AI produces a wrong pattern - using a deprecated library, suggesting an internal API that no longer exists, generating SQL that bypasses ORM escaping - they add a rule to the convention file. That knowledge then applies to every future AI interaction on the codebase, for every team member, including those who joined after the incident. The alternative is that the same wrong pattern is corrected individually by each developer who encounters it, accumulates in no shared record, and recurs as team composition changes.

---

## Footnotes

[^kernel]: **Rumelt's strategy kernel** - the three-part structure Richard Rumelt describes in *Good Strategy Bad Strategy* (2011).

    - **Diagnosis** - names the specific obstacle causing failure.
    - **Guiding policy** - the overall approach chosen to cope with it.
    - **Coherent actions** - specific, mutually reinforcing decisions that implement the policy.

    Coherent actions differ from a to-do list in one way: they reinforce each other. Each action makes the others more effective. A list of independent AI tools to adopt is not coherent action - it is a procurement list with good intentions.

[^dora-metrics]: **DORA four key metrics** - the throughput and stability measures that have been the anchor of DORA research since 2014.

    - **Deployment frequency** - how often code is deployed to production.
    - **Lead time for changes** - elapsed time from commit to production.
    - **Time to restore service (MTTR)** - how quickly teams recover from production failures.
    - **Change failure rate** - percentage of deployments that cause a degraded service or require remediation.

    In the AI era, these metrics remain valid but must be interpreted alongside AI-specific signals. Higher AI adoption correlates with both higher throughput and higher instability - making the change failure rate and MTTR more important as counterweights.

[^ai-caps]: **DORA AI Capabilities Model** - published November 2025. Identifies seven capabilities that amplify the positive impact of AI adoption on team and organisational performance.

    The seven capabilities: (1) AI adoption × user-centric focus, (2) strong version control practices (including prompts), (3) AI-accessible internal data, (4) working in small batches, (5) clear and communicated AI stance, (6) quality internal platform, (7) healthy data ecosystems.

    The model's central finding: AI is an amplifier. It magnifies existing organisational strengths and existing dysfunctions in equal measure. Investment in these seven capabilities determines whether AI amplifies the strengths or the dysfunctions.

[^small-batches]: **Working in small batches - AI note** - from the DORA capabilities page, updated December 2025.

    "This discipline is especially important when using AI coding assistants. While AI excels at generating large blocks of code quickly, large changes are difficult to review, test, and integrate safely. By enforcing small batches, you shift the developer's focus from raw code generation to thoughtful decomposition and verification."

    And: "AI adoption often leads to increased software delivery instability; working in small batches acts as a critical countermeasure to this risk, ensuring that the increased velocity from AI translates into value rather than chaos."

[^diagnosis]: **AI-era diagnoses** - the six additional failure modes identified in `accelerate_problem_diagnosis_in_ai_era.md`, extending the five original *Accelerate* diagnoses.

    - P6: AI amplifies existing dysfunctions
    - P7: Verification bottleneck shift - the primary constraint moves from writing code to verifying AI output
    - P8: Invisible AI risk - fully AI-authored, self-merged, first-contributor PRs are not surfaced by existing review signals
    - P9: Rework masquerading as velocity - AI inflates PR count while rework PRs accumulate unseen
    - P10: Deskilling and false expertise - engineers produce outputs in domains they cannot fully evaluate
    - P11: Signal reliability in flux - traditional activity metrics are insufficient as AI adoption scales

[^safe-delivery]: **Safe delivery** - the set of technical and process practices that allow teams to release changes to production frequently, with high confidence and low blast radius when failures occur.

    Canonical source: Forsgren, Humble, and Kim, *Accelerate* (2018), chapters 4–5 - 24 capabilities across five domains (continuous delivery, architecture, product and process, lean management, culture) empirically validated as drivers of software delivery performance.

    The four practices most directly implied by "safe delivery" in the context of batch size:

    - **Trunk-based development** - all developers integrate to a shared mainline at least daily
    - **Continuous integration** - every change triggers an automated build and test run
    - **Deployment pipeline automation** - build, test, and deploy steps automated end-to-end
    - **Working in small batches** - changes small enough to be deployed and rolled back safely

    Full detail: [`accelerate_coherent_actions_pre_ai_era.md`](./accelerate_coherent_actions_pre_ai_era.md) in this repository. Current maintained definition: DORA's [Continuous Delivery capability page](https://dora.dev/capabilities/continuous-delivery/).

[^dark-launching]: **Dark launching** - deploying new code to production in a state where it executes but its effects are invisible to end users. The code runs on real production traffic and infrastructure, exercising real data paths, but the output is discarded or routed internally rather than surfaced to users. This allows teams to validate behaviour under production conditions - load, data volume, edge cases - before the feature is user-visible. Dark launching is distinct from a feature toggle: it is about validating correctness under real conditions, not about controlling user access. The term originates from Facebook's infrastructure practices (c. 2009) and is documented in Humble and Farley, *Continuous Delivery* (2010), chapter 10, and DORA's [Feature Flags capability page](https://dora.dev/capabilities/feature-flags/).

[^feature-toggles]: **Feature toggles** (also called feature flags or feature switches) - a software mechanism that allows a code path to be enabled or disabled at runtime without a deployment. A toggle wraps new or incomplete functionality behind a conditional; the toggle state is controlled by configuration, a remote flag service, or operator action rather than by deploying new code. This allows trunk-based development teams to merge incomplete features to the mainline - satisfying the continuous integration requirement of daily integration - without exposing those features to users until they are ready.

    Three common toggle types relevant here:

    - **Release toggles** - hide incomplete features from users; removed once the feature ships
    - **Experiment toggles** - enable A/B testing or canary rollouts to a subset of users
    - **Permission toggles** - gate features by user role, subscription tier, or geography

    Canonical reference: Hodgson, P. (2017). "Feature Toggles (aka Feature Flags)." *martinfowler.com*. DORA's [Feature Flags capability page](https://dora.dev/capabilities/feature-flags/) covers the practice in the context of continuous delivery.
