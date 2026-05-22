"""Pre-commit hook to clean Quarto intermediate files.

Uses the Quarto CLI cleanup command when available, and falls back to
safe removal of untracked Quarto intermediate paths for older Quarto versions.
"""

import re
import shutil
import subprocess
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[1]
_QUARTO_PROJECT_FILE = "_quarto.yml"
_SKIP_PARTS = {".git", ".venv", "node_modules"}
_INTERMEDIATE_DIR_NAMES = {".quarto", "_freeze", "_site"}
_INTERMEDIATE_FILE_PREFIXES = {".quarto_ipynb"}


def _find_quarto_projects() -> list[Path]:
    return sorted(
        path.parent
        for path in _REPO_ROOT.rglob(_QUARTO_PROJECT_FILE)
        if not _SKIP_PARTS.intersection(path.parts)
    )


def _supports_clean_subcommand(quarto_executable: str) -> bool:
    result = subprocess.run(
        [quarto_executable, "--help"],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return False
    return re.search(r"^\s+clean\s", result.stdout, flags=re.MULTILINE) is not None


def _run_cleanup_command(quarto_executable: str, project_directory: Path) -> int:
    command = [quarto_executable, "clean", str(project_directory), "--quiet"]
    result = subprocess.run(command, check=False)
    return result.returncode


def _is_path_tracked(path: Path) -> bool:
    relative_path = path.relative_to(_REPO_ROOT).as_posix()
    result = subprocess.run(
        ["git", "ls-files", "--error-unmatch", relative_path],
        cwd=_REPO_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    return result.returncode == 0


def _has_tracked_children(path: Path) -> bool:
    relative_path = path.relative_to(_REPO_ROOT).as_posix()
    result = subprocess.run(
        ["git", "ls-files", "--", relative_path],
        cwd=_REPO_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    return bool(result.stdout.strip())


def _candidate_intermediate_paths() -> list[Path]:
    candidate_paths: set[Path] = set()

    for directory_name in _INTERMEDIATE_DIR_NAMES:
        for path in _REPO_ROOT.glob(f"**/{directory_name}"):
            if path.is_dir() and not _SKIP_PARTS.intersection(path.parts):
                candidate_paths.add(path)

    for path in _REPO_ROOT.glob("**/*_files"):
        if path.is_dir() and not _SKIP_PARTS.intersection(path.parts):
            candidate_paths.add(path)

    for prefix in _INTERMEDIATE_FILE_PREFIXES:
        for path in _REPO_ROOT.glob(f"**/{prefix}*"):
            if path.is_file() and not _SKIP_PARTS.intersection(path.parts):
                candidate_paths.add(path)

    return sorted(candidate_paths)


def _fallback_cleanup_untracked_intermediates() -> int:
    removed_paths: list[Path] = []

    for path in _candidate_intermediate_paths():
        if path.is_dir():
            if _has_tracked_children(path):
                continue
            shutil.rmtree(path)
            removed_paths.append(path)
            continue
        if _is_path_tracked(path):
            continue
        path.unlink(missing_ok=True)
        removed_paths.append(path)

    if removed_paths:
        print("removed Quarto intermediate paths:")
        for removed_path in removed_paths:
            print(f"  {removed_path.relative_to(_REPO_ROOT).as_posix()}")

    return 0


def main() -> int:
    project_directories = _find_quarto_projects()
    if not project_directories:
        return 0

    quarto_executable = shutil.which("quarto")
    if quarto_executable is None:
        print("quarto not found; skipping Quarto intermediate cleanup")
        return 0

    supports_clean_subcommand = _supports_clean_subcommand(quarto_executable)
    if not supports_clean_subcommand:
        return _fallback_cleanup_untracked_intermediates()

    failed_projects: list[Path] = []

    for project_directory in project_directories:
        return_code = _run_cleanup_command(
            quarto_executable=quarto_executable,
            project_directory=project_directory,
        )
        if return_code != 0:
            failed_projects.append(project_directory)

    if not failed_projects:
        return 0

    print("quarto cleanup failed for:")
    for project_directory in failed_projects:
        print(f"  {project_directory}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
