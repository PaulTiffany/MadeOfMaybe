"""Physical moving-phrase and reusable fishhook qualification."""
import unittest
from life.core import evolve
from life.phrase_crawler_eater import (LWSS,EATER_LEFT,EATERS,initial_world,
                                      qualify,expected_clearance_g)

class PhraseCrawlerEaterTests(unittest.TestCase):
    def test_eater_one_swallows_single_left_moving_lwss(self):
        live=set(EATER_LEFT)|set(LWSS)
        self.assertEqual(len(EATER_LEFT),7)
        for g in range(40):live=evolve(live)
        self.assertEqual(live,set(EATER_LEFT))

    def test_actual_blank_cells_encode_a_phrase_break(self):
        world,p=initial_world(('WE MADE','A WINDOW'),gap_g=192)
        self.assertEqual(p[0].glyph_ship_count,107)
        self.assertEqual(p[0].right_x,324)
        self.assertEqual(p[1].left_x,426)
        self.assertEqual(p[1].blank_space_cells,101)
        self.assertEqual(len(EATERS),56)
        self.assertEqual(expected_clearance_g(p),1692)
        self.assertGreater(len(world),2000)

    def test_complete_native_train_ends_at_exactly_original_eaters(self):
        report=qualify(('WE MADE','A WINDOW'),gap_g=192)
        self.assertTrue(report['reusable_eaters_restored'])
        self.assertTrue(report['exact_native_row_independence'])
        self.assertEqual(report['final_population'],56)
        self.assertEqual(report['native_start_stop_marker_ships'],4)
        self.assertFalse(report['cue_markers_operate_color_switch'])
        self.assertFalse(report['whole_universe_extinguished'])

    def test_ablate_start_stop_markers_without_changing_letter_lane(self):
        with_markers,_=initial_world(('WE MADE',),with_markers=True)
        no_markers,_=initial_world(('WE MADE',),with_markers=False)
        self.assertEqual(len(with_markers-no_markers),18)
        self.assertEqual(no_markers-with_markers,set())

    def test_invalid_phrases_and_gaps_are_rejected(self):
        with self.assertRaises(ValueError):initial_world(('WE MADE',),gap_g=3)
        with self.assertRaises(ValueError):initial_world(())
        with self.assertRaises(ValueError):initial_world(('@@@',))

if __name__=='__main__':unittest.main()
