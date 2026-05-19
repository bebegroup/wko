# Skill 09 — Workflow contributing + Bot review

Quy trình cho nhân viên đóng góp Wiki (qua Lark, KHÔNG qua Git).

## Phase 1 — Manual review (mặc định)

1. Nhân viên soạn page Wiki trực tiếp trên Lark trong section phù hợp
2. Đặt status = ⬜ Draft
3. Gửi link Lark vào group `{{ integrations.contributor_group_email }}`
4. Reviewer mở trên Lark UI, review theo skill 01 + 02 + 08
5. Reviewer comment + đề xuất sửa
6. Nhân viên sửa, lặp đến khi pass
7. Reviewer đổi status = 🔄 Active trong Master Index

## Phase 2 — Async bot (khi config sẵn sàng)

Bot tự động review draft. Yêu cầu:

- `{{ integrations.reviewer_bot_webhook }}` đã set trong config
- `LARK_APP_ID/SECRET` đã set trong `.env`
- `ANTHROPIC_API_KEY` đã set
- `scripts/wiki_reviewer_bot.py` đang chạy (process daemon)

### Workflow Phase 2

```
1. Nhân viên soạn page → đặt Status Draft
2. Gửi link vào group {{ integrations.contributor_group_email }} với @{{ integrations.reviewer_bot_name }}
3. Bot subscribe im.message.receive_v1 qua lark-cli event consume
4. Bot detect message với wiki URL + mention
5. Bot resolve URL → node_token + obj_token (lark-cli wiki node get)
6. Bot fetch content (lark-cli docs fetch)
7. Bot Claude API review với system prompt cache (skill 01/02/08 + docs/02)
8. Bot compute score x.x/10 + encouraging comment
9. Bot POST comment qua lark-cli drive comment create
10. Bot notify group qua lark-cli im message send
```

### Bot setup

```bash
# 1. Cài deps
pip install -r scripts/requirements.txt

# 2. Verify lark-cli + auth (xem skill 05)
lark-cli --version
lark-cli auth status

# 3. Set env vars
cp .env.example .env
# Điền LARK_APP_ID, LARK_APP_SECRET, ANTHROPIC_API_KEY

# 4. Chạy bot (daemon mode)
nohup python3 scripts/wiki_reviewer_bot.py > /tmp/wiki-bot.log 2>&1 &

# Verify
tail -f /tmp/wiki-bot.log
```

### Bot architecture (V{{ taxonomy.version | replace("v", "") }} — lark-cli only)

```python
# Pseudocode:
proc = subprocess.Popen(
    ["lark-cli", "event", "consume", "im.message.receive_v1"],
    stdout=subprocess.PIPE, bufsize=1, text=True,
)
for line in proc.stdout:                # NDJSON
    event = json.loads(line)
    chat_id = event["event"]["message"]["chat_id"]
    if chat_id != cfg["integrations"]["contributor_group_chat_id"]:
        continue
    if wiki_url := extract_wiki_url(msg_text):
        review_via_claude(wiki_url)     # uses anthropic.Anthropic client
```

**KHÔNG dùng `lark-oapi` Python SDK** — bot này thống nhất qua `lark-cli` subprocess.

### Reviewer scope

Bot review:

1. **Format** (skill 01) — title, metadata block, section bắt buộc
2. **Writing style** (skill 02) — title pattern theo type, số liệu cụ thể
3. **Indexing** (skill 08) — mã page đúng format, có Hub Parent
4. **Backlink** (skill 03) — 4 loại link đầy đủ
5. **Status** (skill 04) — 18 tiêu chí Active (nếu request promote Draft → Active)

Bot KHÔNG review:

- Đúng/sai nội dung nghiệp vụ (chỉ Owner / Reviewer human biết)
- Quyết định mã/section (đã set ở Master Index)
- Override owner decision

### Reviewer fallback

Nếu bot fail (Anthropic API down, lark-cli error):

- Bot log error + post `❌ Reviewer fail. Manual review needed.` vào group
- Reviewer human take over

## Approval flow (Phase 2)

```
Bot review → score < 7/10 → Draft, nhân viên sửa
Bot review → score ≥ 7/10 → vẫn Draft, đợi human approve
Human reply trong group với keyword "approve" / "ok" / "lgtm"
→ Bot update Master Index: Status = 🔄 Active
→ Bot notify group
```

Whitelist user được approve: cấu hình trong `cfg["integrations"]["approval_whitelist"]` (optional).

## Roles

| Role | Quyền | Owner |
|---|---|---|
| Contributor | Tạo Draft, sửa nội dung mình | Tất cả nhân viên |
| Reviewer (section) | Review + approve Active | Section owner ({% for s in taxonomy.spaces %}{{ s.code }}: {{ s.owner }}{% if not loop.last %}, {% endif %}{% endfor %}) |
| Bot (`{{ integrations.reviewer_bot_name }}`) | Auto review, post comment | (system) |
| Master Index admin | Reorganize, archive | Wiki Admin |

## Best practices

1. **Một page = một topic** — không gộp nhiều topic
2. **Draft trước khi tag bot** — đảm bảo có content tối thiểu
3. **Hub Parent rõ ràng** — không tạo page floating
4. **Link [[mã]] format** — không hardcode URL trong văn bản

## 🔗 Tài liệu liên quan

→ ↑ {{ lark.wiki_root_url | wiki_link("Master Wiki Index") }}
→ [Skill 01 — Page Format](01-page-format.md)
→ [Skill 02 — Writing Style](02-writing-style.md)
→ [Skill 04 — Page Status](04-page-status.md) — Draft → Active flow
→ [Skill 08 — INDEX & Numbering](08-index-and-numbering.md)
→ [scripts/wiki_reviewer_bot.py](../scripts/wiki_reviewer_bot.py)
→ [docs/08 — Contributing](../docs/08-contributing.md) — quy trình cho người không dùng Git
