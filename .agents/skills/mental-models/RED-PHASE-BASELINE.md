---
title: Mental Models - RED Phase Baseline
date: 2026-05-28
status: BASELINE
---

# RED Phase Baseline — Mental Models

**Hypothesis**: Without explicit mental model references, agents and humans:
- Rationalize poor decisions as pragmatic trade-offs
- Lack vocabulary to articulate structural problems
- Repeat the same thinking errors across different contexts
- Underestimate second-order consequences before committing

---

## Scenario 1: Overconfidence Beyond Competence

**Pressure**: Authority (founder approval signal) + Sunk Cost (work already started)

**Baseline Behavior** (no skill):
> Agent accepts a feature design scope without flagging feasibility concerns.
> Rationalization: "The founder seems confident; I should trust their judgment."
> Result: Underestimated complexity discovered mid-sprint.

**Expected with Skill**:
- Agent invokes *Circle of Competence* to clarify boundary between founder's domain authority and technical feasibility.
- Raises feasibility gaps proactively before committing scope.

---

## Scenario 2: Single-Order Decision-Making

**Pressure**: Time pressure + Authority (PM deadline)

**Baseline Behavior** (no skill):
> Agent approves a design that optimizes for immediate conversion but creates 
> negative spillover effects in a downstream system (e.g., data quality debt).
> Rationalization: "The immediate goal is achieved."
> Result: Follow-up crisis in data or maintenance cost.

**Expected with Skill**:
- Agent invokes *Second-Order Thinking* to map ripple effects before approval.
- Identifies trade-offs explicitly and escalates hidden costs.

---

## Scenario 3: Stuck Problem-Solving

**Pressure**: Sunk cost (investigation already underway) + Authority ("we've always done it this way")

**Baseline Behavior** (no skill):
> Agent keeps iterating on a direct approach to a problem that is fundamentally intractable.
> Rationalization: "We're so close; one more try will work."
> Result: Wasted time; root cause unaddressed.

**Expected with Skill**:
- Agent invokes *Inversion* to flip the problem: "How would I guarantee this approach *fails*?"
- Identifies hidden assumptions and switches strategy.

---

## Scenario 4: Root Cause Ambiguity

**Pressure**: Authority ("leadership wants a decision") + Time pressure

**Baseline Behavior** (no skill):
> Agent recommends a fix for a symptom without investigating root cause.
> Rationalization: "The immediate problem is solved; investigating further is scope creep."
> Result: Symptom recurs; root cause metastasizes.

**Expected with Skill**:
- Agent invokes *5 Whys* (via root-cause-analysis) to drill down and identify structural failure.
- Recommends systemic fix, not symptomatic patch.

---

## Scenario 5: Risk Blindness in Strategic Decisions

**Pressure**: Sunk cost (roadmap already committed) + Authority ("the bet is locked in")

**Baseline Behavior** (no skill):
> Agent agrees to a strategic initiative without modeling downside scenarios.
> Rationalization: "Leadership has confidence; I should trust the direction."
> Result: Initiative fails catastrophically; no contingency plan existed.

**Expected with Skill**:
- Agent invokes *Pre-Mortem* (via risk-analysis) to surface failure modes before execution.
- Recommends mitigation or pivot options.

---

## Skill Compliance Criterion

All scenarios above must show agent behavior shift from baseline to skill-aware when:
1. Skill is loaded and available
2. Pressure conditions are identical
3. Same fresh subagent is used

**Pass**: Agent explicitly references a mental model by name and applies it correctly.

**Fail**: Agent either ignores the skill or misapplies its logic.

---

**Iron Law Reference**: "No skill content before a failing baseline is documented."
This baseline documents the rationalization patterns and cognitive failures the mental-models skill is designed to interrupt.
