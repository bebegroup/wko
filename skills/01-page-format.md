# Skill 01 — Format chuẩn mỗi trang Wiki (V{{ taxonomy.version | replace("v", "") }})

V{{ taxonomy.version | replace("v", "") }} có **3 loại template** ứng với 3 loại page:

- **General template** — cho SOP, PROC, CHK, TMP, PBK, DBD, DIC, GDL, LOG, POL
- **MASTER template** — cho MST (riêng vì derive logic)
- **HUB template** — cho HUB (page điều hướng, KHÔNG chứa content)

## 1. Mã page

Format: `{{ taxonomy.page_code_format }}`

Thành phần:

- **SPACE** — 1 trong {{ taxonomy.spaces|length }} space: {% for s in taxonomy.spaces %}`{{ s.code }}`{% if not loop.last %}, {% endif %}{% endfor %}
- **SECTION** — phần sau dấu `-` của section.code (vd `OPS-CS` → `CS`)
- **TYPE** — 1 trong {{ taxonomy.page_types|length }} type: {% for t in taxonomy.page_types %}`{{ t.code }}`{% if not loop.last %}, {% endif %}{% endfor %}
- **NUMBER** — 3 chữ số (001, 002, ...), append-only theo Master Index

### Ví dụ

```
SYS-00-IDX-001      Master Wiki Index
OPS-CS-HUB-001      CSKH — Tổng quan (HUB Master)
OPS-CS-PROC-001     Luồng xử lý khách hàng từ inbox đến đóng ticket
OPS-CS-SOP-001      Tiếp nhận và phân loại yêu cầu
OPS-CS-CHK-001      Checklist trước khi đóng ticket
OPS-CS-PBK-001      Khách tức giận / escalation
```

## 2. Trạng thái

{% for s in policies.page_status_values %}- {{ s }}
{% endfor %}

Default cho page mới: **{{ policies.default_status }}**

Chi tiết: [skill 04](04-page-status.md).

## 3. Template — General page (SOP, PROC, CHK, TMP, PBK, DBD, ...)

```markdown
# {{ '{{' }} space }}-{{ '{{' }} section }}-{{ '{{' }} type }}-{{ '{{' }} number }} {{ '{{' }} title }}

Loại tài liệu: {{ '{{' }} type }}
Owner: {{ '{{' }} owner_role }}
Backup Owner: {{ '{{' }} backup_owner }}
Reviewer: {{ '{{' }} reviewer_role }}
Hub Parent: {{ '{{' }} hub_code }}                    <!-- V{{ taxonomy.version | replace("v", "") }} bắt buộc -->
Status: {{ policies.default_status }}
Version: v0.1
Last updated: __/2026
Next review: __/__/2026
Mức bảo mật: Internal

---

## 1. TL;DR
1-2 câu mô tả page làm gì.

## 2. Khi nào dùng
Trigger cụ thể — khi nào member cần mở page này.

## 3. Đối tượng
Vai trò nào liên quan (Owner, executor, reviewer, ...).

## 4. Input cần có
- Danh sách input
- Format / nguồn

## 5. Output bắt buộc
- Danh sách deliverable
- Định nghĩa "done"

## 6. SLA / Deadline
- Số cụ thể: 24h, 3 ngày, ngày 26 hàng tháng, ...

## 7. Tools dùng
- Lark Base, MISA, Excel, ...

## 8. Hướng dẫn chi tiết từng bước

### Bước 1: ...
- **Tool:** ...
- **Input:** ...
- **Output:** ...
- **Chuẩn đúng:** ...

### Bước 2: ...
...

## 9. Lỗi thường gặp & cách xử lý
| Lỗi | Triệu chứng | Cách xử lý |
|---|---|---|
| ... | ... | ... |

## 10. Cảnh báo & lưu ý

> ⚠️ Cảnh báo nghiêm trọng.

## 11. Link hệ thống

### MASTER liên quan
→ [[{{ '{{' }} space }}-{{ '{{' }} section }}-MST-{{ '{{' }} num }}]] MASTER ...

### Template/Form
→ 📥 [...](sources/excel/...xlsx) — file template

### Dashboard liên quan
→ [[{{ '{{' }} space }}-{{ '{{' }} section }}-DBD-{{ '{{' }} num }}]] Dashboard ...

### Trang điều hướng
→ ↑ [[{{ '{{' }} hub_code }}]] Hub Parent
→ ↑ {{ lark.wiki_root_url | wiki_link("Master Wiki Index") }}

## 12. Change Log
| Version | Ngày | Người sửa | Thay đổi |
|---|---|---|---|
| v0.1 | __/2026 | __ | Tạo mới |
```

## 4. Template — MASTER page (MST)

MST có 2 sub-types:

- **bridge** — derive từ POL external (vd "Nội quy lao động" derive từ "Luật LĐ")
- **standalone** — tự công ty định nghĩa (vd "MASTER SKU List")

### MST bridge — 5 mục bắt buộc

