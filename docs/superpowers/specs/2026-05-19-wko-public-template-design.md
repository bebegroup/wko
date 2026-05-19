# wko — Public Lark Wiki Company OS Template

## 1. Mục tiêu

Chắt lọc repo `Thích Cay Company OS` (private) thành một repo public MIT-licensed
mang tên **`wko`** (Wiki Operating System), có thể được clone bởi nhiều công ty
client khác nhau. Mỗi client cấu hình 1 file `company.config.yaml`, render qua
Jinja2 → publish lên Lark Wiki / Feishu Wiki của họ.

**Không phải là:** library, framework, CLI tool, SaaS. Chỉ là một template repo
+ tooling tối thiểu.

## 2. Bối cảnh

Repo gốc Thích Cay đã chạy V4 (8 SPACE, 11 TYPE) trong production và đang
chuyển sang V4.1 Execution-First (7 SPACE, 13 TYPE, HUB-001 sticky, POL-vs-MST
clarified). Repo public sẽ dùng V4.1 làm default taxonomy.

Audit repo (do Explore agent thực hiện 2026-05-19) phân loại file:
- **Reusable as-is (~20%):** skills 02/03/04/06/07/11, scripts validate/generate/backlink
- **Templatable (~50%):** skills 01/05/08/09/10/12, docs 02/03/05-09, scripts 7 file Lark-dependent
- **Company-specific (~30%):** docs 00/01/04/06, master_registry list, sources/excel/, V3→V4 migration

## 3. Quyết định kiến trúc đã chốt

| # | Quyết định | Giá trị |
|---|---|---|
| 1 | Scope | Full toolkit Lark Wiki Company OS (không skills-only) |
| 2 | Customization model | `company.config.yaml` + Jinja2 placeholder runtime |
| 3 | Render strategy | Approach B — Source + `dist/` rendered (build step) |
| 4 | Ngôn ngữ | Tiếng Việt (tất cả skills, docs, README) |
| 5 | Thích Cay content | Strip sạch — placeholder trống + `<!-- TODO -->` |
| 6 | License | MIT |
| 7 | Repo name | `wko` (Wiki Operating System) |
| 8 | sources/ | Loại bỏ `excel/`, `lark-exports/`. Giữ `schemas/` (generic) |
| 9 | OKR O3K skill pack | Loại khỏi v1 (đang draft) |
| 10 | Lark client SDK | **`lark-cli only`** — drop `lark-oapi`, gọi qua `subprocess` |
| 11 | Default taxonomy | V4.1 Execution-First (7 SPACE, 13 TYPE, HUB-001 sticky) |
| 12 | lark-cli là HARD requirement | Scripts fail-fast nếu thiếu |

## 4. Kiến trúc

### 4.1. Repo file tree

