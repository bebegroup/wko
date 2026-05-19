"""Monthly KPI report cho Wiki — Execution-First compliance + status distribution.

V4.1 metrics:
- Section formula compliance: % section đạt 1 HUB + 1 MST + 1 PROC + 3 SOP + 1 CHK + 1 TMP + 1 PBK
- Page count per type (focus: PROC count V4.1 mới)
- Page status distribution
- Overdue review pages
- Pages thiếu Hub Parent

Usage:
    python3 scripts/wiki_kpi_report.py                              # output → dist/kpi-YYYY-MM.md
    python3 scripts/wiki_kpi_report.py --push-to-lark               # push lên LOG page
    python3 scripts/wiki_kpi_report.py --output docs/07-status-tracker.md  # update local
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any

from _common import load_config, require_lark_auth, require_lark_cli


# Required types per section theo execution_first.section_formula
EXECUTION_FIRST_REQUIRED = ["HUB", "MST", "PROC", "SOP", "CHK", "TMP", "PBK"]


def parse_page_code(code: str) -> tuple[str, str, str, str] | None:
    """Parse SPACE-SECTION_SUFFIX-TYPE-NUMBER → (space, section, type, number)."""
    m = re.match(r"^([A-Z]+)-([A-Z0-9]+)-([A-Z]+)-(\d{3})$", code)
    if not m:
        return None
    space, section_suffix, type_code, number = m.groups()
    return (space, f"{space}-{section_suffix}", type_code, number)


def count_pages_by_section_type(pages: list[dict[str, Any]]) -> dict[str, dict[str, int]]:
    """Return {section_code: {type_code: count, ...}, ...}."""
    counter: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for p in pages:
        parsed = parse_page_code(p.get("page_code", ""))
        if parsed:
            _, section, type_code, _ = parsed
            counter[section][type_code] += 1
    return {k: dict(v) for k, v in counter.items()}


def compute_execution_first_compliance(
    section_counts: dict[str, dict[str, int]],
) -> dict[str, dict[str, Any]]:
    """Per-section compliance with execution-first formula.

    Returns {section: {type: count, "compliance": float 0-1, "missing": [...]}}.
    """
    result: dict[str, dict[str, Any]] = {}
    for section, type_counts in section_counts.items():
        present = sum(1 for t in EXECUTION_FIRST_REQUIRED if type_counts.get(t, 0) > 0)
        missing = [t for t in EXECUTION_FIRST_REQUIRED if type_counts.get(t, 0) == 0]
        result[section] = {
            **type_counts,
            "compliance": present / len(EXECUTION_FIRST_REQUIRED),
            "missing": missing,
        }
    return result


def count_by_status(pages: list[dict[str, Any]]) -> Counter:
    """Count pages by status."""
    return Counter(p.get("status", "Unknown") for p in pages)


def find_overdue_review(pages: list[dict[str, Any]], today: str) -> list[dict[str, Any]]:
    """Pages có next_review < today."""
    return [p for p in pages if p.get("next_review", "") and p["next_review"] < today]


def find_missing_hub_parent(pages: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Pages thiếu Hub Parent (V4.1 requirement)."""
    return [
        p for p in pages
        if not p.get("hub_parent")
        and parse_page_code(p.get("page_code", ""))
        and parse_page_code(p.get("page_code", ""))[2] not in ("HUB", "IDX")
    ]


