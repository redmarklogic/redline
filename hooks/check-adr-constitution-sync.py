"""Git hook: blocks commits that modify ADRs without updating the project constitution.

Enforces the ADR -> constitution sync procedure defined in:
  .agents/skills/adr-constitution-sync/SKILL.md

Per ADR-011 (hook-first enforcement), every architectural invariant requires a
deterministic automated gate. The constitution (.specify/memory/constitution.md)
is a derived artifact of cross-cutting ADRs; they must stay in sync.

Per ADR-001 (single source of truth), the ADRs are SSOT for architectural decisions;
the constitution is a derived summary. Derivations must not lag their source.

See ADR-011 (docs/adr/adr-011-hook-first-enforcement.md).
See ADR-001 (docs/adr/adr-001-single-source-of-truth.md).
"""

import subprocess
import sys

CONSTITUTION_PATH = ".specify/memory/constitution.md"
ADR_PATH_PREFIX = "docs/adr/adr-"


def get_staged_files() -> list[str]:
    """Return list of staged file paths."""
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only"],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.splitlines()


def main() -> int:
    """Entry point."""
    staged = get_staged_files()

    adr_changes = [f for f in staged if f.startswith(ADR_PATH_PREFIX)]
    constitution_staged = CONSTITUTION_PATH in staged

    if not adr_changes or constitution_staged:
        return 0

    adr_list = "\n".join(f"  - {f}" for f in adr_changes)
    print(
        f"\n[BLOCKED] ADR-011: ADR -> constitution sync required\n"
        f"\nADR(s) in this commit:\n{adr_list}\n"
        f"\nProblem: .specify/memory/constitution.md is not staged.\n"
        f"ADRs with cross-cutting implications must be reflected in the constitution\n"
        f"in the same commit.\n"
        f"\nFix:\n"
        f"  1. Open Copilot chat and run:\n"
        f"       Peter, <ADR title> was accepted. Update constitution.md.\n"
        f"  2. Stage the updated file:\n"
        f"       git add .specify/memory/constitution.md\n"
        f"  3. Retry the commit.\n"
        f"\nIf this ADR is implementation-only (no cross-cutting principle added):\n"
        f"  git commit --no-verify\n"
        f"  (documents a conscious exception -- use sparingly)\n"
        f"\nSee: .agents/skills/adr-constitution-sync/SKILL.md\n"
        f"See: ADR-011 docs/adr/adr-011-hook-first-enforcement.md\n"
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
