"""
Skill token-efficiency extraction script.

For each over-limit SKILL.md (>500 words), this script:
1. Parses the file into sections by ## headings
2. Identifies "heavy" sections to extract (Procedure, Context & Guidelines,
   Examples, Core Philosophy, Testing Styles, etc.)
3. Moves heavy sections to procedures/<skill-name>.md
4. Rewrites SKILL.md with lean skeleton (<= 500 words)

Sections always kept in SKILL.md:
  - Frontmatter + title + first paragraph
  - ## Boundary Contract
  - ## Quick Reference (or first table, max 5 rows)
  - ## Common Mistakes
  - ## When to Use (if <= 10 lines)

Everything else (or if still over 500w) goes to procedures.

Usage:
    python scripts/extract_oversized_skills.py [--dry-run] [--skill <name>]
"""

from __future__ import annotations

import argparse  # hook: allow
import pathlib
import re

SKILLS_DIR = pathlib.Path(".agents/skills")
WORD_LIMIT = 500

HEAVY_SECTION_PATTERNS = [
    r"^procedure$",
    r"^context",
    r"^core philosophy",
    r"^testing style",
    r"^examples?$",
    r"^detailed",
    r"^full",
    r"^reference",
    r"^fixture",
    r"^marker",
    r"^mocking",
    r"^parametrize",
    r"^equivalence",
    r"^side.effect",
    r"^cognitive complexity",
    r"^command.query",
    r"^library vs script",
    r"^temporal coupling",
    r"^anonymous function",
    r"^magic number",
    r"^don.t repeat",
    r"^have no side",
    r"^step.down",
    r"^define error",
    r"^layer architect",
    r"^tooling strategy",
    r"^non.negotiable",
    r"^file.?module layout",
    r"^documentation requirement",
    r"^inheritance",
    r"^schema evolution",
    r"^pre.commit",
    r"^testing expectation",
    r"^subdomain classif",
    r"^strategic",
    r"^architectural stance",
    r"^tactical",
    r"^tool reference",
    r"^installation",
    r"^configuration",
    r"^setup",
    r"^how to",
    r"^process",
    r"^workflow",
    r"^script",
    r"^narrative",
    r"^anti.pattern",
    r"^input validation",
    r"^function argument",
    r"^function shape",
    r"^naming",
    r"^principle of",
    r"^do one thing",
]

KEEP_SECTION_PATTERNS = [
    r"^boundary contract",
    r"^quick reference",
    r"^when to use",
    r"^common mistakes",
    r"^applies to",
    r"^produces",
    r"^does not cover",
    r"^layer architecture$",  # keep the compact table version only
]


def word_count(text: str) -> int:
    return len([w for w in text.split() if w])


def is_heavy_section(title: str) -> bool:
    t = title.lower().strip()
    return any(re.match(p, t) for p in HEAVY_SECTION_PATTERNS)


def parse_sections(content: str) -> list[tuple[int, str, str]]:
    """
    Returns list of (level, title, body) tuples.
    level=0 is the frontmatter/title block.
    """
    lines = content.split("\n")
    sections = []
    current_level = 0
    current_title = "PREAMBLE"
    current_body = []

    for line in lines:
        m = re.match(r"^(#{1,3})\s+(.+)$", line)
        if m:
            sections.append((current_level, current_title, "\n".join(current_body)))
            current_level = len(m.group(1))
            current_title = m.group(2)
            current_body = [line]
        else:
            current_body.append(line)

    sections.append((current_level, current_title, "\n".join(current_body)))
    return sections


