import unittest
from pathlib import Path
from life.causal_layout_limit import audit,report
FIXTURE=Path(__file__).resolve().parents[1]/'data'/'first_verse_alignment_fixture.json'

class CausalLayoutLimitTests(unittest.TestCase):
    def test_second_sparse_stage_violates_even_native_speed_of_light(self):
        a,b=audit(FIXTURE)
        self.assertTrue(a.single_g0_source_causally_possible)
        self.assertFalse(b.single_g0_source_causally_possible)
        self.assertGreater(b.distance_L_infty,b.maximum_life_cone_sum)
        self.assertEqual(b.word_generation,2976)
        self.assertGreater(b.distance_L_infty,10_000)

    def test_report_limits_claim_to_one_localized_generation_zero_source(self):
        r=report(FIXTURE)
        self.assertEqual(r['word_line_count'],2)
        self.assertEqual(r['lines_exceeding_absolute_causality_bound'],1)
        self.assertIn('generation zero',r['scope'])
        self.assertIn('distributed',r['does_not_refute'])

if __name__=='__main__':unittest.main()