```markdown
# {{ '{{' }} space }}-{{ '{{' }} section }}-MST-{{ '{{' }} number }} MASTER {{ '{{' }} title }}

Sub-type: bridge
Derive từ: [[{{ '{{' }} pol_code }}]]
Owner: {{ '{{' }} owner_role }}
Reviewer: {{ '{{' }} reviewer_role }}
Status: {{ policies.default_status }}
Version: v0.1

---

## 1. Căn cứ pháp lý                  <!-- BẮT BUỘC, link POL nguồn -->
→ [[{{ '{{' }} pol_code_1 }}]] {{ '{{' }} pol_name_1 }}
→ [[{{ '{{' }} pol_code_2 }}]] {{ '{{' }} pol_name_2 }} (nếu nhiều)

## 2. Quy tắc nội bộ derive            <!-- nội dung công ty áp dụng -->
...

## 3. Chế tài vi phạm (nếu có)
...

## 4. Trang đang dùng MST này          <!-- backlink ngược -->
- [[OPS-CS-SOP-001]] - dùng để xử lý ...
- ...

## 5. Owner + Reviewer + Review cadence
Owner: ...
Reviewer: ...
Review cadence: hàng quý
```

### MST standalone — 3 mục bắt buộc

Bỏ mục 1 + 3 (không có căn cứ pháp lý + chế tài). Chỉ có:

```markdown
## 1. Quy tắc nội bộ
## 2. Trang đang dùng MST này
## 3. Owner + Reviewer + Review cadence
```

## 5. Template — HUB page (điều hướng, KHÔNG content)

```markdown
# {{ '{{' }} space }}-{{ '{{' }} section }}-HUB-{{ hub_rules.master_hub_number }} {{ '{{' }} section_name }} — Tổng quan

Owner: {{ '{{' }} section_owner }}
Status: {{ policies.default_status }}

> HUB-{{ hub_rules.master_hub_number }} là Master entry sticky. Không đổi mã.

## Danh mục page trong section

### MASTER
- [[{{ '{{' }} space }}-{{ '{{' }} section }}-MST-001]] ...

### Process (luồng đa vai trò)
- [[{{ '{{' }} space }}-{{ '{{' }} section }}-PROC-001]] ...

### SOP
- [[{{ '{{' }} space }}-{{ '{{' }} section }}-SOP-001]] ...
- [[{{ '{{' }} space }}-{{ '{{' }} section }}-SOP-002]] ...

### Checklist
- [[{{ '{{' }} space }}-{{ '{{' }} section }}-CHK-001]] ...

### Template
- [[{{ '{{' }} space }}-{{ '{{' }} section }}-TMP-001]] ...

### Playbook (sự cố)
- [[{{ '{{' }} space }}-{{ '{{' }} section }}-PBK-001]] ...

### Dashboard (nếu có)
- [[{{ '{{' }} space }}-{{ '{{' }} section }}-DBD-001]] ...

## Hub nhánh (nếu section đa nhánh)

{{ '{{' }} optional - khi section có pattern A/B/C/D, list HUB nhánh ở đây }}

## Link
→ ↑ {{ lark.wiki_root_url | wiki_link("Master Wiki Index") }}
```

## 6. Section bắt buộc cuối mọi page

```markdown
## 🔗 Tài liệu liên quan

→ ↑ [[{{ '{{' }} hub_parent_code }}]] Hub Parent
→ ↑ {{ lark.wiki_root_url | wiki_link("Master Wiki Index") }}
→ <link liên quan>
```

## 7. Title H1 format

Xem [skill 02 §1](02-writing-style.md) cho rules theo type.

Tóm tắt:

| Type | Title format |
|---|---|
| HUB | `<mã> <Tên section> — Tổng quan` |
| MST | `<mã> MASTER <tên>` |
| SOP | `<mã> <Động từ chỉ thao tác>` (vd: "Xử lý...", "Tiếp nhận...") |
| PROC | `<mã> Luồng <từ X đến Y>` |
| CHK | `<mã> Checklist <chủ đề>` |
| TMP | `<mã> Template <tên>` |
| PBK | `<mã> <Tình huống>` (vd: "Livestream bùng đơn") |
| DBD | `<mã> Dashboard <tên>` |
| DIC | `<mã> <Tên thuật ngữ>` |
| POL | `<mã> <Tên policy ngoài>` |
| GDL | `<mã> <Tên guideline>` |
| LOG | `<mã> <Tên log>` |
| IDX | `<mã> <Tên index>` |

## 🔗 Tài liệu liên quan

→ ↑ {{ lark.wiki_root_url | wiki_link("Master Wiki Index") }}
→ [Skill 02 — Writing Style](02-writing-style.md) — title rules + nội dung
→ [Skill 04 — Page Status](04-page-status.md) — 4 trạng thái Draft/Active/Deprecated/Archived
→ [Skill 08 — INDEX & Numbering](08-index-and-numbering.md) — V{{ taxonomy.version | replace("v", "") }} code format
→ [Skill 11 — Page Types](11-page-types.md) — {{ taxonomy.page_types|length }} type
