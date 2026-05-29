# Verification Gate (Lifecycle: after_implement)

<!-- Extension: verification-gate -->

This hook fires at the end of the `implement` workflow phase.

Load and apply the `verification-before-completion` skill. The Iron Law applies:

```
NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE
```

Before claiming implement is complete, execute the Gate Function:

1. **IDENTIFY** — What command proves this claim?
2. **RUN** — Execute the full command fresh in this message
3. **READ** — Full output, check exit code, count failures
4. **VERIFY** — Does output confirm the claim?
5. **ONLY THEN** — Make the claim with evidence attached

Skipping any step is a violation. Evidence before assertions, always.

---

This command is a lifecycle dispatcher (ADR-013, Option C).
The authoritative procedure is `.agents/skills/verification-before-completion/SKILL.md`.
