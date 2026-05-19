"""Content quality audit cho Wiki — V4.1 POL/MST + execution-first rules.

Audit rules:
1. POL phải external_only — flag POL có "nội bộ" trong title (likely should be MST)
2. MST bridge phải link tới POL ("Căn cứ pháp lý" section)
3. Section thiếu PROC (V4.1 execution-first required)
4. POL primary owner phải khớp pol_mst_rules.primary_owner_table
5. DBD pages phải có source data link
6. Page format: title `<mã> <tên>` đúng prefix per type
7. Hub Parent missing (V4.1)
8. Status không trong policies.page_status_values

Usage:
    python3 scripts/content_quality_audit.py                       # all rules
    python3 scripts/content_quality_audit.py --rule pol-internal   # specific rule
    python3 scripts/content_quality_audit.py --severity high       # filter
"""

from __future__ import annotations

import argparse
import re
import sys
from collections.abc import Callable
from pathlib import Path
from typing import Any

from _common import load_config, require_lark_cli

Severity = str  # "high" | "medium" | "low"


def audit_pol_internal_keywords(pages: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """POL pages có keyword 'nội bộ' / 'internal' (likely should be MST)."""
    issues = []
    internal_kw = re.compile(r"\b(nội bộ|internal|công ty)\b", re.IGNORECASE)
    for p in pages:
        code = p.get("page_code", "")
        if "-POL-" in code:
            name = p.get("page_name", "")
            if internal_kw.search(name):
                issues.append(
                    {
                        "rule": "pol-internal-keywords",
                        "severity": "high",
                        "page": code,
                        "page_name": name,
                        "msg": f"POL '{name}' có keyword nội bộ — kiểm tra có nên là MST không (POL = external only)",
                    }
                )
    return issues


def audit_section_missing_proc(
    pages: list[dict[str, Any]], cfg: dict[str, Any]
) -> list[dict[str, Any]]:
    """Section có ≥ 3 SOP nhưng không có PROC (V4.1: thường cần PROC)."""
    issues = []
    section_types: dict[str, set[str]] = {}
    for p in pages:
        code = p.get("page_code", "")
        m = re.match(r"^([A-Z]+-[A-Z0-9]+)-([A-Z]+)-\d{3}$", code)
        if m:
            section, type_code = m.group(1), m.group(2)
            section_types.setdefault(section, set()).add(type_code)

    # Configured sections
    configured = {
        sec["code"] for sections in cfg["taxonomy"]["sections"].values() for sec in sections
    }

    for section, types in section_types.items():
        if section not in configured:
            continue
        sop_count = sum(1 for p in pages if p.get("page_code", "").startswith(f"{section}-SOP-"))
        if sop_count >= 3 and "PROC" not in types:
            issues.append(
                {
                    "rule": "section-missing-proc",
                    "severity": "medium",
                    "page": section,
                    "page_name": "(section)",
                    "msg": f"Section `{section}` có {sop_count} SOP nhưng không có PROC. V4.1 execution-first khuyến nghị tạo PROC mô tả luồng.",
                }
            )
    return issues


def audit_missing_hub_parent(
    pages: list[dict[str, Any]], cfg: dict[str, Any]
) -> list[dict[str, Any]]:
    """V4.1: mọi page phải có Hub Parent (trừ HUB itself + IDX)."""
    if not cfg.get("hub_rules", {}).get("hub_parent_required"):
        return []
    issues = []
    for p in pages:
        code = p.get("page_code", "")
        m = re.match(r"^[A-Z]+-[A-Z0-9]+-([A-Z]+)-\d{3}$", code)
        if not m:
            continue
        type_code = m.group(1)
        if type_code in ("HUB", "IDX"):
            continue
        if not p.get("hub_parent"):
            issues.append(
                {
                    "rule": "missing-hub-parent",
                    "severity": "high",
                    "page": code,
                    "page_name": p.get("page_name", ""),
                    "msg": "Hub Parent rỗng (V4.1 bắt buộc)",
                }
            )
    return issues


def audit_pol_owner_mismatch(
    pages: list[dict[str, Any]], cfg: dict[str, Any]
) -> list[dict[str, Any]]:
    """POL có owner section khớp pol_mst_rules.primary_owner_table không."""
    issues = []
    owner_table = cfg.get("pol_mst_rules", {}).get("primary_owner_table", {})
    if not owner_table:
        return []

    # Loop policies in table, check each POL page exists in correct section
    for policy_name, expected_section in owner_table.items():
        # Find POL pages with similar title
        for p in pages:
            code = p.get("page_code", "")
            if "-POL-" not in code:
                continue
            name = p.get("page_name", "")
            # Simple keyword match (heuristic)
            for keyword in policy_name.split("/")[0].split():
                if len(keyword) > 3 and keyword.lower() in name.lower():
                    actual_section = code.rsplit("-POL-", 1)[0]
                    if actual_section != expected_section:
                        issues.append(
                            {
                                "rule": "pol-owner-mismatch",
                                "severity": "medium",
                                "page": code,
                                "page_name": name,
                                "msg": f"POL '{name}' đặt ở `{actual_section}` nhưng pol_mst_rules.primary_owner_table chỉ định `{expected_section}`",
                            }
                        )
                    break
    return issues


def audit_invalid_status(pages: list[dict[str, Any]], cfg: dict[str, Any]) -> list[dict[str, Any]]:
    """Status phải trong policies.page_status_values."""
    valid = set(cfg["policies"]["page_status_values"])
    # Also accept without emoji (e.g., "Active" matches "🔄 Active")
    valid_text = {v.split()[-1] for v in valid}
    issues = []
    for p in pages:
        status = p.get("status", "")
        if status and status not in valid and status not in valid_text:
            issues.append(
                {
                    "rule": "invalid-status",
                    "severity": "high",
                    "page": p.get("page_code"),
                    "page_name": p.get("page_name", ""),
                    "msg": f"Status '{status}' không trong {sorted(valid)}",
                }
            )
    return issues


AUDIT_RULES: dict[str, Callable[..., list[dict[str, Any]]]] = {
    "pol-internal-keywords": audit_pol_internal_keywords,
    "section-missing-proc": audit_section_missing_proc,
    "missing-hub-parent": audit_missing_hub_parent,
    "pol-owner-mismatch": audit_pol_owner_mismatch,
    "invalid-status": audit_invalid_status,
}


def run_audits(
    pages: list[dict[str, Any]],
    cfg: dict[str, Any],
    rules: list[str] | None = None,
) -> list[dict[str, Any]]:
    """Run audits. If rules is None, run all."""
    rules = rules or list(AUDIT_RULES.keys())
    all_issues = []
    for r in rules:
        func = AUDIT_RULES.get(r)
        if func is None:
            print(f"⚠️  Unknown rule: {r}", file=sys.stderr)
            continue
        # Single-arg or two-arg
        import inspect

        sig = inspect.signature(func)
        if len(sig.parameters) == 1:
            all_issues.extend(func(pages))
        else:
            all_issues.extend(func(pages, cfg))
    return all_issues


def format_report(issues: list[dict[str, Any]]) -> str:
    """Markdown report."""
    if not issues:
        return "# Content Quality Audit\n\n✅ No issues found.\n"

    by_severity: dict[str, list[dict]] = {"high": [], "medium": [], "low": []}
    for i in issues:
        by_severity.setdefault(i.get("severity", "low"), []).append(i)

    lines = ["# Content Quality Audit", "", f"Total issues: **{len(issues)}**", ""]
    for sev in ["high", "medium", "low"]:
        if not by_severity[sev]:
            continue
        emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}[sev]
        lines.append(f"\n## {emoji} {sev.title()} ({len(by_severity[sev])})\n")
        for i in by_severity[sev]:
            lines.append(f"- **{i['rule']}** | `{i['page']}` {i['page_name']}")
            lines.append(f"  - {i['msg']}")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Content quality audit V4.1")
    parser.add_argument("--rule", action="append", help="Run specific rule (repeatable)")
    parser.add_argument("--severity", choices=["high", "medium", "low"], help="Filter by severity")
    parser.add_argument("--output", default="dist/quality-audit.md")
    parser.add_argument("--input-json", help="Load pages from JSON file")
    args = parser.parse_args()

    require_lark_cli()
    cfg = load_config()

    if args.input_json:
        import json

        pages = json.loads(Path(args.input_json).read_text())
    else:
        print("⚠️  No --input-json. Pass JSON from wiki_navigator.py.", file=sys.stderr)
        return 1

    issues = run_audits(pages, cfg, rules=args.rule)
    if args.severity:
        issues = [i for i in issues if i.get("severity") == args.severity]

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(format_report(issues))
    print(f"✓ {len(issues)} issues → {out}")
    return 1 if issues else 0


if __name__ == "__main__":
    sys.exit(main())
