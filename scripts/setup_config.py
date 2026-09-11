#!/usr/bin/env python3
"""Personalize the vault and merge domain config.

Writes .agent-oversight/domains.json. Does not rewrite hook scripts.
Refuses to overwrite existing custom state.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path
from typing import Any

DEFAULT_DOMAINS = [
    {
        "name": "Work",
        "path": "01 - Work",
        "keywords": ["project", "deadline", "meeting", "standup", "sprint"],
    },
    {
        "name": "Personal",
        "path": "02 - Personal",
        "keywords": ["family", "health", "budget", "journal", "home"],
    },
]

PLACEHOLDERS = (
    "{{PROJECT_NAME}}",
    "{{YOUR_NAME}}",
    "{{ONE_LINE_DESCRIPTION}}",
)

NUMBERED = re.compile(r"^(\d{2}) - ")
TABLE_NOTE = "> Add more domains"


def today() -> str:
    current = date.today()
    return f"{current.year:04d}.{current.month:02d}.{current.day:02d}"


def parse_keywords(raw: Any) -> list[str]:
    if isinstance(raw, list):
        return [item.strip() for item in raw if isinstance(item, str) and item.strip()]
    if isinstance(raw, str):
        return [item.strip() for item in raw.split(",") if item.strip()]
    return []


def safe_domain_name(name: str) -> bool:
    if not name or not name.strip():
        return False
    if any(char in name for char in ("/", "\\", "\x00")):
        return False
    stripped = name.strip()
    if stripped in {".", ".."}:
        return False
    if ".." in stripped:
        return False
    return True


def load_domains_file(path: Path) -> tuple[dict[str, Any], bool]:
    """Return (data, existed). Refuse to clobber unreadable custom state."""
    if not path.is_file():
        return {"domains": [dict(item) for item in DEFAULT_DOMAINS]}, False
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise SystemExit(
            "Refusing to overwrite unreadable .agent-oversight/domains.json"
        ) from exc
    if not isinstance(data, dict) or not isinstance(data.get("domains"), list):
        raise SystemExit(
            "Refusing to overwrite custom .agent-oversight/domains.json"
        )
    return data, True


def next_domain_number(root: Path, domains: list[Any]) -> int:
    number = 3
    if root.is_dir():
        for child in root.iterdir():
            match = NUMBERED.match(child.name)
            if match:
                number = max(number, int(match.group(1)) + 1)
    for domain in domains:
        if not isinstance(domain, dict):
            continue
        path = str(domain.get("path") or "")
        match = NUMBERED.match(Path(path).as_posix())
        if match:
            number = max(number, int(match.group(1)) + 1)
    return number


def personalize_claude(path: Path, project: str, name: str, description: str) -> bool:
    if not path.is_file():
        return False
    text = path.read_text(encoding="utf-8")
    if not any(token in text for token in PLACEHOLDERS):
        return False
    text = text.replace("{{PROJECT_NAME}}", project)
    text = text.replace("{{YOUR_NAME}}", name)
    text = text.replace("{{ONE_LINE_DESCRIPTION}}", description)
    path.write_text(text, encoding="utf-8")
    return True


def table_has_domain(text: str, name: str) -> bool:
    return f"| **{name}** |" in text


def insert_table_row(text: str, name: str, rel_path: str, keywords: list[str]) -> str:
    if table_has_domain(text, name):
        return text
    row = f"| **{name}** | `{rel_path}` | {', '.join(keywords)} |"
    if TABLE_NOTE in text:
        return text.replace(TABLE_NOTE, row + "\n" + TABLE_NOTE, 1)
    return text


def write_context_files(folder: Path, name: str) -> None:
    folder.mkdir(parents=True, exist_ok=True)
    context_path = folder / "_context.md"
    log_path = folder / "_log.md"
    if not context_path.exists() and not context_path.is_symlink():
        context_path.write_text(
            f"# {name} Context\n\n"
            f"last_verified:: {today()}\n\n"
            f"Your {name} domain. Customize this file with current state and priorities.\n\n"
            f"## Current State\n\n"
            f"- (Add your current {name} priorities here)\n",
            encoding="utf-8",
        )
    if not log_path.exists() and not log_path.is_symlink():
        log_path.write_text(
            f"# {name} Log\n\n"
            f"Activity log for the {name} domain.\n\n"
            f"---\n\n"
            f"(Entries will appear here as you work.)\n",
            encoding="utf-8",
        )


def apply_extras(root: Path, extras: list[Any]) -> bool:
    config_dir = root / ".agent-oversight"
    config_path = config_dir / "domains.json"
    data, existed = load_domains_file(config_path)
    domains = data["domains"]
    existing_names = {
        item.get("name").casefold()
        for item in domains
        if isinstance(item, dict) and isinstance(item.get("name"), str)
    }
    number = next_domain_number(root, domains)
    claude_path = root / "CLAUDE.md"
    claude_text = claude_path.read_text(encoding="utf-8") if claude_path.is_file() else None
    original_claude = claude_text
    added = False

    for extra in extras:
        if not isinstance(extra, dict):
            continue
        name = extra.get("name")
        if not isinstance(name, str) or not safe_domain_name(name):
            continue
        name = name.strip()
        keywords = parse_keywords(extra.get("keywords", name))
        if not keywords:
            keywords = [name]
        if name.casefold() in existing_names:
            for item in domains:
                if isinstance(item, dict) and str(item.get("name", "")).casefold() == name.casefold():
                    rel = item.get("path")
                    if isinstance(rel, str):
                        folder = root / rel
                        if _folder_is_inside(root, folder):
                            write_context_files(folder, name)
                    break
            continue
        folder_name = f"{number:02d} - {name}"
        rel_path = folder_name
        folder = root / folder_name
        if not _folder_is_inside(root, folder):
            continue
        write_context_files(folder, name)
        domains.append({"name": name, "path": rel_path, "keywords": keywords})
        existing_names.add(name.casefold())
        added = True
        if claude_text is not None:
            claude_text = insert_table_row(claude_text, name, rel_path + "/_context.md", keywords)
        number += 1

    if not existed:
        config_dir.mkdir(parents=True, exist_ok=True)
        config_path.write_text(
            json.dumps(data, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
    elif added:
        config_path.write_text(
            json.dumps(data, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )

    if (
        claude_path.is_file()
        and claude_text is not None
        and original_claude is not None
        and claude_text != original_claude
    ):
        claude_path.write_text(claude_text, encoding="utf-8")
    return added or not existed


def _folder_is_inside(root: Path, folder: Path) -> bool:
    try:
        root_res = root.resolve()
        folder_res = folder.resolve()
        folder_res.relative_to(root_res)
        return True
    except (OSError, RuntimeError, ValueError):
        return False


def load_extras(raw: str) -> list[Any]:
    if not raw:
        return []
    path = Path(raw)
    if path.is_file():
        text = path.read_text(encoding="utf-8")
    else:
        text = raw
    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        raise SystemExit("Invalid extras JSON") from exc
    if not isinstance(data, list):
        raise SystemExit("Extras must be a JSON list")
    return data


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Write vault domain config")
    parser.add_argument("--root", required=True)
    parser.add_argument("--name", required=True)
    parser.add_argument("--project", required=True)
    parser.add_argument("--description", required=True)
    parser.add_argument("--extras", default="")
    args = parser.parse_args(argv)
    root = Path(args.root).resolve()
    if not root.is_dir():
        print(f"Root is not a directory: {root}", file=sys.stderr)
        return 1
    extras = load_extras(args.extras)
    # Validate every write destination before replacing template placeholders.
    for relative in ("CLAUDE.md", ".agent-oversight", ".agent-oversight/domains.json"):
        if not _folder_is_inside(root, root / relative):
            raise SystemExit("Refusing a setup path outside the vault")
    load_domains_file(root / ".agent-oversight/domains.json")
    personalize_claude(root / "CLAUDE.md", args.project, args.name, args.description)
    apply_extras(root, extras)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
