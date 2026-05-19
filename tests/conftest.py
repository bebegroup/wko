"""Shared pytest fixtures for wko tests."""
from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest
import yaml


@pytest.fixture
def sample_config() -> dict[str, Any]:
    """Minimal valid company.config.yaml as dict (V4.1 default subset)."""
    return {
        "company": {
            "name": "Acme Foods",
            "short_name": "Acme",
            "industry": "F&B",
            "hq_country": "VN",
            "legal_entities": ["Acme Foods Co., Ltd"],
        },
        "lark": {
            "domain": "larksuite.com",
            "tenant_subdomain": "acme",
            "region": "sg",
            "wiki_root_token": "Yix7wqABCDEFGHIJ",
            "wiki_root_url": "https://acme.sg.larksuite.com/wiki/Yix7wqABCDEFGHIJ",
            "master_index": {
                "node_token": "UxOkABCDEFGHIJKL",
                "obj_token": "Vy3RABCDEFGHIJKL",
            },
        },
        "taxonomy": {
            "version": "v4.1",
            "philosophy": "execution-first",
            "spaces": [
                {"code": "SYS", "name": "Wiki OS", "order": "00", "icon": "⚙️", "owner": "IT"},
                {"code": "OPS", "name": "Vận hành", "order": "03", "icon": "⚡", "owner": "Ops"},
                {
                    "code": "ARC",
                    "name": "Archive",
                    "order": "99",
                    "icon": "🗄",
                    "owner": "Admin",
                    "append_only": True,
                },
            ],
            "page_types": [
                {"code": "HUB", "name": "Hub", "question": "Tôi đang ở đâu?"},
                {"code": "MST", "name": "Master"},
                {"code": "PROC", "name": "Process", "new_in_v41": True},
                {"code": "SOP", "name": "SOP"},
                {"code": "CHK", "name": "Checklist"},
                {"code": "TMP", "name": "Template"},
                {"code": "PBK", "name": "Playbook"},
            ],
            "sections": {
                "SYS": [{"code": "SYS-00", "name": "Wiki OS"}],
                "OPS": [{"code": "OPS-CS", "name": "CSKH"}],
            },
            "page_code_format": "{space}-{section_suffix}-{type}-{number:03d}",
        },
        "org": {"departments": [{"code": "HCNS", "name": "HCNS"}]},
        "master_registry": [
            {"code": "SYS-00-MST-001", "name": "Master Registry", "owner": "Admin"}
        ],
        "integrations": {
            "contributor_group_email": "wiki@acme.com",
            "reviewer_bot_webhook": "",
            "reviewer_bot_name": "@wiki-reviewer",
        },
        "lark_bases": [],
        "master_index_fields": {
            "required": [
                "Page Code", "Page Name", "Space", "Section", "Type",
                "Hub Parent", "Owner", "Reviewer", "Status", "Version",
                "Security Level", "Link",
            ],
            "recommended": [
                "Source Type", "Source URL", "Effective Date",
                "Review Cadence", "Impacted Pages",
            ],
        },
        "policies": {
            "page_status_values": ["⬜ Draft", "🔄 Active", "📋 Deprecated", "✅ Archived"],
            "default_status": "⬜ Draft",
            "publish_requires_review": True,
            "arc_append_only": True,
        },
    }


@pytest.fixture
def tmp_repo(tmp_path: Path, sample_config: dict) -> Path:
    """Temporary directory mimicking wko repo structure."""
    (tmp_path / "skills").mkdir()
    (tmp_path / "docs").mkdir()
    (tmp_path / "dist").mkdir()
    cfg_file = tmp_path / "company.config.yaml"
    cfg_file.write_text(yaml.dump(sample_config, allow_unicode=True))
    return tmp_path


@pytest.fixture
def mock_lark_cli_installed(monkeypatch: pytest.MonkeyPatch) -> None:
    """Make shutil.which('lark-cli') return a fake path."""
    monkeypatch.setattr(
        "shutil.which",
        lambda x: "/usr/local/bin/lark-cli" if x == "lark-cli" else None,
    )
