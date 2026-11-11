"""Regression: bubble starts blank; existing redirector genuinely turns inside it."""
import unittest
from life.core import evolve,place
from life.relocated_singer_anchor import SINGER_TRANSLATION,static_bubble
from life.blank_bubble_redirector import (
    bubble_outline,existing_redirector,persistent_hardware,components,
    universe,source_report,OUTPUT_G)

class BlankBubbleRedirectorTests(unittest.TestCase):
    def test_static_words_removed_and_physical_entry_notch_stable(self):
        old=place(static_bubble(),-SINGER_TRANSLATION[0],-SINGER_TRANSLATION[1])
        self.assertEqual(len(old),1144)
        self.assertEqual(len(bubble_outline()),668)
        self.assertEqual(evolve(bubble_outline()),set(bubble_outline()))
    def test_same_19_cell_turner_in_one_real_universe(self):
        self.assertEqual(len(existing_redirector()),49)
        base,turner=components()
        self.assertFalse(base&turner)
        self.assertEqual(len(universe()),8619)
        self.assertEqual(len(persistent_hardware()),21)
    def test_exact_one_shot_converts_vertical_input_to_horizontal_ship(self):
        result=source_report()
        self.assertEqual(result['source_turn_generation'],OUTPUT_G)
        self.assertEqual(result['output_position'],(417,-110))
        self.assertTrue(result['same_19_cell_turner'])
        self.assertFalse(result['full_song_integrated'])

if __name__=='__main__':unittest.main()
