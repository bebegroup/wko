"""Build backlink graph từ source `.md` files.

Parse `[[mã page]]` references, sinh graph forward + reverse.

Output:
- dist/backlink-graph.json — full graph data
- dist/backlink-summary.md — markdown summary
- dist/backlink-graph.svg — visualization (optional, requires graphviz)

Usage:
    python3 scripts/build_backlink_graph.py                       # all sources
    python3 scripts/build_backlink_graph.py --source dist         # rendered output
    python3 scripts/build_backlink_graph.py --no-svg              # skip graphviz
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any


PAGE_REF_RE = re.compile(r"\[\[([A-Z]+-[A-Z0-9]+-[A-Z]+-\d{3})\]\]")
PAGE_CODE_IN_TITLE_RE = re.compile(r"^# ([A-Z]+-[A-Z0-9]+-[A-Z]+-\d{3})\s+(.+)$", re.MULTILINE)


def extract_page_code_from_title(content: str) -> tuple[str, str] | None:
    """Get (code, name) từ H1 nếu match `# <CODE> <name>`."""
    m = PAGE_CODE_IN_TITLE_RE.search(content)
    if m:
        return m.group(1), m.group(2)
    return None


def extract_references(content: str) -> set[str]:
    """Find all `[[mã]]` references in content."""
    return set(PAGE_REF_RE.findall(content))


def scan_directory(root: Path) -> dict[str, Any]:
    """Walk *.md files, build forward + reverse graphs.

    Returns:
        {
            "pages": {code: {file, name}, ...},
            "forward": {code: [referenced codes], ...},
            "reverse": {code: [referencing codes], ...},
            "unresolved": [list of refs to non-existent pages],
        }
    """
    pages: dict[str, dict] = {}
    forward: dict[str, set[str]] = defaultdict(set)
    reverse: dict[str, set[str]] = defaultdict(set)

    # First pass: enumerate pages
    for md_file in root.rglob("*.md"):
        # Skip meta dirs
        if any(part in ("superpowers", "drafts", ".git") for part in md_file.relative_to(root).parts):
            continue
        content = md_file.read_text()
        title = extract_page_code_from_title(content)
        if title:
            code, name = title
            pages[code] = {"file": str(md_file.relative_to(root)), "name": name}

    # Second pass: extract references
    for md_file in root.rglob("*.md"):
        if any(part in ("superpowers", "drafts", ".git") for part in md_file.relative_to(root).parts):
            continue
        content = md_file.read_text()
        title = extract_page_code_from_title(content)
        if not title:
            continue
        source_code = title[0]
        refs = extract_references(content)
        for target_code in refs:
            forward[source_code].add(target_code)
            reverse[target_code].add(source_code)

    unresolved = []
    for source_code, targets in forward.items():
        for t in targets:
            if t not in pages:
                unresolved.append({"from": source_code, "to": t})

    return {
        "pages": pages,
        "forward": {k: sorted(v) for k, v in forward.items()},
        "reverse": {k: sorted(v) for k, v in reverse.items()},
        "unresolved": unresolved,
    }


def format_summary_md(graph: dict[str, Any]) -> str:
    """Markdown summary of backlink graph."""
    lines = [
        "# Backlink Graph Summary",
        "",
        f"Total pages: **{len(graph['pages'])}**",
        f"Total forward links: **{sum(len(v) for v in graph['forward'].values())}**",
        f"Unresolved refs: **{len(graph['unresolved'])}**",
        "",
    ]

    if graph["unresolved"]:
        lines.append("## ⚠️ Unresolved references\n")
        for u in graph["unresolved"][:20]:
            lines.append(f"- `{u['from']}` → `{u['to']}` (target không tồn tại)")
        lines.append("")

    # Top 10 most-referenced
    ref_count = [(code, len(refs)) for code, refs in graph["reverse"].items()]
    ref_count.sort(key=lambda x: -x[1])
    lines.append("\n## Top 10 most-referenced pages\n")
    for code, count in ref_count[:10]:
        name = graph["pages"].get(code, {}).get("name", "?")
        lines.append(f"- `{code}` ({count} refs) — {name}")

    # Top 10 pages with most outgoing links
    out_count = [(code, len(refs)) for code, refs in graph["forward"].items()]
    out_count.sort(key=lambda x: -x[1])
    lines.append("\n## Top 10 pages with most outgoing links\n")
    for code, count in out_count[:10]:
        name = graph["pages"].get(code, {}).get("name", "?")
        lines.append(f"- `{code}` ({count} links out) — {name}")

    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Build backlink graph from markdown")
    parser.add_argument("--source", default=".", help="Root dir to scan (default cwd)")
    parser.add_argument("--no-svg", action="store_true", help="Skip SVG generation")
    parser.add_argument("--output-dir", default="dist")
    args = parser.parse_args()

    root = Path(args.source).resolve()
    print(f"📡 Scanning {root}...")

    graph = scan_directory(root)

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    json_out = out_dir / "backlink-graph.json"
    json_out.write_text(json.dumps(graph, indent=2, ensure_ascii=False))
    print(f"✓ JSON → {json_out}")

    md_out = out_dir / "backlink-summary.md"
    md_out.write_text(format_summary_md(graph))
    print(f"✓ Summary → {md_out}")

    if not args.no_svg:
        try:
            # Optional: graphviz if installed
            import subprocess

            dot_content = "digraph G {\n  rankdir=LR;\n"
            for source, targets in graph["forward"].items():
                for t in targets:
                    dot_content += f'  "{source}" -> "{t}";\n'
            dot_content += "}\n"

            dot_file = out_dir / "backlink.dot"
            dot_file.write_text(dot_content)
            svg_out = out_dir / "backlink-graph.svg"
            subprocess.run(["dot", "-Tsvg", str(dot_file), "-o", str(svg_out)], check=True, timeout=30)
            print(f"✓ SVG → {svg_out}")
        except (FileNotFoundError, subprocess.CalledProcessError):
            print("⚠️  graphviz not installed, skip SVG (brew install graphviz)")

    print(f"\n📊 {len(graph['pages'])} pages, {sum(len(v) for v in graph['forward'].values())} links, {len(graph['unresolved'])} unresolved")
    return 0


if __name__ == "__main__":
    sys.exit(main())
