"""Tests for scripts/validate_config.py."""

from __future__ import annotations

import copy
from typing import Any

import pytest
from validate_config import ValidationError, validate


def test_valid_config_passes(sample_config: dict[str, Any]) -> None:
    validate(sample_config)  # should not raise


def test_missing_company_name_fails(sample_config: dict[str, Any]) -> None:
    cfg = copy.deepcopy(sample_config)
    del cfg["company"]["name"]
    with pytest.raises(ValidationError, match="company.name"):
        validate(cfg)


def test_missing_wiki_root_token_fails(sample_config: dict[str, Any]) -> None:
    cfg = copy.deepcopy(sample_config)
    del cfg["lark"]["wiki_root_token"]
    with pytest.raises(ValidationError, match="lark.wiki_root_token"):
        validate(cfg)


def test_taxonomy_version_warning(
    sample_config: dict[str, Any], capsys: pytest.CaptureFixture
) -> None:
    cfg = copy.deepcopy(sample_config)
    cfg["taxonomy"]["version"] = "v3.0"
    validate(cfg)
    captured = capsys.readouterr()
    assert "v3.0" in captured.err
    assert "v4.1" in captured.err


def test_taxonomy_version_strict_fails(sample_config: dict[str, Any]) -> None:
    cfg = copy.deepcopy(sample_config)
    cfg["taxonomy"]["version"] = "v3.0"
    with pytest.raises(ValidationError, match="v4.1"):
        validate(cfg, strict=True)


def test_missing_core_page_types_fails(sample_config: dict[str, Any]) -> None:
    cfg = copy.deepcopy(sample_config)
    cfg["taxonomy"]["page_types"] = [{"code": "HUB", "name": "Hub"}]  # missing MST, ...
    with pytest.raises(ValidationError, match="core types"):
        validate(cfg)


def test_master_registry_invalid_code_format_fails(sample_config: dict[str, Any]) -> None:
    cfg = copy.deepcopy(sample_config)
    cfg["master_registry"] = [{"code": "INVALID", "name": "x", "owner": "y"}]
    with pytest.raises(ValidationError, match="master_registry"):
        validate(cfg)


def test_spaces_must_have_arc_when_append_only(sample_config: dict[str, Any]) -> None:
    cfg = copy.deepcopy(sample_config)
    cfg["taxonomy"]["spaces"] = [s for s in cfg["taxonomy"]["spaces"] if s["code"] != "ARC"]
    cfg["policies"]["arc_append_only"] = True
    with pytest.raises(ValidationError, match="ARC"):
        validate(cfg)


def test_lark_url_domain_mismatch(sample_config: dict[str, Any]) -> None:
    cfg = copy.deepcopy(sample_config)
    cfg["lark"]["wiki_root_url"] = "https://wrong-domain.com/wiki/Yix7wqABCDEFGHIJ"
    with pytest.raises(ValidationError, match="wiki_root_url"):
        validate(cfg)


def test_lark_url_token_mismatch(sample_config: dict[str, Any]) -> None:
    cfg = copy.deepcopy(sample_config)
    cfg["lark"]["wiki_root_url"] = "https://acme.sg.larksuite.com/wiki/DIFFERENT_TOKEN"
    with pytest.raises(ValidationError, match="wiki_root_token"):
        validate(cfg)
