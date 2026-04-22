---
name: python-crewai
description: Conventions for building CrewAI agents, tasks, flows, and output models in this repo.
---

# Python CrewAI

This skill defines how to structure, implement, and test CrewAI agents and flows in this repo.

## Boundary Contract

### Applies To
- CrewAI agent, task, flow, and output model code under `src/`

### Produces
- Consistently structured CrewAI components following repo directory and naming conventions

### Does Not Cover
- General class design (`python-class-design`)
- Domain modeling (`python-domain-modeling`)
- Unit testing conventions (`python-testing-unit`)

## Context & Guidelines

**Scope**: Apply whenever adding or modifying CrewAI agents, tasks, flows, or their supporting infrastructure under `src/<package>/crewai/`.

---

## Directory Layout

Each agent lives in its own subdirectory with three files. No other files belong at agent level.

```
src/<package>/crewai/
    domain/
        constants.py       # shared constants (e.g. CHARS_PER_TOKEN_ESTIMATE)
        models/
            __init__.py    # re-exports output models from domain.value_objects
    agents/
        <agent_name>/
            agent.py       # builds the crewai.Agent
            task.py        # builds the crewai.Task
            flow.py        # Flow subclass: @start + @listen methods
    functions/
        config.py          # load_agent_llm_config
        crew_output.py     # validate_crew_pydantic_output
        statistics.py      # build_agent_statistics
```

- Shared constants used by 2+ agents belong in `crewai/domain/constants.py`.
- Output Pydantic models are domain value objects; they live in `domain/value_objects/` and are re-exported from `crewai/domain/models/__init__.py` for agent-layer imports.

---

## Flow Pattern

Subclass `Flow[StateModel]` where `StateModel` is a `BaseModel`-based state bag:

```python
from crewai.flow.flow import Flow, listen, start
from pydantic import BaseModel, Field


class MyState(BaseModel):
    text: str = ""
    result: MyOutputModel | None = None
    statistics: dict[str, dict[str, object]] = Field(default_factory=dict)


class MyFlow(Flow[MyState]):
    def __init__(self, *, input_file: Path, rules_prompt: str) -> None:
        super().__init__()
        self._input_file = input_file
        self._rules_prompt = rules_prompt

    @start()
    def load_document(self) -> str:
        ...
        return self.state.text

    @listen(load_document)
    def run_agent(self, _text: str) -> MyOutputModel:
        ...
        self.state.result = output
        return output
```

- The `@start()` method loads/prepares data and returns it for listeners.
- `@listen(method)` methods receive that return value as their first argument (convention: name it `_text` or similar when unused).
- Always assign results back to `self.state` for downstream access.
- Flows are instantiated once per request; do not share state between requests.

---

## Agent and Task Assembly

`agent.py` and `task.py` expose a single factory function each — no classes:

```python
# agent.py
def build_<name>_agent(*, llm_config: LLMConfig) -> Agent: ...

# task.py
def build_<name>_task(*, agent: Agent, rules_prompt: str, text: str) -> Task: ...
```

- Pass configuration, context, and text as keyword-only arguments.
- Do not import `Crew` or flow machinery in `agent.py` / `task.py`.

---

## Structured Output (`output_pydantic`)

### Use `list[T]` not `Sequence[T]` for collection fields

When a Pydantic model is used as `output_pydantic` on a `Task`, collection fields **must** be typed as `list[T]`:

- `Sequence[T]` generates a JSON Schema with an `items` wrapper object and a `title` key. LLMs sometimes echo this schema metadata back as the field _value_ (`{"items": [...], "title": "Findings"}`), causing Pydantic to raise `Input should be a valid array`.
- `list[T]` emits a flat, unambiguous schema.

### Add a defensive `field_validator(mode="before")`

Guard against non-deterministic LLM output by unwrapping the `{"items": [...]}` shape:

```python
from pydantic import BaseModel, Field, field_validator


class ReviewResult(BaseModel):
    findings: list[ReviewFinding] = Field(default_factory=list)

    @field_validator("findings", mode="before")
    @classmethod
    def unwrap_llm_schema_echo(cls, value: object) -> object:
        """Unwrap dict-shaped findings returned by LLMs echoing JSON Schema metadata."""
        if isinstance(value, dict) and "items" in value:
            return value["items"]
        return value
```

### Make `expected_output` explicit

Do not write vague descriptions. State the exact JSON key name and shape:

```python
# Bad
expected_output="Structured list of findings per ReviewResult schema."

# Good
expected_output=(
    "A JSON object with a 'findings' key containing a plain array of finding objects. "
    "Example: {\"findings\": [{\"rule_id\": \"H101B\", \"what_is_wrong\": \"...\", "
    "\"fix_suggestion\": \"...\"}]}. "
    "Do not wrap the array in a schema object with 'items' or 'title' keys."
)
```

---

## Validating Crew Output

Always validate crew output through `validate_crew_pydantic_output` — do not access `crew_output.pydantic` directly:

```python
from faultless.crewai.functions.crew_output import validate_crew_pydantic_output

crew_output = crew.kickoff()
result = validate_crew_pydantic_output(crew_output, MyOutputModel)
```

This helper raises `AttributeError` if the `pydantic` attribute is missing and `TypeError` if the type does not match, giving a clear error instead of a silent `None`.

---

## LLM Configuration

Load LLM config via `load_agent_llm_config("<agent_name>")`. Do not hardcode model names or temperature values in agent or task files:

```python
from faultless.crewai.functions.config import load_agent_llm_config

llm_config = load_agent_llm_config("copyeditor")
agent = build_copyeditor_agent(llm_config=llm_config)
```

---

## Testing CrewAI Flows

- Mock `Crew.kickoff` and `build_<agent>_agent` / `build_<agent>_task` to isolate flow logic from LLM calls.
- Test state mutations directly: call the flow method under test and assert on `flow.state`.
- Use `mocker.Mock(spec=CrewOutput)` and set `.pydantic` on it to simulate a crew output.
- Never call `crew.kickoff()` in unit tests (requires LLM credentials and network).

```python
def test_run_agent_stores_result_in_state(mocker) -> None:
    mocker.patch("faultless.crewai.agents.copyeditor.flow.build_copyeditor_agent")
    mocker.patch("faultless.crewai.agents.copyeditor.flow.build_copyeditor_task")
    mock_crew = mocker.patch("faultless.crewai.agents.copyeditor.flow.Crew").return_value
    mock_crew.kickoff.return_value = mocker.Mock(pydantic=ReviewResult(findings=[]))

    flow = CopyeditorReviewFlow(input_file=Path("doc.docx"), rules_prompt="rules")
    flow.state.text = "sample"
    flow.run_copyeditor("sample")

    assert flow.state.copyeditor_result is not None
```

## Procedure

1. Define output/domain models first, then implement agent and task factory functions.
2. Implement flow methods using `@start` and `@listen`, persisting outputs onto `self.state`.
3. Load LLM configuration via shared config helpers rather than hardcoding model settings.
4. Validate crew outputs via `validate_crew_pydantic_output`.
5. Add unit tests that mock Crew execution and assert flow state mutations.
