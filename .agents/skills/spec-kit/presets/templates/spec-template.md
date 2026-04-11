# Feature Specification: [FEATURE NAME]

**Branch**: `[branch-name]`
**Created**: [DATE]
**Status**: Draft

## Scenarios (mandatory)

<!-- Prioritize using RICE scoring. Order scenarios by score (highest first). -->

### Scenario 1 -- [Title]

[Describe the scenario in plain language]

| Reach | Impact (0.5-3) | Confidence (%) | Effort (person-days) | RICE Score |
| ----- | -------------- | -------------- | -------------------- | ---------- |
| ?     | ?              | ?              | ?                    | ?          |

**Independent test**: [How to verify this works on its own]

**Acceptance criteria**:

1. **Given** [initial state], **When** [action], **Then** [expected outcome]
2. **Given** [initial state], **When** [action], **Then** [expected outcome]

---

### Scenario 2 -- [Title]

[...]

---

### Edge Cases

- What happens when [boundary condition]?
- How does the system handle [error scenario]?

## Requirements (mandatory)

### Functional Requirements

- **FR-001**: System MUST [capability]. [Rationale if non-obvious]
- **FR-002**: System MUST [capability].
- **FR-003**: [NEEDS CLARIFICATION: specific question about ambiguity]

<!-- Max 3 NEEDS CLARIFICATION markers. Beyond that, use clarify to resolve. -->

### Key Entities (if data is involved)

- **[Entity]**: [What it represents, key attributes, relationships -- no implementation detail]

## Success Criteria (mandatory)

- **SC-001**: [Measurable outcome]
- **SC-002**: [Measurable outcome]

## Assumptions

- [State the assumption in plain English. Explain why this gap was filled this way
  and what would change if the assumption turned out to be wrong.]

## Risks

| Risk                    | Impact                                        | Mitigation             |
| ----------------------- | --------------------------------------------- | ---------------------- |
| [What could go wrong]   | [What a stakeholder would observe]            | [How to handle it]     |
