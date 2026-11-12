import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from avatar_plan.core import plan, validate

EXAMPLE = Path(__file__).parents[1] / 'examples' / 'synthetic_plan.json'


class PreflightTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(EXAMPLE.read_text())

    def test_example_declarations_valid_not_generation(self):
        result = plan(self.data)
        self.assertEqual(result['status'], 'declarations_valid')
        self.assertIn('No generation performed', result['warning'])

    def test_no_consent_blocks(self):
        self.data['subject']['consent_reviewed'] = False
        self.assertEqual(plan(self.data)['status'], 'blocked')
        self.assertEqual(plan(self.data)['steps'], [])

    def test_string_true_not_boolean(self):
        self.data['subject']['consent_reviewed'] = 'true'
        self.assertTrue(validate(self.data))

    def test_network_blocks(self):
        self.data['runtime']['network_allowed'] = True
        self.assertTrue(validate(self.data))

    def test_unsafe_paths(self):
        for path in ('../secret.mp4', '/tmp/a.mp4', 'https://site/a.mp4',
                     'C:\\data\\a.mp4', './a.mp4', 'a//b.mp4', 'a/../b.mp4',
                     'a\x00.mp4', '', 'no_extension'):
            with self.subTest(path=path):
                self.data['media']['reference_video'] = path
                self.assertTrue(validate(self.data))

    def test_memory_blocks(self):
        self.data['runtime']['gpu_memory_gib'] = 4
        self.assertTrue(validate(self.data))

    def test_revision_must_be_pinned(self):
        self.data['components'][0]['revision'] = 'main'
        self.assertTrue(validate(self.data))

    def test_commercial_review_required(self):
        self.data['purpose'] = 'commercial'
        self.assertTrue(validate(self.data))
        self.data['components'][0]['commercial_use_allowed'] = True
        self.assertEqual(validate(self.data), [])

    def test_no_license_review(self):
        self.data['components'][0]['license_reviewed'] = False
        self.assertTrue(validate(self.data))

    def test_generated_audio_requires_voice(self):
        self.data['media']['audio_origin'] = 'generated'
        self.assertTrue(validate(self.data))
        voice = copy.deepcopy(self.data['components'][0])
        voice['role'] = 'voice'
        self.data['components'].append(voice)
        self.assertEqual(validate(self.data), [])
        self.assertEqual(len(plan(self.data)['steps']), 5)

    def test_duplicate_roles(self):
        self.data['components'].append(copy.deepcopy(self.data['components'][0]))
        self.assertTrue(validate(self.data))

    def test_unknown_fields(self):
        self.data['secret'] = 'accidental-config'
        self.assertTrue(validate(self.data))

    def test_invalid_roots_and_shapes(self):
        for invalid in (None, [], 'text', 5, {}, {'subject': []}):
            with self.subTest(invalid=invalid):
                self.assertTrue(validate(invalid))

    def test_duration_limits(self):
        for duration in (True, 0, -1, 31, 10 ** 1000, float('nan'), float('inf'), '15'):
            with self.subTest(duration=duration):
                self.data['media']['duration_seconds'] = duration
                self.assertTrue(validate(self.data))

    def test_missing_required_key(self):
        del self.data['media']['audio_origin']
        self.assertTrue(validate(self.data))

    def test_cli_success(self):
        result = subprocess.run([sys.executable, '-m', 'avatar_plan', str(EXAMPLE)],
                                text=True, capture_output=True)
        self.assertEqual(result.returncode, 0)
        self.assertEqual(json.loads(result.stdout)['status'], 'declarations_valid')

    def test_cli_bad_json(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'invalid.json'
            for content in ('{', '{"number": NaN}'):
                path.write_text(content)
                result = subprocess.run([sys.executable, '-m', 'avatar_plan', str(path)],
                                        text=True, capture_output=True)
                self.assertEqual(result.returncode, 2)
                self.assertEqual(json.loads(result.stdout)['status'], 'input_error')

    def test_cli_missing_file(self):
        result = subprocess.run([sys.executable, '-m', 'avatar_plan', 'does-not-exist.json'],
                                text=True, capture_output=True)
        self.assertEqual(result.returncode, 2)


if __name__ == '__main__':
    unittest.main()
