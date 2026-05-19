"""Tests for scripts/render.py."""
from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from render import RenderError, render_string, render_tree


def test_render_simple_placeholder(sample_config: dict[str, Any]) -> None:
    out = render_string("Hello {{ company.name }}", sample_config)
    assert out == "Hello Acme Foods"


def test_render_loop(sample_config: dict[str, Any]) -> None:
    template = "{% for s in taxonomy.spaces %}- {{ s.code }}\n{% endfor %}"
    out = render_string(template, sample_config)
    assert "- SYS" in out
    assert "- OPS" in out
    assert "- ARC" in out


def test_render_undefined_placeholder_fails(sample_config: dict[str, Any]) -> None:
    with pytest.raises(RenderError, match="nonexistent_field"):
        render_string("{{ company.nonexistent_field }}", sample_config)


def test_render_tree_creates_dist(tmp_repo: Path, sample_config: dict[str, Any]) -> None:
    src = tmp_repo / "skills"
    dst = tmp_repo / "dist" / "skills"

    (src / "01-test.md").write_text(
        "# {{ company.name }}\n\nIndustry: {{ company.industry }}"
    )
    (src / "subdir").mkdir()
    (src / "subdir" / "nested.md").write_text("Nested: {{ company.short_name }}")

    count = render_tree(src, dst, sample_config)
    assert count == 2

    out1 = (dst / "01-test.md").read_text()
    assert "# Acme Foods" in out1
    assert "Industry: F&B" in out1

    out2 = (dst / "subdir" / "nested.md").read_text()
    assert "Nested: Acme" in out2


def test_render_raw_block_preserves_literal(sample_config: dict[str, Any]) -> None:
    """Code block với {% raw %}...{% endraw %} giữ literal {{ }}."""
    template = (
        "Outside: {{ company.name }}\n\n"
        "```\n{% raw %}{{ literal }}{% endraw %}\n```"
    )
    out = render_string(template, sample_config)
    assert "Acme Foods" in out
    assert "{{ literal }}" in out


def test_render_custom_filter_upper_dashed(sample_config: dict[str, Any]) -> None:
    out = render_string('{{ "sys-00-idx-001" | upper_dashed }}', sample_config)
    assert out == "SYS-00-IDX-001"


def test_render_custom_filter_wiki_link(sample_config: dict[str, Any]) -> None:
    out = render_string(
        '{{ "https://acme.sg.larksuite.com/wiki/abc" | wiki_link("Wiki Root") }}',
        sample_config,
    )
    assert out == "[Wiki Root](https://acme.sg.larksuite.com/wiki/abc)"
