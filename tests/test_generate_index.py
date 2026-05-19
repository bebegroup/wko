"""Tests for generate_index.py."""

from __future__ import annotations

from pathlib import Path

from generate_index import build_index, extract_title


def test_extract_title_from_h1(tmp_path: Path) -> None:
    f = tmp_path / "x.md"
    f.write_text("# Skill 01 — Format chuẩn\n\nContent")
    assert extract_title(f) == "Skill 01 — Format chuẩn"


def test_extract_title_no_h1_returns_filename(tmp_path: Path) -> None:
    f = tmp_path / "noheader.md"
    f.write_text("Content without h1")
    assert extract_title(f) == "noheader"


def test_build_index_produces_sorted_list(tmp_path: Path) -> None:
    (tmp_path / "02-b.md").write_text("# Second")
    (tmp_path / "01-a.md").write_text("# First")
    (tmp_path / "README.md").write_text("existing")
    out = build_index(tmp_path, title="Skills")
    assert "# Skills" in out
    assert out.index("First") < out.index("Second")
    # Skip self-README (README.md not in output)
    assert "(README.md)" not in out
