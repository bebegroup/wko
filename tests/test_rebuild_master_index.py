"""Tests for rebuild_master_index.py — table rendering logic."""

from __future__ import annotations

from typing import Any

from rebuild_master_index import format_status_badge, render_index_markdown


def test_format_status_badge_active() -> None:
    assert "🔄" in format_status_badge("Active") or "Active" in format_status_badge("Active")


def test_format_status_badge_draft() -> None:
    assert "⬜" in format_status_badge("Draft") or "Draft" in format_status_badge("Draft")


def test_render_index_includes_v41_required_fields(sample_config: dict[str, Any]) -> None:
    """Rendered markdown should have V4.1 12 required columns incl. Hub Parent."""
    pages = [
        {
            "page_code": "SYS-00-IDX-001",
            "page_name": "Master Wiki Index",
            "space": "SYS",
            "section": "SYS-00",
            "type": "IDX",
            "hub_parent": "",
            "owner": "Admin",
            "reviewer": "Admin",
            "status": "Active",
            "version": "v1.0",
            "security_level": "Internal",
            "link": "https://...",
        },
    ]
    md = render_index_markdown(pages, sample_config)
    # All 12 required headers from V4.1 master_index_fields
    for field in sample_config["master_index_fields"]["required"]:
        assert field in md, f"Missing field {field} in rendered markdown"


def test_render_index_groups_by_space(sample_config: dict[str, Any]) -> None:
    pages = [
        {
            "page_code": "OPS-CS-SOP-001",
            "space": "OPS",
            "section": "OPS-CS",
            "type": "SOP",
            "page_name": "x",
            "hub_parent": "OPS-CS-HUB-001",
            "owner": "Ops",
            "reviewer": "Ops",
            "status": "Active",
            "version": "v1.0",
            "security_level": "Internal",
            "link": "",
        },
        {
            "page_code": "SYS-00-IDX-001",
            "space": "SYS",
            "section": "SYS-00",
            "type": "IDX",
            "page_name": "Master Index",
            "hub_parent": "",
            "owner": "Admin",
            "reviewer": "Admin",
            "status": "Active",
            "version": "v1.0",
            "security_level": "Internal",
            "link": "",
        },
    ]
    md = render_index_markdown(pages, sample_config)
    # SYS section should appear before OPS section (by order field in spaces)
    sys_pos = md.index("SYS")
    ops_pos = md.index("OPS")
    assert sys_pos < ops_pos
