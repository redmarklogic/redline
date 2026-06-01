---
name: python-function-design
description: Use when designing Python functions -- decomposing responsibilities, defining signatures, or managing side effects
---

# Python Function Design

This skill covers function design in this repo: decomposition, naming, signatures, and
minimizing side effects.

## Boundary Contract

### Applies To
- Function definitions across `src/` and `tests/`

### Produces
- Focused functions with clear signatures, minimal side effects, and testable decomposition

### Does Not Cover
- Type annotations (`python-typing`)
- Docstrings (`python-documentation`)
- Error handling (`python-error-handling`)
- Module-level ordering (`python-module-structure`)

# In library code - BAD
def build_copyeditor_rules_prompt() -> str:
    """Load the rulebank and format the copyeditor rule prompt."""
    rulebank = load_rulebank()
    copy_rules = select_rulebank_rules(rulebank=rulebank, prefix="H")  # Hardcoded!
    return build_rules_prompt(rules=copy_rules)
```

Good (library provides primitives, script composes):

```python
# In library code - GOOD
from faultless.domain.repository import RulebankRepository
from faultless.functions.rulebank import build_rules_prompt

# In script code - GOOD
def build_copyeditor_prompt() -> str:
    repo = RulebankRepository(path=RULEBANK_PATH)
    prompts = repo.get_prompts(prefix="H")  # Script decides "H"
    return build_rules_prompt(prompts_df=prompts)
```

This separation enables:

- Library code stays reusable (no hardcoded business rules)
- Scripts compose primitives to express intent
- Easy to add new scripts with different selections without changing library code


See `procedures/python-function-design.md` for detailed rules, examples, and extended reference.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Function that both fetches data and transforms it | Split into two functions: one pure transformation, one with I/O side effect |
| Boolean flag parameter that changes the function's fundamental behaviour | Split into two separate functions instead of a mode flag |
| More than 3 positional parameters | Introduce a dataclass or named keyword arguments to reduce call-site ambiguity |