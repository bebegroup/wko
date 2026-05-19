"""Lint folder structure of wko repo."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


class StructureError(Exception):
    """Raised khi structure sai."""


REQUIRED_DIRS = ["skills", "docs", "scripts", "docs-meta"]
REQUIRED_GITIGNORE_ENTRIES = ["dist/", ".env", "company.config.yaml"]


def validate_structure(root: Path) -> None:
    """Raise StructureError nếu structure sai."""
    missing = [d for d in REQUIRED_DIRS if not (root / d).is_dir()]
    if missing:
        raise StructureError(f"Missing required dirs: {missing}")

    gitignore = root / ".gitignore"
    if not gitignore.exists():
        raise StructureError(".gitignore missing")

    ignore_content = gitignore.read_text()
    if (root / "dist").exists() and "dist/" not in ignore_content and "dist" not in ignore_content:
        raise StructureError("dist/ exists but not in .gitignore — secret leak risk")

    for entry in REQUIRED_GITIGNORE_ENTRIES:
        if entry not in ignore_content:
            print(f"⚠️  .gitignore missing entry: {entry}", file=sys.stderr)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    try:
        validate_structure(Path(args.root).resolve())
        print("✅ Structure OK")
        return 0
    except StructureError as e:
        print(f"❌ {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
