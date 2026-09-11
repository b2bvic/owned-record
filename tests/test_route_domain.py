#!/usr/bin/env python3
"""Isolated tests for candidate-path-only domain routing."""
from __future__ import annotations

import builtins
import json
import os
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
HOOKS = ROOT / ".claude" / "hooks"
sys.path.insert(0, str(HOOKS))
import route_domain  # noqa: E402

SENTINEL = "SECRET_SENTINEL_NEVER_IN_HOOK_OUTPUT_9f3c2a"


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def make_vault(tmp: Path, name: str = "vault") -> Path:
    vault = tmp / name
    (vault / "01 - Work").mkdir(parents=True)
    (vault / "02 - Personal").mkdir(parents=True)
    (vault / "01 - Work" / "_context.md").write_text(
        f"# Work Context\n{SENTINEL}\n", encoding="utf-8"
    )
    (vault / "02 - Personal" / "_context.md").write_text(
        f"# Personal Context\n{SENTINEL}\n", encoding="utf-8"
    )
    write_json(
        vault / ".agent-oversight" / "domains.json",
        {
            "domains": [
                {
                    "name": "Work",
                    "path": "01 - Work",
                    "keywords": [
                        "project",
                        "deadline",
                        "meeting",
                        "standup",
                        "sprint",
                    ],
                },
                {
                    "name": "Personal",
                    "path": "02 - Personal",
                    "keywords": [
                        "family",
                        "health",
                        "budget",
                        "journal",
                        "home",
                    ],
                },
            ]
        },
    )
    dest_hooks = vault / ".claude" / "hooks"
    dest_hooks.mkdir(parents=True)
    shutil.copy(HOOKS / "route-domain.sh", dest_hooks / "route-domain.sh")
    shutil.copy(HOOKS / "route_domain.py", dest_hooks / "route_domain.py")
    os.chmod(dest_hooks / "route-domain.sh", 0o755)
    return vault


def parse_hook_stdout(stdout: str) -> dict[str, Any]:
    payload = json.loads(stdout)
    extra = payload["hookSpecificOutput"]["additionalContext"]
    pointer = json.loads(extra)
    return pointer


def run_hook(
    vault: Path,
    prompt: str | None = None,
    *,
    cwd: Path | None = None,
    env_project_dir: Path | str | None = "VAULT",
    stdin_raw: str | None = None,
) -> subprocess.CompletedProcess[str]:
    hook = vault / ".claude" / "hooks" / "route-domain.sh"
    env = os.environ.copy()
    if env_project_dir == "VAULT":
        env["CLAUDE_PROJECT_DIR"] = str(vault)
    elif env_project_dir is None:
        env.pop("CLAUDE_PROJECT_DIR", None)
    else:
        env["CLAUDE_PROJECT_DIR"] = str(env_project_dir)
    if stdin_raw is None:
        stdin_raw = json.dumps(
            {"prompt": prompt, "cwd": str(cwd or vault)}
        )
    return subprocess.run(
        ["bash", str(hook)],
        input=stdin_raw,
        capture_output=True,
        text=True,
        env=env,
        cwd=str(cwd or vault),
        check=False,
    )


class RouteDomainTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        self.vault = make_vault(self.tmp, "vault dir")

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def test_matched_emits_candidate_path_not_body(self) -> None:
        proc = run_hook(self.vault, "review the sprint backlog")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        pointer = parse_hook_stdout(proc.stdout)
        self.assertEqual(pointer["status"], "matched")
        self.assertIs(pointer["context_loaded"], False)
        self.assertEqual(
            pointer["candidates"],
            [{"name": "Work", "path": "01 - Work", "context": "01 - Work/_context.md", "log": "01 - Work/_log.md"}],
        )
        self.assertNotIn(SENTINEL, proc.stdout)
        self.assertNotIn(SENTINEL, proc.stderr)

    def test_zero_context_body_reads_chmod_and_open_guard(self) -> None:
        work = self.vault / "01 - Work" / "_context.md"
        os.chmod(work, 0)
        try:
            opens: list[str] = []
            real_open = builtins.open

            def spy(path: Any, *args: Any, **kwargs: Any) -> Any:
                text = str(path)
                if text.endswith("_context.md"):
                    opens.append(text)
                return real_open(path, *args, **kwargs)

            with mock.patch("builtins.open", spy), mock.patch("io.open", spy):
                result = route_domain.route(
                    "review the sprint backlog", self.vault
                )
            self.assertEqual(opens, [])
            self.assertEqual(result["status"], "matched")
            self.assertIs(result["context_loaded"], False)
            self.assertNotIn(SENTINEL, json.dumps(result))

            proc = run_hook(self.vault, "review the sprint backlog")
            self.assertEqual(proc.returncode, 0, proc.stderr)
            pointer = parse_hook_stdout(proc.stdout)
            self.assertEqual(pointer["status"], "matched")
            self.assertNotIn(SENTINEL, proc.stdout)
        finally:
            os.chmod(work, stat.S_IRUSR | stat.S_IWUSR)

    def test_word_boundaries(self) -> None:
        sprinting = route_domain.route("sprinting later", self.vault)
        self.assertEqual(sprinting["status"], "unmatched")
        self.assertIs(sprinting["context_loaded"], False)

        projection = route_domain.route("the projection is off", self.vault)
        self.assertEqual(projection["status"], "unmatched")

        punct = route_domain.route("the Sprint.", self.vault)
        self.assertEqual(punct["status"], "matched")
        self.assertEqual(punct["candidates"][0]["name"], "Work")

        proc = run_hook(self.vault, "misprint in the journal")
        pointer = parse_hook_stdout(proc.stdout)
        self.assertEqual(pointer["status"], "matched")
        self.assertEqual(pointer["candidates"][0]["name"], "Personal")
        self.assertNotIn(SENTINEL, proc.stdout)

    def test_ambiguous(self) -> None:
        proc = run_hook(self.vault, "family sprint planning")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        pointer = parse_hook_stdout(proc.stdout)
        self.assertEqual(pointer["status"], "ambiguous")
        self.assertIs(pointer["context_loaded"], False)
        names = [item["name"] for item in pointer["candidates"]]
        self.assertEqual(names, ["Work", "Personal"])
        self.assertNotIn(SENTINEL, proc.stdout)
        self.assertNotIn(SENTINEL, json.dumps(pointer))

    def test_unmatched(self) -> None:
        pointer = route_domain.route("hello world", self.vault)
        self.assertEqual(pointer["status"], "unmatched")
        self.assertEqual(pointer["candidates"], [])
        self.assertIs(pointer["context_loaded"], False)

    def test_wrong_stdin(self) -> None:
        cases = [
            "",
            "{not json",
            "[]",
            '{"cwd": "/tmp"}',
            '{"prompt": null}',
            '{"prompt": 12}',
        ]
        for raw in cases:
            with self.subTest(raw=raw):
                proc = run_hook(self.vault, stdin_raw=raw)
                self.assertEqual(proc.returncode, 0, proc.stderr)
                pointer = parse_hook_stdout(proc.stdout)
                self.assertEqual(pointer["status"], "error")
                self.assertEqual(pointer["error"], "invalid stdin")
                self.assertIs(pointer["context_loaded"], False)
                self.assertEqual(pointer["candidates"], [])
                self.assertNotIn(SENTINEL, proc.stdout)

    def test_missing_config(self) -> None:
        shutil.rmtree(self.vault / ".agent-oversight")
        proc = run_hook(self.vault, "review the sprint backlog")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        pointer = parse_hook_stdout(proc.stdout)
        self.assertEqual(pointer["status"], "error")
        self.assertEqual(pointer["error"], "missing config")
        self.assertIs(pointer["context_loaded"], False)
        self.assertNotIn(SENTINEL, proc.stdout)

    def test_path_escape(self) -> None:
        outside = self.tmp / "outside"
        outside.mkdir()
        secret = outside / "_context.md"
        secret.write_text(SENTINEL, encoding="utf-8")
        write_json(
            self.vault / ".agent-oversight" / "domains.json",
            {
                "domains": [
                    {
                        "name": "Work",
                        "path": "../outside/_context.md",
                        "keywords": ["sprint"],
                    }
                ]
            },
        )
        proc = run_hook(self.vault, "sprint")
        pointer = parse_hook_stdout(proc.stdout)
        self.assertEqual(pointer["status"], "error")
        self.assertEqual(pointer["error"], "path escape")
        self.assertIs(pointer["context_loaded"], False)
        self.assertEqual(pointer["candidates"], [])
        self.assertNotIn(SENTINEL, proc.stdout)
        self.assertNotIn(str(secret), proc.stdout)

        write_json(
            self.vault / ".agent-oversight" / "domains.json",
            {
                "domains": [
                    {
                        "name": "Work",
                        "path": str(secret),
                        "keywords": ["sprint"],
                    }
                ]
            },
        )
        proc = run_hook(self.vault, "sprint")
        pointer = parse_hook_stdout(proc.stdout)
        self.assertEqual(pointer["status"], "error")
        self.assertEqual(pointer["error"], "path escape")
        self.assertNotIn(SENTINEL, proc.stdout)

    def test_symlink_escape(self) -> None:
        outside = self.tmp / "outside"
        outside.mkdir()
        secret = outside / "secret.md"
        secret.write_text(SENTINEL, encoding="utf-8")
        work = self.vault / "01 - Work" / "_context.md"
        work.unlink()
        work.symlink_to(secret)
        proc = run_hook(self.vault, "sprint")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        pointer = parse_hook_stdout(proc.stdout)
        self.assertEqual(pointer["status"], "error")
        self.assertEqual(pointer["error"], "path escape")
        self.assertIs(pointer["context_loaded"], False)
        self.assertEqual(pointer["candidates"], [])
        self.assertNotIn(SENTINEL, proc.stdout)
        self.assertNotIn(SENTINEL, proc.stderr)

    def test_stdin_cwd_and_project_dir(self) -> None:
        other = make_vault(self.tmp, "other vault")
        (other / "01 - Work" / "_context.md").write_text(
            "OTHER_BODY\n", encoding="utf-8"
        )
        proc = run_hook(
            self.vault,
            "sprint",
            cwd=other,
            env_project_dir=None,
        )
        pointer = parse_hook_stdout(proc.stdout)
        self.assertEqual(pointer["status"], "matched")
        self.assertEqual(pointer["candidates"][0]["path"], "01 - Work")
        self.assertNotIn("OTHER_BODY", proc.stdout)
        self.assertNotIn(SENTINEL, proc.stdout)

        proc = run_hook(
            self.vault,
            "sprint",
            cwd=other,
            env_project_dir=self.vault,
        )
        pointer = parse_hook_stdout(proc.stdout)
        self.assertEqual(pointer["status"], "matched")
        self.assertNotIn(SENTINEL, proc.stdout)

    def test_config_symlink_escape_and_invalid_map(self):
        config = self.vault / ".agent-oversight/domains.json"
        outside = self.tmp / "outside.json"
        outside.write_text(config.read_text())
        config.unlink()
        config.symlink_to(outside)
        self.assertEqual(route_domain.route("sprint", self.vault)["status"], "error")
        config.unlink()
        for domains in [[], [{"name": "Work"}], [
            {"name": "Work", "path": "01 - Work", "keywords": ["sprint"]},
            {"name": "work", "path": "02 - Personal", "keywords": ["home"]},
        ]]:
            write_json(config, {"domains": domains})
            self.assertEqual(route_domain.route("sprint", self.vault)["status"], "error")

    def test_settings_are_pointer_only(self) -> None:
        settings = json.loads(
            (ROOT / ".claude" / "settings.json").read_text(encoding="utf-8")
        )
        command = settings["hooks"]["UserPromptSubmit"][0]["hooks"][0]["command"]
        self.assertEqual(
            command,
            '"$CLAUDE_PROJECT_DIR/.claude/hooks/route-domain.sh"',
        )
        self.assertNotIn("PreToolUse", settings.get("hooks", {}))
        self.assertNotIn("permissions", settings)
        self.assertTrue((HOOKS / "pretool-memory.sh").is_file())


if __name__ == "__main__":
    unittest.main(verbosity=2)
