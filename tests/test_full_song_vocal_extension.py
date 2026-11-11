"""Preserve every original 20-second native singer part and add two V tiles."""
import unittest
from life.core import evolve,place
from life.full_song_vocal_extension import (
    later_vocal_episodes,native_lip_gliders,components,TARGETS,
    TARGET_MODES,quantize_make,quantize_erase,LAST_NATIVE_G)

class PreservedSingerExtendedVTests(unittest.TestCase):
    def test_original_stem_43_later_source_episodes(self):
        ev=later_vocal_episodes()
        self.assertEqual(len(ev),43)
        self.assertEqual((ev[0].source_index,ev[0].physical_make_g),(10,4992))
        self.assertEqual((ev[-1].source_index,ev[-1].physical_erase_g),(52,44850))
        self.assertEqual(LAST_NATIVE_G,44862)

    def test_preserve_first20_actor_and_every_existing_source(self):
        from life.two_line_native_singer import components as old
        ps=components()
        old_parts=old(900,144)
        self.assertEqual(tuple(ps[:5]),tuple(old_parts))
        self.assertEqual(tuple(map(len,ps)),(6408,742,240,52,1372,645,645))
        self.assertEqual(len(set().union(*ps)),10104)
        self.assertEqual(TARGETS,{'medium_0':(991,-933),'open_1':(1046,-862)})

    def test_actual_B3S23_pulse_make_erase_for_first_two_later_episodes(self):
        from life.glider_controlled_mouth import (
             BLOCK,ROUTING,rotate,block_make_at,block_erase_at)
        for name in ('medium_0','open_1'):
            bank,index=TARGET_MODES[name]
            _,md,ed=ROUTING[bank,index]
            target=TARGETS[name]
            state=set()
            records=later_vocal_episodes()[:2]
            for e in records:
                state |= place(rotate(block_make_at(e.physical_make_g),md),*target)
                state |= place(rotate(block_erase_at(e.physical_erase_g),ed),*target)
            checkpoints={e.physical_make_g+2:True for e in records}
            checkpoints.update({e.physical_erase_g+4:False for e in records})
            for g in range(max(checkpoints)+1):
                if g in checkpoints:
                    self.assertEqual(place(BLOCK,*target)<=state,checkpoints[g],
                        f'wrong physical lip signal {name} at g{g}')
                if g<max(checkpoints):state=evolve(state)

if __name__=='__main__':unittest.main()
