"""Tests for migrate_v4_to_v41.py."""

from __future__ import annotations

from migrate_v4_to_v41 import (
    SECTION_MAPPING,
    SPACE_MAPPING,
    build_migration_plan,
    migrate_page_code,
    suggest_proc_reclassification,
)


def test_migrate_com_to_gen() -> None:
    assert migrate_page_code("COM-01-MST-001") == "GEN-01-MST-001"
    assert migrate_page_code("COM-04-DIC-001") == "GEN-04-DIC-001"


def test_migrate_emg_to_arc_old() -> None:
    assert migrate_page_code("EMG-OPS-PBK-001") == "ARC-OLD-PBK-001"


def test_migrate_no_change_for_other_spaces() -> None:
    assert migrate_page_code("OPS-CS-SOP-001") is None
    assert migrate_page_code("SYS-00-IDX-001") is None
    assert migrate_page_code("INT-HR-MST-001") is None


def test_migrate_invalid_returns_none() -> None:
    assert migrate_page_code("invalid") is None
    assert migrate_page_code("") is None


def test_suggest_proc_for_luong() -> None:
    page = {"page_code": "OPS-CS-SOP-001", "page_name": "Luồng xử lý CSKH"}
    assert suggest_proc_reclassification(page) is True


def test_no_proc_suggest_for_plain_sop() -> None:
    page = {"page_code": "OPS-CS-SOP-001", "page_name": "Tiếp nhận yêu cầu"}
    assert suggest_proc_reclassification(page) is False


def test_build_migration_plan_summary() -> None:
    pages = [
        {"page_code": "COM-01-MST-001", "page_name": "x"},
        {"page_code": "EMG-OPS-PBK-001", "page_name": "y"},
        {"page_code": "OPS-CS-SOP-001", "page_name": "Luồng xử lý"},
        {"page_code": "SYS-00-IDX-001", "page_name": "Index"},
    ]
    plan = build_migration_plan(pages)
    assert plan["summary"]["renames"] == 1  # COM → GEN
    assert plan["summary"]["archives"] == 1  # EMG → ARC
    assert plan["summary"]["proc_suggestions"] == 1  # SOP "Luồng"


def test_space_mapping_constants() -> None:
    assert SPACE_MAPPING["COM"] == "GEN"
    assert SPACE_MAPPING["EMG"] == "ARC"
    assert SECTION_MAPPING["COM-01"] == "GEN-01"
