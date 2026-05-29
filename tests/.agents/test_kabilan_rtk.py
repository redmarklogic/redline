"""Tests that Kabilan's agent JD enforces the RTK terminal-command prefix.

RTK is a CLI proxy that compresses command output, saving 60-90% context tokens.
Kabilan runs the most terminal-heavy sessions (tests, linting, migrations) so the
constraint must be explicit in his Hard Constraints section.
"""

from pathlib import Path

AGENTS_DIR = Path(__file__).parents[2] / ".github" / "agents"
KABILAN_JD = AGENTS_DIR / "rl.kabilan.agent.md"


def test_kabilan_jd_hard_constraints_require_rtk_prefix() -> None:
    """Kabilan's Hard Constraints section must mandate the rtk prefix for all
    shell commands."""
    content = KABILAN_JD.read_text(encoding="utf-8")

    hard_constraints_idx = content.lower().find("## hard constraints")
    assert hard_constraints_idx != -1, (
        "Kabilan JD missing '## Hard Constraints' section"
    )

    hard_constraints_section = content[hard_constraints_idx:]
    assert "rtk" in hard_constraints_section, (
        "Kabilan's Hard Constraints must contain an RTK rule. "
        "Add: 'I MUST prefix all shell commands with `rtk`' under a "
        "'### Terminal Commands' subsection."
    )
