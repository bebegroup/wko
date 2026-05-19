"""Validate company.config.yaml schema + V4.1 rules.

Usage:
    python3 scripts/validate_config.py              # lint với warnings
    python3 scripts/validate_config.py --strict     # warnings as errors
"""

from __future__ import annotations

import argparse
import re
import sys
from typing import Any

from _common import load_config

CORE_EXECUTION_FIRST_TYPES = {"HUB", "MST", "PROC", "SOP", "CHK", "TMP", "PBK"}
PAGE_CODE_RE = re.compile(r"^[A-Z]+-[A-Z0-9]+-[A-Z]+-\d{3}$")


class ValidationError(Exception):
    """Raised khi config sai schema."""


def _require(cfg: dict, path: str) -> Any:
    """Get nested key, raise ValidationError nếu thiếu."""
    parts = path.split(".")
    cur: Any = cfg
    for p in parts:
        if not isinstance(cur, dict) or p not in cur:
            raise ValidationError(f"Missing required field: {path}")
        cur = cur[p]
    return cur


def validate(cfg: dict[str, Any], strict: bool = False) -> None:
    """Validate config dict. Print warnings to stderr. Raise on errors.

    Args:
        cfg: parsed company.config.yaml
        strict: warnings become errors
    """
    # Required fields
    _require(cfg, "company.name")
    _require(cfg, "company.short_name")
    _require(cfg, "lark.domain")
    _require(cfg, "lark.wiki_root_token")
    _require(cfg, "lark.wiki_root_url")
    _require(cfg, "taxonomy.spaces")
    _require(cfg, "taxonomy.page_types")

    # Lark URL consistency
    url = cfg["lark"]["wiki_root_url"]
    token = cfg["lark"]["wiki_root_token"]
    domain = cfg["lark"]["domain"]
    if domain not in url:
        raise ValidationError(f"lark.wiki_root_url domain không khớp lark.domain ({domain})")
    if token not in url:
        raise ValidationError(f"lark.wiki_root_url phải chứa wiki_root_token ({token})")

    # Taxonomy version
    version = cfg.get("taxonomy", {}).get("version", "unknown")
    if version != "v4.1":
        msg = (
            f"⚠️  taxonomy.version = {version!r}, không phải 'v4.1'. "
            f"Default execution-first formula có thể không khớp."
        )
        if strict:
            raise ValidationError(msg)
        print(msg, file=sys.stderr)

    # Core execution-first types must exist
    type_codes = {t["code"] for t in cfg["taxonomy"]["page_types"]}
    missing = CORE_EXECUTION_FIRST_TYPES - type_codes
    if missing:
        raise ValidationError(
            f"taxonomy.page_types thiếu core types execution-first: {sorted(missing)}"
        )

    # ARC space required if arc_append_only
    arc_append = cfg.get("policies", {}).get("arc_append_only", False)
    space_codes = {s["code"] for s in cfg["taxonomy"]["spaces"]}
    if arc_append and "ARC" not in space_codes:
        raise ValidationError("policies.arc_append_only=true requires taxonomy.spaces có 'ARC'")

    # Master registry code format
    for m in cfg.get("master_registry", []):
        if not PAGE_CODE_RE.match(m.get("code", "")):
            raise ValidationError(
                f"master_registry code sai format: {m.get('code')!r}. "
                f"Expected: SPACE-SECTION-TYPE-NUMBER (e.g., SYS-00-MST-001)"
            )

    # POL primary owner table must reference real sections
    pol_rules = cfg.get("pol_mst_rules", {})
    primary_owners = pol_rules.get("primary_owner_table", {})
    all_section_codes = {
        sec["code"] for secs in cfg.get("taxonomy", {}).get("sections", {}).values() for sec in secs
    }
    for policy_name, section_code in primary_owners.items():
        if all_section_codes and section_code not in all_section_codes:
            msg = (
                f"⚠️  pol_mst_rules primary_owner '{policy_name}' → "
                f"section '{section_code}' không tồn tại trong taxonomy.sections"
            )
            if strict:
                raise ValidationError(msg)
            print(msg, file=sys.stderr)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate company.config.yaml")
    parser.add_argument("--strict", action="store_true", help="Warnings as errors")
    parser.add_argument("--config", default="company.config.yaml", help="Config path")
    args = parser.parse_args()

    try:
        cfg = load_config(args.config)
    except FileNotFoundError as e:
        print(f"❌ {e}", file=sys.stderr)
        return 1

    try:
        validate(cfg, strict=args.strict)
        print(f"✅ {args.config} valid (V4.1 schema)")
        return 0
    except ValidationError as e:
        print(f"❌ ValidationError: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
