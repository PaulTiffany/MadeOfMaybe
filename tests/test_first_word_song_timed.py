"""First moving word appears at the ORIGINAL Suno karaoke tick, not g6000."""
import unittest
from pathlib import Path
from life.core import evolve,place
from life.first_word_song_timed import (
    routes,components,universe,final_eaters,ONSET_G,CLEARANCE_END_G,
    STATION_X0,DELAY_REDUCTION
)
from life.full_song_karaoke import compile_plan,GPS
from life.lyric_cues import read_alignment
from life.compact_full_word_mesh import expected_word

FIXTURE=Path(__file__).resolve().parents[1]/'data'/'first_verse_alignment_fixture.json'

class FirstWordSongTimedTests(unittest.TestCase):
    def test_exact_suno_first_word_and_35_true_lwss_phases(self):
        plan=compile_plan(read_alignment(FIXTURE))
        self.assertEqual((plan[0].words[0].text,plan[0].words[0].make_g),('WE',ONSET_G))
        self.assertEqual((GPS,ONSET_G,CLEARANCE_END_G,STATION_X0),(192,2156,3500,152))
        self.assertEqual(DELAY_REDUCTION,887)
        rs=routes()
        self.assertEqual(len(rs),35)
        self.assertEqual((min(r.source_delay_4gens for r in rs),
                          max(r.source_delay_4gens for r in rs)),(3,489))
        for r in rs:
            travel=(ONSET_G-r.output_reference_generation)//4
            self.assertEqual(r.station_x-43-2*travel,r.final_x)
            self.assertEqual(r.station_y+12,r.final_y)
        self.assertEqual(len(expected_word()),420)

    def test_real_g0_hardware_and_77_eaters(self):
        self.assertEqual(len(components()),36)
        self.assertEqual(len(universe()),1519)
        self.assertEqual(len(final_eaters()),539)
        self.assertEqual(evolve(final_eaters()),final_eaters())
        self.assertEqual(len(universe(omit_index=34)),1510)
        self.assertEqual(len(final_eaters(omit_index=34)),558)
        with self.assertRaises(ValueError):components(omit_index=35)

if __name__=='__main__':unittest.main()
