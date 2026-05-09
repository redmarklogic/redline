"""Pre-commit hook to delete Quarto-generated output artifacts.

Quarto produces HTML files and companion *_files/ asset directories alongside
source .qmd/.md files. These artifacts must not be committed to version control.

Deleted patterns:
  - {stem}.html  where {stem}.qmd or {stem}.md exists in the same directory
  - {stem}_files/ directories (Quarto HTML dependency assets)
"""

import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def find_artifacts() -> list[Path]:
    """Return all Quarto-generated artifacts found in the repository."""
    artifacts: list[Path] = []

    for candidate in sorted(REPO_ROOT.rglob("*")):
        if _is_hidden_or_venv(candidate):
            continue

        if candidate.is_dir() and candidate.name.endswith("_files"):
            artifacts.append(candidate)
        elif candidate.is_file() and candidate.suffix == ".html":
            stem = candidate.stem
            parent = candidate.parent
            if (parent / f"{stem}.qmd").exists() or (parent / f"{stem}.md").exists():
                artifacts.append(candidate)

    return artifacts


def _is_hidden_or_venv(path: Path) -> bool:
    return any(
        part.startswith(".") or part in (".venv", "__pycache__", "node_modules")
        for part in path.relative_to(REPO_ROOT).parts
    )


def main() -> int:
    artifacts = find_artifacts()

    if not artifacts:
        return 0

    for artifact in artifacts:
        if artifact.is_dir():
            shutil.rmtree(artifact)
            print(f"Removed directory: {artifact.relative_to(REPO_ROOT)}")
        else:
            artifact.unlink()
            print(f"Removed file:      {artifact.relative_to(REPO_ROOT)}")

    print(
        f"\nRemoved {len(artifacts)} Quarto artifact(s). Stage the deletions and re-commit."
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