```
wko/
├── README.md                              # entry point
├── CLAUDE.md / AGENTS.md                  # AI agent rules (template-aware)
├── LICENSE                                # MIT
├── CONTRIBUTING.md
├── SECURITY.md
├── ROADMAP.md
├── company.config.yaml.example            # schema mẫu
├── company.config.yaml                    # gitignored, client fill
├── .env.example                           # LARK_APP_ID/SECRET placeholder
├── .gitignore                             # ignore .env, company.config.yaml, dist/, drafts/
│
├── skills/                                # 12 file source (V4.1)
│   ├── 01-page-format.md
│   ├── 02-writing-style.md
│   ├── 03-linking-rules.md
│   ├── 04-page-status.md
│   ├── 05-publish-workflow.md
│   ├── 06-excel-to-wiki.md
│   ├── 07-source-protection.md
│   ├── 08-index-and-numbering.md
│   ├── 09-contributing-workflow.md
│   ├── 10-master-registry.md
│   ├── 11-page-types.md
│   └── 12-emergency-playbook.md
│
├── docs/                                  # 11 docs source (V4.1)
│   ├── 00-company-overview.md             # strip 100% → TODO skeleton
│   ├── 01-org-structure.md                # render từ org.departments
│   ├── 02-wiki-architecture.md            # loop spaces, sections
│   ├── 03-permissions.md
│   ├── 04-glossary.md                     # giữ thuật ngữ Wiki chuẩn, strip Thích Cay
│   ├── 05-lark-base-connections.md
│   ├── 06-context-notes.md                # strip 100%
│   ├── 07-status-tracker.md               # strip live data
│   ├── 08-contributing.md
│   ├── 09-master-registry.md
│   └── 10-page-types-taxonomy.md          # 13 types V4.1
│
├── scripts/                               # 16 .py + 1 requirements.txt
│   ├── _common.py                         # shared: load_config, require_lark_cli, require_lark_auth
│   ├── render.py                          # MỚI — Jinja2 substitute → dist/
│   ├── validate_config.py                 # MỚI — lint company.config.yaml
│   ├── init_company.py                    # MỚI — interactive first-time setup
│   ├── validate_structure.py              # giữ generic
│   ├── generate_index.py                  # giữ generic
│   ├── build_backlink_graph.py            # giữ generic
│   ├── wiki_navigator.py                  # templatize: đọc config
│   ├── pull_from_lark.py                  # implement đầy đủ (hiện skeleton)
│   ├── rebuild_master_index.py            # templatize, support master_index_fields V4.1
│   ├── rebuild_hub_toc.py                 # templatize, support hub_rules
│   ├── sync_index_contributed_column.py   # templatize
│   ├── wiki_kpi_report.py                 # templatize, KPI per execution-first formula
│   ├── content_quality_audit.py           # templatize, audit POL-vs-MST + execution-first
│   ├── wiki_reviewer_bot.py               # REWRITE — lark-cli event consume (bỏ lark-oapi)
│   ├── migrate_v4_to_v41.py               # MỚI — optional migration cho client V4
│   └── requirements.txt                   # PyYAML, jinja2, anthropic, python-dotenv, pytest, watchdog
│
├── .github/
│   ├── workflows/
│   │   ├── ci-lint.yml                    # markdown + python lint
│   │   ├── ci-validate.yml                # structure + config validate
│   │   ├── ci-render.yml                  # render.py dry-run
│   │   ├── auto-index.yml                 # auto-update skills/README + docs/README (main)
│   │   ├── lark-rebuild-index.yml         # Lark-dependent, opt-in
│   │   ├── lark-kpi-monthly.yml           # Lark-dependent, cron
│   │   └── release.yml                    # tag-based release
│   ├── actions/
│   │   └── setup-lark-cli/
│   │       └── action.yml                 # composite action: install lark-cli binary
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.yml
│   │   ├── feature_request.yml
│   │   └── company_onboarding.yml
│   ├── PULL_REQUEST_TEMPLATE.md
│   └── dependabot.yml
│
├── .claude/
│   └── settings.local.json.example        # cho client copy
│
├── docs-meta/                             # meta doc về repo public (KHÔNG render)
│   ├── ONBOARDING.md                      # 30 phút setup
│   ├── ARCHITECTURE.md                    # giải thích placeholder system
│   ├── PUBLISHING.md                      # workflow publish lên Lark
│   └── UPGRADING.md                       # sync upstream khi có version mới
│
├── examples/                              # 3 ví dụ fully-filled config
│   ├── README.md
│   ├── acme-foods-vietnam/                # F&B Việt
│   ├── tech-startup-singapore/            # SaaS, 4 SPACE custom
│   └── minimal-3-space/                   # tối giản
│
├── sources/
│   └── schemas/                           # giữ JSON+SVG schema generic
│
└── dist/                                  # gitignored — output của render.py
    ├── skills/
    └── docs/
```

### 4.2. `company.config.yaml` schema (V4.1 default)

12 section chính:

1. **`company`** — identity (name, short_name, legal_entities, industry, hq_country)
2. **`lark`** — instance (domain, tenant_subdomain, region, wiki_root_token, master_index.{node,obj}_token)
3. **`taxonomy`** — V4.1 default:
   - `version: "v4.1"`, `philosophy: "execution-first"`
   - `spaces` (7): SYS / GEN / INT / OPS / BOD / TMP / ARC
   - `page_types` (13): MST / SOP / CHK / TMP / HUB / PBK / DBD / DIC / POL / LOG / IDX / **PROC** / **GDL**
   - `sections` (24 mặc định, mỗi SPACE 2-8 section)
   - `page_code_format: "{space}-{section_suffix}-{type}-{number:03d}"`
4. **`hub_rules`** — `master_hub_number: "001"`, `branch_hub_min_pages: 3`, `branch_patterns` (A/B/C/D), `hub_parent_required: true`
5. **`execution_first`** — `section_formula`, `page_purpose_questions`, `rejection_rules`
6. **`pol_mst_rules`** — `pol_scope: "external_only"`, `primary_owner_table`, `pol_required_sections: 8`, `mst_bridge_required_sections: 5`
7. **`org`** — departments list
8. **`master_registry`** — 12 MASTER bắt buộc (client điền)
9. **`integrations`** — `contributor_group_email`, `reviewer_bot_webhook`, `reviewer_bot_name`
10. **`lark_bases`** — 5-10 Lark Base với name + base_token + purpose
11. **`master_index_fields`** — `required` (12 trường incl. Hub Parent), `recommended` (Source Type / URL / Effective Date / Review Cadence / Impacted Pages)
12. **`policies`** — `page_status_values`, `default_status`, `publish_requires_review`, `arc_append_only: true`, `no_renumber_on_rename: true`

