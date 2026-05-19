# Onboarding — Setup wko trong 30 phút

> Hướng dẫn cho team đang bắt đầu dùng `saucevn/wko` để dựng Wiki Company OS của công ty mình trên Lark / Feishu.
>
> Theo thứ tự, đừng skip.

---

## Trước khi bắt đầu

Bạn cần:

- Máy macOS / Linux / WSL (Windows native chưa test)
- Tài khoản Lark / Feishu admin của công ty bạn
- Quyền tạo Custom App trên Lark Open Platform
- Khoảng 30 phút tập trung

Nếu bạn chưa có Lark workspace: tạo tại [larksuite.com](https://www.larksuite.com) (free tier hỗ trợ).

---

## Bước 1 — Fork & clone (5 phút)

Vì `company.config.yaml` của bạn sẽ chứa Lark token nhạy cảm, **bắt buộc fork về private repo**, không clone trực tiếp:

```bash
# 1. Fork saucevn/wko trên GitHub (UI: nút "Fork", chọn "Private")
#    Hoặc qua gh CLI:
gh repo fork saucevn/wko --clone --remote --fork-name wko-acme

cd wko-acme

# 2. Đổi visibility nếu fork tạo public mặc định
gh repo edit --visibility private

# 3. Set upstream để pull update từ saucevn/wko
git remote add upstream https://github.com/saucevn/wko.git
git remote -v
```

Verify remote:

```
origin    https://github.com/<your-org>/wko-acme.git (fetch/push)
upstream  https://github.com/saucevn/wko.git           (fetch/push)
```

---

## Bước 2 — Cài lark-cli & Python deps (5 phút)

`lark-cli` là **hard requirement**. Repo này không chạy mà thiếu nó.

```bash
# macOS
brew install lark-cli

# Linux
curl -fsSL https://github.com/larksuite/lark-cli/releases/latest/download/lark-cli-linux-x64.tar.gz \
  | sudo tar -xz -C /usr/local/bin

# Cross-platform qua npm
npm i -g @larksuiteoapi/lark-cli

# Verify >= 1.0.30
lark-cli --version
```

Python deps:

```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r scripts/requirements.txt
```

---

## Bước 3 — Đăng nhập Lark (2 phút)

```bash
lark-cli auth login --as user
```

Browser sẽ mở → đăng nhập tài khoản Lark của bạn → grant scope `wiki:*`, `docx:*`, `im:*`, `drive:*`.

Verify:

```bash
lark-cli auth status
lark-cli wiki space list
```

Bạn nên thấy ít nhất 1 Wiki space của tổ chức.

---

## Bước 4 — Tạo Lark Wiki Space (5 phút)

Trong Lark app:

1. Tab **Wiki** → nút **+ Create Wiki**
2. Đặt tên: `<Company> Company OS` (vd: `Acme Foods Company OS`)
3. Chọn visibility "Internal" hoặc "Team only"
4. Sau khi tạo, copy URL — sẽ có dạng:
   ```
   https://<tenant>.<region>.larksuite.com/wiki/<WIKI_ROOT_TOKEN>
   ```
5. Note lại `<WIKI_ROOT_TOKEN>` (ký tự sau `/wiki/`) → sẽ điền vào config

---

## Bước 5 — Tạo Lark Custom App (5 phút)

1. Mở [open.larksuite.com](https://open.larksuite.com) (hoặc `open.feishu.cn` nếu Feishu)
2. **Developer Console** → **Create Custom App** (Bot mode)
3. Đặt tên: `wko-bot-<company>` (vd: `wko-bot-acme`)
4. Mở app vừa tạo → tab **Permissions & Scopes** → cấp các scope:

   | Scope | Mục đích |
   |---|---|
   | `wiki:wiki` | Đọc Wiki spaces |
   | `wiki:node:retrieve` | Đọc node hierarchy |
   | `wiki:node:write` | Tạo/sửa node (publish) |
   | `docx:document` | Đọc/sửa nội dung Docs |
   | `docx:document:readonly` | Fetch nội dung để render |
   | `drive:file` | Comment trên file |
   | `im:message` | Bot gửi notification |
   | `im:message:send_as_bot` | Send message qua webhook |

5. Tab **Credentials & Basic Info** → copy:
   - **App ID** (vd `cli_a1b2c3...`)
   - **App Secret** (giữ kín!)

---

## Bước 6 — Cấu hình `company.config.yaml` (10 phút)

```bash
cp company.config.yaml.example company.config.yaml
```

Mở `company.config.yaml` và điền các trường quan trọng (tối thiểu):

```yaml
company:
  name: "Acme Foods"
  short_name: "Acme"
  industry: "F&B / Gia vị"
  hq_country: "VN"

lark:
  domain: "larksuite.com"              # hoặc feishu.cn
  tenant_subdomain: "acme"              # phần trước .sg.larksuite.com
  region: "sg"                          # sg | cn | us
  wiki_root_token: "<WIKI_ROOT_TOKEN từ Bước 4>"
  wiki_root_url: "https://acme.sg.larksuite.com/wiki/<WIKI_ROOT_TOKEN>"
  master_index:
    node_token: ""                      # sẽ tạo ở Bước 7
    obj_token: ""

taxonomy:
  version: "v4.1"                       # giữ V4.1 mặc định (7 SPACE, 13 TYPE)
  # spaces, page_types, sections — giữ mặc định, hoặc custom

org:
  departments:
    - { code: HCNS, name: "Hành chính – Nhân sự" }
    - { code: KT, name: "Kế toán" }
    # ... điền theo công ty

master_registry:
  # 12 MASTER bắt buộc — điền theo nghiệp vụ công ty
  - code: "SYS-00-MST-001"
    name: "Master Registry"
    owner: "Admin"
```

Tạo `.env`:

```bash
cp .env.example .env
```

Điền `.env`:

```
LARK_APP_ID=cli_a1b2c3...
LARK_APP_SECRET=<APP_SECRET từ Bước 5>
ANTHROPIC_API_KEY=sk-ant-...           # optional, chỉ cần nếu chạy reviewer bot
```

Validate:

```bash
python3 scripts/validate_config.py --strict
```

Phải PASS hết. Nếu fail, đọc error message và fix.

---

## Bước 7 — Render + tạo Master Index node (3 phút)

Render template:

```bash
python3 scripts/render.py
```

Output ở `dist/skills/`, `dist/docs/`. Mở `dist/docs/02-wiki-architecture.md` — bạn sẽ thấy 7 SPACE liệt kê đúng tên công ty bạn.

Tạo Master Index node trên Lark:

```bash
# Tạo node con dưới wiki_root_token
lark-cli wiki node create \
  --space-id "<WIKI_ROOT_TOKEN>" \
  --title "SYS-00-IDX-001 Master Wiki Index" \
  --obj-type docx

# Output sẽ in node_token + obj_token — copy về company.config.yaml
```

Update `company.config.yaml`:

```yaml
lark:
  master_index:
    node_token: "<từ output trên>"
    obj_token: "<từ output trên>"
```

Re-validate:

```bash
python3 scripts/validate_config.py --strict
```

---

## Bước 8 — Setup GitHub CI (5 phút)

Trong repo private của bạn (vd `your-org/wko-acme`):

### Secrets

`Settings → Secrets and variables → Actions → New repository secret`:

| Tên | Giá trị |
|---|---|
| `LARK_APP_ID` | App ID từ Bước 5 |
| `LARK_APP_SECRET` | App Secret từ Bước 5 |
| `COMPANY_CONFIG_B64` | `base64 -i company.config.yaml \| pbcopy` (macOS) hoặc `base64 -w0 company.config.yaml` (Linux) |
| `ANTHROPIC_API_KEY` | (optional) Cho reviewer bot |

### Variables

`Settings → Secrets and variables → Actions → Variables tab → New repository variable`:

| Tên | Giá trị |
|---|---|
| `LARK_INTEGRATION_ENABLED` | `true` |

### Test workflow

```bash
gh workflow run lark-rebuild-index.yml
gh run watch
```

Verify Master Index đã được push lên Lark — mở `dist/docs/master-index-snapshot.md` hoặc trực tiếp link Lark.

---

## ✅ Hoàn thành

Wiki Company OS đã sẵn sàng. Bước tiếp theo:

1. Đọc [skills/05-publish-workflow.md](../skills/05-publish-workflow.md) (sau khi render → `dist/skills/05-publish-workflow.md`)
2. Soạn page đầu tiên theo [skills/01-page-format.md](../skills/01-page-format.md)
3. Update Master Index sau mỗi page mới
4. Định kỳ pull upstream từ `saucevn/wko`:
   ```bash
   git fetch upstream
   git merge upstream/main          # hoặc git rebase upstream/main
   ```
5. Khi taxonomy thay đổi (vd v4.1 → v4.2), đọc [docs-meta/UPGRADING.md](UPGRADING.md)

---

## Troubleshooting

### `lark-cli: command not found`
→ Cài lại theo [Bước 2](#bước-2--cài-lark-cli--python-deps-5-phút).

### `lark-cli auth login` failed
→ Kiểm tra firewall/proxy chặn `passport.larksuite.com`. Thử mạng khác.

### `validate_config.py` fail với `KeyError: lark.wiki_root_token`
→ Bạn chưa điền `wiki_root_token` trong `company.config.yaml`. Xem [Bước 6](#bước-6--cấu-hình-companyconfigyaml-10-phút).

### `render.py` fail với `UndefinedError: 'company.foo' is undefined`
→ File source có placeholder không tồn tại trong config. Mở error message để biết file:line cụ thể.

### CI workflow `lark-rebuild-index` skip
→ Bạn chưa set `LARK_INTEGRATION_ENABLED=true` ở Variables (không phải Secrets).

### Cần help?
- GitHub Issues: <https://github.com/saucevn/wko/issues>
- Discussion: <https://github.com/saucevn/wko/discussions>
- Discord (community): (xem README để có link mới nhất)

---

## Tham khảo

- **Repo gốc:** <https://github.com/saucevn/wko>
- **License:** MIT
- **Maintainer:** [@saucevn](https://github.com/saucevn)
- **Kiến trúc chi tiết:** [docs-meta/ARCHITECTURE.md](ARCHITECTURE.md)
- **Workflow publish:** [docs-meta/PUBLISHING.md](PUBLISHING.md)
- **Sync upstream:** [docs-meta/UPGRADING.md](UPGRADING.md)
