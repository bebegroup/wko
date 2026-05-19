"""Traverse Lark Wiki tree via lark-cli.

Output: tree.json with hierarchy + metadata for each node.

Usage:
    python3 scripts/wiki_navigator.py                   # default output dist/wiki-tree.json
    python3 scripts/wiki_navigator.py --output tree.json
    python3 scripts/wiki_navigator.py --max-depth 3
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

from _common import load_config, require_lark_auth, require_lark_cli


def fetch_node(node_token: str) -> dict[str, Any] | None:
    """Get single node metadata via lark-cli."""
    try:
        r = subprocess.run(
            ["lark-cli", "wiki", "node", "get", "--node-token", node_token, "--output", "json"],
            capture_output=True,
            text=True,
            check=True,
            timeout=15,
        )
        return json.loads(r.stdout)
    except (subprocess.CalledProcessError, json.JSONDecodeError) as e:
        print(f"⚠️  fetch_node {node_token}: {e}", file=sys.stderr)
        return None


def list_children(parent_token: str) -> list[dict[str, Any]]:
    """List immediate children of a node."""
    try:
        r = subprocess.run(
            [
                "lark-cli",
                "wiki",
                "node",
                "list",
                "--parent-node-token",
                parent_token,
                "--output",
                "json",
            ],
            capture_output=True,
            text=True,
            check=True,
            timeout=30,
        )
        return json.loads(r.stdout)
    except (subprocess.CalledProcessError, json.JSONDecodeError):
        return []


def walk_tree(root_token: str, max_depth: int = 10, _depth: int = 0) -> dict[str, Any]:
    """Recursively walk wiki tree starting from root_token."""
    node = fetch_node(root_token) or {"node_token": root_token, "title": "(unknown)"}
    if _depth >= max_depth:
        node["children"] = []
        return node
    children = list_children(root_token)
    node["children"] = [walk_tree(c["node_token"], max_depth, _depth + 1) for c in children]
    return node


def main() -> int:
    parser = argparse.ArgumentParser(description="Traverse Lark Wiki tree")
    parser.add_argument("--output", default="dist/wiki-tree.json", help="Output JSON path")
    parser.add_argument("--max-depth", type=int, default=10, help="Max recursion depth")
    parser.add_argument("--root", help="Root node token (default: cfg.lark.wiki_root_token)")
    args = parser.parse_args()

    require_lark_cli()
    cfg = load_config()
    require_lark_auth()

    root = args.root or cfg["lark"]["wiki_root_token"]
    print(f"📡 Walking tree from {root[:8]}... (max depth: {args.max_depth})")

    tree = walk_tree(root, args.max_depth)

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(tree, indent=2, ensure_ascii=False))
    print(f"✓ Tree → {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
