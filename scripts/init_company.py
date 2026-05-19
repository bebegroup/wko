"""Interactive first-time setup: build company.config.yaml from 12 questions.

Usage:
    python3 scripts/init_company.py

Tạo company.config.yaml ban đầu với V4.1 defaults (7 SPACE, 13 TYPE).
Sau khi chạy, user vẫn cần bổ sung sections, org.departments, master_registry.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import yaml
from _common import require_lark_cli

DEFAULT_SPACES_V41: list[dict[str, Any]] = [
    {
        "code": "SYS",
        "name": "Wiki Operating System",
        "order": "00",
        "icon": "⚙️",
        "owner": "IT",
        "purpose": "Hệ thống Wiki: hướng dẫn dùng, Index gốc, change log",
    },
    {
        "code": "GEN",
        "name": "Chung / General",
        "order": "01",
        "icon": "🏢",
        "owner": "HCNS + Admin",
        "purpose": "Nền tảng công ty, onboarding, công cụ, thuật ngữ",
    },
    {
        "code": "INT",
        "name": "Nội bộ / Internal",
        "order": "02",
        "icon": "🤝",
        "owner": "HCNS / Kế toán / Xfn",
        "purpose": "HR, Finance, O3K, Phối hợp liên phòng",
    },
    {
        "code": "OPS",
        "name": "Vận hành / Operations",
        "order": "03",
        "icon": "⚡",
        "owner": "Operations Lead",
        "purpose": "CS, Kho, Sàn, Hoá đơn, PIM, MFG, MKT, Livestream",
    },
    {
        "code": "BOD",
        "name": "Ban giám đốc / Board",
        "order": "04",
        "icon": "👔",
        "owner": "CEO + BOD",
        "purpose": "Chiến lược, FIN, HR cấp cao, Governance",
    },
    {
        "code": "TMP",
        "name": "Templates",
        "order": "05",
        "icon": "📋",
        "owner": "Admin",
        "purpose": "Mẫu chung (meeting, decision log, RACI, …)",
    },
    {
        "code": "ARC",
        "name": "Archive",
        "order": "99",
        "icon": "🗄",
        "owner": "Admin",
        "append_only": True,
        "purpose": "Lưu trữ append-only — không tái dùng mã",
    },
]

DEFAULT_TYPES_V41: list[dict[str, Any]] = [
    {
        "code": "HUB",
        "name": "Hub / Mục lục",
        "question": "Tôi đang ở đâu trong luồng?",
        "mandatory_per_section": True,
    },
    {
        "code": "MST",
        "name": "Master (luật/dữ liệu gốc)",
        "question": "Luật gốc / dữ liệu gốc là gì?",
        "sub_types": ["bridge", "standalone"],
    },
    {
        "code": "PROC",
        "name": "Process (luồng đa vai trò)",
        "question": "Ai làm, làm khi nào?",
        "new_in_v41": True,
    },
    {
        "code": "SOP",
        "name": "Standard Operating Procedure",
        "question": "Tôi phải làm từng bước gì?",
    },
    {"code": "CHK", "name": "Checklist", "question": "Tôi đã làm đủ chưa?"},
    {"code": "TMP", "name": "Template", "question": "Tôi dùng mẫu nào?"},
    {
        "code": "PBK",
        "name": "Playbook (lệch / lỗi / nhánh)",
        "question": "Lệch / lỗi / có nhánh thì sao?",
    },
    {
        "code": "DBD",
        "name": "Dashboard",
        "question": "Kết quả có ổn không?",
        "requires_real_data": True,
    },
    {
        "code": "POL",
        "name": "Policy (luật ngoài)",
        "scope": "external_only",
        "mandatory_sections": 8,
    },
    {
        "code": "DIC",
        "name": "Dictionary (thuật ngữ)",
        "condition": "chỉ tạo khi thuật ngữ gây sai thao tác",
    },
    {
        "code": "GDL",
        "name": "Guideline (luật mềm)",
        "condition": "chỉ tạo khi ảnh hưởng hành vi thực thi",
        "new_in_v41": True,
    },
    {"code": "LOG", "name": "Log (nhật ký / lịch sử quyết định)"},
    {"code": "IDX", "name": "Index"},
]

DEFAULT_POL_PRIMARY_OWNER: dict[str, str] = {
    "TikTok/Shopee/Web/FB policy": "OPS-ECM",
    "Luật Lao động + BHXH + NĐ lương": "INT-HR",
    "Luật Thuế + Hóa đơn điện tử": "INT-FIN",
    "Luật Quảng cáo": "OPS-MKT",
    "Luật ATTP + QCVN": "OPS-MFG",
    "NĐ 13/2023 dữ liệu cá nhân": "BOD-GOV",
}


def ask(prompt: str, default: str = "") -> str:
    """Prompt user, return default if empty input."""
    suffix = f" [{default}]" if default else ""
    val = input(f"{prompt}{suffix}: ").strip()
    return val or default


def ask_bool(prompt: str, default: bool = True) -> bool:
    suffix = "[Y/n]" if default else "[y/N]"
    val = input(f"{prompt} {suffix}: ").strip().lower()
    if not val:
        return default
    return val in ("y", "yes")


def build_config_from_answers(a: dict[str, Any]) -> dict[str, Any]:
    """Build full config dict from interactive answers."""
    domain = "feishu.cn" if a["lark_region"] == "cn" else "larksuite.com"
    return {
        "company": {
            "name": a["company_name"],
            "short_name": a["short_name"],
            "industry": a["industry"],
            "hq_country": a["hq_country"],
            "legal_entities": [a["company_name"]],
        },
        "lark": {
            "domain": domain,
            "tenant_subdomain": a["lark_subdomain"],
            "region": a["lark_region"],
            "wiki_root_token": a["wiki_root_token"],
            "wiki_root_url": f"https://{a['lark_subdomain']}.{a['lark_region']}.{domain}/wiki/{a['wiki_root_token']}",
            "master_index": {"node_token": "", "obj_token": ""},
        },
        "taxonomy": {
            "version": a["taxonomy_version"],
            "philosophy": "execution-first",
            "spaces": list(DEFAULT_SPACES_V41) if a["use_default_spaces"] else [],
            "page_types": list(DEFAULT_TYPES_V41) if a["use_default_types"] else [],
            "sections": {},
            "page_code_format": "{space}-{section_suffix}-{type}-{number:03d}",
        },
        "hub_rules": {
            "master_hub_number": "001",
            "branch_hub_min_pages": 3,
            "branch_patterns": [
                {"name": "A — sub-area", "example": "kênh bán hàng nhiều biến thể"},
                {"name": "B — audience", "example": "1 source nhiều team đọc"},
                {"name": "C — lifecycle/phase", "example": "trước/trong/sau"},
                {"name": "D — role", "example": "self-service/leader/admin"},
            ],
            "hub_parent_required": True,
        },
        "execution_first": {
            "enforce": True,
            "section_formula": {
                "required": ["1 HUB", "1-2 MST", "1 PROC", "3-5 SOP", "1 CHK", "1 TMP", "1 PBK"],
                "optional_when_needed": [
                    "0-1 DBD (chỉ khi có số liệu thật)",
                    "0-1 DIC (chỉ khi thuật ngữ gây sai thao tác)",
                    "0-1 GDL (chỉ khi ảnh hưởng hành vi)",
                    "0-1 POL (chỉ external)",
                ],
            },
            "page_purpose_questions": [
                "Tôi đang ở đâu trong luồng? → HUB",
                "Ai làm, làm khi nào? → PROC",
                "Tôi phải làm từng bước gì? → SOP",
                "Tôi đã làm đủ chưa? → CHK",
                "Tôi dùng mẫu nào? → TMP",
                "Lệch / lỗi / có nhánh? → PBK",
                "Kết quả có ổn không? → DBD",
                "Luật gốc / dữ liệu gốc? → MST",
            ],
            "rejection_rules": [
                "Vì nên có (không phục vụ thực thi cụ thể)",
                "DIC mà thuật ngữ không gây sai thao tác",
                "GDL mà guideline không ảnh hưởng cách làm",
                "DBD mà chưa có source số liệu thật",
            ],
        },
        "pol_mst_rules": {
            "pol_scope": "external_only",
            "mst_types": ["bridge", "standalone"],
            "pol_primary_owner_per_section": True,
            "primary_owner_table": dict(DEFAULT_POL_PRIMARY_OWNER),
            "pol_required_sections": 8,
            "mst_bridge_required_sections": 5,
            "cross_section_rule": "link, không copy",
        },
        "org": {"departments": []},
        "master_registry": [],
        "integrations": {
            "contributor_group_email": a["contributor_email"],
            "reviewer_bot_webhook": "",
            "reviewer_bot_name": "@wiki-reviewer",
            "contributor_group_chat_id": "",
        },
        "lark_bases": [],
        "master_index_fields": {
            "required": [
                "Page Code",
                "Page Name",
                "Space",
                "Section",
                "Type",
                "Hub Parent",
                "Owner",
                "Reviewer",
                "Status",
                "Version",
                "Security Level",
                "Link",
            ],
            "recommended": [
                "Source Type",
                "Source URL",
                "Effective Date",
                "Review Cadence",
                "Impacted Pages",
            ],
        },
        "policies": {
            "page_status_values": ["⬜ Draft", "🔄 Active", "📋 Deprecated", "✅ Archived"],
            "default_status": "⬜ Draft",
            "publish_requires_review": True,
            "review_quorum": 1,
            "arc_append_only": True,
            "no_renumber_on_rename": True,
        },
    }


def main() -> int:
    print("🚀 wko Interactive Setup\n")
    print("Tạo company.config.yaml cho tổ chức của bạn (V4.1 defaults).\n")

    require_lark_cli()

    cfg_path = Path("company.config.yaml")
    if cfg_path.exists():
        if not ask_bool("⚠️  company.config.yaml đã tồn tại. Ghi đè?", default=False):
            print("Aborted.")
            return 1

    print("\n--- 1. Identity ---")
    answers = {
        "company_name": ask("Tên công ty đầy đủ", "Acme Foods"),
        "short_name": ask("Tên ngắn (≤ 10 ký tự)", "Acme"),
        "industry": ask("Ngành", "F&B"),
        "hq_country": ask("HQ country code", "VN"),
    }

    print("\n--- 2. Lark instance ---")
    answers["lark_subdomain"] = ask(
        "Lark tenant subdomain (vd 'acme' cho acme.sg.larksuite.com)", "acme"
    )
    answers["lark_region"] = ask("Region (sg/cn/us)", "sg")
    answers["wiki_root_token"] = ask("Lark Wiki root token (từ URL /wiki/<TOKEN>)")

    print("\n--- 3. Taxonomy ---")
    answers["taxonomy_version"] = ask("Taxonomy version", "v4.1")
    answers["use_default_spaces"] = ask_bool("Dùng 7 SPACE V4.1 mặc định?")
    answers["use_default_types"] = ask_bool("Dùng 13 TYPE V4.1 mặc định?")

    print("\n--- 4. Integrations ---")
    answers["contributor_email"] = ask(
        "Group email cho contributor",
        f"wiki@{answers['lark_subdomain']}.com",
    )

    cfg = build_config_from_answers(answers)
    cfg_path.write_text(yaml.dump(cfg, sort_keys=False, allow_unicode=True))

    print(f"\n✅ Đã ghi {cfg_path}\n")
    print("Bước tiếp:")
    print("  1. Xem lại + bổ sung taxonomy.sections, org.departments, master_registry")
    print("  2. cp .env.example .env và điền LARK_APP_ID/SECRET")
    print("  3. python3 scripts/validate_config.py --strict")
    print("  4. python3 scripts/render.py")
    print("  5. Đọc docs-meta/ONBOARDING.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
