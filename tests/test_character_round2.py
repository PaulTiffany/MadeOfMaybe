"""Character round 2: native Life hair, timed eyebrow accent, and iris wink."""
from __future__ import annotations
import unittest
from life.core import evolve,place,parse_rle
from life.glider_controlled_mouth import BLOCK
from life.character_round2 import (
    components,universe,prepared_character_art,expressivity_signals,
    BROW_ROUTES,WINK_ROUTES,QUALIFICATION_END,
)
from life.expressive_mouth import LINE_CELLS
from life.symmetric_full_mouth import target_blocks
from life.styled_singer import components as base_components
from life.export_operational import compact_rle


class CharacterRound2Qualification(unittest.TestCase):
    def test_real_still_life_hair_and_eyeliner(self):
        art=prepared_character_art()
        for name,cells in art.items():
            with self.subTest(name=name):
                self.assertEqual(evolve(set(cells)),set(cells))
                self.assertEqual(len(cells)%4,0)
        self.assertGreater(len(art['art_hair_mass'])//4,650)
        self.assertGreater(len(art['art_hair_waves'])//4,350)
        self.assertGreaterEqual(len(art['art_jewelry'])//4,16)
        self.assertGreater(len(art['art_eye_liner'])//4,45)
        self.assertGreater(len(art['art_brows'])//4,30)

    def test_added_signals_really_make_and_erase_life_blocks(self):
        parts=expressivity_signals()
        self.assertEqual(len(parts),6)
        for key,seed in parts.items():
            self.assertGreater(len(seed),4)
            cells=set(seed)
            positions=BROW_ROUTES if key.startswith('right_brow_lift') else WINK_ROUTES
            target=positions[int(key.rsplit('_',1)[1])][0]
            tile=place(BLOCK,*target)
            expected={60:False,180:False,288:True,420:True,540:False,680:False,960:False} if key.startswith('right_brow_lift') else {60:True,180:True,288:True,420:True,540:False,680:True,960:True}
            for gen in range(QUALIFICATION_END):
                if gen in expected:
                    self.assertEqual(tile<=cells,expected[gen],(key,gen))
                cells=evolve(cells)
            if key.startswith('right_brow_lift'):
                self.assertEqual(cells,set(),key)
            else:
                self.assertEqual(cells,tile,key)

    def test_bubble_and_original_mouth_routes_unmodified(self):
        old=base_components(True)
        updated=components(True)
        for name in ('bubble_outline','bubble_lyrics','pulsar'):
            self.assertEqual(updated[name],old[name],name)
        for name in old:
            if name.startswith(('upper_','lower_','line_')):
                self.assertEqual(updated[name],old[name],name)
        self.assertNotIn('left_eye_glint',updated)

    def test_rle_is_exact_generation_zero_world(self):
        initial=universe(True)
        rle=compact_rle(initial,('native Life round 2',))
        rebuilt=parse_rle(rle)
        minx=min(x for x,y in initial);miny=min(y for x,y in initial)
        self.assertEqual(rebuilt,{(x-minx,y-miny) for x,y in initial})

    def test_exact_980_generation_whole_world_independence(self):
        parts=components(True)
        world=universe(True)
        self.assertGreaterEqual(len(parts),68)
        fixed=set().union(*(p for k,p in parts.items() if k.startswith('art_')))
        for gen in range(QUALIFICATION_END):
            self.assertEqual(world,set().union(*parts.values()),f'unexpected cross-component interaction g{gen}')
            self.assertTrue(fixed<=world,f'artwork changed g{gen}')
            if gen in (60,180,288,420,540,680,960):
                brow=[place(BLOCK,*item[0])<=world for item in BROW_ROUTES]
                iris=[place(BLOCK,*item[0])<=world for item in WINK_ROUTES]
                self.assertEqual(brow,[gen in (288,420)]*3,(gen,'brow'))
                self.assertEqual(iris,[gen!=540]*3,(gen,'wink'))
                if gen in (288,680):
                    self.assertTrue(target_blocks('open')<=world,gen)
                if gen in (60,960):
                    self.assertTrue(LINE_CELLS<=world,gen)
            world=evolve(world)
            parts={k:evolve(v) for k,v in parts.items()}


if __name__=='__main__':unittest.main()
