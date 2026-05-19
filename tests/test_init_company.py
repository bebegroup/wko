"""Tests for init_company.py — build_config_from_answers logic."""

from __future__ import annotations

from typing import Any

from init_company import (
    DEFAULT_SPACES_V41,
    DEFAULT_TYPES_V41,
    build_config_from_answers,
)


def _minimal_answers() -> dict[str, Any]:
    return {
        "company_name": "Beta Corp",
        "short_name": "Beta",
        "industry": "SaaS",
        "hq_country": "VN",
        "lark_subdomain": "beta",
        "lark_region": "sg",
        "wiki_root_token": "Yix7wq123ABCDEFG",
        "taxonomy_version": "v4.1",
        "use_default_spaces": True,
        "use_default_types": True,
        "contributor_email": "wiki@beta.com",
    }


def test_build_config_minimal_answers() -> None:
    cfg = build_config_from_answers(_minimal_answers())
    assert cfg["company"]["name"] == "Beta Corp"
    assert cfg["company"]["short_name"] == "Beta"
    assert cfg["lark"]["wiki_root_token"] == "Yix7wq123ABCDEFG"
    assert cfg["lark"]["wiki_root_url"].endswith("Yix7wq123ABCDEFG")


def test_build_config_v41_defaults_loaded() -> None:
    cfg = build_config_from_answers(_minimal_answers())
    assert cfg["taxonomy"]["version"] == "v4.1"
    assert len(cfg["taxonomy"]["spaces"]) == 7  # V4.1 default
    assert len(cfg["taxonomy"]["page_types"]) == 13


def test_build_config_no_default_spaces() -> None:
    answers = _minimal_answers()
    answers["use_default_spaces"] = False
    cfg = build_config_from_answers(answers)
    assert cfg["taxonomy"]["spaces"] == []


def test_build_config_cn_region_uses_feishu() -> None:
    answers = _minimal_answers()
    answers["lark_region"] = "cn"
    cfg = build_config_from_answers(answers)
    assert cfg["lark"]["domain"] == "feishu.cn"


def test_default_spaces_v41_structure() -> None:
    """V4.1 default has SYS, GEN, INT, OPS, BOD, TMP, ARC."""
    codes = {s["code"] for s in DEFAULT_SPACES_V41}
    assert codes == {"SYS", "GEN", "INT", "OPS", "BOD", "TMP", "ARC"}
    # ARC is append_only
    arc = next(s for s in DEFAULT_SPACES_V41 if s["code"] == "ARC")
    assert arc.get("append_only") is True


def test_default_types_v41_structure() -> None:
    """V4.1 default has 13 types incl. PROC and GDL."""
    codes = {t["code"] for t in DEFAULT_TYPES_V41}
    assert "PROC" in codes  # new V4.1
    assert "GDL" in codes  # new V4.1
    assert len(codes) == 13
