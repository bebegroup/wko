# sources/schemas/

Lark Wiki schema reference files (generic, no PII).

| File | Mô tả |
|---|---|
| `lark_wiki_schema.json` | JSON schema cho Lark Wiki node structure (V4.1 fields) |
| `lark_wiki_erd.svg` | Entity-Relationship Diagram cho Lark Wiki data model |
| `wiki_nodes_response.json` | Sample response từ `lark-cli wiki node list` để tham chiếu |

## Cập nhật

Khi Lark API thay đổi:

```bash
# Pull mới
lark-cli wiki node list --space-id <token> --output json > sources/schemas/wiki_nodes_response.json
# Regenerate ERD nếu cần (manual via diagrams.net hoặc tương đương)
```

## Generic vs company-specific

Files trong folder này **generic** — không chứa nội dung công ty cụ thể.

Để store data thật:

- `sources/excel/` — Excel files (gitignored, không commit)
- `sources/lark-exports/` — snapshots qua `pull_from_lark.py` (gitignored)

Xem [docs-meta/ARCHITECTURE.md](../../docs-meta/ARCHITECTURE.md) cho overview.
