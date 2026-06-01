---
name: python-crewai
description: Use when building CrewAI agents, tasks, flows, or output models in this repo
---

## Boundary Contract

### Applies To
- CrewAI agent, task, flow, and output model code under `src/`

### Produces
- Consistently structured CrewAI components following repo directory and naming conventions

### Does Not Cover
- General class design (`python-class-design`)
- Domain modeling (`python-domain-modeling`)
- Unit testing conventions (`python-testing-unit`)


See `procedures/python-crewai.md` for detailed rules, examples, and extended reference.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Defining output schema inline with dict instead of a Pydantic model | Use a typed BaseModel as the task output_pydantic — enables validation and serialisation |
| Giving an agent a tool it doesn't need | Scope tools per agent; unused tools increase hallucination surface |
| Using blocking I/O in a CrewAI task without async | Wrap in a thread if the tool is synchronous; don't block the event loop |