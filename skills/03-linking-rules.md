# Skill 03 — Quy tắc liên kết (V{{ taxonomy.version | replace("v", "") }})

3 loại link cần biết: **internal Wiki**, **Lark Base**, **backlink chiều ngược**.

## 1. Link nội bộ Wiki — `[[mã page]]`

Trong văn bản, dùng format `[[mã]]`:

```markdown
Khi xử lý khiếu nại, follow [[OPS-CS-SOP-001]].
Tham chiếu MASTER chính sách: [[OPS-CS-MST-002]].
```

Build script `scripts/build_backlink_graph.py` parse `[[...]]` → tạo backlink graph.

### Khi link tới page khác section/space

Vẫn dùng format `[[mã]]` — không cần prefix section:

```
[[INT-HR-MST-001]]   ✅ link tới MASTER HR từ bất kỳ đâu
[[OPS-CS-PROC-001]]  ✅ link tới PROC CS
```

### Khi link kèm anchor (deep link)

```markdown
Xem [[OPS-CS-SOP-001#bước-3-xử-lý-lệch]] cho bước cụ thể.
```

## 2. Link tới URL Lark thực tế

Khi cần URL HTTP (vd cho Lark Base, Doc bên ngoài Wiki):

```markdown
[Lark Base — Tracking đơn](https://{{ lark.tenant_subdomain }}.{{ lark.region }}.{{ lark.domain }}/base/{{ "{{ base_token }}" }})
```

URL Wiki root: `{{ lark.wiki_root_url }}`

### Lark Base list

{% if lark_bases %}
{% for b in lark_bases %}
- **{{ b.name }}** — `{{ b.base_token }}` — {{ b.purpose }}
{% endfor %}
{% else %}
<!-- TODO: điền lark_bases trong company.config.yaml -->
{% endif %}

## 3. Backlink chiều ngược

Mỗi page **MUST** có section `## 🔗 Tài liệu liên quan` cuối page với 4 loại link:

```markdown
## 🔗 Tài liệu liên quan

### MASTER liên quan
→ [[OPS-CS-MST-001]] MASTER tên page

### Template/Form
→ [[TMP-GEN-TMP-001]] Template họp nội bộ

### Dashboard liên quan
→ [[OPS-INV-DBD-001]] Dashboard Settlement

### Trang điều hướng
→ ↑ [[OPS-CS-HUB-001]] CSKH — Tổng quan         <!-- Hub Parent -->
→ ↑ {{ lark.wiki_root_url | wiki_link("Master Wiki Index") }}
```

**Quy tắc backlink:**

1. Mọi MASTER được link bởi SOP/PROC phải có entry "Trang đang dùng" (V4.1 — xem [skill 10](10-master-registry.md))
2. Mọi POL (external) phải có entry "Trang đang sử dụng policy này" (V4.1)
3. Khi đổi MASTER content → notify all "Impacted Pages" trong Master Index
4. Khi archive page → update backlink ngược ở các page link tới

## 4. Format link 4 loại — Symbols

| Symbol | Loại | Khi nào |
|---|---|---|
| `→` | Forward link | Page hiện tại link đi |
| `← ` | Reverse link | Page khác link đến |
| `↑` | Hub parent | Page con link lên hub |
| `📊` | Dashboard | DBD page |
| `📥` | Download | File Excel, PDF |

## 5. Hub Parent (V4.1)

Mọi page MUST có **Hub Parent** trong Master Index. Quy tắc:

- Page là source of truth chung (Pattern B): Hub Parent = HUB-001 Master
- Page thuộc 1 nhánh (Pattern A/C/D): Hub Parent = HUB nhánh tương ứng
- Page cross-nhánh trong section: Hub Parent = HUB-001 Master

Xem [skill 08 §HUB Rules](08-index-and-numbering.md) cho 4 pattern phân nhánh.

## 6. Cross-section link

Khi page thuộc section A nhưng reference section B:

```markdown
Theo policy sàn TikTok ([[OPS-ECM-POL-001]]), khi đối soát bị lệch...
```

**KHÔNG copy nội dung policy. Chỉ link.** Lý do: khi POL thay đổi, chỉ cần update 1 chỗ.

## 7. External link

```markdown
- [Lark Developer Console](https://open.larksuite.com)
- [Anthropic API docs](https://docs.anthropic.com)
```

Đặt URL trực tiếp, không qua `[[...]]`.

## 🔗 Tài liệu liên quan

→ ↑ {{ lark.wiki_root_url | wiki_link("Master Wiki Index") }} — canonical
→ [Skill 01 — Page Format](01-page-format.md) — section 🔗 cuối page
→ [Skill 02 — Writing Style](02-writing-style.md) — format `[[mã]]` trong văn bản
→ [Skill 08 — INDEX & Numbering](08-index-and-numbering.md) — V{{ taxonomy.version | replace("v", "") }} HUB rules
→ [Skill 10 — Master Registry](10-master-registry.md) — backlink cho MASTER
→ [scripts/build_backlink_graph.py](../scripts/build_backlink_graph.py) — auto-gen backlink graph
