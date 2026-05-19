# CLAUDE.md — Quy tắc làm việc với repo `{{ company.short_name }} Wiki Company OS`

> File này dành cho **AI agent** (Claude Code, Cursor, Codex, Gemini, …) làm việc trên repo này.
> Mọi agent đọc file này TRƯỚC khi bắt đầu bất kỳ task nào.
> File `AGENTS.md` là mirror của file này.
>
> **Repo này được dựng từ template:** [saucevn/wko](https://github.com/saucevn/wko) (MIT licensed).
> Khi pull update từ upstream, file này có thể được rewrite — giữ section "Custom rules" cuối file để override.

---

## 1. Repo này là gì

| Câu hỏi | Trả lời |
|---|---|
| Repo GitHub này dùng để làm gì? | Lưu **source template** (skills, docs, scripts) + **config** (`company.config.yaml`) để dựng Wiki Company OS của `{{ company.name }}` trên Lark / Feishu |
| Nội dung Wiki thực tế ở đâu? | **Lark Wiki "{{ company.short_name }} Company OS"** — {{ lark.wiki_root_url }} |
| **Master Wiki Index ở đâu?** | **`SYS-00-IDX-001`** trên Lark (node `{{ lark.master_index.node_token }}`, obj `{{ lark.master_index.obj_token }}`) — nguồn **canonical** với 12 cột bắt buộc (Code/Name/Space/Section/Type/Hub Parent/Owner/Reviewer/Status/Version/Security Level/Link). Đọc trước khi viết. |
| **Đánh số + đặt tên trang? (V4.1)** | **Mã page:** `[SPACE]-[SECTION]-[TYPE]-[NUMBER]` vd `OPS-CS-PROC-001`. **Title trên Lark:** `<MÃ> <Tên page>` vd `OPS-CS-PROC-001 Luồng xử lý khách hàng từ inbox đến đóng ticket`. **7 SPACE V4.1:** SYS / GEN / INT / OPS / BOD / TMP / ARC. **13 TYPE:** MST / SOP / CHK / TMP / HUB / PBK / DBD / DIC / POL / LOG / IDX / PROC / GDL. Xem [skill 08](skills/08-index-and-numbering.md) + [skill 11](skills/11-page-types.md). |
| **Execution-First là gì?** | Wiki không phải thư viện đọc hiểu — là **hệ thống thực thi công việc**. Mỗi page phải trả lời ≥ 1 câu hỏi thực thi (HUB / PROC / SOP / CHK / TMP / PBK / DBD / MST). Công thức section: `1 HUB + 1-2 MST + 1 PROC + 3-5 SOP + 1 CHK + 1 TMP + 1 PBK` (+ optional DBD/DIC/GDL/POL). |
| Repo này có phải nơi soạn thảo nội dung Wiki không? | **KHÔNG.** Soạn thảo & publish thực hiện trực tiếp trên Lark, qua `lark-cli`. Repo này chỉ chứa quy tắc, config, công cụ. |
| Đẩy lên Lark bằng cách nào? | Qua `lark-cli` (hard requirement) — xem [skills/05-publish-workflow.md](skills/05-publish-workflow.md) sau khi render |

---

## 2. Hai nguyên tắc tối thượng

### 🛡️ Nguyên tắc 1 — Bảo vệ source code & secret

```
KHÔNG xóa, sửa, hoặc publish nhầm các file source.
KHÔNG commit secret (token, .env, company.config.yaml).
```

**Files protected (chỉ thay khi có review):**
- `company.config.yaml` — chứa Lark token, **KHÔNG commit** (đã gitignored)
- `.env` — chứa App Secret, **KHÔNG commit** (đã gitignored)
- `skills/*.md`, `docs/*.md` — source template từ saucevn/wko, sửa khi có lý do rõ
- `scripts/*.py` — chỉ sửa qua PR có review
- `.github/workflows/*` — chỉ sửa qua PR có review
- `sources/schemas/*` — schema sinh tự động

**KHÔNG gọi `lark-cli ... publish` với input là `*.py`, `*.json`, `*.xml`, `*.yaml`** — chỉ publish markdown đã được render từ `dist/`.

### 🧹 Nguyên tắc 2 — Clean-slate trước soạn thảo

Trước mỗi phiên soạn thảo Wiki, **luôn** chạy checklist:

1. `git status` → working tree phải sạch
2. `git pull origin main` → đồng bộ rules mới nhất
3. `git fetch upstream && git log HEAD..upstream/main` → check có update từ saucevn/wko không
4. `python3 scripts/render.py` → đảm bảo `dist/` tươi
5. Đọc skill liên quan trong `dist/skills/`
6. **Xác định đích Lark trước khi viết** (Space → Section → Page). Không có đích = không soạn.
7. Drafts viết ngoài repo hoặc trong `drafts/` (đã gitignored). **KHÔNG** commit draft vào repo.

---

## 3. Index dẫn lối — Khi nào dùng cái gì

> ⚠️ Mọi link dưới đây trỏ tới `skills/` và `docs/` (source). Khi đọc, mở file tương ứng trong `dist/skills/` hoặc `dist/docs/` để xem nội dung đã render với data của `{{ company.name }}`.

### Khi cần biết **VIẾT NHƯ THẾ NÀO** → đọc `skills/`

| Tình huống | File |
|---|---|
| Viết 1 trang Wiki mới | [skills/01-page-format.md](skills/01-page-format.md) |
| Đặt tiêu đề, dùng từ ngữ | [skills/02-writing-style.md](skills/02-writing-style.md) |
| Link giữa các trang & Lark Base + backlink chiều ngược | [skills/03-linking-rules.md](skills/03-linking-rules.md) |
| Gán trạng thái trang (Draft/Active/Deprecated/Archived) | [skills/04-page-status.md](skills/04-page-status.md) |
| Đẩy nội dung lên Lark (6-step V4.1) | [skills/05-publish-workflow.md](skills/05-publish-workflow.md) |
| Chuyển nội dung từ Excel sang Wiki | [skills/06-excel-to-wiki.md](skills/06-excel-to-wiki.md) |
| Bảo vệ source + clean-slate | [skills/07-source-protection.md](skills/07-source-protection.md) |
| Maintain Master Wiki Index + mã V4.1 | [skills/08-index-and-numbering.md](skills/08-index-and-numbering.md) |
| Workflow contributing + bot review (AI agent) | [skills/09-contributing-workflow.md](skills/09-contributing-workflow.md) |
| **Master Registry — MASTER bắt buộc** | [skills/10-master-registry.md](skills/10-master-registry.md) |
| **Taxonomy 13 loại page V4.1 (MST/SOP/CHK/TMP/HUB/PBK/DBD/DIC/POL/LOG/IDX/PROC/GDL)** | [skills/11-page-types.md](skills/11-page-types.md) |
| **Emergency Playbook — PBK rules** | [skills/12-emergency-playbook.md](skills/12-emergency-playbook.md) |

### Khi cần biết **THÔNG TIN CÔNG TY** → đọc `docs/`

| Câu hỏi | File |
|---|---|
| `{{ company.name }}` là ai? | [docs/00-company-overview.md](docs/00-company-overview.md) |
| Cơ cấu tổ chức | [docs/01-org-structure.md](docs/01-org-structure.md) |
| Wiki có cấu trúc gì? (7 SPACE V4.1) | [docs/02-wiki-architecture.md](docs/02-wiki-architecture.md) |
| Ai đọc/viết được Space nào? | [docs/03-permissions.md](docs/03-permissions.md) |
| Thuật ngữ nội bộ | [docs/04-glossary.md](docs/04-glossary.md) |
| Lark Base nào, link ở đâu? | [docs/05-lark-base-connections.md](docs/05-lark-base-connections.md) |
| Ngữ cảnh vận hành | [docs/06-context-notes.md](docs/06-context-notes.md) |
| Trạng thái Wiki hiện tại | [docs/07-status-tracker.md](docs/07-status-tracker.md) |
| Cách contribute Wiki (qua Lark, không qua Git) | [docs/08-contributing.md](docs/08-contributing.md) |
| **Master Registry — MASTER bắt buộc của công ty** | [docs/09-master-registry.md](docs/09-master-registry.md) |
| **Page Types Taxonomy — 13 type V4.1** | [docs/10-page-types-taxonomy.md](docs/10-page-types-taxonomy.md) |

### Khi cần biết **CÁCH DỰNG / DUY TRÌ TEMPLATE** → đọc `docs-meta/`

| Câu hỏi | File |
|---|---|
| Setup lần đầu (cho người mới onboarding) | [docs-meta/ONBOARDING.md](docs-meta/ONBOARDING.md) |
| Kiến trúc placeholder + render flow | [docs-meta/ARCHITECTURE.md](docs-meta/ARCHITECTURE.md) |
| Workflow publish 1 page lên Lark (chi tiết) | [docs-meta/PUBLISHING.md](docs-meta/PUBLISHING.md) |
| Pull update từ saucevn/wko upstream | [docs-meta/UPGRADING.md](docs-meta/UPGRADING.md) |

---

## 4. Quy trình mặc định khi nhận task soạn thảo

```
Bước 1: Đọc CLAUDE.md (file này) + skill phù hợp với task
Bước 2: Render template nếu chưa: `python3 scripts/render.py`
Bước 3: Xác định đích Lark (Space → Section → Page)
        → Tra dist/docs/02-wiki-architecture.md
Bước 4: Tra Master Index lấy NUMBER tiếp theo
        → Mở SYS-00-IDX-001 trên Lark, filter [SPACE]-[SECTION]-[TYPE]
Bước 5: Soạn draft ngoài repo (drafts/ gitignored hoặc /tmp/)
Bước 6: Review draft với owner (`{{ company.short_name }} repo maintainer`) trước khi publish
Bước 7: Publish qua lark-cli theo skills/05-publish-workflow.md
        → Log node_id + space_id vào commit message nếu có code change
Bước 8: Update Master Index — thêm row mới với 12 cột bắt buộc
```

---

## 5. Quy tắc tương tác AI agent

1. **KHÔNG tự động commit** mọi thay đổi. Hỏi owner trước khi commit + push.
2. **KHÔNG tự động publish lên Lark.** Publish luôn manual hoặc qua CI có review.
3. **KHÔNG viết toàn bộ Wiki trong 1 phiên.** Viết từng trang, xác nhận.
4. **LUÔN** tuân theo format trong [skills/01-page-format.md](skills/01-page-format.md).
5. **LUÔN** gán trạng thái cho trang mới ([skills/04-page-status.md](skills/04-page-status.md)).
6. **LUÔN** thêm section "🔗 Tài liệu liên quan" cuối trang Wiki.
7. **LUÔN** điền cột "Hub Parent" trong Master Index — page phải có parent rõ ràng.
8. **KHÔNG** xóa hay đổi tên file trong `sources/` mà không có lý do rõ ràng.
9. **KHÔNG** sửa file trong `dist/` — đó là output của `render.py`, sẽ bị overwrite. Sửa source trong `skills/` hoặc `docs/`.
10. **KHÔNG** commit `company.config.yaml` hoặc `.env` — đã gitignored, nếu git status thấy chúng = something is wrong.

---

## 6. Execution-First — không tạo page bừa

> Trước khi tạo page mới, trả lời: page này giúp **AI** làm việc **GÌ**?

| Nhu cầu thực tế | Type page nên dùng |
|---|---|
| Sai / thiếu luật gốc | MST |
| Chính sách bên ngoài (sàn, luật) thay đổi | POL (external only) |
| Chưa có luồng "ai làm trước sau" | PROC |
| Nhân viên không biết từng bước làm | SOP |
| Hay quên bước kiểm tra | CHK |
| Thiếu mẫu để điền / gửi / báo cáo | TMP |
| Có ngoại lệ, lỗi, tình huống rẽ nhánh | PBK |
| Sai do không hiểu thuật ngữ (hiếm — chỉ tạo khi gây sai thao tác) | DIC |
| Sai do tone / cách ứng xử / style | GDL |
| Không nhìn được số để quản trị (chỉ tạo khi có source số thật) | DBD |
| Cần ghi nhận lịch sử quyết định | LOG |

**KHÔNG tạo page nếu:**
- Chỉ vì "nên có" mà không phục vụ thực thi cụ thể
- DIC mà thuật ngữ không gây sai thao tác
- GDL mà guideline không ảnh hưởng cách làm việc
- DBD mà chưa có source số liệu thật
- POL mà nó thực ra là nội bộ (phải là MST, không phải POL)

---

## 7. Stack & công cụ

| Công cụ | Vai trò | Lệnh kiểm tra |
|---|---|---|
| `lark-cli` (≥ 1.0.30) | **HARD REQUIREMENT.** Mọi tương tác với Lark | `lark-cli --version` |
| Python 3.11+ | Chạy scripts/ | `python3 --version` |
| Jinja2 (qua pip) | Render placeholder | `pip show jinja2` |
| Git | Source control | `git status` |
| markdownlint-cli2 | Lint markdown (qua CI) | (dùng trong workflow) |
| Anthropic API | (optional) Cho `wiki_reviewer_bot.py` | `echo $ANTHROPIC_API_KEY` |

Cấu hình permission Bash: xem `.claude/settings.local.json.example`. Copy thành `.claude/settings.local.json` và customize.

---

## 8. Khi nào cần hỏi owner

> Owner của repo này: **{{ company.short_name }} repo maintainer** (xem `MAINTAINERS.md` của fork để biết người cụ thể).
> Owner của template upstream: **[@saucevn](https://github.com/saucevn)** — chỉ hỏi qua GitHub Issues nếu là bug/feature request về template.

Hỏi owner khi:

- Tạo trang mới **không có** trong cấu trúc `docs/02-wiki-architecture.md`
- Đổi cấu trúc 7 SPACE V4.1 (SYS/GEN/INT/OPS/BOD/TMP/ARC)
- Thêm Type tag ngoài 13 loại V4.1
- Thêm MASTER ngoài danh sách bắt buộc
- Đổi quy tắc trong `skills/` (lưu ý: sẽ conflict khi merge upstream)
- Push branch lên `main`
- Bất cứ điều gì ảnh hưởng nhiều người

---

## 9. Quan hệ với template upstream `saucevn/wko`

Repo này là **fork** của [saucevn/wko](https://github.com/saucevn/wko). Khi:

| Tình huống | Hành xử đúng |
|---|---|
| Upstream có version mới | Pull qua `git fetch upstream && git merge upstream/main`. Xem [docs-meta/UPGRADING.md](docs-meta/UPGRADING.md) |
| Bug trong template | Report tại <https://github.com/saucevn/wko/issues> |
| Cần feature mới generic (mọi công ty đều cần) | PR lên `saucevn/wko` (đóng góp upstream) |
| Cần feature riêng cho `{{ company.short_name }}` | Custom local — không PR lên upstream |
| Conflict khi merge upstream | `company.config.yaml`: giữ local; `skills/*.md`, `docs/*.md`: ưu tiên upstream; `scripts/*.py`: ưu tiên upstream |

**License:** Template `saucevn/wko` là MIT. Fork private của bạn không bắt buộc public, nhưng vẫn phải giữ MIT notice trong file `LICENSE`.

---

## 10. Custom rules (override section)

> Section này **KHÔNG bị overwrite** khi pull upstream. Thêm rule custom của `{{ company.short_name }}` ở đây.

```
(Để trống lúc đầu. Owner thêm khi cần.)
```

---

*Cập nhật: Render từ template `saucevn/wko` — taxonomy V4.1 Execution-First (7 SPACE, 13 TYPE)*
*Template upstream: <https://github.com/saucevn/wko>*
*License: MIT*
