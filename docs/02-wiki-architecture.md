# Cấu trúc Wiki "{{ company.short_name }} Company OS" (V{{ taxonomy.version | replace("v", "") }})

> Philosophy: **{{ taxonomy.philosophy | default("execution-first") }}** — mở Wiki vào là làm được việc, không phải đọc hiểu.

## 4 tầng

```
Workspace → {{ taxonomy.spaces|length }} SPACE → SECTION → PAGE
```

- **SPACE** ({{ taxonomy.spaces|length }}) — phân loại nghiệp vụ cấp cao nhất
- **SECTION** — sub-domain trong SPACE (vd `OPS-CS`, `INT-HR`)
- **PAGE** — đơn vị nội dung nhỏ nhất, có mã `{{ taxonomy.page_code_format }}`

## {{ taxonomy.spaces|length }} SPACE chi tiết

{% for s in taxonomy.spaces %}
### {{ s.order }}_{{ s.code }} — {{ s.name }} {{ s.icon }}

**Owner cấp space:** {{ s.owner }}
**Mục đích:** {{ s.get("purpose") | default("(chưa điền)") }}
{% if s.get("append_only") %}
> ⚠️ **Append-only** — mã page đã Archived không tái sử dụng.
{% endif %}

#### Sections ({{ taxonomy.sections.get(s.code, []) | length }})

{% if taxonomy.sections.get(s.code) %}
| Code | Tên section |
|---|---|
{% for sec in taxonomy.sections[s.code] %}| `{{ sec.code }}` | {{ sec.name }} |
{% endfor %}
{% else %}
<!-- Chưa cấu hình section cho space {{ s.code }} -->
{% endif %}

---
{% endfor %}

## URL Lark

- **Wiki root:** {{ lark.wiki_root_url | wiki_link("Mở trên Lark") }}
- **Master Index:** `SYS-00-IDX-001` (node `{{ lark.master_index.node_token }}`)
- **Tenant:** `{{ lark.tenant_subdomain }}.{{ lark.region }}.{{ lark.domain }}`

## Quy tắc cấp space

- SYS không chứa nội dung nghiệp vụ — chỉ rules + index
- TMP append-only nếu có pages mới (templates chuẩn)
- ARC chỉ chứa archived pages — không tạo mới trực tiếp

## Quy trình thêm SECTION mới

1. Đề xuất + thảo luận với section owner
2. Cập nhật `taxonomy.sections` trong `company.config.yaml`:
   ```yaml
   taxonomy:
     sections:
       OPS:
         - { code: "OPS-NEW", name: "Tên section mới" }
   ```
3. Re-validate: `python3 scripts/validate_config.py --strict`
4. Tạo HUB-{{ hub_rules.master_hub_number }} cho section mới trên Lark
5. Update Master Index
6. Commit config change

## Quy trình thêm SPACE mới

Hiếm khi cần. Quy trình:

1. RFC discussion trong group `{{ integrations.contributor_group_email }}`
2. Owner approve
3. Update `company.config.yaml` `taxonomy.spaces`
4. Tạo space mới trên Lark
5. Update Master Index headers

⚠️ Đổi cấu trúc SPACE = breaking change cho mọi page hiện hữu. Cẩn thận.

## 🔗 Tài liệu liên quan

→ ↑ {{ lark.wiki_root_url | wiki_link("Master Wiki Index") }}
→ [Phân quyền theo space](03-permissions.md)
→ [Master Registry](09-master-registry.md)
→ [Page Types Taxonomy](10-page-types-taxonomy.md)
→ [Skill 08 — INDEX & Numbering](../skills/08-index-and-numbering.md)
