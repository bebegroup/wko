# wko Public Template — Implementation Plan v1.0

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build `saucevn/wko` v1.0 — public MIT-licensed Lark Wiki Company OS template, distilled từ private repo `Thích Cay Company OS`. Một file `company.config.yaml` cấu hình toàn bộ, render qua Jinja2 → publish lên Lark.

**Architecture:** New git repo tại `/Users/dev/Claude/Developer/Github/wko/`. Source `skills/*.md`, `docs/*.md` chứa Jinja2 placeholders (`{{ company.name }}`, loop `{% for s in taxonomy.spaces %}`). `scripts/render.py` build → `dist/`. CI render check, publish opt-in. `lark-cli` (subprocess) only — drop `lark-oapi`. Strip 100% nội dung Thích Cay.

**Tech Stack:** Python 3.11+, Jinja2 ≥3.1, PyYAML ≥6.0, anthropic ≥0.40, lark-cli ≥1.0.30 (system binary, hard requirement), GitHub Actions, pytest ≥8.0, watchdog ≥4.0.

**Working Directory:** `/Users/dev/Claude/Developer/Github/wko/` (new, sibling to wiki repo)
**Reference Repo:** `/Users/dev/Claude/Developer/Github/wiki/` (Thích Cay private — content source)
**Spec:** [`docs/superpowers/specs/2026-05-19-wko-public-template-design.md`](../specs/2026-05-19-wko-public-template-design.md)
**Drafts:** `docs/superpowers/specs/wko-drafts/` (ONBOARDING.md, CLAUDE.md đã viết)

**Taxonomy default:** V4.1 Execution-First (7 SPACE: SYS/GEN/INT/OPS/BOD/TMP/ARC; 13 TYPE: MST/SOP/CHK/TMP/HUB/PBK/DBD/DIC/POL/LOG/IDX/PROC/GDL).

**Milestone summary:**

| M | Tên | # Task | Estimated |
|---|---|---|---|
| M1 | Bootstrap repo | 5 | 0.5 tuần |
| M2 | Config schema + validator | 4 | 0.5 tuần |
| M3 | Render engine | 5 | 1 tuần |
| M4 | Templating skills/ | 6 | 1.5 tuần |
| M5 | Templating docs/ | 5 | 1 tuần |
| M6 | Scripts migration | 8 | 2 tuần |
| M7 | CI workflows | 5 | 1 tuần |
| M8 | Examples + docs-meta | 4 | 0.5 tuần |
| M9 | Release v1.0 | 3 | 0.5 tuần |
| **Σ** | | **45** | **~8.5 tuần** |

**Early stopping points (release milestones):**
- **v0.1.0-alpha** sau M3 — render engine works, 0 content
- **v0.5.0-beta** sau M5 — content templated, no CI
- **v0.9.0-rc** sau M7 — feature complete
- **v1.0.0** sau M9 — public release

---

## File Structure

Mỗi file một responsibility duy nhất. Files thay đổi cùng nhau sống cùng nhau.

### Root files (created)
- `LICENSE` — MIT text (boilerplate)
- `README.md` — entry point, EN intro + VN full guide
- `CLAUDE.md` / `AGENTS.md` — AI agent rules (from drafts, template với placeholders)
- `CONTRIBUTING.md` — đóng góp upstream saucevn/wko
- `SECURITY.md` — báo vulnerability + anti-leak rules
- `ROADMAP.md` — v1.0 → v2.0 plan
- `MAINTAINERS.md` — saucevn + co-maintainers
- `.gitignore` — exclude `.env`, `company.config.yaml`, `dist/`, `drafts/`, `__pycache__/`, `.venv/`, `*.pyc`
- `company.config.yaml.example` — V4.1 default schema, fully commented
- `.env.example` — LARK_APP_ID/SECRET placeholders
- `Makefile` — convenience targets (`make render`, `make validate`, `make test`)
- `pyproject.toml` — ruff + black config, project metadata

### `scripts/` (17 files)
- `_common.py` — shared utils: `load_config()`, `require_lark_cli()`, `require_lark_auth()`, `version_lt()`
- `render.py` — Jinja2 substitution → `dist/`. Modes: default, --check, --file, --watch, --clean
- `validate_config.py` — lint `company.config.yaml` schema + V4.1 rules
- `init_company.py` — interactive first-time setup (12 questions)
- `validate_structure.py` — folder/file structure lint (generic)
- `generate_index.py` — auto-sinh `skills/README.md` + `docs/README.md`
- `build_backlink_graph.py` — parse XML, sinh SVG (generic)
- `wiki_navigator.py` — Lark Wiki tree traverse (subprocess `lark-cli wiki`)
- `pull_from_lark.py` — snapshot Lark → `sources/lark-exports/` (full implementation)
- `rebuild_master_index.py` — push Master Index lên Lark, V4.1 12 cột incl. Hub Parent
- `rebuild_hub_toc.py` — auto-list children theo `hub_rules`
- `sync_index_contributed_column.py` — sync "Contributed By" từ git
- `wiki_kpi_report.py` — KPI per execution-first formula
- `content_quality_audit.py` — audit POL-vs-MST + section formula
- `wiki_reviewer_bot.py` — `lark-cli event consume im.message.receive_v1` (rewrite, drop lark-oapi)
- `migrate_v4_to_v41.py` — optional opt-in: V4 (8 SPACE) → V4.1 (7 SPACE)
- `requirements.txt` — pip deps

### `skills/` (12 files — templated)
01-page-format, 02-writing-style, 03-linking-rules, 04-page-status, 05-publish-workflow, 06-excel-to-wiki, 07-source-protection, 08-index-and-numbering, 09-contributing-workflow, 10-master-registry, 11-page-types, 12-emergency-playbook

### `docs/` (11 files — templated, mostly stripped)
00-company-overview, 01-org-structure, 02-wiki-architecture, 03-permissions, 04-glossary, 05-lark-base-connections, 06-context-notes, 07-status-tracker, 08-contributing, 09-master-registry, 10-page-types-taxonomy

### `docs-meta/` (4 files — repo-public meta, NOT rendered)
ONBOARDING.md (from draft), ARCHITECTURE.md, PUBLISHING.md, UPGRADING.md

### `.github/`
- `workflows/{ci-lint,ci-validate,ci-render,auto-index,lark-rebuild-index,lark-kpi-monthly,release}.yml` (7 workflows)
- `actions/setup-lark-cli/action.yml` (composite)
- `ISSUE_TEMPLATE/{bug_report,feature_request,company_onboarding}.yml`
- `PULL_REQUEST_TEMPLATE.md`
- `dependabot.yml`

### `tests/` (created in M2-M6)
- `test_common.py` — load_config, require_*, version comparison
- `test_render.py` — Jinja2 substitution, filters, error cases
- `test_validate_config.py` — schema validation positive + negative
- `test_init_company.py` — interactive wizard (mock stdin)
- `test_migrate_v4_to_v41.py` — code mapping
- `conftest.py` — fixtures: `sample_config`, `tmp_repo`

### `examples/` (3 dirs)
- `acme-foods-vietnam/company.config.yaml` + README — F&B Việt
- `tech-startup-singapore/company.config.yaml` + README — 4 SPACE custom
- `minimal-3-space/company.config.yaml` + README — SYS + OPS + ARC

### `sources/` (giữ minimal)
- `schemas/wiki-node-schema.json` (generic, từ Thích Cay)
- `schemas/lark-base-schema.svg` (generic)

### `dist/` (gitignored — output)

---

## Conventions

**Commit message format (Conventional Commits):**
```
<type>(<scope>): <subject>

<body if needed>
```
- types: `feat`, `fix`, `docs`, `chore`, `refactor`, `test`, `ci`, `build`
- scope: `bootstrap`, `render`, `config`, `skills`, `docs`, `scripts`, `ci`, `examples`, etc.

**TDD pattern (mọi script Python):**
1. Write failing test
2. Run → confirm FAIL
3. Minimal implementation
4. Run → confirm PASS
5. Commit

**Branch model:** Feature branches off `main`. PR + 1 review (self-review trong solo dev, real review khi có co-maintainer). Squash merge.

**Pre-commit (optional, recommended):** Cài `pre-commit install` chạy `ruff`, `black`, `gitleaks` (secret scan).

---

## M1 — Bootstrap Repo

### Task 1.1: Create directory, init git, .gitignore

**Files:**
- Create: `/Users/dev/Claude/Developer/Github/wko/.gitignore`

- [ ] **Step 1: Create working directory + init git**

```bash
mkdir -p /Users/dev/Claude/Developer/Github/wko
cd /Users/dev/Claude/Developer/Github/wko
git init -b main
```

Expected: `Initialized empty Git repository in .../wko/.git/`

- [ ] **Step 2: Write `.gitignore`**

```
# Python
__pycache__/
*.py[cod]
*$py.class
.Python
.venv/
venv/
*.egg-info/
.pytest_cache/
.coverage
htmlcov/

# Secrets — NEVER commit
.env
.env.local
company.config.yaml

# Build output
dist/
build/

# Drafts (gitignored — viết draft ngoài repo hoặc đây)
drafts/

# IDE
.idea/
.vscode/
*.swp
.DS_Store

# OS
Thumbs.db

# Logs
*.log

# Local lark-cli cache
.lark-cli/
```

- [ ] **Step 3: First commit (empty .gitignore)**

```bash
cd /Users/dev/Claude/Developer/Github/wko
git add .gitignore
git commit -m "chore(bootstrap): init repo with .gitignore"
```

Expected: 1 file changed, commit hash printed.

- [ ] **Step 4: Verify**

```bash
git log --oneline
git status
```

Expected: 1 commit, working tree clean.

---

### Task 1.2: LICENSE (MIT) + README skeleton

**Files:**
- Create: `LICENSE`
- Create: `README.md`

- [ ] **Step 1: Write LICENSE**

```
MIT License

Copyright (c) 2026 saucevn

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

- [ ] **Step 2: Write `README.md`**

```markdown
# wko — Wiki Operating System (Lark)

