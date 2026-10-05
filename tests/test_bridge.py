import importlib.machinery
import importlib.util
import json
import os
import tempfile
import time
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
loader = importlib.machinery.SourceFileLoader('bridge', str(ROOT / 'cc-bridge'))
spec = importlib.util.spec_from_loader(loader.name, loader)
bridge = importlib.util.module_from_spec(spec)
loader.exec_module(bridge)


def message(kind, text):
    content = text if kind == 'user' else [{'type': 'text', 'text': text}]
    return json.dumps({'type': kind, 'timestamp': '2026-10-05T12:00:00Z',
                       'message': {'content': content}}, ensure_ascii=False) + '\n'


class BridgeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.project = self.base / 'project'
        self.project.mkdir()
        self.transcript = self.project / 'session.jsonl'
        self.output = self.base / 'logs'
        self.state = self.base / 'state.json'
        self.patches = mock.patch.multiple(bridge, PROJECTS_DIR=self.project,
                                          LOG_DIR=self.output, STATE_FILE=self.state)
        self.patches.start()
        self.addCleanup(self.patches.stop)

    def log_text(self):
        return '\n'.join(p.read_text() for p in self.output.glob('*.md'))

    def test_complete_exchange_and_incremental_resume(self):
        self.transcript.write_text(message('user', 'Unicode café 日本語') +
                                   message('assistant', 'Answer one') + message('user', 'Next question'))
        bridge.main()
        self.assertIn('Unicode café 日本語', self.log_text())
        self.assertIn('Answer one', self.log_text())
        self.assertNotIn('Next question', self.log_text())
        bridge.main()
        self.assertEqual(self.log_text().count('Answer one'), 1)
        with self.transcript.open('a') as stream:
            stream.write(message('assistant', 'Answer two') + message('user', 'Third'))
        bridge.main()
        self.assertEqual(self.log_text().count('Answer two'), 1)

    def test_stale_last_exchange_flushes(self):
        self.transcript.write_text(message('user', 'Question') + message('assistant', 'Final answer'))
        bridge.main()
        self.assertFalse(self.output.exists())
        old = time.time() - bridge.STALE_THRESHOLD_SECS - 1
        os.utime(self.transcript, (old, old))
        bridge.main()
        self.assertIn('Final answer', self.log_text())
        bridge.main()
        self.assertEqual(self.log_text().count('Final answer'), 1)

    def test_partial_jsonl_record_is_retried(self):
        text = message('user', 'Partial question')
        self.transcript.write_text(text[:30])
        bridge.main()
        self.assertEqual(json.loads(self.state.read_text())['last_position'], 0)
        with self.transcript.open('a') as stream:
            stream.write(text[30:] + message('assistant', 'Recovered answer') + message('user', 'Next'))
        bridge.main()
        self.assertIn('Recovered answer', self.log_text())

    def test_truncated_transcript_restarts(self):
        self.transcript.write_text(message('user', 'First' * 300) + message('assistant', 'Old') + message('user', 'Pending'))
        bridge.main()
        self.transcript.write_text(message('user', 'New') + message('assistant', 'Recovered') + message('user', 'End'))
        bridge.main()
        self.assertIn('Recovered', self.log_text())

    def test_nonobject_records_are_skipped(self):
        self.transcript.write_text('null\n[]\n' + message('user', 'Question') +
                                   message('assistant', 'Answer') + message('user', 'Next'))
        bridge.main()
        self.assertIn('Answer', self.log_text())

    def test_source_filters_and_truncation(self):
        self.assertIsNone(bridge.extract_user_text({'isMeta': True, 'message': {'content': 'Context'}}))
        self.assertIsNone(bridge.extract_user_text({'message': {'content': [{'type': 'tool_result', 'content': 'result'}]}}))
        self.assertIsNone(bridge.extract_assistant_text({'message': {'content': [{'type': 'thinking', 'thinking': 'private'}]}}))
        self.assertEqual(bridge.truncate('a' * 5, 3), 'aaa\n\n[...truncated]')

    def test_missing_project_and_bad_state(self):
        bridge.main()
        self.assertFalse(self.state.exists())
        for value in ['{broken', '[]', '{"last_position": -1}', '{"last_position": "wrong"}', '{"last_position": true}']:
            self.state.write_text(value)
            self.assertEqual(bridge.load_state()['last_position'], 0)
        (self.project / 'subagent').mkdir()
        (self.project / 'subagent' / 'child.jsonl').write_text(message('user', 'Nested'))
        self.assertIsNone(bridge.find_active_transcript())


if __name__ == '__main__':
    unittest.main(verbosity=2)
