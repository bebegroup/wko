"""Pull snapshot of Lark Wiki → sources/lark-exports/.

Pull tree + content của mỗi node, save thành tree.json + nodes/<slug>.xml.

Usage:
    python3 scripts/pull_from_lark.py --all                    # full snapshot
    python3 scripts/pull_from_lark.py --tree-only              # chỉ tree, không fetch content
    python3 scripts/pull_from_lark.py --node-token <token>     # pull 1 node
    python3 scripts/pull_from_lark.py --output sources/lark-exports/snapshot-YYYYMMDD

Cần `lark-cli auth login` trước (scope: wiki:node:read + docx:document:readonly).
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import unicodedata
from datetime import datetime
from pathlib import Path
from typing import Any

from _common import load_config, require_lark_auth, require_lark_cli


def slugify(text: str, max_len: int = 80) -> str:
    """Convert title to filesystem-safe slug."""
    text = unicodedata.normalize("NFKD", text).encode("ASCII", "ignore").decode()
    text = re.sub(r"[^\w\s-]", "", text).strip().lower()
    text = re.sub(r"[\s_-]+", "-", text)
    return text[:max_len] or "untitled"


def fetch_content(obj_token: str) -> str | None:
    """Fetch docx content as XML."""
    try:
        r = subprocess.run(
            ["lark-cli", "docs", "fetch", obj_token, "--api-version", "v2", "--format", "xml"],
            capture_output=True,
            text=True,
            check=True,
            timeout=30,
        )
        return r.stdout
    except subprocess.CalledProcessError as e:
        print(f"⚠️  fetch_content {obj_token}: {e}", file=sys.stderr)
        return None


def list_descendants(root_token: str) -> list[dict[str, Any]]:
    """Walk all descendants of root, return flat list."""
    queue = [root_token]
    all_nodes: list[dict[str, Any]] = []
    while queue:
        token = queue.pop(0)
        try:
            r = subprocess.run(
                [
                    "lark-cli",
                    "wiki",
                    "node",
                    "list",
                    "--parent-node-token",
                    token,
                    "--output",
                    "json",
                ],
                capture_output=True,
                text=True,
                check=True,
                timeout=30,
            )
            children = json.loads(r.stdout)
            for c in children:
                all_nodes.append(c)
                queue.append(c["node_token"])
        except (subprocess.CalledProcessError, json.JSONDecodeError):
            continue
    return all_nodes


def pull_snapshot(
    root_token: str,
    output_dir: Path,
    tree_only: bool = False,
) -> dict[str, Any]:
    """Pull tree + content (optional). Returns manifest dict."""
    output_dir.mkdir(parents=True, exist_ok=True)
    nodes_dir = output_dir / "nodes"
    nodes_dir.mkdir(exist_ok=True)

    print(f"📡 Walking descendants of {root_token[:8]}...")
    nodes = list_descendants(root_token)
    print(f"   Found {len(nodes)} nodes")

    manifest: dict[str, Any] = {
        "root_token": root_token,
        "snapshot_time": datetime.utcnow().isoformat(),
        "total_nodes": len(nodes),
        "nodes": {},
    }

    for i, n in enumerate(nodes, 1):
        node_token = n["node_token"]
        title = n.get("title", "untitled")
        obj_token = n.get("obj_token", "")
        slug = slugify(title)
        manifest["nodes"][node_token] = {
            "title": title,
            "slug": slug,
            "obj_token": obj_token,
        }

        if not tree_only and obj_token:
            content = fetch_content(obj_token)
            if content:
                (nodes_dir / f"{slug}.xml").write_text(content)
                if i % 10 == 0:
                    print(f"   [{i}/{len(nodes)}] {title[:40]}")

    # Write manifest + tree
    (output_dir / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False))
    (output_dir / "tree.json").write_text(json.dumps(nodes, indent=2, ensure_ascii=False))

    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description="Pull Lark Wiki snapshot")
    parser.add_argument("--all", action="store_true", help="Full snapshot")
    parser.add_argument("--tree-only", action="store_true", help="Chỉ tree, không fetch content")
    parser.add_argument("--node-token", help="Pull 1 node thay vì root")
    parser.add_argument(
        "--output", help="Output directory (default sources/lark-exports/<timestamp>)"
    )
    args = parser.parse_args()

    require_lark_cli()
    cfg = load_config()
    require_lark_auth()

    root = args.node_token or cfg["lark"]["wiki_root_token"]

    if args.output:
        out = Path(args.output)
    else:
        ts = datetime.utcnow().strftime("%Y%m%d-%H%M%S")
        out = Path("sources/lark-exports") / f"snapshot-{ts}"

    manifest = pull_snapshot(root, out, tree_only=args.tree_only)
    print(f"\n✓ Snapshot done. Manifest: {out / 'manifest.json'}")
    print(f"  Total nodes: {manifest['total_nodes']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
