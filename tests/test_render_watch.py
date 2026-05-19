"""Smoke test for --watch mode. Marked interactive — skip in CI."""
from __future__ import annotations

import subprocess
import sys
import time
from pathlib import Path

import pytest


@pytest.mark.interactive
@pytest.mark.slow
def test_watch_mode_detects_change(tmp_repo: Path) -> None:
    """Start watch, modify file, verify re-render happens within 3s."""
    (tmp_repo / "skills").mkdir(exist_ok=True)
    src = tmp_repo / "skills" / "watched.md"
    src.write_text("# {{ company.name }}\n")

    repo_root = Path(__file__).resolve().parent.parent
    proc = subprocess.Popen(
        [
            sys.executable,
            str(repo_root / "scripts" / "render.py"),
            "--watch",
            "--config",
            str(tmp_repo / "company.config.yaml"),
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=tmp_repo,
        text=True,
    )
    try:
        time.sleep(1.5)  # let observer start
        src.write_text("# {{ company.short_name }}\n")  # trigger re-render
        time.sleep(2)
        out_file = tmp_repo / "dist" / "skills" / "watched.md"
        assert out_file.exists(), "dist/skills/watched.md not created"
        content = out_file.read_text()
        assert "Acme" in content, f"Expected 'Acme' in {content!r}"
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
