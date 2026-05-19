"""Tests for content_quality_audit.py."""

from __future__ import annotations

from typing import Any

from content_quality_audit import (
    audit_invalid_status,
    audit_missing_hub_parent,
    audit_pol_internal_keywords,
    audit_section_missing_proc,
    format_report,
    run_audits,
)


def test_audit_pol_internal_keywords_flags_internal_pol() -> None:
    pages = [
        {"page_code": "INT-HR-POL-001", "page_name": "Nội quy lao động (nội bộ)"},
        {"page_code": "OPS-ECM-POL-001", "page_name": "TikTok Shop policy"},
    ]
    issues = audit_pol_internal_keywords(pages)
    assert len(issues) == 1
    assert issues[0]["page"] == "INT-HR-POL-001"


def test_audit_missing_hub_parent(sample_config: dict[str, Any]) -> None:
    pages = [
        {"page_code": "OPS-CS-SOP-001", "hub_parent": ""},
        {"page_code": "OPS-CS-HUB-001", "hub_parent": ""},  # OK for HUB
        {"page_code": "SYS-00-IDX-001", "hub_parent": ""},  # OK for IDX
        {"page_code": "OPS-CS-MST-001", "hub_parent": "OPS-CS-HUB-001"},  # OK
    ]
    issues = audit_missing_hub_parent(pages, sample_config)
    assert len(issues) == 1
    assert issues[0]["page"] == "OPS-CS-SOP-001"


def test_audit_section_missing_proc(sample_config: dict[str, Any]) -> None:
    # OPS-CS với 3 SOP nhưng không PROC → issue
    pages = [
        {"page_code": "OPS-CS-SOP-001"},
        {"page_code": "OPS-CS-SOP-002"},
        {"page_code": "OPS-CS-SOP-003"},
        # Note: SYS-00 không có SOP, no issue
        {"page_code": "SYS-00-IDX-001"},
    ]
    issues = audit_section_missing_proc(pages, sample_config)
    assert len(issues) == 1
    assert issues[0]["page"] == "OPS-CS"
    assert "PROC" in issues[0]["msg"]


def test_audit_invalid_status_accepts_emoji_and_text(sample_config: dict[str, Any]) -> None:
    pages = [
        {"page_code": "p1", "status": "🔄 Active"},  # OK (full)
        {"page_code": "p2", "status": "Active"},  # OK (text only)
        {"page_code": "p3", "status": "Bogus"},  # FAIL
    ]
    issues = audit_invalid_status(pages, sample_config)
    assert len(issues) == 1
    assert issues[0]["page"] == "p3"


def test_run_audits_aggregates_all_rules(sample_config: dict[str, Any]) -> None:
    pages = [
        {"page_code": "OPS-CS-SOP-001", "hub_parent": "", "status": "Active"},
    ]
    issues = run_audits(pages, sample_config)
    # At minimum: missing-hub-parent should fire
    assert any(i["rule"] == "missing-hub-parent" for i in issues)


def test_format_report_no_issues() -> None:
    assert "✅ No issues" in format_report([])


def test_format_report_groups_by_severity() -> None:
    issues = [
        {"rule": "a", "severity": "high", "page": "P1", "page_name": "n1", "msg": "msg1"},
        {"rule": "b", "severity": "medium", "page": "P2", "page_name": "n2", "msg": "msg2"},
        {"rule": "c", "severity": "low", "page": "P3", "page_name": "n3", "msg": "msg3"},
    ]
    report = format_report(issues)
    assert "🔴 High" in report
    assert "🟡 Medium" in report
    assert "🟢 Low" in report
