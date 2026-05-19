# Contributing — đóng góp Wiki nội bộ {{ company.short_name }}

> Quy trình cho nhân viên đóng góp Wiki **trên Lark trực tiếp** (KHÔNG qua Git).
> Đóng góp upstream (saucevn/wko template) → xem [CONTRIBUTING.md](../CONTRIBUTING.md).

## Trước khi đóng góp

1. Đã đọc [skills/02-writing-style.md](../skills/02-writing-style.md) — biết title format theo type
2. Đã đọc [skills/01-page-format.md](../skills/01-page-format.md) — biết template chuẩn
3. Đã hiểu [skills/11-page-types.md](../skills/11-page-types.md) — chọn type đúng
4. Đã biết section đích — tra [02-wiki-architecture.md](02-wiki-architecture.md)

## Quy trình 3 bước

### Bước 1: Soạn page

1. Mở Lark Wiki ({{ lark.wiki_root_url }})
2. Tra section đích trên Master Wiki Index
3. Click "Add page" → đặt title theo format `<mã> <tên>`
4. Copy template từ [skills/01](../skills/01-page-format.md) (general/MASTER/HUB)
5. Điền nội dung
6. Đặt status = ⬜ Draft

### Bước 2: Yêu cầu review

Cách 1 — Phase 1 (manual):

- Copy link Lark page
- Gửi vào group `{{ integrations.contributor_group_email }}` với tag "@Reviewer"
- Wait reviewer human

Cách 2 — Phase 2 (bot, khi đã setup):

- Copy link Lark page
- Gửi vào group `{{ integrations.contributor_group_email }}` với mention `{{ integrations.reviewer_bot_name }}`
- Bot tự review trong < 5 phút, post comment + score

### Bước 3: Sửa theo feedback → Active

1. Đọc comment từ reviewer / bot
2. Sửa nội dung trên Lark
3. Yêu cầu re-review (lặp lại Bước 2)
4. Khi pass, reviewer đổi status = 🔄 Active trong Master Index

## Quy tắc

### Title

- Format: `<mã> <tên>` (vd: `OPS-CS-SOP-001 Tiếp nhận yêu cầu`)
- KHÔNG dấu chấm sau mã
- Theo prefix rule per type (xem [skill 02](../skills/02-writing-style.md))

### Mã page

- Tra Master Wiki Index lấy NUMBER kế tiếp
- KHÔNG tự đặt số

### Nội dung

- Không copy nội dung từ Excel — link file (xem [skill 06](../skills/06-excel-to-wiki.md))
- Số liệu phải cụ thể (24h, ngày 26 hàng tháng)
- Tránh từ mơ hồ ("nhanh chóng", "kịp thời")
- ≤ 2 trang A4 (trừ MASTER)

### Backlink

- Mọi page có section "🔗 Tài liệu liên quan" cuối page (xem [skill 03](../skills/03-linking-rules.md))
- Link tới MASTER → MASTER phải có entry "Trang đang dùng" ngược lại

### Status

- Mới tạo: ⬜ Draft
- Sau review: 🔄 Active
- Không dùng: 📋 Deprecated → ✅ Archived sau 30 ngày
- Chi tiết: [skill 04](../skills/04-page-status.md)

## Khi nào cần hỏi owner trước

- Tạo section mới chưa có trong [02-wiki-architecture.md](02-wiki-architecture.md)
- Đổi cấu trúc {{ taxonomy.spaces|length }} SPACE
- Thêm MASTER ngoài [09-master-registry.md](09-master-registry.md)
- Đổi quy tắc trong skills/

Owner per space:

{% for s in taxonomy.spaces %}
- **{{ s.code }}** → {{ s.owner }}
{% endfor %}

## Đóng góp template (upstream wko)

Nếu bạn phát hiện bug hoặc muốn thêm feature **cho template chính** (không phải nội bộ {{ company.short_name }}):

1. Xem [CONTRIBUTING.md](../CONTRIBUTING.md)
2. PR upstream: https://github.com/saucevn/wko

## 🔗 Tài liệu liên quan

→ ↑ {{ lark.wiki_root_url | wiki_link("Master Wiki Index") }}
→ [Skill 09 — Workflow contributing](../skills/09-contributing-workflow.md) — chi tiết Phase 1/2 bot
→ [Cấu trúc Wiki](02-wiki-architecture.md)
→ [CONTRIBUTING (upstream)](../CONTRIBUTING.md) — đóng góp template
