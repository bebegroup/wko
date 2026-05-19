# Master Registry — {{ company.name }}

> Mirror của [skills/10-master-registry.md](../skills/10-master-registry.md) — tham chiếu doc cho người không đọc skill.

## {{ master_registry|length }} MASTER bắt buộc

| Mã | Tên | Owner |
|---|---|---|
{% for m in master_registry %}| `{{ m.code }}` | {{ m.name }} | {{ m.owner }} |
{% endfor %}

## MASTER là gì?

MASTER (`MST`) = **luật / dữ liệu gốc nội bộ** mà nhiều SOP/PROC khác derive từ.

Có 2 sub-types:

- **bridge** — derive từ POL external (luật, sàn policy)
- **standalone** — tự công ty định nghĩa (vd MASTER SKU, MASTER ma trận vị trí)

POL ≠ MST. POL chỉ external (luật, sàn, NĐ). Internal là MST. Xem [10-page-types-taxonomy.md](10-page-types-taxonomy.md).

## Quy tắc cốt lõi

1. **Owner duy nhất** mỗi MASTER — không co-owned
2. **Backlink ngược** — MASTER có section "Trang đang dùng MST này", cập nhật mỗi khi SOP/PROC link tới
3. **Cross-section: link, không copy** — KHÔNG copy nội dung MST vào SOP/PROC khác section
4. **Review cadence** — bridge: theo POL + quarterly; standalone: monthly

## Cấu hình master_registry

Sửa trong `company.config.yaml`:

```yaml
master_registry:
  - code: "OPS-NEW-MST-001"     # tuân format [SPACE]-[SECTION]-MST-[NUMBER]
    name: "MASTER tên page"
    owner: "<role name>"
    required: true
```

## MASTER bắt buộc theo space (V{{ taxonomy.version | replace("v", "") }} guide)

Đề xuất tối thiểu mỗi space:

| SPACE | MASTER bắt buộc |
|---|---|
| SYS | Master Registry (chính file này) |
| GEN | (optional) Brand identity, Tone guideline |
| INT-HR | Ma trận vị trí & JD, Quy trình tuyển dụng |
| INT-FIN | Vai trò kế toán, Quy trình lương, Quy trình đóng tháng |
| INT-O3K | Mapping O3K, Cadence O3K, KPI definitions |
| OPS-CS | Chính sách CSKH, Chính sách đổi/trả |
| OPS-WH | Vị trí kho, Quy chuẩn đóng gói |
| OPS-ECM | Quy tắc vận hành kênh, Fee dictionary |
| OPS-INV | Settlement definition, Fee dictionary |
| OPS-PIM | SKU master, Tên sản phẩm chuẩn |
| OPS-MFG | BOM (từng SKU), Tiêu chuẩn QC |
| OPS-MKT | Campaign tiêu chí duyệt, Ads master |
| OPS-LIVE | Luật chơi livestream, Offer/voucher |
| BOD | Ngân sách, Compensation philosophy, Governance |

Tùy nghiệp vụ thực tế, không cần đủ hết.

## Workflow khi MASTER thay đổi

1. Owner update content trên Lark
2. Open section "Trang đang dùng MST này" trong MASTER
3. Notify từng page trong list (qua group Lark)
4. SOP/PROC chỉ update nếu **cách làm** đổi (không phải mọi sửa MST)
5. Log change vào Change Log của MASTER
6. Update Master Index: increment version

## 🔗 Tài liệu liên quan

→ ↑ {{ lark.wiki_root_url | wiki_link("Master Wiki Index") }}
→ [Skill 10 — Master Registry](../skills/10-master-registry.md) — chi tiết quy tắc
→ [Skill 11 — Page Types](../skills/11-page-types.md) — POL vs MST distinction
→ [Page Types Taxonomy](10-page-types-taxonomy.md)
