# Contributing to saucevn/wko

Cảm ơn bạn quan tâm! `wko` là dự án open source MIT licensed.

## Loại đóng góp được welcome

| Loại | Ví dụ |
|---|---|
| Bug fix | `render.py` crash khi config thiếu field optional |
| Doc improvement | Sửa lỗi typo, dịch sang ngôn ngữ khác |
| New placeholder | Thêm `{{ company.fiscal_year_start }}` cho phần tài chính |
| New example | `examples/agency-thailand/` cho công ty agency |
| Taxonomy extension | Thêm SPACE/TYPE mới cho industry-specific case |
| Script improvement | Tăng performance, thêm dry-run mode |

## Loại đóng góp KHÔNG accept

- **Company-specific content** — wko là template generic, không chứa nội dung công ty cụ thể
- **Breaking change không có RFC** — đổi config schema, đổi placeholder syntax phải có discussion trước
- **Lark API SDK Python (lark-oapi)** — repo này thống nhất qua `lark-cli` subprocess

## Workflow

1. Fork `saucevn/wko`
2. Tạo branch: `git checkout -b fix/short-description` hoặc `feat/short-description`
3. Code + test (TDD pattern, xem `tests/`)
4. CI pass (lint + validate + render + tests)
5. PR vào `main`, mô tả rõ:
   - Vấn đề giải quyết
   - Approach
   - Backward compat (có/không)
6. 1 maintainer review → merge (squash)

## Setup dev env

```bash
git clone https://github.com/<your-fork>/wko.git
cd wko
python3 -m venv .venv && source .venv/bin/activate
pip install -r scripts/requirements.txt
pip install -e ".[dev]"          # pyproject.toml extras
pre-commit install               # optional
make test
```

## Code style

- Python: `ruff` + `black` (config trong `pyproject.toml`)
- Markdown: `markdownlint-cli2`
- Commits: Conventional Commits (`feat:`, `fix:`, `docs:`, ...)
- Vietnamese là primary language. EN translation contribution welcome cho `docs-meta/` và `README.md`.

## RFC process

Cho breaking change hoặc feature lớn:

1. Open GitHub Discussion với title `RFC: <feature>`
2. Mô tả: motivation, design, alternatives, drawbacks
3. Wait ≥ 7 ngày cho community feedback
4. Maintainer decision: accept / reject / request changes
5. Nếu accept → implement qua PR reference RFC discussion

## Maintainers

Xem [`MAINTAINERS.md`](MAINTAINERS.md).

## Code of Conduct

Tôn trọng. Không tolerance cho harassment. Disagree về kỹ thuật OK, attack cá nhân không.
