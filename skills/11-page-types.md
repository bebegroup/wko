# Skill 11 — Taxonomy {{ taxonomy.page_types|length }} loại page (V{{ taxonomy.version | replace("v", "") }})

V{{ taxonomy.version | replace("v", "") }} Execution-First định nghĩa {{ taxonomy.page_types|length }} type page. Mỗi page Wiki phải thuộc 1 type duy nhất.

## Triết lý: Execution-First

> Wiki không phải thư viện đọc hiểu. Là **hệ thống thực thi công việc**.

Mỗi page phải trả lời ≥ 1 câu hỏi thực thi:

{% for q in execution_first.page_purpose_questions %}
{{ loop.index }}. {{ q }}
{% endfor %}

Nếu page chỉ trả lời "cái này là gì" → cân nhắc xem có cần thiết không.

## {{ taxonomy.page_types|length }} type

{% for t in taxonomy.page_types %}
### {{ t.code }} — {{ t.name }}

{% if t.question %}**Câu hỏi thực thi:** _{{ t.question }}_{% endif %}

{% if t.scope %}**Scope:** `{{ t.scope }}`{% endif %}

{% if t.sub_types %}**Sub-types:** {{ t.sub_types | join(", ") }}{% endif %}

{% if t.condition %}**Điều kiện tạo:** {{ t.condition }}{% endif %}

{% if t.mandatory_per_section %}> ⚠️ **Bắt buộc** mỗi section có 1 {{ t.code }}.{% endif %}

{% if t.requires_real_data %}> ⚠️ Chỉ tạo khi có **source số liệu thật**.{% endif %}

{% if t.new_in_v41 %}> 🆕 **Mới trong V{{ taxonomy.version | replace("v", "") }}**{% endif %}

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

## Rejection rules — KHÔNG tạo page nếu

{% for r in execution_first.rejection_rules %}
- {{ r }}
{% endfor %}

## Phân biệt POL vs MST (V{{ taxonomy.version | replace("v", "") }})

| Aspect | POL | MST |
|---|---|---|
| **Scope** | External only (luật, sàn policy, NĐ) | Internal (nội bộ công ty áp dụng) |
| **Sửa được không** | KHÔNG (chỉ source bên ngoài sửa) | CÓ (công ty tự sửa) |
| **Sub-types** | (không) | bridge (derive từ POL) / standalone |
| **Mục bắt buộc** | {{ pol_mst_rules.pol_required_sections | default(8) }} mục | {{ pol_mst_rules.mst_bridge_required_sections | default(5) }} mục (bridge) |
| **Primary owner** | 1 section duy nhất (xem bảng) | Section nội bộ phụ trách |

### Primary owner table cho POL

| External Policy | Section primary owner |
|---|---|
{% for policy, section in pol_mst_rules.primary_owner_table.items() %}| {{ policy }} | `{{ section }}` |
{% endfor %}

### Workflow khi POL thay đổi

1. Update POL gốc (nội dung + ngày hiệu lực + Change Log)
2. Mở mục "Trang đang sử dụng" trong POL
3. Update từng MST bridge có trong list
4. SOP chỉ sửa nếu CÁCH LÀM thay đổi (không phải chỉ số đổi)

## HUB rules (V{{ taxonomy.version | replace("v", "") }})

HUB-{{ hub_rules.master_hub_number }} = **Master entry** của section (sticky, KHÔNG đổi mã).

HUB-002+ = nhánh, tạo khi:
- Section có ≥ {{ hub_rules.branch_hub_min_pages }} page con thuộc cùng nhánh
- Có owner / use-case khác nhau

### 4 Branch patterns

{% for p in hub_rules.branch_patterns %}
**{{ p.name }}**: {{ p.example }}
{% endfor %}

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
| Sai do không hiểu thuật ngữ | DIC (hiếm) |
| Sai do tone / cách ứng xử / style | GDL |
| Không nhìn được số để quản trị | DBD (chỉ khi có số thật) |
| Cần ghi nhận lịch sử quyết định | LOG |
| Cần điều hướng section | HUB |
| Cần index tổng | IDX |

## 🔗 Tài liệu liên quan

→ ↑ {{ lark.wiki_root_url | wiki_link("Master Wiki Index") }} — canonical
→ [Skill 01 — Page Format](01-page-format.md) — template cho từng type
→ [Skill 02 — Writing Style](02-writing-style.md) — format title `<mã> <tên>` theo type
→ [Skill 08 — INDEX & Numbering](08-index-and-numbering.md) — V{{ taxonomy.version | replace("v", "") }} code format
→ [Skill 10 — Master Registry](10-master-registry.md) — MASTER bắt buộc
→ [docs/10 — Page Types Taxonomy](../docs/10-page-types-taxonomy.md) — mirror doc
