import copy
import json
from pathlib import Path
import unittest
from avatar_plan.audit import audit, changed_paths, fingerprint, unique_object


class AuditTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((Path(__file__).parents[1] / 'examples/synthetic_plan.json').read_text())

    def test_order_independent_hash(self):
        self.assertEqual(fingerprint({'a': 1, 'b': 2}), fingerprint({'b': 2, 'a': 1}))

    def test_change_changes_hash(self):
        self.assertNotEqual(fingerprint({'a': 1}), fingerprint({'a': 2}))

    def test_duplicate_keys_rejected(self):
        with self.assertRaises(ValueError):
            json.loads('{"a":1,"a":2}', object_pairs_hook=unique_object)

    def test_comparison_has_paths_not_values(self):
        previous = copy.deepcopy(self.data)
        self.data['media']['audio'] = 'private/new.wav'
        comparison = audit(self.data, previous)['comparison']
        self.assertEqual(comparison['changed_paths'], ['/media/audio'])
        self.assertTrue(comparison['review_required'])
        self.assertNotIn('private/new.wav', json.dumps(comparison))

    def test_identical_no_new_review(self):
        self.assertFalse(audit(self.data, self.data)['comparison']['review_required'])

    def test_blocked_still_fingerprinted(self):
        self.data['subject']['consent_reviewed'] = False
        result = audit(self.data)
        self.assertEqual(result['status'], 'blocked')
        self.assertEqual(len(result['provenance']['manifest_sha256']), 64)

    def test_pointer_escaping_and_types(self):
        self.assertEqual(changed_paths({'a/b~': True}, {'a/b~': 1}), ['/a~1b~0'])

    def test_list_addition(self):
        self.assertEqual(changed_paths([1], [1, 2]), ['/1'])

    def test_nonfinite_hash_rejected(self):
        with self.assertRaises(ValueError):
            fingerprint({'x': float('nan')})

class AuditCliTests(unittest.TestCase):
    def test_compare_cli(self):
        import subprocess
        import sys
        root = Path(__file__).parents[1]
        example = str(root / 'examples/synthetic_plan.json')
        proc = subprocess.run([sys.executable, '-m', 'avatar_plan', example, '--compare', example], cwd=root, capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0)
        self.assertEqual(json.loads(proc.stdout)['comparison']['changed_paths'], [])

    def test_duplicate_cli_rejected(self):
        import subprocess
        import sys
        import tempfile
        with tempfile.TemporaryDirectory() as folder:
            file = Path(folder) / 'duplicate.json'
            file.write_text('{"schema_version":1,"schema_version":2}')
            proc = subprocess.run([sys.executable, '-m', 'avatar_plan', str(file)], cwd=Path(__file__).parents[1], capture_output=True, text=True)
            self.assertEqual(proc.returncode, 2)
            self.assertEqual(json.loads(proc.stdout)['status'], 'input_error')