Validation by `scripts/validate_config.py`:
- Required fields present (fail-fast nếu thiếu)
- `taxonomy.version` exists (warn nếu không phải v4.1)
- 7 type cốt lõi execution-first phải có (HUB/MST/PROC/SOP/CHK/TMP/PBK)
- POL primary_owner_table phải khớp với sections tồn tại
- `master_registry` codes khớp `page_code_format`
- `hub_rules.master_hub_number` consistent

### 4.3. Render engine — `scripts/render.py`

**Stack:** Python 3.11+, Jinja2, PyYAML.

**Behavior:**
- Source `.md` chứa `{{ company.name }}`, loops `{% for s in taxonomy.spaces %}`
- `render.py` → `dist/skills/`, `dist/docs/` (đã substitute)
- `StrictUndefined` — fail nếu placeholder thiếu config
- Code blocks raw (không render bên trong `\`\`\`...\`\`\``)
- Modes:
  - `python3 scripts/render.py` — render toàn bộ
  - `--check` — CI mode, fail nếu render lỗi
  - `--file path` — render 1 file
  - `--watch` — re-render khi source thay đổi (dev)
  - `--clean` — xoá dist/ trước

**Performance:** ~23 file × Jinja2 ≈ < 200ms.

**Custom filters:**
- `{{ url|wiki_link }}` → `[label](url)`
- `{{ code|page_code }}` → format code
- `{{ table }}` macro → markdown table từ list-of-dict

### 4.4. Templating strategy — per file

| Nhóm | Files | Strategy |
|---|---|---|
| Tổng quát (~20%) | skills 02/03/04/06/07/11 | Chỉ thay tên công ty + URL Lark ở vài ví dụ |
| Heavy templating | skills 01/05/08/09/10/12 | Loop spaces/sections/types/masters từ config |
| Strip + skeleton | docs 00/01/06/07 | Để TODO comment, render placeholder rỗng |
| Render từ list | docs 02/03/05/09 | Loop từ config.taxonomy / org / master_registry / lark_bases |
| Hybrid | skills 02-11 (writing style), docs 04 (glossary), docs 10 (page_types) | Giữ structure chuẩn, replace ví dụ |

### 4.5. Scripts strategy — 4 nhóm

**A. Generic, copy as-is (3 file):**
`validate_structure.py`, `generate_index.py`, `build_backlink_graph.py`

**B. Templatable, đọc config (8 file):**
`wiki_navigator.py`, `rebuild_master_index.py`, `rebuild_hub_toc.py`,
`sync_index_contributed_column.py`, `wiki_kpi_report.py`,
`content_quality_audit.py`, `wiki_reviewer_bot.py` (rewrite),
`pull_from_lark.py` (implement)

**C. Mới (5 file):**
`_common.py`, `render.py`, `validate_config.py`, `init_company.py`,
`migrate_v4_to_v41.py` (optional opt-in)

**D. Drop (1 file):**
`migrate_to_v4.py` (V3→V4 legacy)

**Pattern dùng config:**
```python
from _common import load_config, require_lark_cli, require_lark_auth

def main():
    require_lark_cli()                       # fail-fast nếu thiếu binary
    require_lark_auth()                      # fail-fast nếu chưa login
    cfg = load_config()
    wiki_token = cfg["lark"]["wiki_root_token"]
```

### 4.6. lark-cli là HARD dependency

**Pre-flight check** (mọi script):
```python
def require_lark_cli() -> None:
    if shutil.which("lark-cli") is None:
        sys.exit("❌ lark-cli không tìm thấy. brew install lark-cli...")
    # Check version >= 1.0.30
```

**README §1 — Yêu cầu bắt buộc:** đặt lên đầu, không thể skip.

**CI workflow setup-lark-cli composite action:** install binary trước khi chạy script.

### 4.7. `wiki_reviewer_bot.py` — kiến trúc mới

Drop `lark-oapi`. Dùng `lark-cli event consume im.message.receive_v1` qua subprocess:

```python
proc = subprocess.Popen(
    ["lark-cli", "event", "consume", "im.message.receive_v1"],
    stdout=subprocess.PIPE, bufsize=1, text=True,
)
for line in proc.stdout:            # NDJSON, 1 line = 1 event
    event = json.loads(line)
    # ... filter chat_id, branch approval vs URL, call Claude, post comment via lark-cli drive comment
```

