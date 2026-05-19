"""Sync 'Contributed By' column trong Master Wiki Index từ git log.

For each page file in skills/ or docs/, get list of contributors (git log --format='%an').
Push lên Lark Master Index cột Contributed By.

Usage:
    python3 scripts/sync_index_contributed_column.py              # dry-run
    python3 scripts/sync_index_contributed_column.py --confirm    # push lên Lark
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

from _common import load_config, require_lark_auth, require_lark_cli


def get_contributors(file_path: Path) -> list[str]:
    """Get unique authors of a file from git log."""
    try:
        r = subprocess.run(
            ["git", "log", "--format=%an", "--follow", str(file_path)],
            capture_output=True, text=True, check=True, timeout=10,
        )
        # Unique, preserve order
        seen = set()
        ordered = []
        for line in r.stdout.splitlines():
            name = line.strip()
            if name and name not in seen:
                seen.add(name)
                ordered.append(name)
        return ordered
    except subprocess.CalledProcessError:
        return []


def get_page_code_from_file(file_path: Path) -> str | None:
    """Read first line for page code (`# CODE name`)."""
    try:
        first_line = file_path.read_text().splitlines()[0]
        import re

        m = re.match(r"^# ([A-Z]+-[A-Z0-9]+-[A-Z]+-\d{3})\s+", first_line)
        if m:
            return m.group(1)
    except (FileNotFoundError, IndexError, UnicodeDecodeError):
        pass
    return None


def scan_repo_contributors(root: Path) -> dict[str, list[str]]:
    """Scan skills/ + docs/, return {page_code: [contributors]}."""
    result = {}
    for d in ("skills", "docs"):
        sub = root / d
        if not sub.exists():
            continue
        for md in sub.glob("*.md"):
            if md.name == "README.md":
                continue
            code = get_page_code_from_file(md)
            if code:
                result[code] = get_contributors(md)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync Contributed By to Lark Master Index")
    parser.add_argument("--confirm", action="store_true", help="Push lên Lark (default dry-run)")
    parser.add_argument("--output", default="dist/contributors.json")
    args = parser.parse_args()

    require_lark_cli()
    cfg = load_config()
    if args.confirm:
        require_lark_auth()

    repo = Path.cwd()
    print(f"📡 Scanning {repo}/skills + {repo}/docs...")
    contributors = scan_repo_contributors(repo)

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(contributors, indent=2, ensure_ascii=False))
    print(f"✓ Contributors map → {out} ({len(contributors)} pages)")

    if args.confirm:
        obj_token = cfg["lark"]["master_index"]["obj_token"]
        if not obj_token:
            print("❌ lark.master_index.obj_token chưa cấu hình", file=sys.stderr)
            return 1
        print(f"📤 Pushing to Lark obj {obj_token[:8]}...")
        # Implementation would: fetch current Master Index → patch Contributed By column → push
        # For now, dry-run preview only
        print("⚠️  Full Lark patch not yet implemented. Use the JSON to update manually.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
