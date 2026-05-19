"""Render skills/ + docs/ với Jinja2 substitution → dist/.

Usage:
    python3 scripts/render.py                        # render toàn bộ
    python3 scripts/render.py --check                # CI mode, fail nếu render lỗi
    python3 scripts/render.py --file skills/01-x.md  # 1 file
    python3 scripts/render.py --watch                # dev mode
    python3 scripts/render.py --clean                # xóa dist/ trước
"""
from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path
from typing import Any

from jinja2 import (
    Environment,
    FileSystemLoader,
    StrictUndefined,
    TemplateError,
    UndefinedError,
)

from _common import load_config


class RenderError(Exception):
    """Raised khi render fails (placeholder thiếu, syntax error, etc.)."""


PAGE_CODE_RE = re.compile(r"^[A-Z]+-[A-Z0-9]+-[A-Z]+-\d{3}$")

# Subdirs trong skills/ và docs/ KHÔNG render (meta artifacts)
SKIP_SUBDIRS = {"superpowers", "drafts", ".git"}


def _filter_upper_dashed(s: str) -> str:
    """Validate & normalize page code."""
    s = s.strip().upper()
    if not PAGE_CODE_RE.match(s):
        raise RenderError(f"Invalid page code: {s!r}")
    return s


def _filter_wiki_link(url: str, label: str = "") -> str:
    """Format Lark URL as markdown link."""
    label = label or url
    return f"[{label}]({url})"


def build_env(loader_path: Path | None = None) -> Environment:
    """Build Jinja2 Environment với custom filters."""
    env = Environment(
        loader=FileSystemLoader(str(loader_path)) if loader_path else None,
        undefined=StrictUndefined,
        keep_trailing_newline=True,
        autoescape=False,
    )
    env.filters["upper_dashed"] = _filter_upper_dashed
    env.filters["wiki_link"] = _filter_wiki_link
    return env


def render_string(template_str: str, ctx: dict[str, Any]) -> str:
    """Render a template string with context. Raises RenderError on failures."""
    env = build_env()
    try:
        tmpl = env.from_string(template_str)
        return tmpl.render(**ctx)
    except (UndefinedError, TemplateError) as e:
        raise RenderError(str(e)) from e


def render_tree(src: Path, dst: Path, ctx: dict[str, Any]) -> int:
    """Render all .md files from src/ → dst/. Returns count rendered."""
    env = build_env(loader_path=src)
    dst.mkdir(parents=True, exist_ok=True)
    count = 0
    for md in src.rglob("*.md"):
        rel = md.relative_to(src)
        # Skip meta subdirs (docs/superpowers/, drafts/, etc.)
        if any(part in SKIP_SUBDIRS for part in rel.parts):
            continue
        try:
            tmpl = env.get_template(str(rel).replace("\\", "/"))
            out = tmpl.render(**ctx)
        except (UndefinedError, TemplateError) as e:
            raise RenderError(f"{md}: {e}") from e
        out_path = dst / rel
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(out)
        count += 1
    return count


def main() -> int:
    parser = argparse.ArgumentParser(description="Render wko templates")
    parser.add_argument("--check", action="store_true", help="CI dry-run mode")
    parser.add_argument("--file", help="Render single file")
    parser.add_argument("--watch", action="store_true", help="Re-render on change")
    parser.add_argument("--clean", action="store_true", help="rm -rf dist/ trước")
    parser.add_argument("--config", default="company.config.yaml")
    args = parser.parse_args()

    cfg = load_config(args.config)
    repo_root = Path(__file__).resolve().parent.parent
    dist = repo_root / "dist"

    if args.clean and dist.exists():
        shutil.rmtree(dist)
        print(f"🧹 Cleaned {dist}")

    if args.file:
        f = Path(args.file)
        out = render_string(f.read_text(), cfg)
        if not args.check:
            out_path = dist / f.relative_to(repo_root)
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(out)
            print(f"✓ {f} → {out_path}")
        else:
            print(out)
        return 0

    if args.watch:
        from watchdog.events import FileSystemEventHandler
        from watchdog.observers import Observer

        class Handler(FileSystemEventHandler):
            def on_modified(self, event):
                if event.src_path.endswith(".md"):
                    try:
                        skills_count = render_tree(
                            repo_root / "skills", dist / "skills", cfg
                        )
                        docs_count = render_tree(repo_root / "docs", dist / "docs", cfg)
                        print(f"♻️  Re-rendered ({skills_count}+{docs_count})")
                    except RenderError as e:
                        print(f"❌ {e}", file=sys.stderr)

        observer = Observer()
        for d in ("skills", "docs"):
            sub = repo_root / d
            if sub.exists():
                observer.schedule(Handler(), str(sub), recursive=True)
        observer.start()
        print("👀 Watching skills/ + docs/ (Ctrl+C để stop)")
        try:
            observer.join()
        except KeyboardInterrupt:
            observer.stop()
        return 0

    # Default: render all
    try:
        skills_count = (
            render_tree(repo_root / "skills", dist / "skills", cfg)
            if (repo_root / "skills").exists()
            else 0
        )
        docs_count = (
            render_tree(repo_root / "docs", dist / "docs", cfg)
            if (repo_root / "docs").exists()
            else 0
        )
    except RenderError as e:
        print(f"❌ {e}", file=sys.stderr)
        return 1

    if args.check:
        print(f"✅ Render check OK ({skills_count} skills, {docs_count} docs)")
    else:
        print(f"✓ Rendered {skills_count} skills, {docs_count} docs → {dist}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
