# Phân quyền {{ taxonomy.spaces|length }} SPACE — {{ company.name }}

## Bảng phân quyền

| SPACE | Editor | Viewer | Restricted |
|---|---|---|---|
{% for s in taxonomy.spaces %}| `{{ s.code }}` ({{ s.name }}) | {{ s.owner }} | <!-- TODO --> | <!-- TODO --> |
{% endfor %}

<!-- TODO {{ company.short_name }} owner:
- Editor: ai được sửa nội dung trực tiếp
- Viewer: ai được đọc
- Restricted: ai bị hạn chế truy cập (vd: BOD chỉ BOD, KT chỉ KT)
-->

## Quy tắc gán quyền

### Nguyên tắc

1. **Default deny** — page mới mặc định chỉ Owner + Reviewer xem được
2. **Least privilege** — chỉ cấp quyền tối thiểu cần
3. **Group, không user** — gán theo Lark group, không gán user trực tiếp
4. **Document** — mọi thay đổi quyền log vào BOD-GOV-LOG-001 Decision Log

### Lark group đề xuất

<!-- TODO: tạo Lark group + add member, list ở đây.

Đề xuất:
- @wiki-editor-{{ space.code | lower }}      — editor cho từng space
- @wiki-viewer-all                            — viewer toàn wiki (default cho all employees)
- @wiki-admin                                  — admin (move/archive/permission change)
- @bod-only                                    — restricted BOD content
-->

## Quy trình cấp / thu hồi quyền

### Cấp quyền

1. Yêu cầu qua HR ticket hoặc Lark message tới Wiki Admin
2. Wiki Admin verify với owner space liên quan
3. Add member vào Lark group tương ứng
4. Log vào BOD-GOV-LOG-001

### Thu hồi quyền

1. Khi off-board: HR notify Wiki Admin
2. Remove khỏi tất cả Lark group
3. Re-assign owner/reviewer các page member đang phụ trách
4. Log vào BOD-GOV-LOG-001

## Public sharing

- **KHÔNG share public** page trừ khi BOD approve
- External (vendor, partner) → tạo space riêng + invite cụ thể, không share whole space

## Audit

`scripts/wiki_kpi_report.py` chạy hàng tháng để audit permissions. Bất thường:

- Page có >50 viewer mà owner không nhớ approve
- User có access > 3 SPACE (có thể cần re-evaluate)
- External user còn access sau off-board

## 🔗 Tài liệu liên quan

→ ↑ {{ lark.wiki_root_url | wiki_link("Master Wiki Index") }}
→ [Cơ cấu tổ chức](01-org-structure.md)
→ [Cấu trúc Wiki ({{ taxonomy.spaces|length }} SPACE)](02-wiki-architecture.md)
