"""Real fast native LWSS eater, not cinematic drawn text."""
import unittest
from life.core import evolve,place
from life.phrase_crawler_eater import LWSS,EATER_LEFT
from life.full_song_lwss_readhead import (
    motion_phases,layout,verify_train_geometry,PITCH,
    row_events,singer_parts,full_word_plan)

class FullSongLWSSReadhead(unittest.TestCase):
    def test_period_four_native_WEST_ship(self):
        self.assertEqual(len(LWSS),9)
        self.assertEqual(len(EATER_LEFT),7)
        self.assertEqual(evolve(set(motion_phases()[3])),place(LWSS,-2,0))
    def test_true_eater_clears_dense_24_ship_pixel_trains(self):
        # A much denser test than the old 36-cell pitch: genuine B3/S23
        # ship launches eight cells apart, only 16 generations between hits.
        for pitch in (8,12,16):
            w=set(EATER_LEFT)
            for j in range(24):w|=place(LWSS,pitch*j,0)
            for g in range(2*pitch*23+96):w=evolve(w)
            self.assertEqual(w,set(EATER_LEFT),(pitch,len(w)))
    def test_full_original_suno_403_words_compose_without_g0_overlaps(self):
        report=verify_train_geometry()
        self.assertEqual(report['Suno_sung_words_total'],403)
        self.assertEqual(report['prepositioned_output_WEST_LWSS_words'],401)
        self.assertEqual(report['prepositioned_output_WEST_LWSS_pixels'],10317)
        self.assertEqual(len(full_word_plan()),403)
        self.assertEqual(len(layout()[0]),401)
        self.assertEqual(report['physical_rounded_bubble_cells'],0)
        self.assertFalse(report['actual_90_degree_converters_for_all_403_words'])
        self.assertFalse(report['full_song_WV_lips_physically_wired'])

if __name__=='__main__':unittest.main()
