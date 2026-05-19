"""Shared utilities for wko scripts.

Every script that interacts with Lark MUST call ``require_lark_cli()`` and
``require_lark_auth()`` at the top of ``main()`` for fail-fast behavior.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

import yaml

LARK_CLI_MIN_VERSION = "1.0.30"


def load_config(path: str = "company.config.yaml") -> dict[str, Any]:
    """Load company.config.yaml. Raises FileNotFoundError with helpful message."""
    cfg_file = Path(path)
    if not cfg_file.exists():
        raise FileNotFoundError(
            f"{path} not found. Run `python3 scripts/init_company.py` "
            f"or copy `company.config.yaml.example`."
        )
    with open(cfg_file) as f:
        return yaml.safe_load(f)


def version_lt(a: str, b: str) -> bool:
    """Return True if version a < b (semantic). Both must be 'X.Y.Z' format."""
    a_parts = tuple(int(x) for x in a.split("."))
    b_parts = tuple(int(x) for x in b.split("."))
    return a_parts < b_parts


def require_lark_cli() -> None:
    """Fail-fast nếu lark-cli không cài hoặc version cũ."""
    if shutil.which("lark-cli") is None:
        sys.exit(
            "❌ lark-cli không tìm thấy.\n"
            "   Cài đặt:\n"
            "     macOS:  brew install lark-cli\n"
            "     Linux:  curl -fsSL https://github.com/larksuite/lark-cli/releases/latest/download/lark-cli-linux-x64.tar.gz | sudo tar -xz -C /usr/local/bin\n"
            "     npm:    npm i -g @larksuiteoapi/lark-cli\n"
            "   Sau đó: lark-cli auth login --as user"
        )
    try:
        out = subprocess.run(
            ["lark-cli", "--version"],
            capture_output=True,
            text=True,
            check=True,
            timeout=5,
        ).stdout
        version = out.strip().split()[-1]
        if version_lt(version, LARK_CLI_MIN_VERSION):
            sys.exit(
                f"❌ lark-cli phiên bản {version} quá cũ. "
                f"Yêu cầu ≥ {LARK_CLI_MIN_VERSION}.\n"
                f"   Nâng cấp: brew upgrade lark-cli"
            )
    except (subprocess.TimeoutExpired, subprocess.CalledProcessError) as e:
        sys.exit(f"❌ lark-cli không phản hồi: {e}")


def require_lark_auth() -> None:
    """Fail-fast nếu chưa lark-cli auth login. Chỉ gọi cho script cần API call."""
    result = subprocess.run(
        ["lark-cli", "auth", "status"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0 or "expired" in result.stdout.lower():
        sys.exit(
            "❌ Chưa đăng nhập Lark.\n"
            "   Chạy: lark-cli auth login --as user\n"
            "   Hoặc: lark-cli auth login --as bot"
        )
