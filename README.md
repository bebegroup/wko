# wko — Wiki Operating System (Lark)

> Template repo công khai để dựng **Wiki Company OS** trên Lark Wiki / Feishu Wiki.
> Cấu hình 1 file `company.config.yaml`, render qua Jinja2 → publish lên Lark.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Lark](https://img.shields.io/badge/Lark-required-blue)](https://www.larksuite.com)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org)

---

## ⚠️ Yêu cầu bắt buộc

Repo này **KHÔNG chạy** nếu thiếu một trong các thứ sau:

1. **`lark-cli >= 1.0.30`** — system-level binary (không qua pip)
2. **Python `>= 3.11`**
3. **Tài khoản Lark + Custom App** có scope: `wiki:*`, `docx:*`, `drive:*`, `im:*`

Mọi script Python đều gọi `lark-cli` qua `subprocess`. Repo này **không dùng `lark-oapi`** (Python SDK).

---

## Quick start (10 phút)

```bash
# 1. Fork + clone (private fork khuyến nghị — chứa Lark token)
gh repo fork saucevn/wko --clone --fork-name wko-acme
cd wko-acme
gh repo edit --visibility private
git remote add upstream https://github.com/saucevn/wko.git

# 2. Cài lark-cli (macOS — xem ONBOARDING cho Linux/npm)
brew install lark-cli
lark-cli auth login --as user

# 3. Setup Python
python3 -m venv .venv && source .venv/bin/activate
pip install -r scripts/requirements.txt

# 4. Cấu hình
cp company.config.yaml.example company.config.yaml
# Sửa company.config.yaml theo công ty bạn, hoặc:
python3 scripts/init_company.py        # interactive wizard

python3 scripts/validate_config.py --strict

# 5. Render template → dist/
python3 scripts/render.py
```

Setup chi tiết 30 phút (8 bước): [`docs-meta/ONBOARDING.md`](docs-meta/ONBOARDING.md).

---

## Cấu trúc

```
wko/
├── skills/           # 12 quy tắc viết Wiki (source, có Jinja2 placeholder)
├── docs/             # 11 docs tham chiếu công ty (source)
├── scripts/          # 17 Python scripts (render, validate, Lark integration)
├── docs-meta/        # Meta docs về template (ONBOARDING, ARCHITECTURE, ...)
├── examples/         # 3 ví dụ company.config.yaml
├── .github/          # CI workflows + issue templates
└── dist/             # gitignored — output của render.py
```

---

## Taxonomy mặc định: V4.1 Execution-First

- **7 SPACE:** `SYS / GEN / INT / OPS / BOD / TMP / ARC`
- **13 TYPE:** `MST / SOP / CHK / TMP / HUB / PBK / DBD / DIC / POL / LOG / IDX / PROC / GDL`
- **HUB-001 sticky** + 4 branch patterns (sub-area / audience / lifecycle / role)
- **POL = external only**, MST = internal (bridge derive từ POL, hoặc standalone)
- **Execution-first**: mỗi section có 1 HUB + 1-2 MST + 1 PROC + 3-5 SOP + 1 CHK + 1 TMP + 1 PBK

Customizable hoàn toàn qua `company.config.yaml`. Xem [`examples/`](examples/) cho 3 shape khác nhau.

---

## Tài liệu

| Audience | File |
|---|---|
| Client mới setup | [`docs-meta/ONBOARDING.md`](docs-meta/ONBOARDING.md) |
| Hiểu placeholder + render | [`docs-meta/ARCHITECTURE.md`](docs-meta/ARCHITECTURE.md) |
| Workflow publish lên Lark | [`docs-meta/PUBLISHING.md`](docs-meta/PUBLISHING.md) |
| Sync upstream | [`docs-meta/UPGRADING.md`](docs-meta/UPGRADING.md) |
| AI agent rules | [`CLAUDE.md`](CLAUDE.md) |
| Đóng góp upstream | [`CONTRIBUTING.md`](CONTRIBUTING.md) |
| Lộ trình | [`ROADMAP.md`](ROADMAP.md) |
| Báo vulnerability | [`SECURITY.md`](SECURITY.md) |

---

## License

[MIT](LICENSE) — Copyright (c) 2026 [saucevn](https://github.com/saucevn).

Repo này được chắt lọc từ private repo "Thích Cay Company OS" (V4.1 Execution-First taxonomy). Mọi nội dung công ty cụ thể đã được strip — chỉ giữ framework + skills + tooling.

## Contributing

Welcome! Xem [`CONTRIBUTING.md`](CONTRIBUTING.md).

## Issues & Discussion

- 🐛 [Bug reports](https://github.com/saucevn/wko/issues)
- 💡 [Feature requests](https://github.com/saucevn/wko/issues/new?template=feature_request.yml)
- 💬 [Discussions](https://github.com/saucevn/wko/discussions)
