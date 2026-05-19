"""Tests for rebuild_hub_toc.py."""

from __future__ import annotations

from typing import Any

from rebuild_hub_toc import (
    evaluate_branch_eligibility,
    find_section_info,
    group_pages_by_type,
    render_hub_content,
)


def test_group_pages_by_type_extracts_type_code() -> None:
    pages = [
        {"page_code": "OPS-CS-SOP-001"},
        {"page_code": "OPS-CS-SOP-002"},
        {"page_code": "OPS-CS-PROC-001"},
        {"page_code": "OPS-CS-MST-001"},
    ]
    grouped = group_pages_by_type(pages)
    assert len(grouped["SOP"]) == 2
    assert len(grouped["PROC"]) == 1
    assert len(grouped["MST"]) == 1


def test_render_hub_content_includes_section_name(sample_config: dict[str, Any]) -> None:
    content = render_hub_content("OPS-CS", "CSKH", [], sample_config)
    assert "OPS-CS-HUB-001 CSKH — Tổng quan" in content
    assert "Sticky, không đổi mã" in content


def test_render_hub_content_orders_types_execution_first(sample_config: dict[str, Any]) -> None:
    pages = [
        {"page_code": "OPS-CS-DIC-001", "page_name": "Dict"},
        {"page_code": "OPS-CS-MST-001", "page_name": "MST"},
        {"page_code": "OPS-CS-SOP-001", "page_name": "SOP"},
    ]
    content = render_hub_content("OPS-CS", "CSKH", pages, sample_config)
    # MST should appear before SOP, both before DIC
    mst_pos = content.index("### MST")
    sop_pos = content.index("### SOP")
    dic_pos = content.index("### DIC")
    assert mst_pos < sop_pos < dic_pos


def test_branch_eligibility_under_threshold(sample_config: dict[str, Any]) -> None:
    pages = [{"page_code": "OPS-CS-SOP-001"}] * 2  # 2 < min_pages*2 = 6
    result = evaluate_branch_eligibility(pages, sample_config)
    assert result["needs_branch_hub"] is False


def test_find_section_info_exists(sample_config: dict[str, Any]) -> None:
    info = find_section_info(sample_config, "OPS-CS")
    assert info is not None
    assert info["name"] == "CSKH"
    assert info["space"] == "OPS"


def test_find_section_info_missing(sample_config: dict[str, Any]) -> None:
    assert find_section_info(sample_config, "NOT-EXIST") is None
