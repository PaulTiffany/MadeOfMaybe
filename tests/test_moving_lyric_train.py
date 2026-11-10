"""Moving typography proof, without asserting an unbuilt color switch."""
import unittest
from pathlib import Path
from life.core import evolve, place
from life.full_song_karaoke import compile_plan
from life.lyric_cues import read_alignment
from life.moving_lyric_train import (
    LWSS, seed, lit_ship_origins, native_motion_certificate,
    onset_gap_vs_word_extent,
)

FIXTURE = Path(__file__).resolve().parents[1]/'data'/'first_verse_alignment_fixture.json'

class MovingLyricTrainTests(unittest.TestCase):
    def test_single_pixel_is_a_real_moving_spaceship(self):
        one = set(LWSS)
        self.assertEqual(len(one), 9)
        for _ in range(4):
            one = evolve(one)
        self.assertEqual(one, place(LWSS, -2, 0))

    def test_whole_phrase_physically_moves_as_independent_spaceships(self):
        report = native_motion_certificate('WE MADE', steps=128)
        self.assertGreater(report['ships'], 100)
        self.assertTrue(report['all_ships_independent'])
        self.assertEqual(report['initial_cells'], 9 * report['ships'])
        self.assertTrue(report['exactly_translates_c2_orthogonal'])
        self.assertFalse(report['word_highlight_switch_implemented'])

    def test_48_generation_gap_cannot_fit_two_whole_words_on_one_rail(self):
        line = compile_plan(read_alignment(FIXTURE))[0]
        gap = onset_gap_vs_word_extent(line.words[0], line.words[1])
        self.assertEqual(gap['generations_between_word_onsets'], 48)
        self.assertEqual(gap['linear_cells_available_at_c2'], 24)
        self.assertEqual(gap['first_word_lwss_extent_cells'], 93)
        self.assertFalse(gap['one_rail_nonoverlap_possible'])

    def test_reject_unverified_packing(self):
        with self.assertRaises(ValueError):
            lit_ship_origins('WE', pitch=4)
        with self.assertRaises(ValueError):
            seed('©')

if __name__ == '__main__':
    unittest.main()
