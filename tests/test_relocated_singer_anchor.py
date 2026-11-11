"""Physical placement (not optical only), word cues and singer clearance."""
import unittest
from life.core import place
from life.relocated_singer_anchor import (
    TRANSLATION,RELOCATED_SPLITTER_LOCAL,relocated_anchor,
    qualified_integration,universe)
from life.reusable_word_cue import seed as original_word

class RelocatedSingerAnchorTests(unittest.TestCase):
    def test_source_hardware_moved_not_only_camera(self):
        self.assertEqual(RELOCATED_SPLITTER_LOCAL,(420,120))
        self.assertEqual(TRANSLATION,(983,-369))
        self.assertEqual(relocated_anchor(),place(original_word(),983,-369))
        self.assertGreater(len(universe()),6800)
    def test_actual_3403_generation_integration(self):
        r=qualified_integration()
        self.assertEqual(r['catalyst_cells'],84)
        self.assertTrue(r['controller_is_physically_below_real_bubble'])
        self.assertTrue(r['static_portrait_and_bubble_unchanged'])
        self.assertTrue(r['two_cell_spacetime_clearance'])
        self.assertEqual(r['real_life_generations_replayed'],3403)
        self.assertTrue(r['checkpoints'][2156]['word_live'])
        self.assertFalse(r['checkpoints'][2578]['word_live'])
        self.assertTrue(r['checkpoints'][2976]['word_live'])
        self.assertFalse(r['checkpoints'][3402]['word_live'])
        self.assertFalse(r['new_mouth_expression_fanout_connected'])

if __name__=='__main__':unittest.main()
