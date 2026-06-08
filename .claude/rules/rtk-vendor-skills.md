---
paths:
  - ".agents/skills/**/*.md"
  - ".github/instructions/**/*.md"
  - ".github/agents/**/*.md"
  - "docs/**/*.md"
  - "specs/**/*.md"
---

RTK is a CLI proxy that saves 60-90% tokens. All shell commands in documentation
and skill files must use the `rtk` prefix for eligible commands:
`git`, `pytest`, `ruff`, `docker`, `uv`, `pip`, `mypy`, `prek`.

For vendor skills (`speckit-*`): add the `rtk` prefix directly to commands.
Do NOT use `<!-- rtk:skip -->` suppression in vendor skill files.
