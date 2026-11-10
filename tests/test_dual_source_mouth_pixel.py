"""One native Life world per 2-source combination; no camera lip hacks."""
import unittest
from life.core import evolve
from life.glider_controlled_mouth import UPPER_LIP
from life.dual_source_mouth_pixel import seed,state,qualify
class NativeVocalMouthPilotTests(unittest.TestCase):
    def test_four_real_B3S23_worlds(self):
        r=qualify()
        self.assertEqual(set(r['four_source_truth_table_cases']),{'00','01','10','11'})
        self.assertTrue(r['real_four_pixel_medium_bank'])
        self.assertTrue(r['real_four_pixel_open_bank'])
        self.assertFalse(r['repeatable_priority_gate_qualified'])
    def test_voice_sustain_with_no_word_oscillates_real_mouth_lips(self):
        r=qualify()['four_source_truth_table_cases']
        for name in ('01','11'):
            self.assertTrue(r[name]['checkpoint_poses'][180]['medium'])
            self.assertTrue(r[name]['checkpoint_poses'][288]['open'])
            self.assertTrue(r[name]['checkpoint_poses'][420]['medium'])
            self.assertTrue(r[name]['checkpoint_poses'][680]['open'])
        for name in ('00','10'):
            self.assertFalse(r[name]['checkpoint_poses'][680]['open'])
        self.assertTrue(r['10']['checkpoint_poses'][180]['word_accent'])
        self.assertFalse(r['01']['checkpoint_poses'][180]['word_accent'])
    def test_existing_upper_lip_stays_native_still_life(self):
        for word in (False,True):
            for voice in (False,True):
                self.assertTrue(UPPER_LIP<=seed(word,voice))
    def test_full_two_source_input_eventually_cleans_to_upper_lip_only(self):
        cells=seed(True,True)
        for _ in range(784):cells=evolve(cells)
        self.assertEqual(cells,set(UPPER_LIP))
if __name__=='__main__':unittest.main()
