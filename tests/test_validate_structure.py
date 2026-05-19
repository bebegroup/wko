"""Tests for validate_structure.py."""

from __future__ import annotations

from pathlib import Path

import pytest
from validate_structure import StructureError, validate_structure


def test_passes_with_required_dirs(tmp_path: Path) -> None:
    for d in ["skills", "docs", "scripts", "docs-meta"]:
        (tmp_path / d).mkdir()
    (tmp_path / ".gitignore").write_text("dist/\n.env\ncompany.config.yaml\n")
    validate_structure(tmp_path)


def test_fails_missing_required_dir(tmp_path: Path) -> None:
    (tmp_path / "skills").mkdir()
    (tmp_path / ".gitignore").write_text("dist/\n")
    with pytest.raises(StructureError, match="docs"):
        validate_structure(tmp_path)


def test_fails_when_dist_not_gitignored(tmp_path: Path) -> None:
    for d in ["skills", "docs", "scripts", "docs-meta"]:
        (tmp_path / d).mkdir()
    (tmp_path / "dist").mkdir()
    (tmp_path / ".gitignore").write_text("nothing\n")
    with pytest.raises(StructureError, match="dist/"):
        validate_structure(tmp_path)


def test_pass_with_dist_gitignored(tmp_path: Path) -> None:
    for d in ["skills", "docs", "scripts", "docs-meta"]:
        (tmp_path / d).mkdir()
    (tmp_path / "dist").mkdir()
    (tmp_path / ".gitignore").write_text("dist/\n.env\ncompany.config.yaml\n")
    validate_structure(tmp_path)
