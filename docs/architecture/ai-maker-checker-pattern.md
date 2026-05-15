# Architectural Pattern: The AI Maker-Checker

## 1. The Notion

The Maker-Checker pattern (often referred to in AI literature as the Generator-Evaluator or Critique-Revision pattern) is a multi-agent architectural design used to improve the reliability, accuracy, and safety of Generative AI outputs.

It involves separating the execution of a task into two distinct roles handled by either different LLM instances, different prompts, or entirely different models:

- **The Maker (Generator):** Responsible for taking the initial user prompt and generating a draft output (code, text, data transformation). Its objective is purely creative and task-oriented.
- **The Checker (Reviewer):** Responsible for analysing the Maker's draft against a specific rubric, set of constraints, or guidelines.

> **Crucial Distinction:** Unlike a simple quality gate (which acts as a binary pass/fail filter), the Checker acts as a reviewer. If it finds flaws, it does not simply reject the output; it generates actionable, natural language feedback detailing exactly what is wrong and how to fix it. This feedback is fed back to the Maker in an iterative loop until the Checker approves the output or a maximum iteration limit is reached.

The implementation of the Maker-Checker pattern addresses the **"generation-verification asymmetry"** — a phenomenon where an AI model may lack the capacity to generate a perfect solution in a single pass but possesses the discriminative ability to identify flaws in a provided response when guided by an evaluation rubric. By separating the creative act of generation from the analytical act of review, organisations can achieve significant improvements in output reliability. Research indicates that approximately 40% of data extractions improve after a single feedback cycle, and in highly technical tasks such as code translation, iterative feedback loops can boost performance by up to 50% compared to non-retrieval baselines.

---

## 2. Mechanics of the Feedback Loop: Generation, Review, and Rectification

The operational heart of the Maker-Checker pattern is the iterative loop, which typically consists of four distinct stages: initial generation, critique, reflection, and revision. In the initial stage, the Maker agent processes a user request to produce a draft. This draft is then passed to the Checker agent, which evaluates the output against a predefined set of criteria, such as factual consistency, coverage gaps, and tone alignment.

If the Checker identifies an error, it generates structured feedback. For instance, in generating a Geotechnical Baseline Report (GBR), the Checker might flag a missing baseline statement for groundwater elevation or a malformed JSON object. This feedback is then injected into the Maker's context for the next iteration. This stage is often referred to as **"Reflexion"**, where the Maker reflects on the Checker's critique to identify the underlying reasoning failure. The loop continues until the Checker issues an "approval" signal or a maximum number of retries is reached — typically three to five to avoid infinite loops and excessive token consumption.

### The Workflow Loop

1. **Initialisation:** System sends task prompt to the Maker.
2. **Generation:** Maker produces Draft V1.
3. **Review:** System sends Draft V1 + Evaluation Rubric to the Checker.
4. **Feedback:** Checker analyses Draft V1. If flaws exist, it outputs a critique (e.g., "The tone is too informal, and paragraph 2 hallucinates a statistic.").
5. **Rectification:** System appends the Checker's critique to the Maker's context window and requests a revision.
6. **Iteration:** Maker produces Draft V2. Steps 3–5 repeat until the Checker outputs a `PASS` token or the system hits a loop limit.

---

## 3. Optimization of Model Parameters for Collaborative Roles

A critical insight for implementing this pattern effectively is the **deliberate divergence of model configurations** for the Maker and Checker agents. If both agents utilise the same model and the same temperature settings, they are prone to the same biases and hallucinations, rendering the feedback loop ineffective.

Professional implementations generally configure the Maker with a higher temperature (0.7–1.0) to encourage creative problem-solving and diverse output generation. Conversely, the Checker is set to a low temperature (0.0–0.2) to ensure deterministic, critical, and consistent evaluation. Furthermore, the agents are often assigned distinct "personas" to further differentiate their cognitive roles: the Maker may be cast as a "Creative Content Generator" or "Technical Specialist," while the Checker assumes the role of a "Senior Auditor," "Legal Compliance Officer," or "Technical Reviewer."

| Agent Role | Temperature Setting | Tool Access | Primary Responsibility |
|---|---|---|---|
| Maker | 0.7 – 1.0 | High (RAG, Browsers, APIs) | Content creation and initial synthesis |
| Checker | 0.0 – 0.2 | Low (Reference rubrics) | Identifying errors and providing feedback |
| Optimizer | 0.3 – 0.5 | Moderate | Synthesizing feedback into the final draft |

---

## 4. When to Use

This pattern introduces latency and doubles (or triples) token costs. Therefore, it should only be deployed when the benefits outweigh the overheads.