**Lợi ích:**
- Auth central qua `lark-cli auth login` (OS keychain)
- Không lock Python SDK version
- Match 20+ `lark-*` skills hiện có

### 4.8. CI workflows (7 + composite action)

| Workflow | Trigger | Lark? | Mục đích |
|---|---|---|---|
| `ci-lint.yml` | PR + push | No | markdown + ruff + black |
| `ci-validate.yml` | PR + push | No | structure + config validate |
| `ci-render.yml` | PR + push | No | render.py --check + upload artifact |
| `auto-index.yml` | push main (skills/docs) | No | regen README, commit lại |
| `lark-rebuild-index.yml` | manual + weekly cron | Yes | push Master Index lên Lark (opt-in via repo var) |
| `lark-kpi-monthly.yml` | monthly cron | Yes | KPI report (opt-in) |
| `release.yml` | tag push | No | semantic version + changelog |

**Secrets:** `LARK_APP_ID`, `LARK_APP_SECRET`, `COMPANY_CONFIG_B64`, `ANTHROPIC_API_KEY` (optional).
**Repo var:** `LARK_INTEGRATION_ENABLED=false` (mặc định) — client set `true` khi sẵn sàng.

### 4.9. Onboarding (30 phút, 8 bước)

1. Clone + venv + pip install + brew install lark-cli (5 phút)
2. `lark-cli auth login --as user` (2 phút)
3. Tạo Lark Wiki space + note `wiki_root_token` (5 phút)
4. Tạo Lark App + note `App ID/Secret` (5 phút)
5. `cp company.config.yaml.example company.config.yaml` + fill + `validate_config.py --strict` (10 phút)
6. `render.py` + verify dist/ (2 phút)
7. Publish first page lên Lark (5 phút)
8. Setup GitHub secrets + vars, run `Lark Rebuild Index` workflow (5 phút)

### 4.10. Documentation map

| File | Audience | Mục đích |
|---|---|---|
| `README.md` | Anyone | Entry point, quick start |
| `docs-meta/ONBOARDING.md` | Client mới | Setup 30 phút |
| `docs-meta/ARCHITECTURE.md` | Dev | Hiểu placeholder + render flow |
| `docs-meta/PUBLISHING.md` | Editor | Workflow soạn → publish |
| `docs-meta/UPGRADING.md` | Maintainer | Sync upstream khi có version mới |
| `examples/*/README.md` | Client | 3 ví dụ company shapes khác nhau |
| `ROADMAP.md` | Community | Lộ trình v1.x / v2.0 |
| `CONTRIBUTING.md` | Contributor | Cách đóng góp upstream |
| `SECURITY.md` | All | Báo vulnerability, anti-leak rules |
| `LICENSE` | All | MIT |
| `CLAUDE.md / AGENTS.md` | AI agent | Quy tắc làm việc với repo |

## 5. Data flow

```
┌─────────────────────┐
│ company.config.yaml │  ← client fill (manual hoặc init_company.py)
└──────────┬──────────┘
           │ validate_config.py
           ▼
   ┌──────────────────┐
   │ Validated config │
   └────────┬─────────┘
            │
            │ render.py (Jinja2 + StrictUndefined)
            ▼
     ┌────────────┐         ┌─────────────────────┐
     │   dist/    │ ──────▶ │ Lark Wiki (publish) │
     │ skills/    │         │ via lark-cli docs   │
     │ docs/      │         └─────────────────────┘
     └────────────┘                    │
                                       ▼
                            ┌─────────────────────┐
                            │ Master Wiki Index   │
                            │ (SYS-00-IDX-001)    │
                            └─────────────────────┘
                                       ▲
                                       │
                            scripts/rebuild_master_index.py
```

## 6. Error handling

| Scenario | Behavior |
|---|---|
| Thiếu `lark-cli` | `require_lark_cli()` sys.exit với hướng dẫn cài |
| Chưa `lark-cli auth login` | `require_lark_auth()` sys.exit |
| Thiếu `company.config.yaml` | `load_config()` raise FileNotFoundError, gợi ý `init_company.py` |
| Placeholder thiếu trong config | Jinja2 `StrictUndefined` raise — file:line cụ thể |
| `taxonomy.version` không phải v4.1 | Warn, nhưng vẫn render (custom OK) |
| `master_registry` code sai format | `validate_config.py` fail |
| Lark API call lỗi (network, scope) | `subprocess.CalledProcessError` propagate với stderr |
| CI workflow Lark-dependent thiếu secret | Workflow check `if: vars.LARK_INTEGRATION_ENABLED == 'true'` → skip nếu chưa set |
| Commit nhầm `company.config.yaml` chứa token | Pre-commit hook (optional, docs-meta/UPGRADING.md hướng dẫn) + SECURITY.md có rotation guide |

