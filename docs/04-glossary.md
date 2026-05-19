# Thuật ngữ & viết tắt — {{ company.name }}

## A. Wiki Operating System (chung mọi công ty)

| Thuật ngữ | Nghĩa |
|---|---|
| **SPACE** | Cấp 1 phân loại nghiệp vụ ({{ taxonomy.spaces|length }} space trong {{ company.short_name }}) |
| **SECTION** | Cấp 2, sub-domain trong SPACE |
| **TYPE** | Cấp 3, loại page ({{ taxonomy.page_types|length }} type V{{ taxonomy.version | replace("v", "") }}) |
| **HUB** | Page điều hướng (menu) của section, KHÔNG chứa nội dung thực |
| **MST** | Master — luật/dữ liệu gốc nội bộ. Có sub-types: bridge (derive từ POL) và standalone |
| **POL** | Policy — luật/policy NGOÀI ban hành (sàn, luật, NĐ). Internal là MST, không phải POL |
| **PROC** | Process — luồng đa vai trò có bàn giao (V{{ taxonomy.version | replace("v", "") }} mới) |
| **SOP** | Standard Operating Procedure — thao tác tuyến tính cho 1 vai trò |
| **CHK** | Checklist — kiểm tra "đã làm đủ chưa" |
| **TMP** | Template — mẫu để điền |
| **PBK** | Playbook — xử lý sự cố/ngoại lệ |
| **DBD** | Dashboard — chỉ tạo khi có source số liệu thật |
| **DIC** | Dictionary — thuật ngữ, chỉ tạo khi thuật ngữ gây sai thao tác |
| **GDL** | Guideline — luật mềm (V{{ taxonomy.version | replace("v", "") }} mới) |
| **LOG** | Log — nhật ký quyết định hoặc sự kiện |
| **IDX** | Index — tổng quan / table of contents |
| **Hub Parent** | Field trong Master Index, page phải có parent HUB rõ ràng (V{{ taxonomy.version | replace("v", "") }}) |

## B. Wiki workflow

| Thuật ngữ | Nghĩa |
|---|---|
| **Master Wiki Index** | Source of truth canonical về mọi page Wiki. Trên Lark, mã `SYS-00-IDX-001` |
| **Source Type** | Internal / External / Derived / Manual (V{{ taxonomy.version | replace("v", "") }} field) |
| **Effective Date** | Ngày policy/luật/quy trình có hiệu lực (V{{ taxonomy.version | replace("v", "") }} field) |
| **Review Cadence** | Chu kỳ review: monthly / quarterly / yearly / ad-hoc (V{{ taxonomy.version | replace("v", "") }} field) |
| **Impacted Pages** | Pages chịu ảnh hưởng khi nội dung MASTER/POL thay đổi (V{{ taxonomy.version | replace("v", "") }} field) |
| **Backlink chiều ngược** | Khi A link tới B, B phải có entry ngược "Trang đang dùng" |
| **Render** | Process: source `.md` (với Jinja2 placeholder) → `dist/` (substitute từ config) |

## C. Lark concepts

| Thuật ngữ | Nghĩa |
|---|---|
| **Lark Wiki** | Wiki app trong Lark workspace, root của Company OS |
| **Lark Base** | Spreadsheet-database hybrid, dùng cho data structured (HR, KPI, ...) |
| **Lark Docs** | Document app, dùng cho page có rich formatting |
| **node_token** | ID của node trong wiki tree (tham chiếu vị trí) |
| **obj_token** | ID của document object (tham chiếu nội dung) |
| **lark-cli** | CLI tool — bắt buộc cho repo này, mọi script gọi qua subprocess |

## D. Trạng thái page

| Trạng thái | Ý nghĩa |
|---|---|
{% for s in policies.page_status_values %}| {{ s }} | <!-- xem skill 04 cho chi tiết --> |
{% endfor %}

## E. Thuật ngữ nội bộ {{ company.short_name }}

<!-- TODO {{ company.short_name }} owner: thêm thuật ngữ riêng của công ty.

Format đề xuất:
| Thuật ngữ | Nghĩa |
|---|---|
| **<viết tắt>** | <giải thích đầy đủ> |

Ví dụ:
| **eNPS** | Employee Net Promoter Score — đo hài lòng nhân viên |
| **BOM** | Bill of Materials — danh mục nguyên vật liệu cấu thành SKU |
-->

## F. Phòng ban viết tắt

| Code | Tên đầy đủ |
|---|---|
{% for d in org.departments %}| `{{ d.code }}` | {{ d.name }} |
{% endfor %}

## 🔗 Tài liệu liên quan

→ ↑ {{ lark.wiki_root_url | wiki_link("Master Wiki Index") }}
→ [Page Types Taxonomy](10-page-types-taxonomy.md) — {{ taxonomy.page_types|length }} type chi tiết
→ [Cơ cấu tổ chức](01-org-structure.md)
→ [Skill 02 — Writing Style](../skills/02-writing-style.md) — quy tắc dùng thuật ngữ
