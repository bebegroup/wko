# Page Types Taxonomy — V{{ taxonomy.version | replace("v", "") }}

> Mirror của [skills/11-page-types.md](../skills/11-page-types.md) cho người không đọc skill files.

## Triết lý: Execution-First

Wiki không phải thư viện đọc hiểu. Là **hệ thống thực thi**.

Mỗi page phải trả lời ≥ 1 câu hỏi thực thi:

{% for q in execution_first.page_purpose_questions %}
{{ loop.index }}. {{ q }}
{% endfor %}

## {{ taxonomy.page_types|length }} loại page

| Code | Tên | Câu hỏi thực thi | Đặc điểm |
|---|---|---|---|
{% for t in taxonomy.page_types %}| `{{ t.code }}` | {{ t.name }} | {{ t.get("question") | default("—") }} | {% if t.get("new_in_v41") %}🆕 V{{ taxonomy.version | replace("v", "") }} mới · {% endif %}{% if t.get("scope") %}scope: `{{ t.scope }}` · {% endif %}{% if t.get("mandatory_per_section") %}bắt buộc per section · {% endif %}{% if t.get("requires_real_data") %}cần data thật · {% endif %} |
{% endfor %}

## Công thức section (Execution-First)

Mỗi section nên có:

**Required:**
{% for r in execution_first.section_formula.required %}
- {{ r }}
{% endfor %}

**Optional (khi cần):**
{% for r in execution_first.section_formula.optional_when_needed %}
- {{ r }}
{% endfor %}

## KHÔNG tạo page nếu

{% for r in execution_first.rejection_rules %}
- {{ r }}
{% endfor %}

## POL vs MST (V{{ taxonomy.version | replace("v", "") }})

| Aspect | POL | MST |
|---|---|---|
| **Scope** | External ({{ pol_mst_rules.pol_scope }}) | Internal |
| **Owner** | 1 section primary (xem bảng dưới) | Section nội bộ |
| **Sửa được không** | KHÔNG (source ngoài sửa) | CÓ |
| **Sub-types** | (không) | bridge / standalone |
| **Required sections** | {{ pol_mst_rules.pol_required_sections }} mục | {{ pol_mst_rules.mst_bridge_required_sections }} mục bridge |
| **Cross-section** | {{ pol_mst_rules.cross_section_rule }} | {{ pol_mst_rules.cross_section_rule }} |

### POL primary owner table

| External Policy | Section primary owner |
|---|---|
{% for policy, section in pol_mst_rules.primary_owner_table.items() %}| {{ policy }} | `{{ section }}` |
{% endfor %}

## HUB rules (V{{ taxonomy.version | replace("v", "") }})

- **HUB-{{ hub_rules.master_hub_number }}** = Master entry sticky (không đổi mã)
- **HUB-002+** = nhánh, tạo khi có ≥ {{ hub_rules.branch_hub_min_pages }} page con
- **Hub Parent** required cho mọi page

### 4 Branch patterns

| Pattern | Khi dùng |
|---|---|
{% for p in hub_rules.branch_patterns %}| {{ p.name }} | {{ p.example }} |
{% endfor %}

## Workflow chọn type

```
1. Page này giúp AI làm việc GÌ?
   → tham khảo execution-first questions ở trên

2. Nội dung là gì?
   → tham khảo bảng "Khi nào dùng type nào"

3. Có vi phạm rejection rule không?
   → nếu có → KHÔNG tạo page
```

## Khi nào dùng type nào — Quick reference

| Vấn đề thực tế | Type |
|---|---|
| Sai / thiếu luật gốc nội bộ | MST |
| Chính sách bên ngoài thay đổi | POL (external only) |
| Chưa có luồng "ai làm trước sau" | PROC |
| Nhân viên không biết từng bước làm | SOP |
| Hay quên bước kiểm tra | CHK |
| Thiếu mẫu để điền / gửi / báo cáo | TMP |
| Có ngoại lệ, lỗi, tình huống rẽ nhánh | PBK |
| Sai do không hiểu thuật ngữ (hiếm) | DIC |
| Sai do tone / cách ứng xử / style | GDL |
| Không nhìn được số (cần data thật) | DBD |
| Cần ghi nhận lịch sử quyết định | LOG |
| Cần điều hướng section | HUB |
| Cần index tổng | IDX |

## 🔗 Tài liệu liên quan

→ ↑ {{ lark.wiki_root_url | wiki_link("Master Wiki Index") }}
→ [Skill 11 — Page Types](../skills/11-page-types.md) — chi tiết từng type
→ [Skill 01 — Page Format](../skills/01-page-format.md) — template per type
→ [Master Registry](09-master-registry.md)
→ [Cấu trúc Wiki](02-wiki-architecture.md)
