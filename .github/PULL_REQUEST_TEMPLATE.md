<!-- Cảm ơn bạn đã contribute! Điền các mục dưới. -->

## Summary

<!-- 1-2 dòng mô tả thay đổi -->

## Type of change

- [ ] 🐛 Bug fix (non-breaking)
- [ ] ✨ New feature (non-breaking)
- [ ] 📝 Documentation
- [ ] ♻️ Refactor / chore
- [ ] ⚠️ BREAKING CHANGE (cần [RFC discussion](https://github.com/saucevn/wko/discussions) trước)

## Scope

- [ ] `skills/` (writing rules)
- [ ] `docs/` (company docs)
- [ ] `scripts/` (tooling)
- [ ] `.github/` (CI)
- [ ] `company.config.yaml.example` (schema)
- [ ] `examples/`
- [ ] `docs-meta/`
- [ ] `tests/`

## Test plan

- [ ] Tests added/updated (`pytest`)
- [ ] CI passing (lint + validate + render + tests)
- [ ] Render check OK với `company.config.yaml.example`
- [ ] Tested locally với 1 example trong `examples/`

## Backward compatibility

- [ ] Non-breaking — existing configs render OK
- [ ] Breaking — đã document trong CHANGELOG.md + có RFC discussion link

## Checklist

- [ ] Code follows project conventions (ruff + black)
- [ ] Commit messages follow [Conventional Commits](https://www.conventionalcommits.org/)
- [ ] KHÔNG commit `company.config.yaml`, `.env`, secret
- [ ] KHÔNG dùng `lark-oapi` (Python SDK) — repo này `lark-cli only`
- [ ] Documentation updated (skills/, docs/, hoặc docs-meta/ nếu cần)

## Related issue

Closes #
