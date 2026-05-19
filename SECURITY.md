# Security Policy

## Reporting a vulnerability

Email: **security@saucevn.dev** (hoặc GitHub Security Advisory)
Response: 48h tối đa.

## ⚠️ KHÔNG commit

- `company.config.yaml` — chứa Lark `wiki_root_token`, `master_index.obj_token`
- `.env` — chứa `LARK_APP_SECRET`, `ANTHROPIC_API_KEY`
- Files trong `drafts/` — draft nội bộ
- Files trong `dist/` — output của `render.py` (có thể chứa data sensitive sau substitute)

Tất cả đã được `.gitignore`. Nếu `git status` thấy chúng = STOP, kiểm tra ngay.

## Nếu vô tình commit secret

1. **Revoke token ngay lập tức** tại Lark Developer Console
2. Xoá khỏi git history:

   ```bash
   pip install git-filter-repo
   git filter-repo --path company.config.yaml --invert-paths
   git push origin --force --all
   ```

3. Notify maintainers (xem `MAINTAINERS.md`)
4. Tạo token mới + update local `.env`

## Anti-leak checklist

Trước khi `git push`:

- [ ] `git status` không thấy `company.config.yaml` hoặc `.env`
- [ ] `git diff --cached` không có chuỗi giống Lark token (24 chars base62)
- [ ] (Optional) Chạy `gitleaks detect` (cài qua `brew install gitleaks`)

## Supported versions

Chỉ phiên bản latest minor được nhận security updates. Bạn dùng v0.x → upgrade lên v1.x trước khi report.

| Version | Supported |
|---|---|
| 1.x | ✅ |
| 0.x | ❌ (alpha/beta) |
