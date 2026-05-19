# Cơ cấu tổ chức — {{ company.name }}

## {{ org.departments | length }} phòng ban

| Code | Tên | Head role |
|---|---|---|
{% for d in org.departments %}| `{{ d.code }}` | {{ d.name }} | {{ d.get("head_role") | default("(chưa định)") }} |
{% endfor %}

<!-- TODO {{ company.short_name }} owner: bổ sung phòng ban còn thiếu trong company.config.yaml field `org.departments` -->

## Sơ đồ tổ chức

<!-- TODO: vẽ sơ đồ trên Lark Whiteboard, link về đây -->

```
                  ┌──────┐
                  │  BOD │
                  └───┬──┘
       ┌──────────────┼──────────────┐
       │              │              │
       ▼              ▼              ▼
   {{ org.departments[0].code if org.departments else "..." }}            ...            ...
   ({{ org.departments[0].name if org.departments else "..." }})
```

## Phân vai chính

<!-- TODO: liệt kê vai trò cốt lõi mỗi phòng ban.

Format đề xuất:

### HCNS (Hành chính – Nhân sự)
- HCNS Lead — chiến lược nhân sự
- HCNS Specialist — execution: tuyển dụng, onboarding, đánh giá
- Office Admin — vận hành văn phòng

### KT (Kế toán)
- Kế toán trưởng (KTT) — sign-off, đối soát
- Kế toán Tổng hợp (KTTH) — daily entries
- Kế toán Kho — inventory tracking
...

-->

## Báo cáo & phối hợp

| Phòng ban | Báo cáo về | Phối hợp với |
|---|---|---|
{% for d in org.departments %}| {{ d.code }} | BOD | <!-- TODO --> |
{% endfor %}

## Cross-functional teams

<!-- TODO: nếu có team chéo (vd: launch product, campaign), liệt kê ở đây -->

## 🔗 Tài liệu liên quan

→ ↑ {{ lark.wiki_root_url | wiki_link("Master Wiki Index") }}
→ [Tổng quan công ty](00-company-overview.md)
→ [Phân quyền Wiki](03-permissions.md)
→ [Phối hợp liên phòng (INT-XFN)](07-status-tracker.md) — nếu đã có section INT-XFN
