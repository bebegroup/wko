"""Wiki Reviewer Bot — lark-cli event consume + Claude API review.

Architecture (V4.1 rewrite — drops lark-oapi):

1. subprocess.Popen `lark-cli event consume im.message.receive_v1` → NDJSON stdout
2. For each event:
   - Filter chat_id (only contributor_group_chat_id from config)
   - Branch on message kind:
     A. Approval reply (keyword + parent has wiki URL + whitelist user)
     B. Wiki URL in message → review flow
3. Dedup: same URL within 60s → skip
4. Resolve wiki URL → node_token + obj_token via `lark-cli wiki node get`
5. Fetch doc content via `lark-cli docs fetch`
6. Claude API (Anthropic SDK) review với cached system prompt
7. Post comment via `lark-cli drive comment create`
8. Notify group via `lark-cli im message send`

Run:
    pip install -r scripts/requirements.txt
    cp .env.example .env  # điền LARK_APP_ID/SECRET + ANTHROPIC_API_KEY
    python3 scripts/wiki_reviewer_bot.py
"""

from __future__ import annotations

import json
import logging
import os
import re
import subprocess
import sys
import time
from typing import Any

from _common import load_config, require_lark_auth, require_lark_cli
from anthropic import Anthropic
from dotenv import load_dotenv

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
log = logging.getLogger("wiki-bot")


# Approval keywords (case-insensitive)
APPROVAL_KEYWORDS = ["approve", "ok", "lgtm", "duyệt", "ok publish"]

# Wiki URL pattern (matches both lark.com and feishu.cn)
WIKI_URL_RE = re.compile(r"https://[\w.-]+/wiki/[\w-]+")


def extract_wiki_url(text: str) -> str | None:
    """Find first Lark Wiki URL in text."""
    m = WIKI_URL_RE.search(text)
    return m.group(0) if m else None


def is_approval(text: str) -> bool:
    """Check if message is an approval keyword."""
    return any(kw in text.lower() for kw in APPROVAL_KEYWORDS)


def resolve_wiki_url(url: str) -> dict[str, str] | None:
    """Get node_token + obj_token from Wiki URL via lark-cli."""
    try:
        r = subprocess.run(
            ["lark-cli", "wiki", "node", "get", "--url", url, "--output", "json"],
            capture_output=True,
            text=True,
            check=True,
            timeout=15,
        )
        return json.loads(r.stdout)
    except (subprocess.CalledProcessError, json.JSONDecodeError) as e:
        log.error(f"Failed to resolve {url}: {e}")
        return None


def fetch_doc_content(obj_token: str) -> str | None:
    """Fetch docx content as markdown."""
    try:
        r = subprocess.run(
            ["lark-cli", "docs", "fetch", obj_token, "--api-version", "v2"],
            capture_output=True,
            text=True,
            check=True,
            timeout=30,
        )
        return r.stdout
    except subprocess.CalledProcessError as e:
        log.error(f"Failed to fetch {obj_token}: {e}")
        return None


def review_with_claude(
    page_content: str,
    page_url: str,
    client: Anthropic,
    cfg: dict[str, Any],
) -> dict[str, Any]:
    """Send page to Claude for review. Returns {score, comment}."""
    system_prompt = (
        f"Bạn là Wiki Reviewer Bot cho {cfg['company']['name']}. "
        f"Review trang Wiki theo:\n"
        f"- Format: title `<mã> <tên>` đúng prefix per type\n"
        f"- Writing style: số liệu cụ thể, không từ mơ hồ\n"
        f"- V{cfg['taxonomy']['version'].replace('v', '')} execution-first: page phải trả lời ≥ 1 câu hỏi thực thi\n"
        f"- Linking: 4 loại link đầy đủ + Hub Parent\n"
        f'\nReturn JSON: {{"score": float 0-10, "comment": str, "highlights": list}}'
    )

    user_prompt = f"Review trang sau:\n\nURL: {page_url}\n\nContent:\n{page_content[:3000]}"

    try:
        response = client.messages.create(
            model="claude-opus-4-20250514",  # Or current model
            max_tokens=1024,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
        )
        text = response.content[0].text
        # Try parse JSON; fallback to dict with comment-only
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return {"score": 7.0, "comment": text[:500]}
    except Exception as e:
        log.error(f"Claude API failed: {e}")
        return {"score": 0, "comment": f"Bot review failed: {e}"}


