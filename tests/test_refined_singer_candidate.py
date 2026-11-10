"""Narrower/lower glider-driven candidate; no karaoke linkage claim."""
import unittest
from life.core import evolve
from life.refined_singer_candidate import (
    qualified_layout,new_target_cells,seed)

class RefinedSingerCandidateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.q=qualified_layout()
    def test_real_mouth_and_cheeks_survive_980_generations(self):
        q=self.q
        self.assertEqual(q['native_generations_checked'],980)
        self.assertEqual(q['mouth_delta_y'],32)
        self.assertEqual(q['max_medium_half_width'],53)
        self.assertEqual(q['max_open_half_width'],49)
        self.assertTrue(q['native_dynamic_channel_independence'])
        self.assertTrue(q['strict_two_cell_spacetime_guard'])
        self.assertEqual(q['preserved_cheek_tiles'],9)
        self.assertGreater(q['preserved_art_cells'],6600)
        self.assertFalse(q['new_mouth_causal_lyric_bridge_qualified'])
        fixed=set().union(*q['art'].values())
        self.assertEqual(evolve(fixed),fixed)
    def test_native_pose_checkpoints(self):
        obs=self.q['checkpoint_poses']
        for g,state in ((180,'medium'),(288,'open'),(420,'medium'),(680,'open')):
            self.assertTrue(obs[g][state],(g,state))
        self.assertTrue(obs[60]['centerline'])
        self.assertTrue(obs[960]['centerline'])
        self.assertFalse(obs[540]['centerline'])
    def test_output_pixels_are_actual_stable_life_blocks(self):
        for state in ('medium','open'):
            cells=new_target_cells(state)
            self.assertEqual(evolve(cells),cells)
            self.assertGreater(len(cells),20)
        self.assertGreater(len(seed()),6600)

if __name__=='__main__':unittest.main()
