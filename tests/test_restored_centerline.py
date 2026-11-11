import unittest
from life.core import evolve,place
from life.glider_controlled_mouth import BLOCK
from life.restored_centerline import START_LINE,QUALIFICATION_END,components,universe
from life.symmetric_full_mouth import target_blocks,POSE_SAMPLES

class RestoredCenterLineTests(unittest.TestCase):
    def test_full_universe_coupling_with_real_glider_reconstruction(self):
        parts=components(True)
        world=universe(True)
        fixed=set().union(*(cells for k,cells in parts.items()
                            if k in ('eyes_nose','outline','bubble_outline','bubble_lyrics')))
        for g in range(QUALIFICATION_END):
            self.assertEqual(world,set().union(*parts.values()),f'cross component at gen {g}')
            self.assertTrue(fixed<=world,f'face or bubble changed at gen {g}')
            if g==60:
                for pos in START_LINE:self.assertTrue(place(BLOCK,*pos)<=world,pos)
            if g in (180,288,420,540,680):
                for pos in START_LINE:self.assertFalse(place(BLOCK,*pos)<=world,(g,pos))
            if g==960:
                for pos in START_LINE:self.assertTrue(place(BLOCK,*pos)<=world,pos)
            if g in POSE_SAMPLES:
                self.assertTrue(target_blocks(POSE_SAMPLES[g]) <= world,(g,POSE_SAMPLES[g]))
            world=evolve(world)
            parts={k:evolve(v) for k,v in parts.items()}

if __name__=='__main__':unittest.main()
