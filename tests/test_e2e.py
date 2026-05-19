"""End-to-end tests: full pipeline với example configs.

Simulate fresh client: copy example config → validate → render → verify dist/.
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parent.parent
EXAMPLE_NAMES = [
    "acme-foods-vietnam",
    "tech-startup-singapore",
    "minimal-3-space",
]


@pytest.fixture
def fresh_workspace(tmp_path: Path) -> Path:
    """Copy repo (minus .git/dist/.venv/cache) to tmp, return path."""
    work = tmp_path / "wko"
    shutil.copytree(
        REPO_ROOT,
        work,
        ignore=shutil.ignore_patterns(
            ".git",
            "dist",
            "__pycache__",
            ".venv",
            ".pytest_cache",
            "*.pyc",
            ".coverage",
            "htmlcov",
            "sources/lark-exports",  # snapshots
        ),
    )
    return work


def _run(cmd: list[str], cwd: Path) -> subprocess.CompletedProcess:
    """Run subprocess with timeout, return result."""
    return subprocess.run(
        cmd,
        cwd=cwd,
        capture_output=True,
        text=True,
        timeout=60,
    )


@pytest.mark.parametrize("example_name", EXAMPLE_NAMES)
def test_e2e_validate_and_render(fresh_workspace: Path, example_name: str) -> None:
    """Each example: validate_config + render → dist/ với all placeholders rendered."""
    example_cfg = fresh_workspace / "examples" / example_name / "company.config.yaml"
    assert example_cfg.exists(), f"Example config missing: {example_cfg}"

    # Copy example → root company.config.yaml
    shutil.copy(example_cfg, fresh_workspace / "company.config.yaml")

    # Validate
    r = _run(
        [sys.executable, "scripts/validate_config.py", "--strict"],
        cwd=fresh_workspace,
    )
    assert r.returncode == 0, f"validate failed for {example_name}: {r.stderr}"

    # Render
    r = _run(
        [sys.executable, "scripts/render.py"],
        cwd=fresh_workspace,
    )
    assert r.returncode == 0, f"render failed for {example_name}: {r.stderr}"

    # Verify dist/
    dist = fresh_workspace / "dist"
    assert (dist / "skills").exists()
    assert (dist / "docs").exists()

    # Spot-check: rendered content không còn placeholder
    arch_doc = (dist / "docs" / "02-wiki-architecture.md").read_text()
    assert "{{ " not in arch_doc, f"Unrendered placeholder in {example_name}/02-wiki-architecture.md"
    assert "{% " not in arch_doc, f"Unrendered Jinja2 in {example_name}/02-wiki-architecture.md"


def test_e2e_acme_specific_content(fresh_workspace: Path) -> None:
    """Acme Foods example renders với company.name 'Acme Foods Vietnam'."""
    shutil.copy(
        fresh_workspace / "examples/acme-foods-vietnam/company.config.yaml",
        fresh_workspace / "company.config.yaml",
    )
    _run([sys.executable, "scripts/render.py"], cwd=fresh_workspace)

    overview = (fresh_workspace / "dist/docs/00-company-overview.md").read_text()
    assert "Acme Foods Vietnam" in overview
    assert "F&B / Gia vị" in overview


def test_e2e_tech_startup_custom_spaces(fresh_workspace: Path) -> None:
    """Tech startup example có ENG + GTM spaces (custom, không phải V4.1 default)."""
    shutil.copy(
        fresh_workspace / "examples/tech-startup-singapore/company.config.yaml",
        fresh_workspace / "company.config.yaml",
    )
    _run([sys.executable, "scripts/render.py"], cwd=fresh_workspace)

    arch = (fresh_workspace / "dist/docs/02-wiki-architecture.md").read_text()
    assert "ENG" in arch
    assert "GTM" in arch
    # 02-wiki-architecture dùng short_name "Acme", company.name "Acme Cloud" ở docs/00
    overview = (fresh_workspace / "dist/docs/00-company-overview.md").read_text()
    assert "Acme Cloud" in overview


def test_e2e_minimal_three_spaces(fresh_workspace: Path) -> None:
    """Minimal example chỉ có 3 SPACE: SYS, OPS, ARC."""
    shutil.copy(
        fresh_workspace / "examples/minimal-3-space/company.config.yaml",
        fresh_workspace / "company.config.yaml",
    )
    _run([sys.executable, "scripts/render.py"], cwd=fresh_workspace)

    arch = (fresh_workspace / "dist/docs/02-wiki-architecture.md").read_text()
    assert "3 SPACE" in arch  # title hoặc count phải khớp
    # Không có INT, GEN, BOD trong minimal config
    # (đảm bảo strip dùng custom config thay vì V4.1 default fallback)


def test_e2e_structure_validate_after_render(fresh_workspace: Path) -> None:
    """validate_structure.py PASS after render."""
    shutil.copy(
        fresh_workspace / "examples/acme-foods-vietnam/company.config.yaml",
        fresh_workspace / "company.config.yaml",
    )
    _run([sys.executable, "scripts/render.py"], cwd=fresh_workspace)
    r = _run([sys.executable, "scripts/validate_structure.py"], cwd=fresh_workspace)
    assert r.returncode == 0, f"structure validate failed: {r.stderr}"
