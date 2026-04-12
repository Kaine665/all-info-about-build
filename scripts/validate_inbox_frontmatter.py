#!/usr/bin/env python3
"""
Validate YAML frontmatter of inbox Markdown entries against inbox/schema/frontmatter.schema.json.
Also checks required level-2 headings: ## 上下文, ## 正文.
"""

from __future__ import annotations

import datetime as dt
import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError as e:  # pragma: no cover
    print("Missing dependency: pyyaml. Install with: pip install pyyaml", file=sys.stderr)
    raise SystemExit(2) from e

try:
    from jsonschema import Draft202012Validator
except ImportError as e:  # pragma: no cover
    print("Missing dependency: jsonschema. Install with: pip install jsonschema", file=sys.stderr)
    raise SystemExit(2) from e


REPO_ROOT = Path(__file__).resolve().parents[1]
INBOX = REPO_ROOT / "inbox"
SCHEMA_PATH = REPO_ROOT / "inbox" / "schema" / "frontmatter.schema.json"

# Index / agent instructions / copy-paste template — not validated as entries.
SKIP_NAMES = frozenset({"README.md", "AGENT.md", "_TEMPLATE.md"})


def normalize_yaml_dates(obj: object) -> object:
    """PyYAML may parse YYYY-MM-DD as datetime.date; JSON Schema expects string."""
    if isinstance(obj, dict):
        return {k: normalize_yaml_dates(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [normalize_yaml_dates(x) for x in obj]
    if isinstance(obj, dt.datetime):
        return obj.strftime("%Y-%m-%d")
    if isinstance(obj, dt.date):
        return obj.strftime("%Y-%m-%d")
    return obj


def split_frontmatter(text: str) -> tuple[dict | None, str, str | None]:
    """
    Returns (meta_dict, body, error_message).
    """
    if not text.startswith("---"):
        return None, text, "file must start with YAML frontmatter (---)"
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if not m:
        return None, text, "missing closing --- for frontmatter"
    raw_yaml = m.group(1)
    body = text[m.end() :]
    try:
        loaded = yaml.safe_load(raw_yaml)
    except yaml.YAMLError as e:
        return None, body, f"invalid YAML in frontmatter: {e}"
    if loaded is None:
        loaded = {}
    if not isinstance(loaded, dict):
        return None, body, "frontmatter YAML must parse to a mapping (object)"
    return normalize_yaml_dates(loaded), body, None


def check_headings(body: str) -> list[str]:
    errors: list[str] = []
    if "## 上下文" not in body:
        errors.append('body must contain heading "## 上下文"')
    if "## 正文" not in body:
        errors.append('body must contain heading "## 正文"')
    return errors


def iter_inbox_markdown_files() -> list[Path]:
    if not INBOX.is_dir():
        return []
    out: list[Path] = []
    for p in sorted(INBOX.rglob("*.md")):
        if p.name in SKIP_NAMES:
            continue
        out.append(p)
    return out


def main() -> int:
    if not SCHEMA_PATH.is_file():
        print(f"Schema not found: {SCHEMA_PATH}", file=sys.stderr)
        return 2

    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)

    files = iter_inbox_markdown_files()
    if not files:
        print("No inbox Markdown files to validate (excluding README/AGENT/_TEMPLATE).")
        return 0

    exit_code = 0
    for path in files:
        rel = path.relative_to(REPO_ROOT)
        text = path.read_text(encoding="utf-8")
        meta, body, err = split_frontmatter(text)
        if err:
            print(f"{rel}: {err}", file=sys.stderr)
            exit_code = 1
            continue
        assert meta is not None
        for v_err in validator.iter_errors(meta):
            print(f"{rel}: frontmatter schema: {v_err.message}", file=sys.stderr)
            exit_code = 1
        for h_err in check_headings(body):
            print(f"{rel}: {h_err}", file=sys.stderr)
            exit_code = 1

    if exit_code == 0:
        print(f"OK: validated {len(files)} inbox file(s).")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
