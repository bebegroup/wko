"""Tests for wiki_reviewer_bot.py — pure functions."""

from __future__ import annotations

from wiki_reviewer_bot import (
    extract_wiki_url,
    is_approval,
)


def test_extract_wiki_url_larksuite() -> None:
    text = "Check trang này: https://acme.sg.larksuite.com/wiki/Yix7wq123 ngon"
    assert extract_wiki_url(text) == "https://acme.sg.larksuite.com/wiki/Yix7wq123"


def test_extract_wiki_url_feishu() -> None:
    text = "https://acme.feishu.cn/wiki/ABC123"
    assert extract_wiki_url(text) == "https://acme.feishu.cn/wiki/ABC123"


def test_extract_wiki_url_no_match() -> None:
    assert extract_wiki_url("just plain text") is None
    assert extract_wiki_url("https://github.com/repo") is None


def test_is_approval_keywords() -> None:
    assert is_approval("approve") is True
    assert is_approval("LGTM!") is True
    assert is_approval("ok publish") is True
    assert is_approval("duyệt rồi nhé") is True


def test_is_approval_negative() -> None:
    assert is_approval("not yet") is False
    assert is_approval("xem lại đi") is False
    assert is_approval("") is False
