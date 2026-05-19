"""Tests for wiki_kpi_report.py."""
from __future__ import annotations

from typing import Any

from wiki_kpi_report import (
    compute_execution_first_compliance,
    count_by_status,
    count_pages_by_section_type,
    find_missing_hub_parent,
    find_overdue_review,
    parse_page_code,
    render_report,
)


def test_parse_page_code_valid() -> None:
    assert parse_page_code("OPS-CS-SOP-001") == ("OPS", "OPS-CS", "SOP", "001")
    assert parse_page_code("SYS-00-IDX-001") == ("SYS", "SYS-00", "IDX", "001")


def test_parse_page_code_invalid() -> None:
    assert parse_page_code("invalid") is None
    assert parse_page_code("OPS-CS-SOP-1") is None  # number must be 3 digits
    assert parse_page_code("") is None


def test_count_pages_by_section_type() -> None:
    pages = [
        {"page_code": "OPS-CS-SOP-001"},
        {"page_code": "OPS-CS-SOP-002"},
        {"page_code": "OPS-CS-HUB-001"},
        {"page_code": "INT-HR-MST-001"},
    ]
    counts = count_pages_by_section_type(pages)
    assert counts["OPS-CS"]["SOP"] == 2
    assert counts["OPS-CS"]["HUB"] == 1
    assert counts["INT-HR"]["MST"] == 1


def test_compute_execution_first_full_compliance() -> None:
    counts = {
        "OPS-CS": {"HUB": 1, "MST": 1, "PROC": 1, "SOP": 3, "CHK": 1, "TMP": 1, "PBK": 1}
    }
    result = compute_execution_first_compliance(counts)
    assert result["OPS-CS"]["compliance"] == 1.0
    assert result["OPS-CS"]["missing"] == []


def test_compute_execution_first_partial() -> None:
    counts = {"OPS-CS": {"HUB": 1, "SOP": 2}}  # missing 5: MST, PROC, CHK, TMP, PBK
    result = compute_execution_first_compliance(counts)
    assert result["OPS-CS"]["compliance"] == 2 / 7
    assert set(result["OPS-CS"]["missing"]) == {"MST", "PROC", "CHK", "TMP", "PBK"}


def test_count_by_status() -> None:
    pages = [
        {"status": "Active"},
        {"status": "Active"},
        {"status": "Draft"},
        {"status": "Archived"},
    ]
    counts = count_by_status(pages)
    assert counts["Active"] == 2
    assert counts["Draft"] == 1
    assert counts["Archived"] == 1


def test_find_missing_hub_parent_excludes_hub_idx() -> None:
    pages = [
        {"page_code": "OPS-CS-SOP-001", "hub_parent": ""},  # missing
        {"page_code": "OPS-CS-SOP-002", "hub_parent": "OPS-CS-HUB-001"},  # OK
        {"page_code": "OPS-CS-HUB-001", "hub_parent": ""},  # HUB itself OK
        {"page_code": "SYS-00-IDX-001", "hub_parent": ""},  # IDX OK
    ]
    missing = find_missing_hub_parent(pages)
    assert len(missing) == 1
    assert missing[0]["page_code"] == "OPS-CS-SOP-001"


def test_find_overdue_review() -> None:
    pages = [
        {"page_code": "OPS-CS-SOP-001", "next_review": "2025-01-01"},  # overdue
        {"page_code": "OPS-CS-SOP-002", "next_review": "2099-12-31"},  # not yet
        {"page_code": "OPS-CS-SOP-003", "next_review": ""},  # not set, skip
    ]
    overdue = find_overdue_review(pages, "2026-05-19")
    assert len(overdue) == 1
    assert overdue[0]["page_code"] == "OPS-CS-SOP-001"


def test_render_report_basic(sample_config: dict[str, Any]) -> None:
    pages = [
        {"page_code": "OPS-CS-SOP-001", "status": "Active", "page_name": "x"},
    ]
    report = render_report(pages, sample_config)
    assert "Wiki KPI Report" in report
    assert "Acme Foods" in report
    assert "v4.1" in report
    assert "Execution-First Compliance" in report
