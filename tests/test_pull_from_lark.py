"""Tests for pull_from_lark.py."""

from __future__ import annotations

from pull_from_lark import slugify


def test_slugify_basic() -> None:
    assert slugify("Hello World") == "hello-world"


def test_slugify_vietnamese() -> None:
    assert slugify("Tiếp nhận và phân loại") == "tiep-nhan-va-phan-loai"


def test_slugify_strips_special_chars() -> None:
    assert slugify("OPS-CS-SOP-001 — Xử lý!") == "ops-cs-sop-001-xu-ly"


def test_slugify_max_length() -> None:
    long_title = "Lorem ipsum " * 30
    result = slugify(long_title, max_len=20)
    assert len(result) <= 20


def test_slugify_empty_returns_untitled() -> None:
    assert slugify("") == "untitled"
    assert slugify("!!!") == "untitled"
