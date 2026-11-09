"""Verifies the one-board composition against separately evolved components."""
import unittest
from life.core import evolve,parse_rle,encode_rle
from life.composition import components,face,bubble_parts,scene
from life.catalog import CATALOG,pattern
from life.singer_pilot import APPARATUS,MOUTH_BLOCK

class CompositionTests(unittest.TestCase):
    def test_still_lifes_stable_and_separate(self):
        border,words=bubble_parts()
        for part in (face(),border,words,border|words):
            self.assertEqual(evolve(part),part)
        self.assertFalse(face() & border)
        self.assertFalse(border & words)
        self.assertFalse(face() & words)

    def test_catalog_oscillators(self):
        for name in ('pulsar','heart','smiley'):
            with self.subTest(name=name):
                s=start=pattern(name)
                for _ in range(CATALOG[name]['period']):
                    s=evolve(s)
                self.assertEqual(s,start)

    def test_gosper_emits(self):
        s=start=pattern('gosper_gun')
        self.assertEqual(len(start),36)
        for _ in range(240):
            s=evolve(s)
        self.assertGreater(max(x for x,y in s),max(x for x,y in start))

    def test_entire_scene_independent_for_610_generations(self):
        independent=components()
        actual=scene()
        for gen in range(610):
            self.assertEqual(actual,set().union(*independent.values()),gen)
            if gen in (170,362,554):
                self.assertEqual(MOUTH_BLOCK.issubset(actual),gen!=362)
            independent={name:evolve(cells) for name,cells in independent.items()}
            actual=evolve(actual)

    def test_actuator_quiescence(self):
        cells=components()['mouth_actuator']
        for _ in range(575):
            cells=evolve(cells)
        self.assertEqual(cells,APPARATUS|MOUTH_BLOCK)
        self.assertEqual(evolve(cells),cells)

    def test_rle_roundtrip(self):
        original=scene()
        recovered=parse_rle(encode_rle(original,['Scene']))
        x0=min(x for x,y in original);y0=min(y for x,y in original)
        self.assertEqual(recovered,{(x-x0,y-y0) for x,y in original})

if __name__=='__main__':
    unittest.main()