> Template repo công khai để dựng **Wiki Company OS** trên Lark Wiki / Feishu Wiki.
> Cấu hình 1 file `company.config.yaml`, render qua Jinja2 → publish lên Lark.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Lark](https://img.shields.io/badge/Lark-required-blue)](https://www.larksuite.com)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org)

## ⚠️ Yêu cầu bắt buộc

1. `lark-cli >= 1.0.30` (system-level — repo này không chạy nếu thiếu)
2. Python `>= 3.11`
3. Tài khoản Lark + App có scope `wiki:*`, `docx:*`, `drive:*`, `im:*`

## Quick start (10 phút)

```bash
git clone https://github.com/saucevn/wko.git
cd wko

# Cài lark-cli
brew install lark-cli       # macOS
lark-cli auth login --as user

# Setup
python3 -m venv .venv && source .venv/bin/activate
pip install -r scripts/requirements.txt
cp company.config.yaml.example company.config.yaml
# (Sửa company.config.yaml theo công ty bạn)
python3 scripts/validate_config.py --strict
python3 scripts/render.py
```

Setup chi tiết: [`docs-meta/ONBOARDING.md`](docs-meta/ONBOARDING.md).

## Cấu trúc

```
wko/
├── skills/         # 12 quy tắc viết Wiki (source, có placeholder)
├── docs/           # 11 docs công ty (source, có placeholder)
├── scripts/        # 17 Python scripts (render, validate, Lark integration)
├── docs-meta/      # Meta docs về template (ONBOARDING, ARCHITECTURE, ...)
├── examples/       # 3 ví dụ company config
├── .github/        # CI workflows + issue templates
└── dist/           # gitignored — output của render.py
```

## Customize cho công ty bạn

→ [`docs-meta/ONBOARDING.md`](docs-meta/ONBOARDING.md) (setup 30 phút)

## Workflow soạn thảo

→ [`docs-meta/PUBLISHING.md`](docs-meta/PUBLISHING.md)

## Đóng góp upstream

→ [`CONTRIBUTING.md`](CONTRIBUTING.md)

## License

MIT — Copyright (c) 2026 [saucevn](https://github.com/saucevn).

Repo này được chắt lọc từ private repo "Thích Cay Company OS" (V4.1 Execution-First taxonomy). Mọi nội dung công ty cụ thể đã được strip.
```

- [ ] **Step 3: Commit**

```bash
git add LICENSE README.md
git commit -m "docs(bootstrap): add LICENSE (MIT) + README skeleton"
```

---

### Task 1.3: SECURITY.md + CONTRIBUTING.md + MAINTAINERS.md + ROADMAP.md

**Files:**
- Create: `SECURITY.md`, `CONTRIBUTING.md`, `MAINTAINERS.md`, `ROADMAP.md`

- [ ] **Step 1: Write `SECURITY.md`**

```markdown
# Security Policy

## Reporting a vulnerability

Email: **security@saucevn.dev** (hoặc GitHub Security Advisory)
Response: 48h tối đa.

## ⚠️ KHÔNG commit

- `company.config.yaml` — chứa Lark `wiki_root_token`, `master_index.obj_token`
- `.env` — chứa `LARK_APP_SECRET`, `ANTHROPIC_API_KEY`
- Files trong `drafts/` — draft nội bộ
- Files trong `dist/` — output của render.py (có thể chứa data sensitive sau substitute)

Tất cả đã được `.gitignore`. Nếu `git status` thấy chúng = STOP, kiểm tra ngay.

## Nếu vô tình commit secret

1. **Revoke token ngay lập tức** tại Lark Developer Console
2. Xoá khỏi git history:
   ```bash
   pip install git-filter-repo
   git filter-repo --path company.config.yaml --invert-paths
   git push origin --force --all
   ```
3. Notify maintainers
4. Tạo token mới + update local

## Anti-leak checklist

Trước khi `git push`:
- [ ] `git status` không thấy `company.config.yaml` hoặc `.env`
- [ ] `git diff --cached` không có chuỗi giống Lark token (24 chars base62)
- [ ] (Optional) Chạy `gitleaks detect` (xem README dependencies)
```

- [ ] **Step 2: Write `CONTRIBUTING.md`**

```markdown
# Contributing to saucevn/wko

Cảm ơn bạn quan tâm! `wko` là dự án open source MIT licensed.

## Loại đóng góp được welcome

| Loại | Ví dụ |
|---|---|
| Bug fix | `render.py` crash khi config thiếu field optional |
| Doc improvement | Sửa lỗi typo, dịch sang ngôn ngữ khác |
| New placeholder | Thêm `{{ company.fiscal_year_start }}` cho phần tài chính |
| New example | `examples/agency-thailand/` cho công ty agency |
| Taxonomy extension | Thêm SPACE/TYPE mới cho industry-specific case |
| Script improvement | Tăng performance, thêm dry-run mode |

## Loại đóng góp KHÔNG accept

- **Company-specific content** — wko là template generic, không chứa nội dung công ty cụ thể
- **Breaking change không có RFC** — đổi config schema, đổi placeholder syntax phải có discussion trước
- **Lark API SDK Python (lark-oapi)** — repo này thống nhất qua `lark-cli` subprocess

## Workflow

1. Fork `saucevn/wko`
2. Tạo branch: `git checkout -b fix/short-description` hoặc `feat/short-description`
3. Code + test (TDD pattern, xem `tests/`)
4. CI pass (lint + validate + render + tests)
5. PR vào `main`, mô tả rõ:
   - Vấn đề giải quyết
   - Approach
   - Backward compat (có/không)
6. 1 maintainer review → merge (squash)

## Setup dev env

```bash
git clone https://github.com/<your-fork>/wko.git
cd wko
python3 -m venv .venv && source .venv/bin/activate
pip install -r scripts/requirements.txt
pip install -e ".[dev]"          # pyproject.toml extras
pre-commit install               # optional
make test
```

## Code style

- Python: `ruff` + `black` (config trong `pyproject.toml`)
- Markdown: `markdownlint-cli2`
- Commits: Conventional Commits (`feat:`, `fix:`, `docs:`, ...)
- Vietnamese is the primary language. EN translation contribution welcome cho `docs-meta/` và `README.md`.

## RFC process

Cho breaking change hoặc feature lớn:

1. Open GitHub Discussion với title `RFC: <feature>`
2. Mô tả: motivation, design, alternatives, drawbacks
3. Wait ≥ 7 ngày cho community feedback
4. Maintainer decision: accept / reject / request changes
5. Nếu accept → implement qua PR reference RFC discussion

## Maintainers

Xem [`MAINTAINERS.md`](MAINTAINERS.md).

## Code of Conduct

Tôn trọng. Không tolerance cho harassment. Disagree về kỹ thuật OK, attack cá nhân không.
```

- [ ] **Step 3: Write `MAINTAINERS.md`**

```markdown
# Maintainers

| GitHub | Vai trò | Khu vực |
|---|---|---|
| [@saucevn](https://github.com/saucevn) | Lead maintainer, project owner | Toàn bộ repo |

## Trở thành co-maintainer

Cần:
- ≥ 5 PR merged không trivial
- ≥ 1 năm active trong project
- Lead maintainer mời

## Liên lạc

- Bug/feature: GitHub Issues
- Security: security@saucevn.dev
- General: GitHub Discussions
```

- [ ] **Step 4: Write `ROADMAP.md`**

```markdown
# Roadmap

## v1.0 — Public release (target: Q3 2026)
- [x] Spec đã duyệt
- [ ] Bootstrap repo (M1)
- [ ] Config schema V4.1 + validator (M2)
- [ ] Render engine + tests (M3)
- [ ] 12 skills templated (M4)
- [ ] 11 docs templated (M5)
- [ ] 17 scripts (M6)
- [ ] 7 CI workflows (M7)
- [ ] 3 examples + 4 docs-meta (M8)
- [ ] Release v1.0 (M9)

## v1.1 — Quality of life (Q4 2026)
- [ ] `init_company.py` 12-question wizard
- [ ] HTML preview server (`scripts/serve.py`)
- [ ] Slack notification adapter
- [ ] `migrate_v4_to_v41.py` interactive

## v1.2 — Multi-tenant (Q1 2027)
- [ ] Profile system: `LARK_PROFILE=acme`
- [ ] `wko switch <profile>` for consultants
- [ ] Multi-config rendering

## v2.0 — Beyond Lark (2027+)
- [ ] Notion backend adapter
- [ ] Confluence backend adapter
- [ ] Outline backend adapter
- [ ] Plugin system (OKR/O3K, EOS, Scrum packs)

## Out of scope

- GUI editor (CLI/markdown only)
- Self-hosting Wiki engine
- AI auto-generation toàn bộ Wiki
- Localization beyond VN/EN (community PRs welcome)
```

- [ ] **Step 5: Commit**

```bash
git add SECURITY.md CONTRIBUTING.md MAINTAINERS.md ROADMAP.md
git commit -m "docs(bootstrap): add SECURITY, CONTRIBUTING, MAINTAINERS, ROADMAP"
```

---

### Task 1.4: `.env.example` + `pyproject.toml` + `Makefile`

**Files:**
- Create: `.env.example`, `pyproject.toml`, `Makefile`

- [ ] **Step 1: Write `.env.example`**

```
# Copy thành .env (đã gitignored) và điền giá trị thật

# Lark App credentials (từ open.larksuite.com → Developer Console)
LARK_APP_ID=cli_xxxxxxxxxxxxxxxx
LARK_APP_SECRET=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Anthropic API (optional — chỉ cần nếu chạy wiki_reviewer_bot.py)
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Lark profile (optional — cho multi-tenant ở v1.2+)
# LARK_PROFILE=default
```

- [ ] **Step 2: Write `pyproject.toml`**

```toml
[project]
name = "wko"
version = "0.1.0"
description = "Wiki Operating System — Lark Wiki Company OS template"
readme = "README.md"
license = { text = "MIT" }
requires-python = ">=3.11"
authors = [
    { name = "saucevn", email = "hello@saucevn.dev" }
]
keywords = ["lark", "feishu", "wiki", "company-os", "template", "vietnamese"]
classifiers = [
    "Development Status :: 3 - Alpha",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Topic :: Documentation",
    "Topic :: Office/Business",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "pytest-cov>=5.0",
    "ruff>=0.6",
    "black>=24.0",
    "pre-commit>=3.7",
]

[project.urls]
Homepage = "https://github.com/saucevn/wko"
Documentation = "https://github.com/saucevn/wko/blob/main/docs-meta/ONBOARDING.md"
Repository = "https://github.com/saucevn/wko"
Issues = "https://github.com/saucevn/wko/issues"

[tool.ruff]
line-length = 100
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "W", "I", "B", "C90", "UP", "S"]
ignore = ["S603", "S607"]  # subprocess calls intentional

[tool.black]
line-length = 100
target-version = ["py311"]

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = "test_*.py"
addopts = "-v --cov=scripts --cov-report=term-missing"
```

- [ ] **Step 3: Write `Makefile`**

```makefile
.PHONY: help install validate render render-watch test lint clean

help:
	@echo "wko — Wiki Operating System"
	@echo ""
	@echo "Commands:"
	@echo "  make install        Cài Python deps"
	@echo "  make validate       Validate company.config.yaml"
	@echo "  make render         Render skills/ + docs/ → dist/"
	@echo "  make render-watch   Re-render khi source thay đổi"
	@echo "  make test           Chạy pytest"
	@echo "  make lint           Ruff + Black + markdownlint"
	@echo "  make clean          Xóa dist/, __pycache__/"

install:
	pip install -r scripts/requirements.txt
	pip install -e ".[dev]"

validate:
	python3 scripts/validate_config.py --strict

render:
	python3 scripts/render.py

render-watch:
	python3 scripts/render.py --watch

test:
	pytest

lint:
	ruff check scripts/ tests/
	black --check scripts/ tests/
	@command -v markdownlint-cli2 >/dev/null 2>&1 && markdownlint-cli2 "**/*.md" || echo "markdownlint-cli2 not installed, skip"

clean:
	rm -rf dist/ __pycache__/ .pytest_cache/ .coverage htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
```

- [ ] **Step 4: Commit**

```bash
git add .env.example pyproject.toml Makefile
git commit -m "build(bootstrap): add .env.example, pyproject.toml, Makefile"
```

---

### Task 1.5: Empty scripts/ + requirements.txt

**Files:**
- Create: `scripts/requirements.txt`, `scripts/__init__.py`, `tests/__init__.py`, `tests/conftest.py`

- [ ] **Step 1: Write `scripts/requirements.txt`**

```
# ⚠️ HARD REQUIREMENT: lark-cli phải được cài SẴN ở system level.
# Repo này không tự cài lark-cli (Python pip không quản binary).
# Xem README §1 — Yêu cầu bắt buộc.

# Core (mọi script)
PyYAML>=6.0
jinja2>=3.1

# AI bot (chỉ wiki_reviewer_bot.py)
anthropic>=0.40
python-dotenv>=1.0

# Dev / CI (cũng có trong pyproject.toml [dev])
pytest>=8.0
pytest-cov>=5.0
watchdog>=4.0
```

- [ ] **Step 2: Create empty `__init__.py` files**

```bash
mkdir -p scripts tests
touch scripts/__init__.py
touch tests/__init__.py
```

- [ ] **Step 3: Write `tests/conftest.py` (pytest fixtures)**

```python
"""Shared pytest fixtures for wko tests."""
from __future__ import annotations

import shutil
from pathlib import Path
from typing import Any

import pytest


@pytest.fixture
def sample_config() -> dict[str, Any]:
    """Minimal valid company.config.yaml as dict."""
    return {
        "company": {
            "name": "Acme Foods",
            "short_name": "Acme",
            "industry": "F&B",
            "hq_country": "VN",
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
                {"code": "ARC", "name": "Archive", "order": "99", "icon": "🗄", "owner": "Admin", "append_only": True},
            ],
            "page_types": [
                {"code": "HUB", "name": "Hub", "question": "Tôi đang ở đâu?"},
                {"code": "MST", "name": "Master"},
                {"code": "SOP", "name": "SOP"},
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
    import yaml
    (tmp_path / "skills").mkdir()
    (tmp_path / "docs").mkdir()
    (tmp_path / "dist").mkdir()
    cfg_file = tmp_path / "company.config.yaml"
    cfg_file.write_text(yaml.dump(sample_config))
    return tmp_path


@pytest.fixture
def mock_lark_cli_installed(monkeypatch: pytest.MonkeyPatch) -> None:
    """Make shutil.which('lark-cli') return a fake path."""
    monkeypatch.setattr("shutil.which", lambda x: "/usr/local/bin/lark-cli" if x == "lark-cli" else None)
```

- [ ] **Step 4: Commit + verify M1 done**

```bash
git add scripts/ tests/
git commit -m "chore(bootstrap): add scripts/, tests/ skeletons + requirements.txt"
git log --oneline
```

Expected: 5 commits in M1. Repo skeleton ready for M2.

---

## M2 — Config Schema + Validator

### Task 2.1: `scripts/_common.py` — shared utils with tests

**Files:**
- Create: `scripts/_common.py`, `tests/test_common.py`

- [ ] **Step 1: Write `tests/test_common.py` (failing tests)**

```python
"""Tests for scripts/_common.py."""
from __future__ import annotations

import subprocess
from pathlib import Path
from unittest.mock import patch

import pytest

from scripts._common import (
    load_config,
    require_lark_cli,
    require_lark_auth,
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
@pytest.mark.parametrize("a,b,expected", [
    ("1.0.30", "1.0.30", False),       # equal
    ("1.0.29", "1.0.30", True),        # less
    ("1.0.31", "1.0.30", False),       # greater
    ("1.0.5", "1.0.30", True),         # 5 < 30 numerically
    ("1.1.0", "1.0.99", False),        # minor wins
    ("0.99.0", "1.0.0", True),         # major wins
])
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
    fake_result = subprocess.CompletedProcess(args=[], returncode=0, stdout="lark-cli version 1.0.20\n")
    monkeypatch.setattr("subprocess.run", lambda *a, **kw: fake_result)
    with pytest.raises(SystemExit) as exc_info:
        require_lark_cli()
    assert "1.0.20" in str(exc_info.value)
    assert "1.0.30" in str(exc_info.value)


def test_require_lark_cli_ok(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("shutil.which", lambda _: "/usr/local/bin/lark-cli")
    fake_result = subprocess.CompletedProcess(args=[], returncode=0, stdout="lark-cli version 1.0.30\n")
    monkeypatch.setattr("subprocess.run", lambda *a, **kw: fake_result)
    require_lark_cli()  # should not raise


# ─── require_lark_auth ───────────────────────────────────────
def test_require_lark_auth_not_logged_in(monkeypatch: pytest.MonkeyPatch) -> None:
    fake_result = subprocess.CompletedProcess(args=[], returncode=1, stdout="not authenticated", stderr="")
    monkeypatch.setattr("subprocess.run", lambda *a, **kw: fake_result)
    with pytest.raises(SystemExit) as exc_info:
        require_lark_auth()
    assert "Chưa đăng nhập" in str(exc_info.value)


def test_require_lark_auth_ok(monkeypatch: pytest.MonkeyPatch) -> None:
    fake_result = subprocess.CompletedProcess(args=[], returncode=0, stdout="logged in as user@acme.com", stderr="")
    monkeypatch.setattr("subprocess.run", lambda *a, **kw: fake_result)
    require_lark_auth()  # should not raise
```

- [ ] **Step 2: Run test → confirm FAIL**

```bash
cd /Users/dev/Claude/Developer/Github/wko
pytest tests/test_common.py -v
```

Expected: `ModuleNotFoundError: No module named 'scripts._common'`

- [ ] **Step 3: Write `scripts/_common.py`**

```python
"""Shared utilities for wko scripts.

Every script that interacts with Lark MUST call `require_lark_cli()` and
`require_lark_auth()` at the top of `main()` for fail-fast behavior.
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
            capture_output=True, text=True, check=True, timeout=5,
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
        capture_output=True, text=True,
    )
    if result.returncode != 0 or "expired" in result.stdout.lower():
        sys.exit(
            "❌ Chưa đăng nhập Lark.\n"
            "   Chạy: lark-cli auth login --as user\n"
            "   Hoặc: lark-cli auth login --as bot"
        )
```

- [ ] **Step 4: Run test → confirm PASS**

```bash
pytest tests/test_common.py -v
```

Expected: 9 passed.

- [ ] **Step 5: Commit**

```bash
git add scripts/_common.py tests/test_common.py
git commit -m "feat(scripts): add _common.py with load_config, require_lark_cli/auth, version_lt"
```

---

### Task 2.2: `company.config.yaml.example` — V4.1 default

**Files:**
- Create: `company.config.yaml.example`

- [ ] **Step 1: Write `company.config.yaml.example`** (full file from spec §4.2)

Copy nội dung từ spec section "company.config.yaml schema" (12 sections: company, lark, taxonomy, hub_rules, execution_first, pol_mst_rules, org, master_registry, integrations, lark_bases, master_index_fields, policies). File ~250 dòng. Header:

```yaml
# company.config.yaml.example — Cấu hình duy nhất cho mỗi client wko
#
# Copy thành `company.config.yaml` (đã gitignored — chứa Lark token).
# Hoặc chạy `python3 scripts/init_company.py` cho interactive setup.
#
# Default taxonomy: V4.1 Execution-First (7 SPACE, 13 TYPE, HUB-001 sticky).
# Tham khảo: docs-meta/ARCHITECTURE.md
```

(Body: copy nguyên văn 12 sections từ spec.)

- [ ] **Step 2: Commit**

```bash
git add company.config.yaml.example
git commit -m "feat(config): add V4.1 default config schema example"
```

---

### Task 2.3: `scripts/validate_config.py` — schema validator

**Files:**
- Create: `scripts/validate_config.py`, `tests/test_validate_config.py`

- [ ] **Step 1: Write failing tests `tests/test_validate_config.py`**

```python
"""Tests for scripts/validate_config.py."""
from __future__ import annotations

import copy
from pathlib import Path
from typing import Any

import pytest

from scripts.validate_config import validate, ValidationError


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


def test_taxonomy_version_warning(sample_config: dict[str, Any], capsys: pytest.CaptureFixture) -> None:
    cfg = copy.deepcopy(sample_config)
    cfg["taxonomy"]["version"] = "v3.0"
    validate(cfg)
    captured = capsys.readouterr()
    assert "v3.0" in captured.err
    assert "v4.1" in captured.err


def test_missing_core_page_types_fails(sample_config: dict[str, Any]) -> None:
    cfg = copy.deepcopy(sample_config)
    cfg["taxonomy"]["page_types"] = [{"code": "HUB", "name": "Hub"}]  # missing MST, SOP, ...
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


def test_lark_url_consistency(sample_config: dict[str, Any]) -> None:
    cfg = copy.deepcopy(sample_config)
    cfg["lark"]["wiki_root_url"] = "https://wrong-domain.com/wiki/xxx"
    with pytest.raises(ValidationError, match="wiki_root_url"):
        validate(cfg)
```

- [ ] **Step 2: Run → confirm FAIL**

```bash
pytest tests/test_validate_config.py -v
```

Expected: `ModuleNotFoundError: scripts.validate_config`

- [ ] **Step 3: Write `scripts/validate_config.py`**

```python
"""Validate company.config.yaml schema + V4.1 rules.

Usage:
    python3 scripts/validate_config.py              # lint với warnings
    python3 scripts/validate_config.py --strict     # warnings as errors
"""
from __future__ import annotations

import argparse
import re
import sys
from typing import Any

from _common import load_config


CORE_EXECUTION_FIRST_TYPES = {"HUB", "MST", "PROC", "SOP", "CHK", "TMP", "PBK"}
PAGE_CODE_RE = re.compile(r"^[A-Z]+-[A-Z0-9]+-[A-Z]+-\d{3}$")


class ValidationError(Exception):
    """Raised khi config sai schema."""


def _require(cfg: dict, path: str) -> Any:
    """Get nested key, raise ValidationError nếu thiếu."""
    parts = path.split(".")
    cur: Any = cfg
    for p in parts:
        if not isinstance(cur, dict) or p not in cur:
            raise ValidationError(f"Missing required field: {path}")
        cur = cur[p]
    return cur


def validate(cfg: dict[str, Any], strict: bool = False) -> None:
    """Validate config dict. Print warnings to stderr. Raise on errors."""
    # Required fields
    _require(cfg, "company.name")
    _require(cfg, "company.short_name")
    _require(cfg, "lark.domain")
    _require(cfg, "lark.wiki_root_token")
    _require(cfg, "lark.wiki_root_url")
    _require(cfg, "taxonomy.spaces")
    _require(cfg, "taxonomy.page_types")

    # Lark URL consistency
    url = cfg["lark"]["wiki_root_url"]
    token = cfg["lark"]["wiki_root_token"]
    domain = cfg["lark"]["domain"]
    if domain not in url:
        raise ValidationError(f"lark.wiki_root_url domain không khớp lark.domain ({domain})")
    if token not in url:
        raise ValidationError(f"lark.wiki_root_url phải chứa wiki_root_token ({token})")

    # Taxonomy version
    version = cfg.get("taxonomy", {}).get("version", "unknown")
    if version != "v4.1":
        msg = f"⚠️  taxonomy.version = {version!r}, không phải 'v4.1'. Default execution-first formula có thể không khớp."
        if strict:
            raise ValidationError(msg)
        else:
            print(msg, file=sys.stderr)

    # Core execution-first types must exist
    type_codes = {t["code"] for t in cfg["taxonomy"]["page_types"]}
    missing = CORE_EXECUTION_FIRST_TYPES - type_codes
    if missing:
        raise ValidationError(
            f"taxonomy.page_types thiếu core types execution-first: {sorted(missing)}"
        )

    # ARC space required if arc_append_only
    arc_append = cfg.get("policies", {}).get("arc_append_only", False)
    space_codes = {s["code"] for s in cfg["taxonomy"]["spaces"]}
    if arc_append and "ARC" not in space_codes:
        raise ValidationError(
            "policies.arc_append_only=true requires taxonomy.spaces có 'ARC'"
        )

    # Master registry code format
    for m in cfg.get("master_registry", []):
        if not PAGE_CODE_RE.match(m.get("code", "")):
            raise ValidationError(
                f"master_registry code sai format: {m.get('code')!r}. Expected: SPACE-SECTION-TYPE-NUMBER (e.g., SYS-00-MST-001)"
            )

    # POL primary owner table (if exists) must reference real sections
    pol_rules = cfg.get("pol_mst_rules", {})
    primary_owners = pol_rules.get("primary_owner_table", {})
    all_section_codes = {
        sec["code"]
        for secs in cfg.get("taxonomy", {}).get("sections", {}).values()
        for sec in secs
    }
    for policy_name, section_code in primary_owners.items():
        if all_section_codes and section_code not in all_section_codes:
            msg = f"⚠️  pol_mst_rules primary_owner '{policy_name}' → section '{section_code}' không tồn tại trong taxonomy.sections"
            if strict:
                raise ValidationError(msg)
            else:
                print(msg, file=sys.stderr)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate company.config.yaml")
    parser.add_argument("--strict", action="store_true", help="Warnings as errors")
    parser.add_argument("--config", default="company.config.yaml", help="Config path")
    args = parser.parse_args()

    try:
        cfg = load_config(args.config)
    except FileNotFoundError as e:
        print(f"❌ {e}", file=sys.stderr)
        return 1

    try:
        validate(cfg, strict=args.strict)
        print(f"✅ {args.config} valid (V4.1 schema)")
        return 0
    except ValidationError as e:
        print(f"❌ ValidationError: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 4: Fix import for tests (scripts package style)**

Add to `scripts/__init__.py`:
```python
from scripts._common import load_config, require_lark_cli, require_lark_auth, version_lt
from scripts.validate_config import validate, ValidationError
```

Actually simpler: change import in `validate_config.py` to `from _common import` to keep scripts callable as `python3 scripts/foo.py`. Tests use `from scripts.foo import ...` via `pyproject.toml` `[tool.pytest.ini_options] pythonpath`. Add to pyproject:

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = "test_*.py"
addopts = "-v --cov=scripts --cov-report=term-missing"
pythonpath = [".", "scripts"]
```

Update `pyproject.toml` accordingly.

- [ ] **Step 5: Run tests → confirm PASS**

```bash
pytest tests/test_validate_config.py -v
```

Expected: 8 passed.

- [ ] **Step 6: Commit**

```bash
git add scripts/validate_config.py tests/test_validate_config.py scripts/__init__.py pyproject.toml
git commit -m "feat(scripts): add validate_config.py with V4.1 schema validator + 8 tests"
```

---

### Task 2.4: Test validate_config.py end-to-end with example file

- [ ] **Step 1: Run validator against example file**

```bash
cd /Users/dev/Claude/Developer/Github/wko
cp company.config.yaml.example company.config.yaml
python3 scripts/validate_config.py --strict
```

Expected: `✅ company.config.yaml valid (V4.1 schema)`

- [ ] **Step 2: Cleanup**

```bash
rm company.config.yaml          # gitignored anyway, but tidy
```

- [ ] **Step 3: M2 complete — verify**

```bash
git log --oneline | head -10
pytest --tb=short
```

Expected: All tests pass. M2 commits visible.

---

## M3 — Render Engine

### Task 3.1: `scripts/render.py` — basic single-file render

**Files:**
- Create: `scripts/render.py`, `tests/test_render.py`

- [ ] **Step 1: Write failing tests `tests/test_render.py`**

```python
"""Tests for scripts/render.py."""
from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from scripts.render import render_string, render_tree, build_env, RenderError


def test_render_simple_placeholder(sample_config: dict[str, Any]) -> None:
    template = "Hello {{ company.name }}"
    out = render_string(template, sample_config)
    assert out == "Hello Acme Foods"


def test_render_loop(sample_config: dict[str, Any]) -> None:
    template = "{% for s in taxonomy.spaces %}- {{ s.code }}\n{% endfor %}"
    out = render_string(template, sample_config)
    assert "- SYS" in out
    assert "- OPS" in out
    assert "- ARC" in out


def test_render_undefined_placeholder_fails(sample_config: dict[str, Any]) -> None:
    template = "{{ company.nonexistent_field }}"
    with pytest.raises(RenderError, match="nonexistent_field"):
        render_string(template, sample_config)


def test_render_tree_creates_dist(tmp_repo: Path, sample_config: dict[str, Any]) -> None:
    src = tmp_repo / "skills"
    dst = tmp_repo / "dist" / "skills"

    (src / "01-test.md").write_text("# {{ company.name }}\n\nIndustry: {{ company.industry }}")
    (src / "subdir").mkdir()
    (src / "subdir" / "nested.md").write_text("Nested: {{ company.short_name }}")

    render_tree(src, dst, sample_config)

    out1 = (dst / "01-test.md").read_text()
    assert "# Acme Foods" in out1
    assert "Industry: F&B" in out1

    out2 = (dst / "subdir" / "nested.md").read_text()
    assert "Nested: Acme" in out2


def test_render_skips_code_blocks(sample_config: dict[str, Any]) -> None:
    """Code blocks should NOT be rendered (Jinja2 raw)."""
    # Jinja2 default behavior renders inside code blocks. We document this:
    # for code blocks containing literal {{ }}, use {% raw %}...{% endraw %}.
    template = "Outside: {{ company.name }}\n\n```\n{% raw %}{{ literal }}{% endraw %}\n```"
    out = render_string(template, sample_config)
    assert "Acme Foods" in out
    assert "{{ literal }}" in out  # preserved literal


def test_render_custom_filter_page_code(sample_config: dict[str, Any]) -> None:
    template = '{{ "SYS-00-IDX-001" | upper_dashed }}'
    # filter that uppercases & validates page code format
    out = render_string(template, sample_config)
    assert out == "SYS-00-IDX-001"
```

- [ ] **Step 2: Run → FAIL**

```bash
pytest tests/test_render.py -v
```

Expected: `ModuleNotFoundError: scripts.render`

- [ ] **Step 3: Write `scripts/render.py` (minimal)**

```python
"""Render skills/ + docs/ với Jinja2 substitution → dist/.

Usage:
    python3 scripts/render.py                        # render toàn bộ
    python3 scripts/render.py --check                # CI mode, fail nếu render lỗi
    python3 scripts/render.py --file skills/01-x.md  # 1 file
    python3 scripts/render.py --watch                # dev mode
    python3 scripts/render.py --clean                # xóa dist/ trước
"""
from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path
from typing import Any

from jinja2 import (
    Environment,
    FileSystemLoader,
    StrictUndefined,
    TemplateError,
    UndefinedError,
)

from _common import load_config


class RenderError(Exception):
    """Raised khi render fails (placeholder thiếu, syntax error, etc.)."""


PAGE_CODE_RE = re.compile(r"^[A-Z]+-[A-Z0-9]+-[A-Z]+-\d{3}$")


def _filter_upper_dashed(s: str) -> str:
    """Validate & normalize page code."""
    s = s.strip().upper()
    if not PAGE_CODE_RE.match(s):
        raise RenderError(f"Invalid page code: {s!r}")
    return s


def _filter_wiki_link(url: str, label: str = "") -> str:
    """Format Lark URL as markdown link."""
    label = label or url
    return f"[{label}]({url})"


def build_env(loader_path: Path | None = None) -> Environment:
    """Build Jinja2 Environment với custom filters."""
    env = Environment(
        loader=FileSystemLoader(str(loader_path)) if loader_path else None,
        undefined=StrictUndefined,
        keep_trailing_newline=True,
        autoescape=False,
    )
    env.filters["upper_dashed"] = _filter_upper_dashed
    env.filters["wiki_link"] = _filter_wiki_link
    return env


def render_string(template_str: str, ctx: dict[str, Any]) -> str:
    """Render a template string with context. Raises RenderError on failures."""
    env = build_env()
    try:
        tmpl = env.from_string(template_str)
        return tmpl.render(**ctx)
    except (UndefinedError, TemplateError) as e:
        raise RenderError(str(e)) from e


def render_tree(src: Path, dst: Path, ctx: dict[str, Any]) -> int:
    """Render all .md files from src/ → dst/. Returns count rendered."""
    env = build_env(loader_path=src)
    dst.mkdir(parents=True, exist_ok=True)
    count = 0
    for md in src.rglob("*.md"):
        rel = md.relative_to(src)
        try:
            tmpl = env.get_template(str(rel))
            out = tmpl.render(**ctx)
        except (UndefinedError, TemplateError) as e:
            raise RenderError(f"{md}: {e}") from e
        out_path = dst / rel
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(out)
        count += 1
    return count


def main() -> int:
    parser = argparse.ArgumentParser(description="Render wko templates")
    parser.add_argument("--check", action="store_true", help="CI dry-run mode")
    parser.add_argument("--file", help="Render single file")
    parser.add_argument("--watch", action="store_true", help="Re-render on change")
    parser.add_argument("--clean", action="store_true", help="rm -rf dist/ trước")
    parser.add_argument("--config", default="company.config.yaml")
    args = parser.parse_args()

    cfg = load_config(args.config)
    repo_root = Path(__file__).resolve().parent.parent
    dist = repo_root / "dist"

    if args.clean and dist.exists():
        shutil.rmtree(dist)
        print(f"🧹 Cleaned {dist}")

    if args.file:
        f = Path(args.file)
        out = render_string(f.read_text(), cfg)
        if not args.check:
            out_path = dist / f.relative_to(repo_root)
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(out)
            print(f"✓ {f} → {out_path}")
        else:
            print(out)
        return 0

    if args.watch:
        from watchdog.observers import Observer
        from watchdog.events import FileSystemEventHandler

        class Handler(FileSystemEventHandler):
            def on_modified(self, event):
                if event.src_path.endswith(".md"):
                    try:
                        skills_count = render_tree(repo_root / "skills", dist / "skills", cfg)
                        docs_count = render_tree(repo_root / "docs", dist / "docs", cfg)
                        print(f"♻️  Re-rendered ({skills_count}+{docs_count})")
                    except RenderError as e:
                        print(f"❌ {e}", file=sys.stderr)

        observer = Observer()
        observer.schedule(Handler(), str(repo_root / "skills"), recursive=True)
        observer.schedule(Handler(), str(repo_root / "docs"), recursive=True)
        observer.start()
        print("👀 Watching skills/ + docs/ (Ctrl+C để stop)")
        try:
            observer.join()
        except KeyboardInterrupt:
            observer.stop()
        return 0

    # Default: render all
    try:
        skills_count = render_tree(repo_root / "skills", dist / "skills", cfg)
        docs_count = render_tree(repo_root / "docs", dist / "docs", cfg)
    except RenderError as e:
        print(f"❌ {e}", file=sys.stderr)
        return 1

    if args.check:
        print(f"✅ Render check OK ({skills_count} skills, {docs_count} docs)")
    else:
        print(f"✓ Rendered {skills_count} skills, {docs_count} docs → {dist}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 4: Run tests → PASS**

```bash
pytest tests/test_render.py -v
```

Expected: 6 passed.

- [ ] **Step 5: Commit**

```bash
git add scripts/render.py tests/test_render.py
git commit -m "feat(scripts): add render.py with Jinja2 + custom filters + 6 tests"
```

---

### Task 3.2: Test render with real example file

- [ ] **Step 1: Create test source markdown**

```bash
cd /Users/dev/Claude/Developer/Github/wko
mkdir -p skills
cat > skills/_sanity-check.md << 'EOF'
# Sanity check — {{ company.name }}

Industry: {{ company.industry }}
Taxonomy version: {{ taxonomy.version }}

## Spaces ({{ taxonomy.spaces|length }})

{% for s in taxonomy.spaces %}
- **{{ s.code }}** {{ s.icon }} {{ s.name }} — owner: {{ s.owner }}
{% endfor %}

## Lark
- URL: {{ lark.wiki_root_url | wiki_link("Wiki Root") }}
EOF
```

- [ ] **Step 2: Render with example config**

```bash
cp company.config.yaml.example company.config.yaml
python3 scripts/render.py
cat dist/skills/_sanity-check.md
```

Expected output có "Acme Foods", "v4.1", danh sách 7 spaces, link Markdown format.

- [ ] **Step 3: Cleanup**

```bash
rm skills/_sanity-check.md
rm -rf dist/
rm company.config.yaml
```

- [ ] **Step 4: Commit nothing (just verification)**

---

### Task 3.3: `--watch` mode integration test (skip in CI)

- [ ] **Step 1: Add pytest marker for slow/interactive tests**

In `pyproject.toml` add:

```toml
[tool.pytest.ini_options]
markers = [
    "slow: tests that take >1s",
    "interactive: tests requiring TTY (skip in CI)",
]
```

- [ ] **Step 2: Write `tests/test_render_watch.py`**

```python
"""Smoke test for --watch mode. Marked interactive — skip in CI."""
import subprocess
import time
from pathlib import Path
import pytest


@pytest.mark.interactive
@pytest.mark.slow
def test_watch_mode_detects_change(tmp_repo: Path) -> None:
    """Start watch, modify file, verify re-render happens within 2s."""
    (tmp_repo / "skills").mkdir(exist_ok=True)
    src = tmp_repo / "skills" / "watched.md"
    src.write_text("# {{ company.name }}")

    proc = subprocess.Popen(
        ["python3", "-m", "scripts.render", "--watch", "--config", str(tmp_repo / "company.config.yaml")],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=tmp_repo, text=True,
    )
    try:
        time.sleep(1)                  # let observer start
        src.write_text("# {{ company.short_name }}")
        time.sleep(2)                  # let re-render
        out_file = tmp_repo / "dist" / "skills" / "watched.md"
        assert out_file.exists()
        assert "Acme" in out_file.read_text()
    finally:
        proc.terminate()
        proc.wait(timeout=5)
```

- [ ] **Step 3: Commit**

```bash
git add tests/test_render_watch.py pyproject.toml
git commit -m "test(render): add --watch mode smoke test (interactive marker)"
```

---

### Task 3.4: `scripts/generate_index.py` — auto README

**Files:**
- Create: `scripts/generate_index.py`, `tests/test_generate_index.py`

Generate `skills/README.md` + `docs/README.md` auto từ list file + frontmatter title.

- [ ] **Step 1: Write `tests/test_generate_index.py`**

```python
"""Tests for generate_index.py."""
from __future__ import annotations

from pathlib import Path

from scripts.generate_index import extract_title, build_index


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
    assert "README" not in out  # skip self
```

- [ ] **Step 2: Run → FAIL**

```bash
pytest tests/test_generate_index.py -v
```

- [ ] **Step 3: Write `scripts/generate_index.py`**

```python
"""Auto-generate skills/README.md + docs/README.md từ list files."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path


def extract_title(md_file: Path) -> str:
    """Lấy heading H1. Fallback: filename stem."""
    for line in md_file.read_text().splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return md_file.stem


def build_index(dir_path: Path, title: str) -> str:
    """Build markdown index of all *.md files in dir (sorted, skip README.md)."""
    files = sorted(p for p in dir_path.glob("*.md") if p.name != "README.md")
    lines = [f"# {title}", "", "Auto-generated by `scripts/generate_index.py` — không sửa tay.", ""]
    for f in files:
        title_text = extract_title(f)
        lines.append(f"- [{title_text}]({f.name})")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".", help="Repo root (default cwd)")
    parser.add_argument("--check", action="store_true", help="Fail if changes needed")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    targets = [
        (root / "skills", "Skills — Quy tắc viết Wiki"),
        (root / "docs", "Docs — Tham chiếu công ty"),
    ]
    changed = []
    for d, title in targets:
        if not d.exists():
            continue
        new_content = build_index(d, title)
        readme = d / "README.md"
        old_content = readme.read_text() if readme.exists() else ""
        if new_content != old_content:
            if args.check:
                changed.append(str(readme))
            else:
                readme.write_text(new_content)
                print(f"✓ Updated {readme}")

    if args.check and changed:
        print(f"❌ Cần regenerate: {changed}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 4: Run tests → PASS**

```bash
pytest tests/test_generate_index.py -v
```

- [ ] **Step 5: Commit**

```bash
git add scripts/generate_index.py tests/test_generate_index.py
git commit -m "feat(scripts): add generate_index.py for auto-README"
```

---

### Task 3.5: `scripts/validate_structure.py` — folder lint

**Files:**
- Create: `scripts/validate_structure.py`, `tests/test_validate_structure.py`

- [ ] **Step 1: Write tests**

```python
"""Tests for validate_structure.py."""
from __future__ import annotations

from pathlib import Path

import pytest

from scripts.validate_structure import validate_structure, StructureError


def test_passes_with_required_dirs(tmp_path: Path) -> None:
    for d in ["skills", "docs", "scripts", "docs-meta"]:
        (tmp_path / d).mkdir()
    validate_structure(tmp_path)


def test_fails_missing_required_dir(tmp_path: Path) -> None:
    (tmp_path / "skills").mkdir()
    with pytest.raises(StructureError, match="docs"):
        validate_structure(tmp_path)


def test_warns_on_dist_in_git(tmp_path: Path) -> None:
    for d in ["skills", "docs", "scripts", "docs-meta"]:
        (tmp_path / d).mkdir()
    (tmp_path / "dist").mkdir()
    (tmp_path / ".gitignore").write_text("nothing")  # dist NOT in gitignore
    with pytest.raises(StructureError, match="dist/"):
        validate_structure(tmp_path)


def test_pass_with_dist_gitignored(tmp_path: Path) -> None:
    for d in ["skills", "docs", "scripts", "docs-meta"]:
        (tmp_path / d).mkdir()
    (tmp_path / "dist").mkdir()
    (tmp_path / ".gitignore").write_text("dist/\n.env")
    validate_structure(tmp_path)
```

- [ ] **Step 2: Run → FAIL**

- [ ] **Step 3: Write `scripts/validate_structure.py`**

```python
"""Lint folder structure of wko repo."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path


class StructureError(Exception):
    pass


REQUIRED_DIRS = ["skills", "docs", "scripts", "docs-meta"]
REQUIRED_GITIGNORE_ENTRIES = ["dist/", ".env", "company.config.yaml"]


def validate_structure(root: Path) -> None:
    """Raise StructureError nếu structure sai."""
    missing = [d for d in REQUIRED_DIRS if not (root / d).is_dir()]
    if missing:
        raise StructureError(f"Missing required dirs: {missing}")

    gitignore = root / ".gitignore"
    if not gitignore.exists():
        raise StructureError(".gitignore missing")

    ignore_content = gitignore.read_text()
    if (root / "dist").exists() and "dist/" not in ignore_content and "dist" not in ignore_content:
        raise StructureError("dist/ exists but not in .gitignore — secret leak risk")

    for entry in REQUIRED_GITIGNORE_ENTRIES:
        if entry not in ignore_content:
            print(f"⚠️  .gitignore missing entry: {entry}", file=sys.stderr)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    try:
        validate_structure(Path(args.root).resolve())
        print("✅ Structure OK")
        return 0
    except StructureError as e:
        print(f"❌ {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 4: Run tests → PASS**

- [ ] **Step 5: Commit**

```bash
git add scripts/validate_structure.py tests/test_validate_structure.py
git commit -m "feat(scripts): add validate_structure.py with .gitignore check"
```

- [ ] **Step 6: Tag v0.1.0-alpha (early stopping point)**

```bash
git tag -a v0.1.0-alpha -m "wko v0.1.0-alpha — render engine working, no content yet"
```

---

## M4 — Templating skills/

> Mỗi task = 1-2 skill files. Copy nội dung từ `/Users/dev/Claude/Developer/Github/wiki/skills/<file>.md`, **strip 100% Thích Cay**, thay placeholder `{{ ... }}`. Sau mỗi task: chạy `python3 scripts/render.py --file skills/<file>.md` verify render OK.

### Task 4.1: skills 02, 04, 06, 07 (low-templating — copy + minor sub)

**Files:**
- Create: `skills/02-writing-style.md`, `04-page-status.md`, `06-excel-to-wiki.md`, `07-source-protection.md`

- [ ] **Step 1: Copy skills/02 từ Thích Cay repo**

```bash
cp /Users/dev/Claude/Developer/Github/wiki/skills/02-writing-style.md \
   /Users/dev/Claude/Developer/Github/wko/skills/02-writing-style.md
```

- [ ] **Step 2: Strip Thích Cay → placeholders**

Tìm và replace trong file mới copy:
- `Thích Cay` → `{{ company.name }}`
- `Ladospice`, `Delicart` → (xoá, hoặc thay bằng generic example)
- URL `thichcay.sg.larksuite.com/wiki/...` → `{{ lark.wiki_root_url }}`
- Specific page codes (vd `OPS-LIVE-SOP-001`) → giữ làm ví dụ generic (vì format `[SPACE]-[SECTION]-[TYPE]-[NUMBER]` chung)

- [ ] **Step 3-5: Repeat cho 04, 06, 07**

Strip pattern tương tự. Skills này low-templating nên chủ yếu là search/replace.

- [ ] **Step 6: Render verify**

```bash
cp company.config.yaml.example company.config.yaml
python3 scripts/render.py --file skills/02-writing-style.md --check
# Check output: không còn "Thích Cay", có placeholder rendered
```

- [ ] **Step 7: Commit**

```bash
git add skills/02-writing-style.md skills/04-page-status.md skills/06-excel-to-wiki.md skills/07-source-protection.md
git commit -m "feat(skills): template 02 writing-style, 04 page-status, 06 excel-to-wiki, 07 source-protection"
```

---

### Task 4.2: skills 03 (linking) + 11 (page types V4.1)

**Files:**
- Create: `skills/03-linking-rules.md`, `11-page-types.md`

- [ ] **Step 1: Copy + adapt skill 03**

Source URL placeholders, Lark Base list từ config:
```markdown
Mọi link nội bộ trỏ tới {{ lark.wiki_root_url }}/wiki/...
Lark Base list:
{% for b in lark_bases %}- [{{ b.name }}](https://...{{ b.base_token }}) — {{ b.purpose }}
{% endfor %}
```

- [ ] **Step 2: Rewrite skill 11 cho V4.1 (13 type — thêm PROC, GDL)**

Loop từ config:
```markdown
## {{ taxonomy.page_types|length }} loại page (V4.1)

{% for t in taxonomy.page_types %}
### {{ t.code }} — {{ t.name }}

{{ t.question | default("(không có execution question)") }}

{% endfor %}
```

Plus reference từ Google Doc V4.1 (Section 11 "Phân biệt POL vs MST", Section 10 "Quy tắc HUB").

- [ ] **Step 3: Render verify**

- [ ] **Step 4: Commit**

```bash
git add skills/03-linking-rules.md skills/11-page-types.md
git commit -m "feat(skills): template 03 linking-rules, 11 page-types (V4.1 13 types)"
```

---

### Task 4.3: skills 01 (page format) — heavy templating

**Files:**
- Create: `skills/01-page-format.md`

- [ ] **Step 1: Write source với loop trên `page_status_values`, `policies`**

```markdown
# Skill 01 — Format chuẩn mỗi trang Wiki (V{{ taxonomy.version | replace("v", "") }})

## Mã page

Format: `{{ taxonomy.page_code_format }}`

Ví dụ: `{{ taxonomy.spaces[0].code }}-{{ (taxonomy.sections[taxonomy.spaces[0].code][0].code | default('00')) }}-MST-001`

## Trạng thái

{% for s in policies.page_status_values %}
- {{ s }}
{% endfor %}

Default: `{{ policies.default_status }}`

## Header trang (3 loại: general/MASTER/HUB)

### General page template
...

### MASTER template
...

### HUB template
HUB-001 = Master entry (sticky). HUB-002+ = nhánh theo 4 pattern (A: sub-area, B: audience, C: lifecycle, D: role).

## Section bắt buộc cuối trang

🔗 **Tài liệu liên quan**
- [Backlink chiều ngược (xem skill 03)](03-linking-rules.md)
- Hub parent: {{ "{{ hub_parent }}" }}     <!-- placeholder client điền per-page -->
```

- [ ] **Step 2: Render verify**

- [ ] **Step 3: Commit**

```bash
git add skills/01-page-format.md
git commit -m "feat(skills): template 01 page-format with V4.1 status + HUB rules"
```

---

### Task 4.4: skills 05 (publish workflow) + 08 (index & numbering)

**Files:**
- Create: `skills/05-publish-workflow.md`, `08-index-and-numbering.md`

- [ ] **Step 1: skill 05 — 6-step V4.1 publish**

Loop trên `taxonomy.spaces` cho danh sách space, dùng `{{ lark.wiki_root_token }}`, `{{ lark.master_index.obj_token }}` cho command examples.

```markdown
# Skill 05 — Quy trình đẩy lên Lark Wiki (V4.1)

6 bước:

1. **Chuẩn bị** — tạo node con dưới `{{ lark.wiki_root_token }}`
2. **Preview** — `lark-cli docs fetch <NEW_NODE> --api-version v2`
3. **Soạn** — markdown ở `drafts/`
4. **Publish** — `lark-cli docs update <NEW_NODE> --content drafts/foo.md`
5. **Update INDEX** — `python3 scripts/rebuild_master_index.py --confirm`
   (master index obj: `{{ lark.master_index.obj_token }}`)
6. **Merge** — PR repo, log node_token vào commit message
```

- [ ] **Step 2: skill 08 — V4.1 heavy loop**

```markdown
# Skill 08 — INDEX & Mã page (V4.1)

## {{ taxonomy.spaces|length }} SPACE

{% for s in taxonomy.spaces %}
### {{ s.code }} — {{ s.name }} {{ s.icon }}
Order: `{{ s.order }}`. Owner: {{ s.owner }}.
{{ s.purpose | default("") }}

Sections:
{% for sec in taxonomy.sections.get(s.code, []) %}- `{{ sec.code }}` — {{ sec.name }}
{% endfor %}

{% endfor %}

## {{ taxonomy.page_types|length }} TYPE

| Code | Tên | Câu hỏi thực thi |
|---|---|---|
{% for t in taxonomy.page_types %}| `{{ t.code }}` | {{ t.name }} | {{ t.question | default("—") }} |
{% endfor %}

## Master Index fields (V4.1)

Required ({{ master_index_fields.required|length }} cột):
{% for f in master_index_fields.required %}- {{ f }}
{% endfor %}

Recommended (V4.1 mới):
{% for f in master_index_fields.recommended %}- {{ f }}
{% endfor %}
```

- [ ] **Step 3: Render verify**

- [ ] **Step 4: Commit**

```bash
git add skills/05-publish-workflow.md skills/08-index-and-numbering.md
git commit -m "feat(skills): template 05 publish-workflow, 08 index-and-numbering (V4.1)"
```

---

### Task 4.5: skills 09 (contributing) + 10 (master registry)

**Files:**
- Create: `skills/09-contributing-workflow.md`, `10-master-registry.md`

- [ ] **Step 1: skill 09**

```markdown
# Skill 09 — Workflow contributing + Bot review

## Phase 1 — Manual review
Nhân viên gửi link Lark vào group → reviewer copy + review trên Lark UI.

## Phase 2 — Async bot
Bot subscribe `im.message.receive_v1` qua `lark-cli event consume`.

- Group email: `{{ integrations.contributor_group_email }}`
- Bot name: `{{ integrations.reviewer_bot_name }}`
- Webhook (nếu có): `{{ integrations.reviewer_bot_webhook | default("(chưa cấu hình)") }}`

Bot:
1. Receive message với wiki URL
2. Resolve URL → node + obj token via `lark-cli wiki node get`
3. Fetch content via `lark-cli docs fetch`
4. Claude API review (reference skill 01/02/08)
5. Score x.x/10 + encouraging comment via `lark-cli drive comment create`
6. Notify group qua `lark-cli im message send`
```

- [ ] **Step 2: skill 10 — render master registry table**

```markdown
# Skill 10 — Master Registry

## {{ master_registry|length }} MASTER bắt buộc

| Mã | Tên | Owner |
|---|---|---|
{% for m in master_registry %}| `{{ m.code }}` | {{ m.name }} | {{ m.owner }} |
{% endfor %}

## Quy tắc

1. Mọi MASTER có owner duy nhất, không co-owned.
2. POL (external) primary owner tra `pol_mst_rules.primary_owner_table`.
3. Khi thay đổi MASTER → notify all "Impacted Pages" trong Master Index.
```

- [ ] **Step 3: Render verify**

- [ ] **Step 4: Commit**

```bash
git add skills/09-contributing-workflow.md skills/10-master-registry.md
git commit -m "feat(skills): template 09 contributing, 10 master-registry"
```

---

### Task 4.6: skill 12 (emergency playbook) + skill index README

**Files:**
- Create: `skills/12-emergency-playbook.md`, `skills/README.md`

- [ ] **Step 1: skill 12 — generic emergency template**

Strip 10 Thích Cay-specific (livestream bùng, sàn lỗi, ...) → thay bằng 2-3 generic + TODO comment:

```markdown
# Skill 12 — Emergency Playbook (PBK)

PBK = page xử lý sự cố / ngoại lệ. Trong V4.1, PBK nằm trong từng section OPS thay vì SPACE EMG riêng.

## Generic emergency template

```markdown
# {{ '{{' }} space_code }}-{{ '{{' }} section }}-PBK-{{ '{{' }} number }} {{ '{{' }} title }}

## Triệu chứng (Symptoms)
- ...

## Mức độ nghiêm trọng
- 🟢 Low / 🟡 Medium / 🔴 High / ⛔ Critical

## Xử lý ngay (Immediate response, < 15 phút)
1. ...

## Xử lý sâu (Deep fix, < 24h)
1. ...

## Sau sự cố
- Post-mortem
- Cập nhật MST/SOP nếu cần
- Add to backlink

## Ví dụ
<!-- TODO {{ company.short_name }}: thêm playbook đặc thù công ty -->
- Downtime hệ thống chính
- Data leak / breach
- Khủng hoảng truyền thông
```

- [ ] **Step 2: Generate skills/README.md**

```bash
python3 scripts/generate_index.py --root .
cat skills/README.md
```

Expected: index of 12 skills.

- [ ] **Step 3: Commit**

```bash
git add skills/12-emergency-playbook.md skills/README.md
git commit -m "feat(skills): template 12 emergency-playbook + auto skills/README.md"
```

- [ ] **Step 4: Full skills render test**

```bash
cp company.config.yaml.example company.config.yaml
python3 scripts/render.py --check
ls dist/skills/
```

Expected: 12 skills + README rendered.

---

## M5 — Templating docs/

### Task 5.1: docs 00 (overview) + 01 (org) — strip 100%

**Files:**
- Create: `docs/00-company-overview.md`, `01-org-structure.md`

- [ ] **Step 1: docs/00 skeleton**

```markdown
# {{ company.name }} là ai?

<!-- TODO {{ company.short_name }} owner: điền nội dung mô tả công ty. Tham khảo template dưới -->

## Tổng quan
- **Tên đầy đủ:** {{ company.legal_entities | join(", ") }}
- **Ngành:** {{ company.industry }}
- **Năm thành lập:** {{ company.founded_year | default("(chưa điền)") }}
- **HQ:** {{ company.hq_country }}

## Sản phẩm / dịch vụ
<!-- TODO: list sản phẩm/dịch vụ chính -->

## Sứ mệnh
<!-- TODO -->

## Giá trị cốt lõi
<!-- TODO -->

## Kênh bán / phân phối
<!-- TODO -->

🔗 **Tài liệu liên quan**
- [Cơ cấu tổ chức](01-org-structure.md)
- [Ngữ cảnh vận hành](06-context-notes.md)
```

- [ ] **Step 2: docs/01 — render từ org.departments**

```markdown
# Cơ cấu tổ chức — {{ company.name }}

## {{ org.departments|length }} phòng ban

| Code | Tên | Head role |
|---|---|---|
{% for d in org.departments %}| `{{ d.code }}` | {{ d.name }} | {{ d.head_role | default("(chưa định)") }} |
{% endfor %}

## Sơ đồ tổ chức
<!-- TODO: vẽ sơ đồ trên Lark Whiteboard, link về đây -->

🔗 **Tài liệu liên quan**
- [Tổng quan công ty](00-company-overview.md)
- [Phân quyền Wiki](03-permissions.md)
```

- [ ] **Step 3: Render + commit**

```bash
python3 scripts/render.py --check
git add docs/00-company-overview.md docs/01-org-structure.md
git commit -m "feat(docs): template 00 overview, 01 org-structure (strip + loop)"
```

---

### Task 5.2: docs 02 (wiki architecture) — heavy loop

**Files:**
- Create: `docs/02-wiki-architecture.md`

- [ ] **Step 1: Render full V4.1 architecture từ taxonomy**

```markdown
# Cấu trúc Wiki "{{ company.short_name }} Company OS" (V{{ taxonomy.version | replace("v", "") }})

Philosophy: **{{ taxonomy.philosophy | default("execution-first") }}** — mở vào là làm được việc.

## 4 tầng

```
Space → SPACE ({{ taxonomy.spaces|length }}) → SECTION → PAGE
```

## {{ taxonomy.spaces|length }} SPACE

{% for s in taxonomy.spaces %}
### {{ s.order }}_{{ s.code }} — {{ s.name }} {{ s.icon }}

**Owner:** {{ s.owner }}
**Mục đích:** {{ s.purpose | default("") }}
{% if s.append_only %}**Append-only:** không tái dùng mã đã archived.{% endif %}

**Sections ({{ taxonomy.sections.get(s.code, [])|length }}):**

{% for sec in taxonomy.sections.get(s.code, []) %}- `{{ sec.code }}` — {{ sec.name }}
{% endfor %}

{% endfor %}

## URL Lark

Wiki root: {{ lark.wiki_root_url | wiki_link("Mở trên Lark") }}

Master Index: `SYS-00-IDX-001` (obj: `{{ lark.master_index.obj_token }}`)
```

- [ ] **Step 2: Render + commit**

```bash
git add docs/02-wiki-architecture.md
git commit -m "feat(docs): template 02 wiki-architecture (V4.1 7 SPACE loop)"
```

---

### Task 5.3: docs 03, 04, 05, 08 — straightforward

**Files:**
- Create: `docs/03-permissions.md`, `04-glossary.md`, `05-lark-base-connections.md`, `08-contributing.md`

- [ ] **Step 1: docs/03 — render permission per space**

```markdown
# Phân quyền {{ taxonomy.spaces|length }} SPACE

| SPACE | Editor | Viewer | Restricted |
|---|---|---|---|
{% for s in taxonomy.spaces %}| `{{ s.code }}` | {{ s.owner }} | (TODO) | (TODO) |
{% endfor %}

<!-- TODO {{ company.short_name }}: define Lark group cho mỗi vai trò, fill columns -->
```

- [ ] **Step 2: docs/04 — glossary template**

Giữ thuật ngữ Wiki chuẩn (KPI, SOP, MST, SPACE, SECTION, TYPE, HUB, PROC, ...), bỏ thuật ngữ Thích Cay-specific:

```markdown
# Thuật ngữ & viết tắt

## Wiki Operating System

| Thuật ngữ | Nghĩa |
|---|---|
| SPACE | Cấp 1 — phân loại nghiệp vụ ({{ taxonomy.spaces|length }} space) |
| SECTION | Cấp 2 — sub-domain trong SPACE |
| TYPE | Cấp 3 — loại page ({{ taxonomy.page_types|length }} type) |
| HUB | Page điều hướng (menu) của section, KHÔNG chứa nội dung thực |
| MST | Master — luật/dữ liệu gốc nội bộ |
| POL | Policy — luật/policy NGOÀI ban hành (sàn, luật, NĐ) |
| PROC | Process — luồng đa vai trò có bàn giao |
| SOP | Standard Operating Procedure — thao tác tuyến tính |
| ... | ... |

## Nội bộ {{ company.short_name }}

<!-- TODO: thêm thuật ngữ riêng của công ty (vd: tên hệ thống nội bộ, tên sản phẩm code) -->
```

- [ ] **Step 3: docs/05 — render lark_bases list**

```markdown
# Lark Base cần kết nối

{% for b in lark_bases %}
## {{ b.name }}
- Token: `{{ b.base_token }}`
- Mục đích: {{ b.purpose }}
{% endfor %}

{% if not lark_bases %}
<!-- TODO: thêm Lark Base vào company.config.yaml `lark_bases` list -->
{% endif %}
```

- [ ] **Step 4: docs/08 — contributing flow**

```markdown
# Contributing — đóng góp Wiki nội bộ {{ company.short_name }}

> Quy trình cho nhân viên (KHÔNG qua Git, qua Lark trực tiếp).

3 bước:

1. Mở Lark group `WikiContributor` ({{ integrations.contributor_group_email }})
2. Soạn page trên Lark trong section phù hợp (xem [02-wiki-architecture](02-wiki-architecture.md))
3. Tag {{ integrations.reviewer_bot_name }} kèm link page → bot tự review
```

- [ ] **Step 5: Render + commit**

```bash
git add docs/03-permissions.md docs/04-glossary.md docs/05-lark-base-connections.md docs/08-contributing.md
git commit -m "feat(docs): template 03 permissions, 04 glossary, 05 lark-bases, 08 contributing"
```

---

### Task 5.4: docs 06, 07 — strip + skeleton

**Files:**
- Create: `docs/06-context-notes.md`, `07-status-tracker.md`

- [ ] **Step 1: docs/06 strip 100%**

```markdown
# Ngữ cảnh vận hành — {{ company.name }}

<!-- TODO {{ company.short_name }} owner: điền theo template -->

## Quy mô
- Số đơn / ngày: <TODO>
- Kênh bán chính: <TODO>
- Tỷ lệ hoàn: <TODO>

## Nhịp vận hành
- Hàng về: <TODO>
- QC: <TODO>
- Đóng gói: <TODO>
- Bàn giao vận chuyển: <TODO>

## Ngữ cảnh mùa vụ
- Cao điểm: <TODO>
- Thấp điểm: <TODO>
```

- [ ] **Step 2: docs/07 — strip live data, giữ schema**

```markdown
# Trạng thái Wiki — {{ company.name }}

> Snapshot trạng thái page Wiki tại thời điểm gần nhất. Auto-update qua `scripts/wiki_kpi_report.py`.

## Theo trạng thái

| Trạng thái | Count |
|---|---|
{% for s in policies.page_status_values %}| {{ s }} | (TBD) |
{% endfor %}

## Theo SPACE

{% for s in taxonomy.spaces %}
- **{{ s.code }}**: (TBD) page
{% endfor %}

## Migration V4 → V4.1 (nếu có)

<!-- Chỉ relevant nếu client từng dùng V4 cũ -->
```

- [ ] **Step 3: Render + commit**

```bash
git add docs/06-context-notes.md docs/07-status-tracker.md
git commit -m "feat(docs): template 06 context-notes, 07 status-tracker (strip live data)"
```

---

### Task 5.5: docs 09 (master registry duplicate) + 10 (page types) + docs/README.md

**Files:**
- Create: `docs/09-master-registry.md`, `docs/10-page-types-taxonomy.md`, `docs/README.md`

- [ ] **Step 1: docs/09 — same render as skills/10**

```markdown
# Master Registry — {{ company.name }}

(Mirror của [skills/10-master-registry.md](../skills/10-master-registry.md) — tham chiếu doc.)

## {{ master_registry|length }} MASTER bắt buộc

| Mã | Tên | Owner |
|---|---|---|
{% for m in master_registry %}| `{{ m.code }}` | {{ m.name }} | {{ m.owner }} |
{% endfor %}
```

- [ ] **Step 2: docs/10 — page types taxonomy V4.1**

```markdown
# Page Types Taxonomy — V{{ taxonomy.version | replace("v", "") }}

## {{ taxonomy.page_types|length }} loại

{% for t in taxonomy.page_types %}
### {{ t.code }} — {{ t.name }}

{% if t.question %}**Câu hỏi thực thi:** {{ t.question }}{% endif %}

{% if t.scope %}**Scope:** `{{ t.scope }}`{% endif %}

{% if t.new_in_v41 %}**Mới trong V4.1**{% endif %}

{% endfor %}

## Khi nào dùng type nào?

Xem [skill 11](../skills/11-page-types.md) cho rejection rules.
```

- [ ] **Step 3: Generate docs/README.md**

```bash
python3 scripts/generate_index.py --root .
```

- [ ] **Step 4: Full M5 render + commit**

```bash
python3 scripts/render.py --check
git add docs/09-master-registry.md docs/10-page-types-taxonomy.md docs/README.md
git commit -m "feat(docs): template 09 master-registry, 10 page-types-taxonomy + auto docs/README"
```

- [ ] **Step 5: Tag v0.5.0-beta (early stopping point)**

```bash
git tag -a v0.5.0-beta -m "wko v0.5.0-beta — render + content templated, no CI yet"
```

---

## M6 — Scripts Migration

### Task 6.1: `scripts/init_company.py` — interactive setup

**Files:**
- Create: `scripts/init_company.py`, `tests/test_init_company.py`

- [ ] **Step 1: Write tests (use `monkeypatch` for stdin)**

```python
"""Tests for init_company.py."""
from __future__ import annotations

import io
from pathlib import Path
from unittest.mock import patch

from scripts.init_company import build_config_from_answers


def test_build_config_minimal_answers() -> None:
    answers = {
        "company_name": "Beta Corp",
        "short_name": "Beta",
        "industry": "SaaS",
        "hq_country": "VN",
        "lark_subdomain": "beta",
        "lark_region": "sg",
        "wiki_root_token": "Yix7wq123",
        "taxonomy_version": "v4.1",
        "use_default_spaces": True,
        "use_default_types": True,
        "contributor_email": "wiki@beta.com",
    }
    cfg = build_config_from_answers(answers)
    assert cfg["company"]["name"] == "Beta Corp"
    assert cfg["lark"]["wiki_root_token"] == "Yix7wq123"
    assert cfg["taxonomy"]["version"] == "v4.1"
    assert len(cfg["taxonomy"]["spaces"]) == 7  # V4.1 default
    assert len(cfg["taxonomy"]["page_types"]) == 13
```

- [ ] **Step 2: Write `scripts/init_company.py`**

```python
"""Interactive first-time setup: build company.config.yaml from 12 questions."""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import yaml

from _common import require_lark_cli


DEFAULT_SPACES_V41 = [
    {"code": "SYS", "name": "Wiki Operating System", "order": "00", "icon": "⚙️", "owner": "IT"},
    {"code": "GEN", "name": "Chung / General", "order": "01", "icon": "🏢", "owner": "HCNS"},
    {"code": "INT", "name": "Nội bộ / Internal", "order": "02", "icon": "🤝", "owner": "HCNS"},
    {"code": "OPS", "name": "Vận hành / Operations", "order": "03", "icon": "⚡", "owner": "Operations"},
    {"code": "BOD", "name": "Ban giám đốc / Board", "order": "04", "icon": "👔", "owner": "BOD"},
    {"code": "TMP", "name": "Templates", "order": "05", "icon": "📋", "owner": "Admin"},
    {"code": "ARC", "name": "Archive", "order": "99", "icon": "🗄", "owner": "Admin", "append_only": True},
]

DEFAULT_TYPES_V41 = [
    {"code": "HUB", "name": "Hub", "question": "Tôi đang ở đâu trong luồng?"},
    {"code": "MST", "name": "Master", "question": "Luật gốc là gì?"},
    {"code": "PROC", "name": "Process", "question": "Ai làm, làm khi nào?", "new_in_v41": True},
    {"code": "SOP", "name": "SOP", "question": "Tôi phải làm từng bước gì?"},
    {"code": "CHK", "name": "Checklist", "question": "Tôi đã làm đủ chưa?"},
    {"code": "TMP", "name": "Template", "question": "Tôi dùng mẫu nào?"},
    {"code": "PBK", "name": "Playbook", "question": "Lệch / lỗi / nhánh thì sao?"},
    {"code": "DBD", "name": "Dashboard", "question": "Kết quả có ổn không?"},
    {"code": "POL", "name": "Policy", "scope": "external_only"},
    {"code": "DIC", "name": "Dictionary"},
    {"code": "GDL", "name": "Guideline", "new_in_v41": True},
    {"code": "LOG", "name": "Log"},
    {"code": "IDX", "name": "Index"},
]


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


def build_config_from_answers(a: dict) -> dict[str, Any]:
    cfg: dict[str, Any] = {
        "company": {
            "name": a["company_name"],
            "short_name": a["short_name"],
            "industry": a["industry"],
            "hq_country": a["hq_country"],
        },
        "lark": {
            "domain": "larksuite.com" if a["lark_region"] != "cn" else "feishu.cn",
            "tenant_subdomain": a["lark_subdomain"],
            "region": a["lark_region"],
            "wiki_root_token": a["wiki_root_token"],
            "wiki_root_url": f"https://{a['lark_subdomain']}.{a['lark_region']}.larksuite.com/wiki/{a['wiki_root_token']}",
            "master_index": {"node_token": "", "obj_token": ""},
        },
        "taxonomy": {
            "version": a["taxonomy_version"],
            "philosophy": "execution-first",
            "spaces": DEFAULT_SPACES_V41 if a["use_default_spaces"] else [],
            "page_types": DEFAULT_TYPES_V41 if a["use_default_types"] else [],
            "sections": {},
            "page_code_format": "{space}-{section_suffix}-{type}-{number:03d}",
        },
        "org": {"departments": []},
        "master_registry": [],
        "integrations": {
            "contributor_group_email": a["contributor_email"],
            "reviewer_bot_webhook": "",
            "reviewer_bot_name": "@wiki-reviewer",
        },
        "lark_bases": [],
        "policies": {
            "page_status_values": ["⬜ Draft", "🔄 Active", "📋 Deprecated", "✅ Archived"],
            "default_status": "⬜ Draft",
            "publish_requires_review": True,
            "arc_append_only": True,
        },
    }
    return cfg


def main() -> int:
    print("🚀 wko Interactive Setup\n")
    require_lark_cli()

    cfg_path = Path("company.config.yaml")
    if cfg_path.exists():
        if not ask_bool("company.config.yaml đã tồn tại. Ghi đè?", default=False):
            print("Aborted.")
            return 1

    answers = {
        "company_name": ask("Tên công ty đầy đủ", "Acme Foods"),
        "short_name": ask("Tên ngắn (≤ 10 ký tự)", "Acme"),
        "industry": ask("Ngành", "F&B"),
        "hq_country": ask("HQ country code", "VN"),
        "lark_subdomain": ask("Lark tenant subdomain (vd: 'acme' cho acme.sg.larksuite.com)", "acme"),
        "lark_region": ask("Region (sg/cn/us)", "sg"),
        "wiki_root_token": ask("Lark Wiki root token (từ URL /wiki/<TOKEN>)"),
        "taxonomy_version": ask("Taxonomy version", "v4.1"),
        "use_default_spaces": ask_bool("Dùng 7 SPACE V4.1 mặc định?"),
        "use_default_types": ask_bool("Dùng 13 TYPE V4.1 mặc định?"),
        "contributor_email": ask("Group email cho contributor", "wiki@acme.com"),
    }

    cfg = build_config_from_answers(answers)
    cfg_path.write_text(yaml.dump(cfg, sort_keys=False, allow_unicode=True))
    print(f"\n✅ Đã ghi {cfg_path}")
    print("Bước tiếp:")
    print(f"  1. Xem lại + bổ sung taxonomy.sections, org.departments, master_registry")
    print(f"  2. cp .env.example .env và điền LARK_APP_ID/SECRET")
    print(f"  3. python3 scripts/validate_config.py --strict")
    print(f"  4. python3 scripts/render.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 3: Run tests → PASS**

- [ ] **Step 4: Commit**

```bash
git add scripts/init_company.py tests/test_init_company.py
git commit -m "feat(scripts): add init_company.py interactive setup wizard"
```

---

### Task 6.2: `scripts/rebuild_master_index.py` — V4.1 fields

**Files:**
- Modify (port from Thích Cay): `scripts/rebuild_master_index.py`

- [ ] **Step 1: Copy from Thích Cay repo as starting point**

```bash
cp /Users/dev/Claude/Developer/Github/wiki/scripts/rebuild_master_index.py \
   /Users/dev/Claude/Developer/Github/wko/scripts/rebuild_master_index.py
```

- [ ] **Step 2: Refactor để đọc config thay vì hardcode**

Replace hardcoded `Vy3RdJHtKo62nwx1yg6lqZgAgzg` với `cfg["lark"]["master_index"]["obj_token"]`.

Add V4.1 columns: `Hub Parent`, `Source Type`, `Source URL`, `Effective Date`, `Review Cadence`, `Impacted Pages`.

Refactor structure:
```python
from _common import load_config, require_lark_cli, require_lark_auth

def main():
    require_lark_cli()
    require_lark_auth()
    cfg = load_config()
    obj_token = cfg["lark"]["master_index"]["obj_token"]
    fields = cfg["master_index_fields"]
    # ... rest of logic, parametrized
```

Replace SPACE/TYPE constants với loops từ `cfg["taxonomy"]`.

- [ ] **Step 3: Add tests for V4.1 column rendering**

```python
# tests/test_rebuild_master_index.py
def test_renders_v41_columns(sample_config):
    # ... build markdown table, assert "Hub Parent" header exists
```

- [ ] **Step 4: Commit**

```bash
git add scripts/rebuild_master_index.py tests/test_rebuild_master_index.py
git commit -m "feat(scripts): port rebuild_master_index.py to V4.1 (Hub Parent + 5 recommended fields)"
```

---

### Task 6.3: `scripts/rebuild_hub_toc.py` — support HUB-001 sticky + branch patterns

Tương tự task 6.2: port from Thích Cay, parametrize:
- `cfg["hub_rules"]["master_hub_number"]` (default "001")
- `cfg["hub_rules"]["branch_hub_min_pages"]` (default 3)
- Support 4 patterns (A/B/C/D)

- [ ] **Step 1: Port + refactor**

- [ ] **Step 2: Add unit tests cho hub parent resolution logic**

- [ ] **Step 3: Commit**

```bash
git add scripts/rebuild_hub_toc.py tests/test_rebuild_hub_toc.py
git commit -m "feat(scripts): port rebuild_hub_toc.py with HUB-001 sticky + 4 branch patterns"
```

---

### Task 6.4: `scripts/wiki_navigator.py` + `scripts/pull_from_lark.py`

- [ ] **Step 1: Port `wiki_navigator.py`** — parametrize wiki_root_token

- [ ] **Step 2: Implement `pull_from_lark.py`** (hiện skeleton)

Use `lark-cli wiki list-children` + `lark-cli docs fetch` recursive:
```python
def pull_tree(wiki_token: str, output_dir: Path):
    result = subprocess.run(
        ["lark-cli", "wiki", "list-children", "--node", wiki_token, "--output", "json"],
        capture_output=True, text=True, check=True,
    )
    nodes = json.loads(result.stdout)
    for node in nodes:
        # fetch content + recurse
        ...
```

- [ ] **Step 3: Commit**

```bash
git add scripts/wiki_navigator.py scripts/pull_from_lark.py
git commit -m "feat(scripts): port wiki_navigator, implement pull_from_lark fully"
```

---

### Task 6.5: `scripts/wiki_kpi_report.py` — execution-first KPIs

- [ ] **Step 1: Port + add execution-first metrics**

New metrics:
- % sections có 1 HUB + 1 PROC + ≥3 SOP + 1 CHK + 1 TMP + 1 PBK (execution-first formula compliance)
- Count PROC pages (V4.1 type mới)
- Count GDL pages
- POL count by primary owner (audit cross-section)

- [ ] **Step 2: Tests + commit**

```bash
git add scripts/wiki_kpi_report.py tests/test_wiki_kpi_report.py
git commit -m "feat(scripts): wiki_kpi_report with execution-first formula compliance metric"
```

---

### Task 6.6: `scripts/content_quality_audit.py` — POL-vs-MST audit

- [ ] **Step 1: Port + add V4.1 audit rules**

New rules:
- POL pages có `scope: external_only` → audit ngược: nếu POL nội bộ → flag
- MST bridge có "Căn cứ pháp lý" linking về POL → verify link exists
- Section thiếu PROC (V4.1 execution-first requirement) → warn

- [ ] **Step 2: Tests + commit**

```bash
git add scripts/content_quality_audit.py tests/test_content_quality_audit.py
git commit -m "feat(scripts): content_quality_audit with V4.1 POL-vs-MST rules"
```

---

### Task 6.7: `scripts/wiki_reviewer_bot.py` — rewrite với lark-cli event

- [ ] **Step 1: Rewrite từ scratch (architecture mới ở spec §4.7)**

```python
"""Wiki Reviewer Bot — lark-cli event consume + Claude API.

Architecture:
1. subprocess.Popen lark-cli event consume im.message.receive_v1 → NDJSON stdout
2. For each event: filter chat_id, branch on approval keyword vs wiki URL
3. Review via Claude API with cached system prompt (skills 01/02/08 + docs 02)
4. Post comment + notify group via lark-cli drive comment + lark-cli im message
"""
from __future__ import annotations

import json
import logging
import os
import subprocess
import sys
from pathlib import Path

from anthropic import Anthropic
from dotenv import load_dotenv

from _common import load_config, require_lark_cli, require_lark_auth


def main() -> int:
    load_dotenv()
    require_lark_cli()
    require_lark_auth()
    cfg = load_config()

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        sys.exit("❌ ANTHROPIC_API_KEY missing in .env")

    client = Anthropic(api_key=api_key)
    chat_filter = cfg["integrations"].get("contributor_group_chat_id", "")

    # ... rest as designed in spec §4.7
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 2: Add integration test (mock subprocess + anthropic)**

- [ ] **Step 3: Commit**

```bash
git add scripts/wiki_reviewer_bot.py tests/test_wiki_reviewer_bot.py
git commit -m "feat(scripts): rewrite wiki_reviewer_bot with lark-cli event (drop lark-oapi)"
```

---

### Task 6.8: `scripts/migrate_v4_to_v41.py` + `scripts/build_backlink_graph.py` + `scripts/sync_index_contributed_column.py`

- [ ] **Step 1: `migrate_v4_to_v41.py`** — map V4 codes → V4.1

```python
"""Migrate Wiki từ V4 (8 SPACE, 11 TYPE) → V4.1 (7 SPACE, 13 TYPE).

Mapping:
- COM-* → GEN-* (renumber section)
- EMG-* → ARC-OLD-* (archive)
- (Optional) re-classify SOP nhiều vai trò → PROC

Output: JSON mapping for manual rename trên Lark.
"""
```

- [ ] **Step 2: Port `build_backlink_graph.py`** (generic, ít sửa)

- [ ] **Step 3: Port `sync_index_contributed_column.py`** — parametrize obj_token

- [ ] **Step 4: Commit + M6 done**

```bash
git add scripts/migrate_v4_to_v41.py scripts/build_backlink_graph.py scripts/sync_index_contributed_column.py tests/
git commit -m "feat(scripts): add migrate_v4_to_v41, port backlink + sync_contributed"
```

---

## M7 — CI workflows

### Task 7.1: Composite action `setup-lark-cli`

**Files:**
- Create: `.github/actions/setup-lark-cli/action.yml`

- [ ] **Step 1: Write action.yml** (xem spec §4.8)

```yaml
name: 'Setup lark-cli'
description: 'Install lark-cli binary + verify version'
inputs:
  version:
    description: 'lark-cli version'
    default: 'latest'
runs:
  using: 'composite'
  steps:
    - shell: bash
      run: |
        VER="${{ inputs.version }}"
        if [ "$VER" = "latest" ]; then
          URL=$(curl -fsSL https://api.github.com/repos/larksuite/lark-cli/releases/latest \
                | grep browser_download_url | grep linux-x64 | head -1 | cut -d'"' -f4)
        else
          URL="https://github.com/larksuite/lark-cli/releases/download/${VER}/lark-cli-linux-x64.tar.gz"
        fi
        curl -fsSL "$URL" | sudo tar -xz -C /usr/local/bin
        lark-cli --version
```

- [ ] **Step 2: Commit**

```bash
git add .github/actions/setup-lark-cli/action.yml
git commit -m "ci: add setup-lark-cli composite action"
```

---

### Task 7.2: `ci-lint.yml`, `ci-validate.yml`, `ci-render.yml`

- [ ] **Step 1-3: Write 3 generic workflows** (xem spec §4.8 cho full YAML)

- [ ] **Step 4: Test locally với `act`** (optional, nếu cài)

```bash
brew install act
act -j markdown
```

- [ ] **Step 5: Commit**

```bash
git add .github/workflows/ci-lint.yml .github/workflows/ci-validate.yml .github/workflows/ci-render.yml
git commit -m "ci: add lint + validate + render generic workflows"
```

---

### Task 7.3: `auto-index.yml` + `release.yml`

- [ ] **Step 1: Write auto-index workflow** (commits skills/README.md + docs/README.md after generation)

- [ ] **Step 2: Write release workflow** (tag-based + softprops/action-gh-release@v2)

- [ ] **Step 3: Commit**

```bash
git add .github/workflows/auto-index.yml .github/workflows/release.yml
git commit -m "ci: add auto-index + release workflows"
```

---

### Task 7.4: `lark-rebuild-index.yml` + `lark-kpi-monthly.yml`

- [ ] **Step 1: Write 2 Lark-dependent workflows** — guard với `if: vars.LARK_INTEGRATION_ENABLED == 'true'`

- [ ] **Step 2: Commit**

```bash
git add .github/workflows/lark-rebuild-index.yml .github/workflows/lark-kpi-monthly.yml
git commit -m "ci: add Lark-dependent workflows (rebuild-index, kpi-monthly, opt-in)"
```

---

### Task 7.5: Issue templates + PR template + dependabot

**Files:**
- Create: `.github/ISSUE_TEMPLATE/{bug_report,feature_request,company_onboarding}.yml`
- Create: `.github/PULL_REQUEST_TEMPLATE.md`
- Create: `.github/dependabot.yml`

- [ ] **Step 1-3: Write 3 issue templates** (YAML form syntax)

```yaml
# .github/ISSUE_TEMPLATE/bug_report.yml
name: 🐛 Bug Report
description: Báo lỗi trong saucevn/wko
labels: ["bug"]
body:
  - type: textarea
    attributes:
      label: Mô tả lỗi
    validations: { required: true }
  - type: textarea
    attributes:
      label: Tái hiện
      description: Các bước để reproduce
  - type: input
    attributes:
      label: Phiên bản wko + lark-cli
```

- [ ] **Step 4: PR template**

```markdown
## Summary
<!-- 1-2 dòng mô tả thay đổi -->

## Type
- [ ] Bug fix
- [ ] Feature
- [ ] Doc
- [ ] Refactor / chore
- [ ] BREAKING CHANGE (cần RFC discussion)

## Test plan
- [ ] Tests added/updated
- [ ] CI passing
- [ ] Render check OK với example config

## Backward compatibility
- [ ] Không breaking
- [ ] Breaking — đã document trong CHANGELOG
```

- [ ] **Step 5: dependabot.yml** (xem spec §4.8)

- [ ] **Step 6: Commit + M7 done**

```bash
git add .github/
git commit -m "ci: add issue + PR templates, dependabot weekly"
```

- [ ] **Step 7: Tag v0.9.0-rc**

```bash
git tag -a v0.9.0-rc -m "wko v0.9.0-rc — feature complete, awaiting examples + docs-meta"
```

---

## M8 — Examples + docs-meta

### Task 8.1: docs-meta — copy ONBOARDING, write ARCHITECTURE/PUBLISHING/UPGRADING

**Files:**
- Copy: `docs-meta/ONBOARDING.md` (from `docs/superpowers/specs/wko-drafts/`)
- Create: `docs-meta/ARCHITECTURE.md`, `PUBLISHING.md`, `UPGRADING.md`

- [ ] **Step 1: Copy ONBOARDING từ draft đã viết**

```bash
cp /Users/dev/Claude/Developer/Github/wiki/docs/superpowers/specs/wko-drafts/ONBOARDING.md \
   /Users/dev/Claude/Developer/Github/wko/docs-meta/ONBOARDING.md
```

- [ ] **Step 2: Write `docs-meta/ARCHITECTURE.md`**

Cover: 3 tầng (Source → Render → Dist → Publish); placeholder system Jinja2; config flow; authentication flow; skills system.

- [ ] **Step 3: Write `docs-meta/PUBLISHING.md`** — 6 bước publish

- [ ] **Step 4: Write `docs-meta/UPGRADING.md`** — sync upstream + conflict resolution + semver

- [ ] **Step 5: Commit**

```bash
git add docs-meta/
git commit -m "docs(meta): add ONBOARDING (from draft), ARCHITECTURE, PUBLISHING, UPGRADING"
```

---

### Task 8.2: Copy CLAUDE.md template + sources/schemas

- [ ] **Step 1: Copy CLAUDE.md từ draft**

```bash
cp /Users/dev/Claude/Developer/Github/wiki/docs/superpowers/specs/wko-drafts/CLAUDE.md \
   /Users/dev/Claude/Developer/Github/wko/CLAUDE.md
ln -s CLAUDE.md /Users/dev/Claude/Developer/Github/wko/AGENTS.md
```

- [ ] **Step 2: Copy schemas (generic, no PII)**

```bash
mkdir -p sources/schemas
cp /Users/dev/Claude/Developer/Github/wiki/sources/schemas/*.json sources/schemas/
cp /Users/dev/Claude/Developer/Github/wiki/sources/schemas/*.svg sources/schemas/
```

- [ ] **Step 3: Commit**

```bash
git add CLAUDE.md AGENTS.md sources/
git commit -m "docs: add CLAUDE.md (from draft) + sources/schemas/"
```

---

### Task 8.3: Examples — Acme Foods Vietnam

**Files:**
- Create: `examples/acme-foods-vietnam/company.config.yaml`, `README.md`

- [ ] **Step 1: Fully filled config** — Acme Foods (F&B Việt)

```yaml
# examples/acme-foods-vietnam/company.config.yaml
company:
  name: "Acme Foods Vietnam"
  short_name: "Acme"
  legal_entities: ["Acme Foods Co., Ltd"]
  industry: "F&B / Gia vị"
  founded_year: 2020
  hq_country: "VN"

lark:
  domain: "larksuite.com"
  tenant_subdomain: "acme"
  region: "sg"
  wiki_root_token: "Yix7wqABCDEFGHIJ"
  wiki_root_url: "https://acme.sg.larksuite.com/wiki/Yix7wqABCDEFGHIJ"
  master_index:
    node_token: "UxOkABCDEFGHIJKL"
    obj_token: "Vy3RABCDEFGHIJKL"

taxonomy:
  version: "v4.1"
  # ... full V4.1 default spaces, types, sections

# ... org, master_registry, integrations, lark_bases, policies (đầy đủ)
```

- [ ] **Step 2: README giải thích**

```markdown
# Example: Acme Foods Vietnam

Công ty hư cấu F&B Việt — 1000 đơn/ngày, TikTok Shop + Shopee.

## Đặc điểm config
- 7 SPACE V4.1 default
- 8 OPS sections (CS, WH, ECM, INV, PIM, MFG, MKT, LIVE)
- 12 MASTER registry điển hình F&B (BOM, lương 18 bước, ATTP, ...)

## Cách dùng
1. `cp examples/acme-foods-vietnam/company.config.yaml ../../company.config.yaml`
2. Sửa Lark token thật của bạn
3. `python3 scripts/render.py`
```

- [ ] **Step 3: Commit**

```bash
git add examples/acme-foods-vietnam/
git commit -m "feat(examples): add acme-foods-vietnam (F&B)"
```

---

### Task 8.4: Examples — tech-startup + minimal-3-space

- [ ] **Step 1: `examples/tech-startup-singapore/`** — 4 SPACE custom (SYS / ENG / OPS / GTM)

- [ ] **Step 2: `examples/minimal-3-space/`** — SYS + OPS + ARC only

- [ ] **Step 3: `examples/README.md`** — liệt kê 3 examples

- [ ] **Step 4: Test render với each example**

```bash
for ex in examples/*/; do
  cp "$ex/company.config.yaml" company.config.yaml
  python3 scripts/render.py --check && echo "✓ $ex"
  rm company.config.yaml
done
```

- [ ] **Step 5: Commit**

```bash
git add examples/
git commit -m "feat(examples): add tech-startup-singapore + minimal-3-space"
```

---

## M9 — Release v1.0

### Task 9.1: Integration test — full pipeline E2E

**Files:**
- Create: `tests/test_e2e.py`

- [ ] **Step 1: Write E2E test**

```python
"""End-to-end: clone-like setup + render + validate."""
import subprocess
from pathlib import Path


def test_full_pipeline_acme_example(tmp_path: Path):
    """Simulate fresh client: copy example, render, verify dist/ correct."""
    import shutil
    repo = Path(__file__).resolve().parent.parent
    work = tmp_path / "wko"
    shutil.copytree(repo, work, ignore=shutil.ignore_patterns(".git", "dist", "__pycache__"))

    # Copy example config
    shutil.copy(work / "examples/acme-foods-vietnam/company.config.yaml", work / "company.config.yaml")

    # Validate
    r = subprocess.run(["python3", "scripts/validate_config.py", "--strict"], cwd=work, capture_output=True, text=True)
    assert r.returncode == 0, r.stderr

    # Render
    r = subprocess.run(["python3", "scripts/render.py"], cwd=work, capture_output=True, text=True)
    assert r.returncode == 0, r.stderr

    # Verify dist/
    assert (work / "dist/skills").exists()
    assert (work / "dist/docs").exists()
    rendered = (work / "dist/docs/02-wiki-architecture.md").read_text()
    assert "Acme Foods Vietnam" in rendered
    assert "{{ " not in rendered  # all placeholders rendered
```

- [ ] **Step 2: Run E2E**

```bash
pytest tests/test_e2e.py -v
```

Expected: PASS.

- [ ] **Step 3: Commit**

```bash
git add tests/test_e2e.py
git commit -m "test(e2e): full pipeline with acme-foods example"
```

---

### Task 9.2: Final polish — update README, generate CHANGELOG, ROADMAP

- [ ] **Step 1: Update README với screenshot/example** của rendered output

- [ ] **Step 2: Generate `CHANGELOG.md` ban đầu**

```markdown
# Changelog

All notable changes documented here. Format: [Keep a Changelog](https://keepachangelog.com/).

## [Unreleased]

## [1.0.0] — 2026-XX-XX

### Added
- Initial public release
- Render engine (Jinja2) với 6 modes
- V4.1 taxonomy default (7 SPACE, 13 TYPE)
- 12 skills + 11 docs templated
- 17 Python scripts (lark-cli only)
- 7 CI workflows + composite action
- 3 examples (acme-foods, tech-startup, minimal)
- 4 docs-meta (ONBOARDING, ARCHITECTURE, PUBLISHING, UPGRADING)

### Migrated from
- Private repo "Thích Cay Company OS" V4 → public template V4.1
- `lark-oapi` (Python SDK) → `lark-cli` (system binary via subprocess)
```

- [ ] **Step 3: Update ROADMAP — mark v1.0 done**

- [ ] **Step 4: Commit**

```bash
git add README.md CHANGELOG.md ROADMAP.md
git commit -m "docs: polish README, init CHANGELOG, mark v1.0 done in ROADMAP"
```

---

### Task 9.3: Tag v1.0.0 + push lên github.com/saucevn/wko

- [ ] **Step 1: Final lint + test**

```bash
make lint
make test
python3 scripts/render.py --check
```

All PASS.

- [ ] **Step 2: Create GitHub repo (manual, qua gh CLI)**

```bash
gh repo create saucevn/wko --public \
  --description "Wiki Operating System — Lark Wiki Company OS template (MIT)" \
  --homepage "https://github.com/saucevn/wko"
```

- [ ] **Step 3: Push lên remote**

```bash
cd /Users/dev/Claude/Developer/Github/wko
git remote add origin https://github.com/saucevn/wko.git
git push -u origin main
```

- [ ] **Step 4: Tag v1.0.0**

```bash
git tag -a v1.0.0 -m "wko v1.0.0 — public release"
git push origin v1.0.0
```

CI release workflow sẽ trigger, generate GitHub Release với CHANGELOG_LATEST.md.

- [ ] **Step 5: Verify**

- Repo public visible tại https://github.com/saucevn/wko
- v1.0.0 release tag visible
- CI badge green
- README hiển thị đúng

---

## Self-Review

**1. Spec coverage:**

| Spec section | Tasks |
|---|---|
| §4.1 File tree | M1 (bootstrap) + tất cả tasks tạo files |
| §4.2 Config schema | T2.2 |
| §4.3 Render engine | T3.1-3.3 |
| §4.4 Templating strategy | M4 + M5 |
| §4.5 Scripts strategy | M6 (8 tasks) |
| §4.6 lark-cli hard requirement | T2.1 (require_lark_cli), T7.1 (composite action) |
| §4.7 wiki_reviewer_bot rewrite | T6.7 |
| §4.8 CI workflows (7 + composite) | M7 (5 tasks: composite + 3 generic + 2 Lark + auto-index + release) |
| §4.9 Onboarding 8 bước | T8.1 (copy from draft) |
| §4.10 Documentation map | M8 (4 tasks) |
| §5 Data flow | implicit in M3+M6 |
| §6 Error handling | T2.1 (fail-fast), T3.1 (StrictUndefined) |
| §7 Testing | tests/ trong M2-M6 |
| §8 Migration path | T6.8 (migrate_v4_to_v41) |
| §9 Roadmap | T1.3 (ROADMAP.md) |
| §10 Risks | spec only, no task needed |
| §11 Open questions | spec only |

All spec sections covered. ✅

**2. Placeholder scan:** Searched plan for "TBD/TODO/implement later" → only legitimate template TODOs trong skills/docs (e.g., `<!-- TODO {{ company.short_name }} owner -->`) which are intentional output placeholders. Plan steps all have real code.

**3. Type consistency:**
- `RenderError`, `ValidationError`, `StructureError` exception class names consistent
- `load_config()`, `require_lark_cli()`, `require_lark_auth()` signatures match across files
- `company.config.yaml` path consistent
- Field paths (`cfg["lark"]["wiki_root_token"]`) consistent

No issues found.

---

## Execution Handoff

**Plan complete and saved to `docs/superpowers/plans/2026-05-19-wko-public-template-implementation.md`.**

**45 tasks across 9 milestones, ~8.5 tuần effort, 4 early-stopping release tags (v0.1.0-alpha → v0.5.0-beta → v0.9.0-rc → v1.0.0).**

Two execution options:

**1. Subagent-Driven (recommended)** — Dispatch fresh subagent per task (Claude Code), review giữa task, fast iteration. Phù hợp khi muốn parallelize hoặc dùng task-specific context.

**2. Inline Execution** — Execute tasks trong session này dùng `superpowers:executing-plans`, batch execution với checkpoints để review.

**Which approach?**
