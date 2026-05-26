"""Check that new skills in .agents/skills/ have a RED phase baseline document.

The Iron Law: no SKILL.md may be committed without evidence that the RED phase
was completed. A skill passes the gate if its directory contains either:
  - RED-PHASE-BASELINE.md  (single-file baseline format)
  - tests/<any>.md         (test directory format)

Only skills whose SKILL.md is being added in the current commit are checked.
Existing skills that pre-date this hook are not retroactively penalised.
"""
# no-adr: enforces test-driven-development skill RED-phase discipline; no governing ADR

import subprocess
import sys
from pathlib import Path

_SKILLS_ROOT = Path(".agents/skills")
_BASELINE_FILE = "RED-PHASE-BASELINE.md"
_TESTS_DIR = "tests"


def _staged_new_files() -> list[Path]:
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=A"],
        capture_output=True,
        text=True,
        check=False,
    )
    return [Path(p) for p in result.stdout.splitlines()]


def _is_new_skill(path: Path) -> bool:
    try:
        relative = path.relative_to(_SKILLS_ROOT)
    except ValueError:
        return False
    parts = relative.parts
    return len(parts) == 2 and parts[1] == "SKILL.md"


def _has_red_phase(skill_dir: Path) -> bool:
    if (skill_dir / _BASELINE_FILE).is_file():
        return True
    tests_dir = skill_dir / _TESTS_DIR
    return bool(tests_dir.is_dir() and any(tests_dir.glob("*.md")))


def main() -> int:
    new_files = _staged_new_files()
    new_skills = [f for f in new_files if _is_new_skill(f)]

    if not new_skills:
        return 0

    failed: list[str] = []
    for skill_md in new_skills:
        skill_dir = skill_md.parent
        if not _has_red_phase(skill_dir):
            failed.append(str(skill_dir))

    if failed:
        print(
            "ERROR: The following new skills are missing a RED phase baseline document:",
            file=sys.stderr,
        )
        for skill in failed:
            print(f"  - {skill}", file=sys.stderr)
        print(file=sys.stderr)
        print(
            "Each new skill must include either:",
            file=sys.stderr,
        )
        print(
            f"  - {_BASELINE_FILE}  (documented baseline failure)",
            file=sys.stderr,
        )
        print(
            f"  - {_TESTS_DIR}/<name>.md  (test directory with at least one .md file)",
            file=sys.stderr,
        )
        print(file=sys.stderr)
        print(
            "The Iron Law: no skill content before a failing baseline is documented.",
            file=sys.stderr,
        )
        print(
            "See .agents/skills/writing-skills/procedures/create-skill.md",
            file=sys.stderr,
        )
        return 1

    print(f"All {len(new_skills)} new skill(s) have RED phase documentation.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
