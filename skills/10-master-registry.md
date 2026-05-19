# Skill 10 — Master Registry

## {{ master_registry|length }} MASTER bắt buộc

Mỗi công ty cấu hình MASTER bắt buộc theo nghiệp vụ trong `company.config.yaml` field `master_registry`.

| Mã | Tên | Owner |
|---|---|---|
{% for m in master_registry %}| `{{ m.code }}` | {{ m.name }} | {{ m.owner }} |
{% endfor %}

## Quy tắc MASTER

### 1. Owner duy nhất

Mỗi MASTER có **1 owner** chịu trách nhiệm chính. KHÔNG co-owned.

Reviewer có thể khác nhưng owner phải rõ.

### 2. MST có 2 sub-types

- **bridge** — derive từ POL external (vd "Nội quy lao động" derive từ "Luật LĐ")
- **standalone** — tự công ty định nghĩa (vd "MASTER SKU List", "MASTER ma trận vị trí")

Chi tiết phân biệt + workflow khi POL thay đổi: xem [skill 11 §POL vs MST](11-page-types.md).

### 3. Mục bắt buộc

**MST bridge ({{ pol_mst_rules.mst_bridge_required_sections | default(5) }} mục):**

```
1. Căn cứ pháp lý           <-- link POL nguồn
2. Quy tắc nội bộ derive    <-- nội dung công ty áp dụng
3. Chế tài vi phạm (nếu có)
4. Trang đang dùng MST này  <-- backlink ngược, cập nhật mỗi khi SOP/PROC link tới
5. Owner + Reviewer + Review cadence
```

**MST standalone (3 mục):** bỏ mục 1 + 3, chỉ có 2 + 4 + 5.

### 4. Backlink ngược — "Trang đang dùng MST này"

Khi 1 SOP/PROC link tới MASTER:

- SOP/PROC: link forward `[[<MST-code>]]` trong section "MASTER liên quan"
- MASTER: thêm reverse entry `[[<SOP-code>]] - dùng để ...` trong section "Trang đang dùng MST này"

Khi MASTER thay đổi nội dung:

- Mở "Trang đang dùng MST này"
- Notify từng page trong list (qua group Lark)
- SOP chỉ cần update nếu **cách làm** đổi, không phải mọi thay đổi MST

### 5. Cross-section rule

> {{ pol_mst_rules.cross_section_rule | default("link, không copy") }}

KHÔNG copy nội dung MASTER vào SOP/PROC khác. Chỉ link.

Lý do: khi MASTER đổi, chỉ cần update 1 chỗ.

### 6. Review cadence

| Loại MASTER | Cadence |
|---|---|
| MST bridge (derive từ POL) | Khi POL thay đổi + hàng quý |
| MST standalone (SKU, JD, etc.) | Hàng tháng |
| MST quan trọng (lương, BOM) | Khi có thay đổi + hàng tháng |
| MASTER catalog/data | Khi data đổi |

### 7. MASTER bắt buộc theo space

Mỗi space nên có ít nhất 1 MASTER chính:

{% for s in taxonomy.spaces %}
{% if s.code != "ARC" and s.code != "TMP" %}
- **{{ s.code }}** — MASTER {{ s.purpose | default("...") }}
{% endif %}
{% endfor %}

Hiện trong `master_registry` đã cấu hình:

{% for m in master_registry %}- `{{ m.code }}` ({{ m.name }})
{% endfor %}

## Thêm MASTER mới vào registry

1. Xác định nhu cầu nghiệp vụ (tránh tạo MASTER chỉ vì "nên có")
2. Tra Master Index lấy mã (theo [skill 08](08-index-and-numbering.md))
3. Thêm row mới vào `company.config.yaml` `master_registry`:

```yaml
master_registry:
  - code: "OPS-NEW-MST-001"
    name: "MASTER mới"
    owner: "<role>"
    required: true
```

4. Re-render: `python3 scripts/render.py`
5. Re-validate: `python3 scripts/validate_config.py --strict`
6. Tạo page trên Lark theo [skill 05](05-publish-workflow.md)

## Xóa MASTER khỏi registry

KHÔNG xóa thẳng. Quy trình:

1. Mark MST status = 📋 Deprecated trong Master Index
2. Notify "Trang đang dùng MST này"
3. Sau 30 ngày → Archived
4. Remove khỏi `master_registry` trong config
5. Re-render

## 🔗 Tài liệu liên quan

→ ↑ {{ lark.wiki_root_url | wiki_link("Master Wiki Index") }}
→ [Skill 01 — Page Format](01-page-format.md) — MST template (bridge vs standalone)
→ [Skill 03 — Linking Rules](03-linking-rules.md) — backlink ngược
→ [Skill 11 — Page Types](11-page-types.md) — POL vs MST distinction
→ [docs/09 — Master Registry](../docs/09-master-registry.md) — mirror doc
