"""Exact 785-generation qualification of mirrored full-mouth Life scene."""
import unittest
from life.core import evolve,place
from life.dense_glider_mouth import BLOCK,FULL_DURATION,POSE_SAMPLES
from life.symmetric_full_mouth import (
    reflect,MEDIUM_TARGETS,OPEN_TARGETS,REST_LINE,
    signal_components,prepared_art,target_blocks,components,universe
)
class SymmetricSingerTests(unittest.TestCase):
    def test_symmetry_and_stable_rest(self):
        self.assertEqual(reflect(reflect(REST_LINE)),set(REST_LINE))
        self.assertEqual(evolve(set(REST_LINE)),set(REST_LINE))
        self.assertEqual(len(MEDIUM_TARGETS),7)
        self.assertEqual(len(OPEN_TARGETS),13)
        for state in ('medium','open'):
            b=target_blocks(state)
            self.assertEqual(b,reflect(b))
            self.assertEqual(evolve(b),b)

    def test_fixed_eyes_and_outline_survive(self):
        outline,eyes=map(set,prepared_art())
        self.assertGreater(len(eyes),0)
        self.assertEqual(evolve(outline),outline)
        self.assertEqual(evolve(eyes),eyes)
        self.assertEqual(evolve(eyes|outline|REST_LINE),eyes|outline|REST_LINE)

    def test_mouth_and_bubble_all_independent_785_generations(self):
        parts=components()
        world=universe()
        self.assertEqual(len(signal_components()),40)
        outline,eyes=map(set,prepared_art())
        fixed=outline|eyes|REST_LINE|parts['bubble_outline']|parts['bubble_lyrics']
        for gen in range(FULL_DURATION):
            self.assertEqual(world,set().union(*parts.values()),gen)
            self.assertTrue(fixed<=world,gen)
            if 550<=gen<=778:
                self.assertFalse(any(place(BLOCK,*p)<=world for p in MEDIUM_TARGETS),gen)
                self.assertFalse(any(reflect(place(BLOCK,*p))<=world for p in MEDIUM_TARGETS),gen)
            if gen in POSE_SAMPLES:
                state=POSE_SAMPLES[gen]
                mm=sum(place(BLOCK,*p)<=world for p in MEDIUM_TARGETS)
                oo=sum(place(BLOCK,*p)<=world for p in OPEN_TARGETS)
                self.assertEqual(mm,7 if state=='medium' else 0,(gen,state))
                self.assertEqual(oo,13 if state=='open' else 0,(gen,state))
                self.assertTrue(target_blocks(state)<=world,(gen,state))
            world=evolve(world)
            parts={k:evolve(v) for k,v in parts.items()}
if __name__=='__main__':
    unittest.main()