- **Asymmetric Difficulty Tasks:** Use this when generating an answer is hard, but verifying it is comparatively easy. For example, writing a complex SQL query (hard to generate) versus checking if the query uses forbidden tables or lacks JOIN limits (easy to check).
- **High-Stakes Content Generation:** Legal drafting, Geotechnical Baseline Reports (GBRs), or compliance-heavy communications where hallucinations or missing baseline parameters carry significant business risk.
- **Enforcing Strict Formatting:** When the output must adhere to a rigid schema (e.g., complex JSON structures) that a single zero-shot generation frequently fails to produce.
- **Separation of Model Capabilities:** When you want to use a cheaper, faster model for the heavy lifting of drafting (the Maker), and a more expensive, highly reasoned model for the rigorous reviewing (the Checker).

---

## 5. When NOT to Use

Do not apply this pattern universally. It is an anti-pattern in several scenarios:

- **Latency-Sensitive Applications:** Real-time chatbots or autocomplete features. The user will not wait for two AI models to debate with one another before receiving a response.
- **Deterministic / Low-Risk Tasks:** Simple summarisation, basic data extraction, or casual content generation where minor imperfections are acceptable.
- **Highly Subjective Creative Writing:** Having an AI "correct" another AI's creative fiction often leads to homogenised, sterile text. The Checker tends to strip away nuance in an attempt to adhere strictly to a prompt.
- **Cost-Constrained Environments:** Every iteration consumes tokens. If your budget is tight, optimise your initial prompt (zero-shot or few-shot) rather than building an iterative Maker-Checker loop.

---

## 6. Implementation Checklist

If you are committing to this architectural decision, ensure the following constraints are built into your system design:

- [ ] **Strict Loop Bounds (The Circuit Breaker):** You must implement a maximum iteration counter (e.g., `MAX_RETRIES = 3`). LLMs can get stuck in infinite loops of apologising and failing to fix the core issue.
- [ ] **Distinct Personas/Prompts:** The Maker and Checker must have completely isolated system prompts. The Checker's prompt should ideally contain a highly structured grading rubric or a checklist.
- [ ] **State Management:** The architecture requires retaining conversational state. When passing feedback back to the Maker, ensure you pass the original prompt, the failed draft, and the Checker's feedback in a clear, structured format (e.g., using Markdown or XML tags).
- [ ] **Fallback Mechanism:** Define what happens when `MAX_RETRIES` is hit. Do you return the best draft to the user with a warning flag? Do you fail gracefully and return an error?
- [ ] **Checker Sovereignty:** The Checker must have a deterministic way of signalling approval. Instruct the Checker to output a specific system token (e.g., `<STATUS: APPROVED>`) when no rectifications are needed, so your application layer knows exactly when to break the loop.
- [ ] **Temperature Tuning:** Set the Maker to a slightly higher temperature (e.g., 0.4–0.7) to allow for creative problem-solving, but set the Checker to a temperature of `0.0` to ensure strictly deterministic, objective evaluations.

---

## 7. The Domain-Expert Gate (Redline-Specific Extension)

For domain-specific use cases in Redline — where the system's output carries geotechnical domain claims — the AI Maker-Checker loop is insufficient on its own. The LLM Checker can confirm that an output is internally consistent and matches the criterion, but it cannot confirm that the domain claim in the user-facing explanation is factually correct.

A third gate is required, held by a human domain expert (Graeme), that sits outside the automated loop.

### Gate 3 — Domain Accuracy of User-Facing Explanation

**What it checks**: After the Checker has issued a `PASS` and the test suite confirms the detection criterion is met, Graeme reviews the user-facing explanation — the text the system shows to the practitioner explaining *why* the standard citation was flagged. This explanation must be domain-accurate, not merely correct-in-output-label.

**Why the LLM Checker cannot hold this gate**: A detection LLM can output the correct flag ("NZS 4431:1989 is outdated") via reasoning that is domain-confused ("flagged because 1989 is before 2000"). If that confused reasoning surfaces in user-facing language, the explanation shipped to a practitioner carries a false domain claim. The AI Checker does not detect this — it sees a correct output label and issues `PASS`.

**Gate ownership**: Graeme (Principal Geotechnical Engineer). Blocking — the use case does not ship until Gate 3 clears.

**What Gate 3 does not replace**: Mark's pass/fail confirmation against the product criterion is separate. Both gates must clear independently before release.

**Interaction with the loop:**

```
Maker → Checker loop (automated, iterative)
                    ↓
         Mark: pass/fail against criterion
                    ↓
         Graeme: domain accuracy of user-facing explanation  ← blocking
                    ↓
         Use case approved for release
```

See `docs/product/prds/acceptance-test-ownership-policy.md` for the full RACI and workflow sequences across Case 1 (outdated version), Case 2 (fabricated standard), and Case 3 (wrong jurisdiction).
