# Roadmap

## v1.0 — Public release (target: Q3 2026)

- [x] Spec đã duyệt — xem `docs/superpowers/specs/2026-05-19-wko-public-template-design.md`
- [x] Implementation plan — xem `docs/superpowers/plans/2026-05-19-wko-public-template-implementation.md`
- [ ] Bootstrap repo (M1)
- [ ] Config schema V4.1 + validator (M2)
- [ ] Render engine + tests (M3) → tag `v0.1.0-alpha`
- [ ] 12 skills templated (M4)
- [ ] 11 docs templated (M5) → tag `v0.5.0-beta`
- [ ] 17 scripts (M6)
- [ ] 7 CI workflows (M7) → tag `v0.9.0-rc`
- [ ] 3 examples + 4 docs-meta (M8)
- [ ] Release v1.0 (M9) → tag `v1.0.0`

## v1.1 — Quality of life (Q4 2026)

- [ ] `init_company.py` 12-question wizard polish (auto-detect Lark tenant)
- [ ] HTML preview server (`scripts/serve.py`) — view rendered docs trong browser
- [ ] Slack notification adapter (alternative to Lark webhook)
- [ ] `migrate_v4_to_v41.py` interactive mode

## v1.2 — Multi-tenant (Q1 2027)

- [ ] Profile system: `LARK_PROFILE=acme`
- [ ] `wko switch <profile>` for consultants quản nhiều client
- [ ] Multi-config rendering: `render.py --config configs/acme.yaml`

## v2.0 — Beyond Lark (2027+)

- [ ] Notion backend adapter
- [ ] Confluence backend adapter
- [ ] Outline backend adapter
- [ ] Plugin system (OKR/O3K, EOS, Scrum skill packs)

## Out of scope (v1.x)

- ❌ GUI editor (CLI/markdown only)
- ❌ Self-hosting Wiki engine (chỉ adapter, không thay Lark)
- ❌ AI auto-generation toàn bộ Wiki (chỉ assist soạn thảo)
- ❌ Localization sang ngôn ngữ khác Việt/Anh (community PRs welcome)
