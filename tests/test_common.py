"""Tests for scripts/_common.py."""
from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from _common import (
    load_config,
    require_lark_auth,
    require_lark_cli,
    version_lt,
)


# ─── load_config ──────────────────────────────────────────────
def test_load_config_returns_dict(tmp_repo: Path) -> None:
    cfg = load_config(str(tmp_repo / "company.config.yaml"))
    assert isinstance(cfg, dict)
    assert cfg["company"]["name"] == "Acme Foods"


def test_load_config_missing_file_raises(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError, match="company.config.yaml"):
        load_config(str(tmp_path / "nonexistent.yaml"))


# ─── version_lt ───────────────────────────────────────────────
@pytest.mark.parametrize(
    "a,b,expected",
    [
        ("1.0.30", "1.0.30", False),  # equal
        ("1.0.29", "1.0.30", True),  # less
        ("1.0.31", "1.0.30", False),  # greater
        ("1.0.5", "1.0.30", True),  # 5 < 30 numerically
        ("1.1.0", "1.0.99", False),  # minor wins
        ("0.99.0", "1.0.0", True),  # major wins
    ],
)
def test_version_lt(a: str, b: str, expected: bool) -> None:
    assert version_lt(a, b) is expected


# ─── require_lark_cli ────────────────────────────────────────
def test_require_lark_cli_missing_exits(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("shutil.which", lambda _: None)
    with pytest.raises(SystemExit) as exc_info:
        require_lark_cli()
    assert "lark-cli không tìm thấy" in str(exc_info.value)


def test_require_lark_cli_old_version_exits(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("shutil.which", lambda _: "/usr/local/bin/lark-cli")
    fake_result = subprocess.CompletedProcess(
        args=[], returncode=0, stdout="lark-cli version 1.0.20\n"
    )
    monkeypatch.setattr("subprocess.run", lambda *a, **kw: fake_result)
    with pytest.raises(SystemExit) as exc_info:
        require_lark_cli()
    assert "1.0.20" in str(exc_info.value)
    assert "1.0.30" in str(exc_info.value)


def test_require_lark_cli_ok(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("shutil.which", lambda _: "/usr/local/bin/lark-cli")
    fake_result = subprocess.CompletedProcess(
        args=[], returncode=0, stdout="lark-cli version 1.0.30\n"
    )
    monkeypatch.setattr("subprocess.run", lambda *a, **kw: fake_result)
    require_lark_cli()  # should not raise


# ─── require_lark_auth ───────────────────────────────────────
def test_require_lark_auth_not_logged_in(monkeypatch: pytest.MonkeyPatch) -> None:
    fake_result = subprocess.CompletedProcess(
        args=[], returncode=1, stdout="not authenticated", stderr=""
    )
    monkeypatch.setattr("subprocess.run", lambda *a, **kw: fake_result)
    with pytest.raises(SystemExit) as exc_info:
        require_lark_auth()
    assert "Chưa đăng nhập" in str(exc_info.value)


def test_require_lark_auth_ok(monkeypatch: pytest.MonkeyPatch) -> None:
    fake_result = subprocess.CompletedProcess(
        args=[], returncode=0, stdout="logged in as user@acme.com", stderr=""
    )
    monkeypatch.setattr("subprocess.run", lambda *a, **kw: fake_result)
    require_lark_auth()  # should not raise