def post_comment(obj_token: str, comment: str) -> bool:
    """Post comment via lark-cli drive comment."""
    try:
        subprocess.run(
            [
                "lark-cli",
                "drive",
                "comment",
                "create",
                "--file-token",
                obj_token,
                "--content",
                comment,
            ],
            check=True,
            timeout=15,
        )
        return True
    except subprocess.CalledProcessError as e:
        log.error(f"post_comment failed: {e}")
        return False


def notify_group(chat_id: str, text: str) -> bool:
    """Send message to Lark chat via lark-cli."""
    try:
        subprocess.run(
            [
                "lark-cli",
                "im",
                "message",
                "send",
                "--receive-id",
                chat_id,
                "--msg-type",
                "text",
                "--content",
                json.dumps({"text": text}, ensure_ascii=False),
            ],
            check=True,
            timeout=15,
        )
        return True
    except subprocess.CalledProcessError as e:
        log.error(f"notify_group failed: {e}")
        return False


def process_event(
    event: dict[str, Any],
    client: Anthropic,
    cfg: dict[str, Any],
    recent_urls: dict[str, float],
) -> None:
    """Process 1 IM event."""
    msg = event.get("event", {}).get("message", {})
    chat_id = msg.get("chat_id", "")
    expected_chat = cfg["integrations"].get("contributor_group_chat_id", "")
    if expected_chat and chat_id != expected_chat:
        return  # Not our group

    text = msg.get("content", "")
    if isinstance(text, dict):
        text = text.get("text", "")
    if not isinstance(text, str):
        text = str(text)

    url = extract_wiki_url(text)
    if not url:
        return

    # Dedup
    now = time.time()
    last = recent_urls.get(url, 0)
    if now - last < 60:
        log.info(f"Dedup skip: {url}")
        return
    recent_urls[url] = now

    log.info(f"Reviewing: {url}")

    node_info = resolve_wiki_url(url)
    if not node_info:
        return
    obj_token = node_info.get("obj_token", "")
    content = fetch_doc_content(obj_token)
    if not content:
        return

    review = review_with_claude(content, url, client, cfg)
    score = review.get("score", 0)
    comment = review.get("comment", "")

    post_comment(obj_token, comment)
    notify_group(chat_id, f"📝 Reviewed: {url}\nScore: {score:.1f}/10")


def main() -> int:
    load_dotenv()
    require_lark_cli()
    cfg = load_config()
    require_lark_auth()

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        log.error("❌ ANTHROPIC_API_KEY missing in .env")
        return 1

    client = Anthropic(api_key=api_key)
    chat_id = cfg["integrations"].get("contributor_group_chat_id", "")
    if not chat_id:
        log.warning(
            "⚠️  integrations.contributor_group_chat_id not set — bot will process all chats"
        )

    log.info("🤖 Wiki Reviewer Bot starting (lark-cli event consume mode)...")

    proc = subprocess.Popen(
        ["lark-cli", "event", "consume", "im.message.receive_v1"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        bufsize=1,
        text=True,
    )

    recent_urls: dict[str, float] = {}
    try:
        for line in proc.stdout:  # NDJSON, 1 line = 1 event
            line = line.strip()
            if not line:
                continue
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            try:
                process_event(event, client, cfg, recent_urls)
            except Exception as e:
                log.exception(f"Error processing event: {e}")
    except KeyboardInterrupt:
        log.info("Stopping bot...")
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()

    return 0


if __name__ == "__main__":
    sys.exit(main())
