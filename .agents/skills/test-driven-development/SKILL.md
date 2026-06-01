---
name: test-driven-development
description: Use when implementing any feature or bugfix, before writing implementation code
---

## Boundary Contract

### Applies To
- Any feature or bugfix implementation -- tests must be written before code

### Produces
- RED-GREEN-REFACTOR cycle: failing test, minimal passing implementation, refactored code

### Does Not Cover
- Unit testing conventions (`python-testing-unit`)
- API testing conventions (`python-testing-api`)
- Debugging (`systematic-debugging`)

## When to Use

**Always:**
- New features
- Bug fixes
- Refactoring
- Behavior changes

**Exceptions (ask the user):**
- Throwaway prototypes
- Generated code
- Configuration files

Thinking "skip TDD just this once"? Stop. That's rationalization.


See `procedures/test-driven-development.md` for detailed rules, examples, and extended reference.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Writing implementation code before a failing test | No code without a red test first — this is the Iron Law; delete and restart if violated |
| Writing multiple failing tests before any implementation | Write one failing test, make it pass, then write the next — the RED-GREEN cycle is one test at a time |
| Refactoring while a test is red | Refactor only when all tests are green; red + refactor means two unknowns at once |