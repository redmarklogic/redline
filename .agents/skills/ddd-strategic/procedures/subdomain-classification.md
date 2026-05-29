# Subdomain Classification Procedure

**Parent skill:** `ddd-strategic`
**Source:** Evans (*DDD*), Khononov (*Learning DDD*)

---

## When to Classify

- When adding a new subdomain to `docs/architecture/domain-model.md`.
- When reviewing whether a Supporting subdomain has become Core (competitive advantage shift).
- During annual strategy review (the Strategy Advisor-triggered).

## Steps

### 1. Name the subdomain

Use a domain noun, not a technical term. Example: "Geotechnical Analysis Engine", not "ML Pipeline".

### 2. Answer the four criteria

| Criterion | Question |
|---|---|
| **Competitive advantage** | Does this capability differentiate us from competitors? Would competitors struggle to replicate it? |
| **Complexity** | Is the logic inherently complex? Does it require deep domain expertise? |
| **Change frequency** | How often does this area change? Weekly? Monthly? Yearly? |
| **Buyability** | Could we use an off-the-shelf solution? At what cost to differentiation? |

### 3. Classify

| Type | Competitive advantage | Complexity | Volatility | Build or buy |
|---|---|---|---|---|
| **Core** | Yes | High | High | Build in-house |
| **Supporting** | No | Moderate | Moderate | Build (simple) or buy |
| **Generic** | Commodity | Low-moderate | Low | Buy off-the-shelf |

### 4. Record with rationale

Add a row to the subdomain table in `docs/architecture/domain-model.md` with a **Rationale** column explaining the classification decision. The rationale must reference at least one of the four criteria.

### 5. Choose tactical patterns

| Classification | Pattern choice | DDD investment |
|---|---|---|
| **Core** | Full DDD: aggregates, domain events, rich model, ACL at boundaries | Maximum |
| **Supporting** | Transaction scripts, thin domain layer, simple validation | Moderate |
| **Generic** | Off-the-shelf libraries, no custom domain model | Minimal |

This table is also in `python-domain-modeling` skill's Subdomain Classification section. Keep both in sync.

---

## Reclassification Triggers

A subdomain may need reclassification when:

- A competitor builds a comparable feature (Core may become Supporting).
- A generic solution emerges for what was previously custom (Core/Supporting may become Generic).
- Market feedback reveals an unexpected competitive advantage (Supporting may become Core).
- The domain expert (the Domain Expert) identifies new complexity in a previously simple area.

Record reclassification decisions as ADRs in `docs/adr/`.
