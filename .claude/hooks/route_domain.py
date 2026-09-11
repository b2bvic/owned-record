#!/usr/bin/env python3
"""Emit domain candidate paths for UserPromptSubmit.

Never read _context.md bodies. Retrieval stays a model or user step.
"""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path
from typing import Any

CONFIG_REL = ".agent-oversight/domains.json"
HOOK_EVENT = "UserPromptSubmit"
_WORD_CHAR = r"\w"


def pointer(
    status: str,
    candidates: list[dict[str, str]] | None = None,
    error: str | None = None,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "status": status,
        "context_loaded": False,
        "candidates": candidates or [],
    }
    if error:
        payload["error"] = error
    return payload


def keyword_matches(prompt: str, keyword: str) -> bool:
    token = keyword.strip()
    if not token:
        return False
    pattern = rf"(?<![{_WORD_CHAR}]){re.escape(token)}(?![{_WORD_CHAR}])"
    return re.search(pattern, prompt, flags=re.IGNORECASE) is not None


def _is_relative_to(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def confined_path(root: Path, configured: str) -> str | None:
    """Return a vault-relative posix path if configured stays inside root.

    Uses metadata and realpath only. Does not read file bodies.
    """
    if not isinstance(configured, str):
        return None
    configured = configured.strip()
    if not configured or "\x00" in configured:
        return None
    try:
        root_res = root.resolve()
    except (OSError, RuntimeError):
        return None
    raw = Path(configured)
    if raw.is_absolute():
        return None
    candidate = root_res / raw
    try:
        resolved = candidate.resolve()
    except (OSError, RuntimeError):
        return None
    if not _is_relative_to(resolved, root_res) or resolved == root_res:
        return None
    return resolved.relative_to(root_res).as_posix()


def load_domains(config_path: Path) -> tuple[list[Any] | None, str | None]:
    if not config_path.is_file():
        return None, "missing config"
    try:
        data = json.loads(config_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        return None, "invalid config"
    if not isinstance(data, dict):
        return None, "invalid config"
    domains = data.get("domains")
    if not isinstance(domains, list):
        return None, "invalid config"
    return domains, None


def route(prompt: str, vault_root: str | Path) -> dict[str, Any]:
    root = Path(vault_root).resolve()
    if not root.is_dir():
        return pointer("error", error="invalid root")
    config = root / CONFIG_REL
    if not _is_relative_to(config.resolve(), root):
        return pointer("error", error="path escape")
    domains, err = load_domains(config)
    if err:
        return pointer("error", error=err)
    if not domains:
        return pointer("error", error="invalid config")
    candidates = []
    names = set()
    for domain in domains:
        if not isinstance(domain, dict):
            return pointer("error", error="invalid config")
        name, path, keywords = domain.get("name"), domain.get("path"), domain.get("keywords")
        if (not isinstance(name, str) or not name.strip() or name.casefold() in names
                or not isinstance(path, str) or not isinstance(keywords, list)
                or any(not isinstance(k, str) or not k.strip() for k in keywords)):
            return pointer("error", error="invalid config")
        names.add(name.casefold())
        confined = confined_path(root, path)
        if confined is None:
            return pointer("error", error="path escape")
        folder = root / confined
        if folder.is_file():
            return pointer("error", error="domain path must select a directory")
        for filename in ("_context.md", "_log.md"):
            if not _is_relative_to((folder / filename).resolve(), root):
                return pointer("error", error="path escape")
        if any(keyword_matches(prompt, keyword) for keyword in keywords):
            candidates.append({"name": name.strip(), "path": confined,
                               "context": f"{confined}/_context.md", "log": f"{confined}/_log.md"})
    status = "matched" if len(candidates) == 1 else "ambiguous" if candidates else "unmatched"
    return pointer(status, candidates)


def parse_stdin(raw: str) -> tuple[str | None, str | None, str | None]:
    if raw is None or not str(raw).strip():
        return None, None, "invalid stdin"
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return None, None, "invalid stdin"
    if not isinstance(data, dict):
        return None, None, "invalid stdin"
    prompt = data.get("prompt")
    if not isinstance(prompt, str):
        return None, None, "invalid stdin"
    cwd = data.get("cwd")
    cwd_s = cwd if isinstance(cwd, str) and cwd.strip() else None
    return prompt, cwd_s, None


def resolve_vault_root(env_project_dir: str | None, stdin_cwd: str | None) -> str:
    if env_project_dir and env_project_dir.strip():
        return env_project_dir
    if stdin_cwd and stdin_cwd.strip():
        return stdin_cwd
    return os.getcwd()


def route_from_stdin(
    raw: str, env_project_dir: str | None = None
) -> dict[str, Any]:
    prompt, cwd, err = parse_stdin(raw)
    if err:
        return pointer("error", error=err)
    return route(prompt, resolve_vault_root(env_project_dir, cwd))


def hook_payload(result: dict[str, Any]) -> dict[str, Any]:
    return {
        "hookSpecificOutput": {
            "hookEventName": HOOK_EVENT,
            "additionalContext": json.dumps(result, indent=2),
        }
    }


def main() -> int:
    raw = sys.stdin.read()
    env_dir = os.environ.get("CLAUDE_PROJECT_DIR")
    result = route_from_stdin(raw, env_dir)
    json.dump(hook_payload(result), sys.stdout)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception:
        json.dump(
            hook_payload(pointer("error", error="internal error")),
            sys.stdout,
        )
        sys.stdout.write("\n")
        raise SystemExit(0)
