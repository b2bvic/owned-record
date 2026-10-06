import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "voice-calibration.sh"

class HookTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.calls = self.base / "calls"
        self.result = self.base / "result"
        self.result.write_text('Sample "quoted" context\nsecond line')
        self.qmd = self.base / "qmd"
        self.qmd.write_text('#!/bin/sh\nprintf "%s\\n" "$*" >> "$TEST_CALLS"\ncat "$TEST_RESULT"\n')
        self.qmd.chmod(0o755)
        self.state = self.base / "cache"
        self.env = dict(os.environ, QMD_BIN=str(self.qmd),
                        TEST_CALLS=str(self.calls), TEST_RESULT=str(self.result),
                        MEMORY_STATE_DIR=str(self.state), VOICE_STATE_DIR=str(self.state),
                        LEDGER_DB=str(self.base / "missing.db"))

    def invoke(self, payload):
        proc = subprocess.run(["bash", str(SCRIPT)], input=payload if isinstance(payload, str) else json.dumps(payload),
                              text=True, capture_output=True, env=self.env)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(proc.stderr, "")
        return json.loads(proc.stdout)["hookSpecificOutput"] if proc.stdout else None

    def test_invalid_input_is_silent(self):
        for payload in ['{invalid', '{}', '[]']:
            self.assertIsNone(self.invoke(payload))
        self.assertFalse(self.calls.exists())

    def test_missing_search_is_silent(self):
        self.env["QMD_BIN"] = str(self.base / "missing-command")
        self.assertIsNone(self.invoke(self.payload()))

    def test_no_results_can_retry(self):
        self.result.write_text("No results found.")
        self.assertIsNone(self.invoke(self.payload()))
        self.result.write_text("Owned Markdown context")
        self.assertIsNotNone(self.invoke(self.payload()))

    def test_session_id_cannot_escape_cache(self):
        payload = self.payload()
        payload["session_id"] = "../../escape"
        self.assertIsNotNone(self.invoke(payload))
        self.assertFalse((self.base / "escape").exists())
        self.assertTrue(all(p.parent == self.state for p in self.state.iterdir()))
        self.assertTrue(all(len(p.name.split('.')[0]) == 64 for p in self.state.iterdir()))

    def test_corrupt_throttle_is_ignored(self):
        self.assertIsNotNone(self.invoke(self.payload()))
        for path in self.state.iterdir():
            if not path.name.endswith('.hash'):
                path.write_text('broken')
        self.refresh_input()
        self.assertIsNotNone(self.invoke(self.payload()))

    def payload(self):
        return {"tool_name": "Write", "session_id": "test", "tool_input": {"file_path": "Journal.md"}}

    def refresh_input(self):
        pass

    def test_genre_throttle_and_context(self):
        payload = self.payload()
        output = self.invoke(payload)
        self.assertEqual(output["hookEventName"], "PreToolUse")
        self.assertIn('Sample "quoted" context', output["additionalContext"])
        self.assertIsNone(self.invoke(payload))
        payload["tool_input"]["file_path"] = "Correspondence/draft.md"
        self.assertIsNotNone(self.invoke(payload))
        self.assertEqual(len(self.calls.read_text().splitlines()), 2)

    def test_tools_and_paths_are_filtered(self):
        payload = self.payload()
        payload["tool_name"] = "Read"
        self.assertIsNone(self.invoke(payload))
        payload["tool_name"] = "Edit"
        payload["tool_input"]["file_path"] = "src/main.py"
        self.assertIsNone(self.invoke(payload))
        self.assertFalse(self.calls.exists())

if __name__ == "__main__":
    unittest.main(verbosity=2)
