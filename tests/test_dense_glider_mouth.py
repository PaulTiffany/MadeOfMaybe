"""Exact qualified 785-generation B3/S23 replay for denser singer."""
import unittest
from life.core import evolve,place,parse_rle
from life.dense_glider_mouth import (
    BLOCK,FULL_DURATION,POSE_SAMPLES,UPPER_LIP,
    DENSE_MEDIUM_TARGETS,DENSE_OPEN_TARGETS,
    prepared_art,active_pixels,signal_components,components,universe,
)
from life.composition import bubble_parts,symbol
from life.export_operational import compact_rle

class DenseSingerTests(unittest.TestCase):
    def test_new_lip_density_and_permanent_still_lifes(self):
        self.assertEqual(len(DENSE_MEDIUM_TARGETS),10)
        self.assertEqual(len(DENSE_OPEN_TARGETS),13)
        self.assertEqual(len(set(DENSE_MEDIUM_TARGETS)),10)
        self.assertEqual(len(set(DENSE_OPEN_TARGETS)),13)
        self.assertFalse(set(DENSE_MEDIUM_TARGETS)&set(DENSE_OPEN_TARGETS))
        face,upper=map(set,prepared_art())
        self.assertGreater(len(upper),len(UPPER_LIP))
        self.assertEqual(evolve(face),face)
        self.assertEqual(evolve(upper),upper)
        self.assertEqual(evolve(face|upper),face|upper)
        self.assertFalse(face&upper)
        for pose in ('medium','open'):
            pixels=active_pixels(pose)
            self.assertEqual(evolve(pixels),pixels)
            self.assertFalse(pixels&(face|upper))

    def test_785_independent_generations_and_holdable_skips(self):
        parts=components();world=universe()
        face,upper=map(set,prepared_art())
        constant=face|upper|parts['bubble_outline']|parts['bubble_lyrics']
        self.assertEqual(len(signal_components()),23)
        for g in range(FULL_DURATION):
            self.assertEqual(world,set().union(*parts.values()),g)
            self.assertTrue(constant<=world,g)
            if g in POSE_SAMPLES:
                pose=POSE_SAMPLES[g]
                medium=sum(place(BLOCK,*p)<=world for p in DENSE_MEDIUM_TARGETS)
                opened=sum(place(BLOCK,*p)<=world for p in DENSE_OPEN_TARGETS)
                self.assertEqual((medium,opened),
                  (10 if pose=='medium' else 0,13 if pose=='open' else 0),
                  (g,pose))
            if 550<=g<=778:
                self.assertFalse(any(place(BLOCK,*p)<=world
                                for p in DENSE_MEDIUM_TARGETS),g)
            world=evolve(world)
            parts={name:evolve(cells) for name,cells in parts.items()}

    def test_existing_bubble_is_translated_not_rebuilt(self):
        parts=components()
        outline,letters=bubble_parts()
        self.assertEqual(parts['bubble_outline'],place(outline,160,-90))
        self.assertEqual(parts['bubble_lyrics'],place(letters,160,-90))
        self.assertEqual(parts['pulsar'],place(symbol(),300,90))
        self.assertEqual(evolve(parts['bubble_outline']),parts['bubble_outline'])
        self.assertEqual(evolve(parts['bubble_lyrics']),parts['bubble_lyrics'])

    def test_golly_rle_exact_initial_condition_roundtrip(self):
        original=universe()
        restored=parse_rle(compact_rle(original,('DENSE B3/S23',)))
        x0=min(x for x,y in original);y0=min(y for x,y in original)
        self.assertEqual(restored,{(x-x0,y-y0) for x,y in original})

if __name__=='__main__':unittest.main()
