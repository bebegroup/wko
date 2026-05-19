# {{ company.name }} là ai?

<!-- TODO {{ company.short_name }} owner: điền nội dung mô tả công ty theo template dưới -->

## Tổng quan

- **Tên đầy đủ:** {{ company.legal_entities | join(", ") }}
- **Ngành:** {{ company.industry }}
- **Năm thành lập:** {{ company.get("founded_year") | default("(chưa điền)") }}
- **HQ:** {{ company.hq_country }}

## Sản phẩm / dịch vụ

<!-- TODO: list sản phẩm/dịch vụ chính. Format đề xuất:

| Tên | Mô tả ngắn | Kênh phân phối |
|---|---|---|
| Product A | ... | Online / Offline |

-->

## Sứ mệnh

<!-- TODO: 1-2 câu sứ mệnh công ty -->

## Tầm nhìn

<!-- TODO: 1-2 câu tầm nhìn 3-5 năm -->

## Giá trị cốt lõi

<!-- TODO: 3-5 giá trị, mỗi giá trị 1-2 câu giải thích.

Ví dụ:
1. **Khách hàng là trung tâm** — mọi quyết định bắt đầu từ giá trị khách nhận được
2. **Học liên tục** — sai để học, không sợ thử
3. **Minh bạch** — quyết định public, data accessible

-->

## Kênh bán / phân phối

<!-- TODO:
- Kênh online (TikTok Shop, Shopee, Lazada, Web, FB, ...)
- Kênh offline (showroom, distributor, ...)
- Tỷ trọng doanh thu mỗi kênh
-->

## Khách hàng mục tiêu

<!-- TODO:
- Segment chính: demographic, behavior
- Use case chính
-->

## Lịch sử & cột mốc

<!-- TODO: timeline ngắn các mốc quan trọng -->

## Cấu trúc pháp lý

{% if company.legal_entities | length > 1 %}
Công ty có {{ company.legal_entities | length }} pháp nhân:
{% for e in company.legal_entities %}- {{ e }}
{% endfor %}
<!-- TODO: giải thích chức năng từng pháp nhân -->
{% else %}
1 pháp nhân duy nhất: {{ company.legal_entities[0] }}
{% endif %}

## 🔗 Tài liệu liên quan

→ ↑ {{ lark.wiki_root_url | wiki_link("Master Wiki Index") }}
→ [Cơ cấu tổ chức](01-org-structure.md)
→ [Ngữ cảnh vận hành](06-context-notes.md)
→ [Thuật ngữ](04-glossary.md)
