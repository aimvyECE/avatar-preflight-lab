import unittest
from avatar_plan.impact import review_impact, REVIEWS


class ImpactTests(unittest.TestCase):
    def test_no_change(self):
        self.assertEqual(review_impact([])['invalidated_reviews'], [])

    def test_disclosure_only(self):
        self.assertEqual(review_impact(['/subject/synthetic_disclosure'])['invalidated_reviews'], ['disclosure'])

    def test_audio_invalidates_downstream(self):
        result = review_impact(['/media/audio'])
        self.assertEqual(result['invalidated_reviews'], ['consent', 'voice', 'lipsync', 'human_qa', 'disclosure'])
        self.assertEqual(result['reasons']['human_qa'], ['/media/audio'])

    def test_reference_invalidates_consent(self):
        self.assertIn('consent', review_impact(['/media/reference_video'])['invalidated_reviews'])

    def test_component_replacement(self):
        reviews = review_impact(['/components/0/revision'])['invalidated_reviews']
        self.assertIn('licensing', reviews)
        self.assertIn('runtime', reviews)
        self.assertIn('human_qa', reviews)

    def test_unknown_fail_closed(self):
        for path in ('', '/purpose', '/schema_version', '/new_field', '/media/unknown'):
            self.assertEqual(review_impact([path])['invalidated_reviews'], list(REVIEWS))

    def test_stable_union(self):
        a = ['/media/audio', '/runtime/gpu_memory_gib']
        self.assertEqual(review_impact(a), review_impact(list(reversed(a)) + a))

    def test_parent_replacement(self):
        self.assertIn('consent', review_impact(['/subject'])['invalidated_reviews'])
        self.assertEqual(review_impact(['/media'])['invalidated_reviews'], list(REVIEWS))
