# Lark Base cần kết nối — {{ company.name }}

## Danh sách Lark Base

{% if lark_bases %}
{{ lark_bases | length }} Lark Base hiện cấu hình trong `company.config.yaml`:

{% for b in lark_bases %}
### {{ b.name }}

- **Token:** `{{ b.base_token }}`
- **Mục đích:** {{ b.purpose }}
{% if b.get("url") %}- **URL:** {{ b.url }}{% endif %}

<!-- TODO: liệt kê các table chính trong Base này -->

{% endfor %}
{% else %}
<!-- TODO {{ company.short_name }} owner: cấu hình lark_bases trong company.config.yaml -->

Format đề xuất:

```yaml
lark_bases:
  - name: "HCNS Database"
    base_token: "bascn..."
    purpose: "Nhân sự, JD, KPI"
  - name: "OKR Tracker"
    base_token: "bascn..."
    purpose: "OKR cycles per quý"
```
{% endif %}

## Lark Base nên có (template gợi ý)

Mỗi công ty nên có ít nhất các Base sau:

| Base | Section liên kết | Mục đích |
|---|---|---|
| HCNS Database | INT-HR | JD, employee directory, performance |
| OKR / O3K Tracker | INT-O3K | Mục tiêu + key results |
| Finance Tracker | INT-FIN | Bookkeeping, settlement |
| Channel Performance | OPS-ECM | Doanh số per kênh |
| SKU / Catalog | OPS-PIM | Master SKU + attributes |
| Inventory | OPS-WH | Tồn kho |
| Customer Support | OPS-CS | Tickets, SLA |

Tùy nghiệp vụ, bổ sung Base khác.

## Quy tắc dùng Lark Base

### Khi nào tạo Base mới

- Dữ liệu structured (rows + columns)
- Cần filter / sort / view khác nhau
- Cần collaborative editing nhiều người
- Cần dashboard tự động từ data

### Khi nào KHÔNG dùng Base

- Document dài (>200 từ free-form) → dùng Wiki page
- Data 1 lần (không update) → file Excel + commit `sources/excel/`
- Data quá lớn (>100k rows) → cân nhắc DB ngoài

### Link từ Wiki vào Base

Trong Wiki page (vd SOP):

```markdown
### Dashboard liên quan
→ 📊 [Tên Base — Tracking](https://...)
```

Hoặc trong section 🔗 Tài liệu liên quan:

```markdown
→ [Lark Base — HCNS Database](https://{{ lark.tenant_subdomain }}.{{ lark.region }}.{{ lark.domain }}/base/<token>)
```

### Backlink Base → Wiki

Trong cell của Base, có thể link tới Wiki page bằng URL hoặc Lark mention.

## Permission

- Editor Base: theo phòng ban owner
- Viewer: all employees mặc định, restricted nếu chứa PII (HR/lương)
- External: tạo Base copy + masked data nếu cần share

## 🔗 Tài liệu liên quan

→ ↑ {{ lark.wiki_root_url | wiki_link("Master Wiki Index") }}
→ [Cấu trúc Wiki](02-wiki-architecture.md)
→ [Phân quyền](03-permissions.md)
→ [Skill 03 — Linking Rules](../skills/03-linking-rules.md) — format link Base ↔ Wiki
