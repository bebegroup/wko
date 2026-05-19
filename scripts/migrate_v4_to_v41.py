"""Migrate Wiki từ V4 (8 SPACE, 11 TYPE) → V4.1 (7 SPACE, 13 TYPE).

Mapping:
- COM-* → GEN-* (4 sections: COM-01..04 → GEN-01..04)
- EMG-* → ARC-OLD-* (archive emergency space)
- (Optional) re-classify một số SOP đa vai trò → PROC

Output: JSON mapping cho manual rename trên Lark.

Usage:
    python3 scripts/migrate_v4_to_v41.py --input v4-tree.json --output dist/v41-mapping.json
    python3 scripts/migrate_v4_to_v41.py --interactive   # review từng mapping
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


# V4 → V4.1 SPACE mapping
SPACE_MAPPING: dict[str, str] = {
    "COM": "GEN",
    "EMG": "ARC",  # archive emergency space
}

# V4 → V4.1 SECTION mapping (COM-01..04 → GEN-01..04)
SECTION_MAPPING: dict[str, str] = {
    "COM-01": "GEN-01",
    "COM-02": "GEN-02",
    "COM-03": "GEN-03",
    "COM-04": "GEN-04",
}


def migrate_page_code(old_code: str) -> str | None:
    """Map V4 → V4.1 page code. Returns None nếu không cần đổi."""
    m = re.match(r"^([A-Z]+)-([A-Z0-9]+)-([A-Z]+)-(\d{3})$", old_code)
    if not m:
        return None

    space, section_suffix, type_code, number = m.groups()
    section_full = f"{space}-{section_suffix}"

    new_space = SPACE_MAPPING.get(space, space)
    new_section = SECTION_MAPPING.get(section_full, section_full)

    # If EMG → ARC, convert to ARC-OLD format
    if space == "EMG":
        return f"ARC-OLD-{type_code}-{number}"

    # If section mapped
    if new_section != section_full:
        new_suffix = new_section.split("-", 1)[1]
        return f"{new_space}-{new_suffix}-{type_code}-{number}"

    return None  # No change needed


def suggest_proc_reclassification(page: dict[str, Any]) -> bool:
    """Heuristic: SOP có 'luồng' / 'từ X đến Y' / multi-role → suggest PROC."""
    code = page.get("page_code", "")
    if "-SOP-" not in code:
        return False
    name = page.get("page_name", "").lower()
    proc_indicators = ["luồng", "từ ... đến", "phối hợp", "xfn", "cross-team"]
    return any(ind in name for ind in proc_indicators)


def build_migration_plan(pages: list[dict[str, Any]]) -> dict[str, Any]:
    """Build migration plan from V4 pages list."""
    renames = []
    archives = []
    proc_suggestions = []

    for p in pages:
        old_code = p.get("page_code", "")
        new_code = migrate_page_code(old_code)
        if new_code:
            if new_code.startswith("ARC-OLD-"):
                archives.append({
                    "old_code": old_code,
                    "new_code": new_code,
                    "page_name": p.get("page_name", ""),
                    "reason": "EMG space deprecated in V4.1",
                })
            else:
                renames.append({
                    "old_code": old_code,
                    "new_code": new_code,
                    "page_name": p.get("page_name", ""),
                    "reason": "COM → GEN mapping",
                })

        if suggest_proc_reclassification(p):
            proc_suggestions.append({
                "code": old_code,
                "page_name": p.get("page_name", ""),
                "suggested_new_type": "PROC",
                "reason": "Title contains 'luồng' or similar multi-role indicator",
            })

    return {
        "summary": {
            "total_pages": len(pages),
            "renames": len(renames),
            "archives": len(archives),
            "proc_suggestions": len(proc_suggestions),
        },
        "renames": renames,
        "archives": archives,
        "proc_suggestions": proc_suggestions,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="V4 → V4.1 migration helper")
    parser.add_argument("--input", required=True, help="JSON file with V4 pages list")
    parser.add_argument("--output", default="dist/v41-migration-plan.json")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"❌ Input file not found: {input_path}", file=sys.stderr)
        return 1

    pages = json.loads(input_path.read_text())
    plan = build_migration_plan(pages)

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(plan, indent=2, ensure_ascii=False))

    s = plan["summary"]
    print(f"✓ Migration plan → {out}")
    print(f"  Total pages: {s['total_pages']}")
    print(f"  Renames (COM → GEN): {s['renames']}")
    print(f"  Archives (EMG → ARC): {s['archives']}")
    print(f"  PROC suggestions: {s['proc_suggestions']}")
    print("\n⚠️  Manual review required. Áp dụng rename qua Lark UI hoặc API.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
