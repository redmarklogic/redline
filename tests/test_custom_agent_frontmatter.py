from pathlib import Path

AGENTS_DIR = Path(".github/agents")
FIRST_PARTY_AGENT_PATTERN = "rl.*.agent.md"
HARRIET_SKILL = Path(".agents/skills/hiring-agent-management/SKILL.md")


def test_first_party_agents_declare_tools_and_subagents() -> None:
    for agent_path in sorted(AGENTS_DIR.glob(FIRST_PARTY_AGENT_PATTERN)):
        frontmatter = _frontmatter_for(agent_path)

        assert _has_key(frontmatter, "name"), f"{agent_path} must declare name"
        assert _has_key(frontmatter, "tools"), f"{agent_path} must declare tools"
        assert _has_key(frontmatter, "agents"), f"{agent_path} must declare agents"

        tools = _yaml_list(frontmatter, "tools")
        agents = _yaml_list(frontmatter, "agents")

        assert tools, f"{agent_path} tools must be an explicit non-empty list"
        assert agents, f"{agent_path} agents must be an explicit non-empty list"
        assert "agent" in tools, f"{agent_path} must include agent tool"
        assert not any(tool == "*" for tool in tools), (
            f"{agent_path} must not allow all tools"
        )
        assert not any(tool.startswith("mcp_notebooklm_") for tool in tools), (
            f"{agent_path} must use official MCP server wildcard syntax"
        )


def test_handoffs_are_limited_to_declared_subagents() -> None:
    for agent_path in sorted(AGENTS_DIR.glob(FIRST_PARTY_AGENT_PATTERN)):
        frontmatter = _frontmatter_for(agent_path)
        declared_agents = set(_yaml_list(frontmatter, "agents"))
        handoff_agents = set(_handoff_agents(frontmatter))
        # Vendor-generated agents (speckit.*) are valid handoff targets
        # but are not listed in our organisational agents field.
        org_handoff_agents = {a for a in handoff_agents if not a.startswith("speckit.")}

        assert org_handoff_agents <= declared_agents, (
            f"{agent_path} handoffs must be included in agents: "
            f"{sorted(org_handoff_agents - declared_agents)}"
        )


def test_harriet_skill_requires_official_custom_agent_frontmatter() -> None:
    skill_text = HARRIET_SKILL.read_text(encoding="utf-8")

    assert (
        "code.visualstudio.com/docs/copilot/customization/custom-agents" in skill_text
    )
    assert "tools" in skill_text
    assert "agents" in skill_text
    assert "handoffs" in skill_text


def _frontmatter_for(path: Path) -> list[str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    assert lines, f"{path} must start with YAML frontmatter"
    assert lines[0] == "---", f"{path} must start with YAML frontmatter"

    try:
        end_index = lines[1:].index("---") + 1
    except ValueError as error:
        raise AssertionError(f"{path} must close YAML frontmatter") from error

    return lines[1:end_index]


def _yaml_list(frontmatter: list[str], key: str) -> list[str]:
    values: list[str] = []
    collecting = False

    for line in frontmatter:
        if line == f"{key}:":
            collecting = True
            continue
        if collecting and line.startswith("  - "):
            values.append(line[4:].strip().strip("'\""))
            continue
        if collecting and line and not line.startswith(" "):
            break

    return values


def _has_key(frontmatter: list[str], key: str) -> bool:
    return any(line == f"{key}:" or line.startswith(f"{key}: ") for line in frontmatter)


def _handoff_agents(frontmatter: list[str]) -> list[str]:
    agents: list[str] = []

    for line in frontmatter:
        stripped = line.strip()
        if stripped.startswith("agent: "):
            agents.append(stripped.removeprefix("agent: ").strip().strip("'\""))

    return agents
