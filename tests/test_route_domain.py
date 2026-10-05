import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

HOOK = Path(__file__).resolve().parents[1] / 'route-domain.sh'


class RoutingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(dir=HOOK.parent, prefix='.test-route demo ')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def context(self, domain, text):
        path = self.root / domain / '_context.md'
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)

    def run_hook(self, prompt):
        env = dict(os.environ, CLAUDE_PROJECT_DIR=str(self.root), CLAUDE_USER_PROMPT=prompt)
        run = subprocess.run(['bash', str(HOOK)], env=env, capture_output=True, text=True, check=True)
        return json.loads(run.stdout)['hookSpecificOutput']['additionalContext'] if run.stdout else ''

    def test_native_hook_reads_stdin_prompt_without_legacy_environment(self):
        self.context('01 - Work', 'native-hook-example')
        env = dict(os.environ, CLAUDE_PROJECT_DIR=str(self.root))
        env.pop('CLAUDE_USER_PROMPT', None)
        data = json.dumps({'hook_event_name': 'UserPromptSubmit', 'prompt': 'release'})
        result = subprocess.run(['bash', str(HOOK)], env=env, input=data,
                                capture_output=True, text=True, check=True)
        output = json.loads(result.stdout)['hookSpecificOutput']
        self.assertEqual(output['hookEventName'], 'UserPromptSubmit')
        self.assertIn('native-hook-example', output['additionalContext'])

    def test_invalid_native_hook_input_does_not_load_context(self):
        self.context('01 - Work', 'native-hook-example')
        env = dict(os.environ, CLAUDE_PROJECT_DIR=str(self.root))
        env.pop('CLAUDE_USER_PROMPT', None)
        for payload in ['not-json', '{}', '{"prompt": ["release"]}']:
            result = subprocess.run(['bash', str(HOOK)], env=env, input=payload,
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, 1)
            self.assertEqual(result.stdout, '')

    def test_empty_and_unmatched_prompts_emit_no_context(self):
        self.context('01 - Work', 'private synthetic context')
        for prompt in ['', 'hello']:
            self.assertEqual(self.run_hook(prompt), '')

    def test_missing_context_emits_no_context(self):
        self.assertEqual(self.run_hook('release'), '')

    def test_case_insensitive_match_and_json_escaping(self):
        text = 'state:: "ready"\npath:: \\example\n'
        self.context('01 - Work', text)
        self.assertIn(text, self.run_hook('RELEASE review'))

    def test_multiple_matches_load_both_configured_files(self):
        self.context('01 - Work', 'work-example')
        self.context('03 - Personal', 'personal-example')
        output = self.run_hook('release budget')
        self.assertIn('work-example', output)
        self.assertIn('personal-example', output)

    def test_old_verification_date_emits_stale_warning(self):
        self.context('01 - Work', 'last_verified:: 2020.01.01\nstate:: example\n')
        self.assertIn('STALE CONTEXT', self.run_hook('release'))

    def test_invalid_verification_date_does_not_emit_stale_warning(self):
        self.context('01 - Work', 'last_verified:: not-a-date\n')
        self.assertNotIn('STALE CONTEXT', self.run_hook('release'))

    def test_previous_session_hint_without_reading_context(self):
        self.assertIn('Cross-Session Lookup', self.run_hook('previous session'))


if __name__ == '__main__':
    unittest.main()
