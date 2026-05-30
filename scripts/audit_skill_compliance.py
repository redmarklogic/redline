"""
Compliance audit for all editable skills in .agents/skills/.

Checks 6 criteria for each SKILL.md:
  FM   - has frontmatter with name + description
  Desc - description starts with 'Use when'
  BC   - has ## Boundary Contract section
  CM   - has ## Common Mistakes section
  Path - no bare hardcoded drive-letter paths (A-Z:\\) outside hook: allow
  Tok  - word count <= 200 (frequently-loaded) or 500 (standard)

Vendor-managed skills (speckit-*) are excluded.
"""

from __future__ import annotations

import pathlib
import re
import sys

SKILLS_DIR = pathlib.Path(".agents/skills")
VENDOR = {
    "speckit-shaping-gate-check",
    "speckit-source-reconciliation-run",
    "speckit-static-checks-run",
    "speckit-verification-gate-run",
}
FREQ_LOADED = {"using-superpowers", "cce-mcp", "dev-environment"}


def word_count(text: str) -> int:
    return len([w for w in text.split() if w])


def audit_skill(name: str, content: str) -> dict[str, bool | int]:
    lim = 200 if name in FREQ_LOADED else 500
    words = word_count(content)
    fm = bool(re.search(r"(?s)^---.*?name:.*?description:.*?---", content))
    desc = bool(re.search(r"(?m)^description: Use when", content))
    bc = bool(re.search(r"## Boundary Contract", content))
    cm = bool(re.search(r"## Common Mistakes", content))
    bad = [
        line
        for line in content.split("\n")
        if re.search(r"[A-Z]:\\", line) and "hook: allow" not in line
    ]
    paths_ok = len(bad) == 0
    tok = words <= lim
    return {
        "words": words,
        "limit": lim,
        "FM": fm,
        "Desc": desc,
        "BC": bc,
        "CM": cm,
        "Paths": paths_ok,
        "Tok": tok,
        "pass": fm and desc and bc and cm and paths_ok and tok,
    }


def main() -> None:
    results = []
    for skill_dir in sorted(SKILLS_DIR.iterdir()):
        name = skill_dir.name
        if name in VENDOR:
            continue
        sf = skill_dir / "SKILL.md"
        if not sf.exists():
            continue
        content = sf.read_text(encoding="utf-8", errors="replace")
        r = audit_skill(name, content)
        results.append((name, r))

    passing = [r for _, r in results if r["pass"]]
    failing = [(n, r) for n, r in results if not r["pass"]]

    print(
        f"\nSkills audited: {len(results)}  Passing: {len(passing)}  Failing: {len(failing)}"
    )

    if failing:
        print(
            f"\n{'Skill':<45} {'Words':>6}/{'>Lim':<5} {'FM':>3} {'Desc':>5} {'BC':>3} {'CM':>3} {'Path':>5} {'Tok':>4}"
        )
        print("-" * 82)
        for name, r in failing:

            def b(v: bool) -> str:
                return "Y" if v else "N"

            print(
                f"  {name:<43} {r['words']:>6}/{r['limit']:<5}"
                f" {b(r['FM']):>3} {b(r['Desc']):>5} {b(r['BC']):>3}"
                f" {b(r['CM']):>3} {b(r['Paths']):>5} {b(r['Tok']):>4}"
            )
    else:
        print("\nAll skills PASS all 6 compliance checks.")

    sys.exit(0 if not failing else 1)


if __name__ == "__main__":
    main()
