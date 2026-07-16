#!/usr/bin/env python3
"""Install the bundled SARA YouTube KOL workflow into a target directory."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
ASSET_ROOT = SKILL_ROOT / "assets" / "yt-kol-workflow"


EXCLUDES = {
    ".git",
    ".venv",
    "__pycache__",
    ".pytest_cache",
    "output",
    "temp",
    ".DS_Store",
    ".env",
    "keyword.txt",
    "keywords.txt",
    "brand_exclusions.json",
    "seen_channels.json",
}


def ignore_names(_dir: str, names: list[str]) -> set[str]:
    return {name for name in names if name in EXCLUDES or name.endswith(".pyc")}


def copy_project(target: Path, force: bool) -> None:
    if not ASSET_ROOT.exists():
        raise SystemExit(f"Bundled workflow asset not found: {ASSET_ROOT}")

    if target.exists() and any(target.iterdir()) and not force:
        raise SystemExit(
            f"Target is not empty: {target}\n"
            "Use --force to merge the bundled workflow into this directory."
        )

    target.mkdir(parents=True, exist_ok=True)
    shutil.copytree(
        ASSET_ROOT,
        target,
        dirs_exist_ok=True,
        ignore=ignore_names,
    )


def ensure_config_files(target: Path) -> None:
    copies = [
        (".env.example", ".env"),
        ("keywords.example.txt", "keyword.txt"),
        ("brand_exclusions.example.json", "brand_exclusions.json"),
    ]
    for source_name, dest_name in copies:
        source = target / source_name
        dest = target / dest_name
        if source.exists() and not dest.exists():
            shutil.copy2(source, dest)


def install_deps(target: Path, python_bin: str) -> None:
    venv = target / ".venv"
    if not venv.exists():
        subprocess.run([python_bin, "-m", "venv", str(venv)], check=True)

    pip = venv / "bin" / "pip"
    if sys.platform.startswith("win"):
        pip = venv / "Scripts" / "pip.exe"
    subprocess.run([str(pip), "install", "-r", str(target / "requirements.txt")], check=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", required=True, help="Directory to install the workflow into")
    parser.add_argument("--force", action="store_true", help="Merge into a non-empty target")
    parser.add_argument("--install-deps", action="store_true", help="Create .venv and install requirements")
    parser.add_argument("--python", default=sys.executable, help="Python executable for venv creation")
    args = parser.parse_args()

    target = Path(args.target).expanduser().resolve()
    copy_project(target, args.force)
    ensure_config_files(target)

    if args.install_deps:
        install_deps(target, args.python)

    print(f"Installed SARA YouTube KOL workflow at: {target}")
    print("Next: edit .env and set YOUTUBE_API_KEY, then update keyword.txt.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