def extract_skill(  # noqa: PLR0912, PLR0915
    skill_dir: pathlib.Path, dry_run: bool = False
) -> tuple[str, int, int]:
    """
    Process one skill. Returns (status, original_words, final_words).
    status: 'skipped', 'extracted', 'already_ok'
    """
    skill_file = skill_dir / "SKILL.md"
    if not skill_file.exists():
        return ("no_file", 0, 0)

    content = skill_file.read_text(encoding="utf-8", errors="replace")
    orig_words = word_count(content)

    if orig_words <= WORD_LIMIT:
        return ("already_ok", orig_words, orig_words)

    # Parse into sections
    sections = parse_sections(content)

    keep_sections = []
    extract_sections = []

    for level, title, body in sections:
        title_clean = title.lower().strip()
        if level == 0:
            keep_sections.append((level, title, body))
            continue

        # Always keep certain sections
        if any(re.match(p, title_clean) for p in KEEP_SECTION_PATTERNS):
            keep_sections.append((level, title, body))
            continue

        # Extract heavy sections
        if level == 2 and is_heavy_section(title):
            extract_sections.append((level, title, body))
            continue

        # Level 3 sub-sections of heavy sections - also extract
        if level == 3:
            extract_sections.append((level, title, body))
            continue

        # Default: keep it
        keep_sections.append((level, title, body))

    # Rebuild lean SKILL.md
    lean_parts = []
    for level, title, body in keep_sections:
        lean_parts.append(body)

    # Add reference link before Common Mistakes if we extracted anything
    if extract_sections:
        procedures_link = f"\nSee `procedures/{skill_dir.name}.md` for detailed rules, examples, and extended reference.\n"
        # Insert before Common Mistakes
        for i, (level, title, body) in enumerate(keep_sections):
            if "common mistakes" in title.lower():
                lean_parts.insert(i, procedures_link)
                break
        else:
            lean_parts.append(procedures_link)

    lean_content = "\n".join(lean_parts)
    lean_words = word_count(lean_content)

    # If still over limit, move more aggressively - keep only BC + QR + CM
    if lean_words > WORD_LIMIT and extract_sections:
        # Find sections to further extract
        further_extract = []
        still_keep = []
        for level, title, body in keep_sections:
            title_clean = title.lower().strip()
            if level == 0 or any(
                re.match(p, title_clean) for p in KEEP_SECTION_PATTERNS
            ):
                still_keep.append((level, title, body))
            else:
                further_extract.append((level, title, body))
                extract_sections.append((level, title, body))

        lean_parts = []
        for level, title, body in still_keep:
            lean_parts.append(body)

        if further_extract:
            procedures_link = f"\nSee `procedures/{skill_dir.name}.md` for detailed rules, examples, and extended reference.\n"
            for i, (level, title, body) in enumerate(still_keep):
                if "common mistakes" in title.lower():
                    lean_parts.insert(i, procedures_link)
                    break
            else:
                lean_parts.append(procedures_link)

        lean_content = "\n".join(lean_parts)
        lean_words = word_count(lean_content)

    if not extract_sections:
        return ("no_extract", orig_words, orig_words)

    # Write procedures file
    procedures_dir = skill_dir / "procedures"
    procedures_file = procedures_dir / f"{skill_dir.name}.md"

    procedures_parts = [
        f"# {skill_dir.name.replace('-', ' ').title()} — Detailed Reference\n"
    ]
    for level, title, body in extract_sections:
        procedures_parts.append(body)
    procedures_content = "\n".join(procedures_parts)

    if not dry_run:
        procedures_dir.mkdir(exist_ok=True)
        if procedures_file.exists():
            # Append to existing rather than overwrite
            existing = procedures_file.read_text(encoding="utf-8", errors="replace")
            procedures_file.write_text(
                existing + "\n\n---\n\n" + "\n".join(procedures_parts[1:]),
                encoding="utf-8",
            )
        else:
            procedures_file.write_text(procedures_content, encoding="utf-8")

        skill_file.write_text(lean_content, encoding="utf-8")

    return ("extracted", orig_words, lean_words)


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract oversized skills")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--skill", help="Process only this skill")
    args = parser.parse_args()

    skills_to_process = []
    if args.skill:
        skills_to_process = [SKILLS_DIR / args.skill]
    else:
        skills_to_process = sorted(SKILLS_DIR.iterdir())

    results = []
    for skill_dir in skills_to_process:
        if not skill_dir.is_dir():
            continue
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.exists():
            continue
        try:
            content = skill_file.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        if word_count(content) <= WORD_LIMIT:
            continue

        status, orig_w, final_w = extract_skill(skill_dir, dry_run=args.dry_run)
        results.append((skill_dir.name, status, orig_w, final_w))

    print(f"\n{'Skill':<45} {'Status':<15} {'Before':>7} {'After':>7}")
    print("-" * 78)
    still_over = 0
    for name, status, orig_w, final_w in results:
        marker = " !" if final_w > WORD_LIMIT else ""
        print(f"  {name:<43} {status:<15} {orig_w:>7} {final_w:>7}{marker}")
        if final_w > WORD_LIMIT:
            still_over += 1

    print(f"\nTotal processed: {len(results)}, still over limit: {still_over}")


if __name__ == "__main__":
    main()