## 7. Testing

- **Unit tests:** `tests/test_render.py`, `tests/test_validate_config.py`, `tests/test_common.py`
  - Jinja2 substitution correctness
  - Config schema validation (positive + negative cases)
  - lark-cli pre-flight check (mock `shutil.which`)
- **Integration tests:** chạy `render.py` với `examples/*/company.config.yaml`, snapshot dist/
- **CI matrix:** Python 3.11, 3.12 × Ubuntu 22.04 (default GitHub Actions)
- **Mock Lark API:** subprocess mocking với `unittest.mock.patch("subprocess.run")`

## 8. Migration path

**Cho Thích Cay (repo gốc):** không migrate. Repo gốc vẫn private, tiếp tục dùng.
Khi `wko` v1.0 release, Thích Cay có thể optional fork về để hưởng improvements.

**Cho client mới:** clone `wko` → fill config → publish.

**Cho client đang ở V4 (8 SPACE, 11 TYPE):** chạy `migrate_v4_to_v41.py`:
- Map `COM-*` codes → `GEN-*`
- Archive `EMG-*` codes → `ARC-OLD-*`
- Output JSON mapping để rename manually trên Lark

## 9. Roadmap

- **v1.0 (Q3 2026):** Public release với tất cả ở mục 4
- **v1.1 (Q4 2026):** `init_company.py` interactive wizard, HTML preview, Slack adapter
- **v1.2 (Q1 2027):** Multi-tenant profile system (`LARK_PROFILE=acme`)
- **v2.0 (2027+):** Notion / Confluence / Outline backend adapters, plugin system

**Out of scope v1.x:** GUI editor, self-hosting wiki engine, AI auto-generation, localization sang ngôn ngữ khác.

## 10. Risks & mitigations

| Risk | Mitigation |
|---|---|
| `lark-cli` API breaking change | Pin version range trong `setup-lark-cli` composite action; CHANGELOG track |
| Client commit secret (config.yaml hoặc .env) | `.gitignore` mặc định + SECURITY.md + optional pre-commit hook |
| V4.1 taxonomy không fit công ty khác | Config cho phép custom spaces/sections/types; default chỉ là suggestion |
| Maintenance overhead khi nhiều client custom | UPGRADING.md document conflict resolution; semver promise; LTS branch nếu cần |
| Vendor lock Lark | v2.0 adapters cho Notion/Confluence — không cản trở v1.0 |
| Repo gốc Thích Cay drift khỏi public | Public template focus generic; Thích Cay-specific changes không backport |

## 11. Open questions / RFC

- **Hub Parent number:** V4.1 doc gốc dùng `HUB-000` (sticky), nhưng repo Thích Cay hiện đang chạy `HUB-001`. Mặc định config = `"001"` cho consistency với V4 cũ. Client có thể override sang `"000"`.
- **Multi-language docs:** v1.0 chỉ tiếng Việt. EN port chờ community contribution v1.x.
- **Plugin system:** OKR O3K skill pack đang draft, loại khỏi v1.0. Reintroduce như external repo + plugin pattern ở v2.0?

## 12. Tổng kết

- Repo public `wko` (MIT) chắt lọc từ Thích Cay Company OS private repo
- Cấu trúc: source `.md` (Jinja2 placeholder) → `render.py` → `dist/` → Lark
- 1 file `company.config.yaml` cấu hình toàn bộ
- Default taxonomy = V4.1 Execution-First (7 SPACE, 13 TYPE)
- `lark-cli` là hard requirement, mọi script gọi qua subprocess
- 7 CI workflows + composite action setup-lark-cli
- Onboarding 30 phút, 8 bước
- 3 ví dụ trong `examples/` để client học flexibility

Effort tổng (ước lượng):
- **Phase 1 (2-3 tuần):** Bootstrap repo, render.py, validate_config.py, strip Thích Cay content
- **Phase 2 (2-3 tuần):** Rewrite wiki_reviewer_bot.py (lark-oapi → lark-cli), implement pull_from_lark.py, migrate_v4_to_v41.py
- **Phase 3 (1-2 tuần):** CI workflows + composite action + secrets docs
- **Phase 4 (1 tuần):** 3 examples, ONBOARDING/ARCHITECTURE/PUBLISHING/UPGRADING docs
- **Phase 5 (1 tuần):** End-to-end test, release v1.0

**Tổng:** ~7-10 tuần engineering.
