"""The real Suno stem observation is traceable but NOT a B3/S23 controller."""
import json,unittest
from pathlib import Path
from life.dual_channel_mouth_logic import time_to_g

MANIFEST=Path(__file__).resolve().parents[1]/'data'/'made_of_maybe_vocal_gate_take1_v0.json'
class QualifiedVocalGateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.m=json.loads(MANIFEST.read_text(encoding='utf8'))
    def test_provenance_and_unqualified_native_limits(self):
        m=self.m
        self.assertEqual(m['gate_episode_count'],53)
        self.assertEqual(len(m['intervals_seconds']),53)
        self.assertTrue(m['source_tag_verified'])
        self.assertFalse(m['dry_wet_separation_qualified'])
        self.assertFalse(m['native_B3S23_full_song_mouth_qualified'])
    def test_all_intervals_ordered_and_translatable_to_192_gps(self):
        previous=0
        for a,b in self.m['intervals_seconds']:
            self.assertLess(a,b);self.assertGreaterEqual(a,previous)
            self.assertEqual(time_to_g(a)%4,0)
            self.assertEqual(time_to_g(b)%4,0)
            previous=b
        self.assertEqual(self.m['intervals_seconds'][0][0],3.5)
        self.assertEqual(self.m['intervals_seconds'][-1][1],233.6)
    def test_qualified_diffuse_tails_are_not_treated_as_vocal_sustain(self):
        m=self.m
        self.assertEqual(len(m['diffuse_release_candidates_seconds']),9)
        for a,b in m['diffuse_release_candidates_seconds']:
            overlap=sum(max(0,min(b,d)-max(a,c)) for c,d in m['intervals_seconds'])
            self.assertAlmostEqual(overlap,0)
        self.assertEqual(m['diffuse_candidates_overlapping_gate'],0)
    def test_sensitivity_not_mistaken_for_phoneme_truth(self):
        m=self.m;values=m['threshold_sensitivity']
        self.assertEqual([x['relative_threshold'] for x in values],[.08,.1,.14,.18,.22,.3])
        self.assertGreater(values[0]['total_activity_s']-values[-1]['total_activity_s'],20)
        self.assertEqual(m['sample_lag_at_16000Hz_in_tested_windows'],[0]*5)
if __name__=='__main__':unittest.main()