def render_report(
    pages: list[dict[str, Any]],
    cfg: dict[str, Any],
) -> str:
    """Render monthly KPI report markdown."""
    today = datetime.utcnow().strftime("%Y-%m-%d")
    month = today[:7]

    section_counts = count_pages_by_section_type(pages)
    compliance = compute_execution_first_compliance(section_counts)
    status_counts = count_by_status(pages)
    overdue = find_overdue_review(pages, today)
    missing_hub = find_missing_hub_parent(pages)

    lines = [
        f"# Wiki KPI Report — {month}",
        "",
        f"> {cfg['company']['name']} · Taxonomy: {cfg['taxonomy']['version']} · Generated: {today}",
        "",
        f"Total pages: **{len(pages)}**",
        "",
        "## 1. Status distribution",
        "",
        "| Status | Count |",
        "|---|---|",
    ]
    for status, count in status_counts.most_common():
        lines.append(f"| {status} | {count} |")

    lines.extend([
        "",
        "## 2. Execution-First Compliance per section",
        "",
        "Required types: " + ", ".join(EXECUTION_FIRST_REQUIRED),
        "",
        "| Section | HUB | MST | PROC | SOP | CHK | TMP | PBK | Compliance | Missing |",
        "|---|---|---|---|---|---|---|---|---|---|",
    ])
    for section in sorted(compliance.keys()):
        c = compliance[section]
        compl_pct = f"{c['compliance']:.0%}"
        missing = ", ".join(c["missing"]) if c["missing"] else "—"
        lines.append(
            f"| `{section}` | "
            f"{c.get('HUB', 0)} | {c.get('MST', 0)} | {c.get('PROC', 0)} | "
            f"{c.get('SOP', 0)} | {c.get('CHK', 0)} | {c.get('TMP', 0)} | {c.get('PBK', 0)} | "
            f"**{compl_pct}** | {missing} |"
        )

    avg_compliance = (
        sum(c["compliance"] for c in compliance.values()) / len(compliance)
        if compliance else 0
    )
    lines.extend([
        "",
        f"**Average compliance:** {avg_compliance:.1%}",
        "",
        "## 3. Pages thiếu Hub Parent (V4.1 issue)",
        "",
        f"Total: **{len(missing_hub)}** pages",
        "",
    ])
    for p in missing_hub[:20]:  # Top 20
        lines.append(f"- `{p.get('page_code')}` {p.get('page_name', '')}")

    lines.extend([
        "",
        "## 4. Overdue review",
        "",
        f"Total: **{len(overdue)}** pages",
        "",
    ])
    for p in overdue[:20]:
        lines.append(
            f"- `{p.get('page_code')}` {p.get('page_name', '')} "
            f"(next_review: {p.get('next_review', '?')})"
        )

    lines.extend([
        "",
        "---",
        "",
        f"_Generated by `scripts/wiki_kpi_report.py` at {today}_",
    ])
    return "\n".join(lines) + "\n"


def fetch_pages_from_lark(wiki_token: str) -> list[dict[str, Any]]:
    """Fetch pages list from Lark via wiki_navigator-like call."""
    import subprocess
    try:
        r = subprocess.run(
            ["lark-cli", "wiki", "node", "list",
             "--space-id", wiki_token, "--output", "json"],
            capture_output=True, text=True, check=True, timeout=60,
        )
        return json.loads(r.stdout)
    except (subprocess.CalledProcessError, json.JSONDecodeError) as e:
        print(f"⚠️  Could not fetch from Lark: {e}", file=sys.stderr)
        return []


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate monthly KPI report")
    parser.add_argument("--output", help="Output path (default: dist/kpi-YYYY-MM.md)")
    parser.add_argument("--push-to-lark", action="store_true", help="Push to Lark LOG page")
    parser.add_argument("--input-json", help="Load pages from JSON file (skip Lark fetch)")
    args = parser.parse_args()

    require_lark_cli()
    cfg = load_config()

    if args.input_json:
        pages = json.loads(Path(args.input_json).read_text())
    else:
        require_lark_auth()
        pages = fetch_pages_from_lark(cfg["lark"]["wiki_root_token"])

    report = render_report(pages, cfg)

    if args.output:
        out = Path(args.output)
    else:
        ts = datetime.utcnow().strftime("%Y-%m")
        out = Path("dist") / f"kpi-{ts}.md"

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(report)
    print(f"✓ Report → {out}")

    if args.push_to_lark:
        # Push to SYS-00-LOG-001 or similar LOG page (would need cfg field)
        print("⚠️  --push-to-lark needs cfg.lark.kpi_log_obj_token (TODO)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
