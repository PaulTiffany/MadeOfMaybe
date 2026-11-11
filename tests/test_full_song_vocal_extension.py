"""Actual 53-event source and first two converter words survive integration."""
import unittest
from life.core import evolve,place
from life.full_song_vocal_extension import (
    episodes,native_pulse_cells,parts,TARGET,LAST_VERIFY_G,
    quantize_make,quantize_erase)

class FullSunoVocalSingerTests(unittest.TestCase):
    def test_original_stem_53_physical_make_erase_episodes(self):
        es=episodes()
        self.assertEqual(len(es),53)
        self.assertEqual((es[0].physical_make_g,es[-1].physical_erase_g),
                         (672,44850))
        self.assertEqual(len(native_pulse_cells()),795)
        self.assertEqual(LAST_VERIFY_G,44862)

    def test_all_original_actor_components_except_replaced_four_event_v(self):
        ps=parts()
        self.assertEqual(tuple(map(len,ps)),(6408,742,0,52,1372,795))
        self.assertEqual(sum(map(len,ps)),9369)
        self.assertEqual(len(set().union(*ps)),9369)
        self.assertEqual(TARGET,(991,-933))

    def test_true_B3S23_rearm_for_first_three_suno_vocal_episodes(self):
        from life.glider_controlled_mouth import (
            block_make_at,block_erase_at,rotate)
        from life.full_song_vocal_extension import MAKE_DIR,ERASE_DIR,BLOCK
        source=set()
        for ep in episodes()[:3]:
            source |= place(rotate(block_make_at(ep.physical_make_g),MAKE_DIR),
                            *TARGET)
            source |= place(rotate(block_erase_at(ep.physical_erase_g),ERASE_DIR),
                            *TARGET)
        reads={ep.physical_make_g+2:(ep.index,True) for ep in episodes()[:3]}
        reads.update({ep.physical_erase_g+4:(ep.index,False)
                      for ep in episodes()[:3]})
        for g in range(max(reads)+1):
            if g in reads:
                _,on=reads[g]
                self.assertEqual(place(BLOCK,*TARGET)<=source,on,
                                 f'physical B3/S23 lip wrong at g{g}')
            if g<max(reads):source=evolve(source)

if __name__=='__main__':unittest.main()
