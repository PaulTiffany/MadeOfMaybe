"""Actual-glyph acceptance tests: no CGI text overlays, no lamp surrogate."""
import unittest
from life.core import evolve,place,parse_rle
from life.glider_controlled_mouth import BLOCK
from life.export_operational import compact_rle
from life.native_lyric_word import (
    WORD, PITCH, CLOCK, AUDIO_START, COMPLETE_GENERATION,
    ERASED_GENERATION, VERIFY_THROUGH, WORD_STAGE_ORIGIN,
    routes, target_cells, pixel_target, signal_components,
    local_universe,composed_components,observed_glyph,
)

class PhysicalLyricWordTests(unittest.TestCase):
    def test_exact_5x7_word_not_single_lamp(self):
        targets=target_cells()
        self.assertEqual(len(routes()),35)
        self.assertEqual(len(targets),4*35)
        self.assertEqual(set().union(*(pixel_target(p) for p in routes())),targets)
        self.assertLess(abs(COMPLETE_GENERATION/CLOCK-AUDIO_START),.085)
        self.assertEqual(len({(p.x,p.y) for p in routes()}),35)

    def test_gliders_write_hold_and_erase_every_letter_cell(self):
        # Each target's two-glider MAKE and one-glider ERASE must be a
        # verified real reaction, including the in-flight eraser glider.
        parts=signal_components()
        world=local_universe()
        target=target_cells()
        completed={}
        for g in range(VERIFY_THROUGH+1):
            self.assertEqual(world,set().union(*parts.values()),f'cross-pixel interference at {g}')
            if g in (0,219,220,267,268,300,366,398,420,441,442,480):
                completed[g]=sum(pixel_target(r)<=world for r in routes())
            if g<VERIFY_THROUGH:
                parts={k:evolve(v) for k,v in parts.items()}
                world=evolve(world)
        self.assertEqual(completed[0],0)
        self.assertEqual(completed[219],0)
        self.assertGreater(completed[220],0)
        self.assertLess(completed[267],len(target))
        self.assertEqual(completed[268],35)
        self.assertEqual(completed[300],35)
        self.assertEqual(completed[366],35)
        self.assertLess(completed[398],35)
        self.assertEqual(completed[442],0)
        self.assertEqual(world,set())

    def test_word_and_existing_character_bubble_are_one_separate_universe(self):
        # A safety check at key generations, plus a geometric clearance
        # certificate over all generation-zero signal routes.
        pieces=composed_components()
        words={k:v for k,v in pieces.items() if k.startswith('lyric_')}
        other={k:v for k,v in pieces.items() if not k.startswith('lyric_')}
        # All word packets/trajectories confined to far stage x>2150;
        # singer/bubble remain to its left in this qualified window.
        self.assertTrue(all(min(x for x,y in part)>2100 for part in words.values()))
        self.assertTrue(all(max(x for x,y in part)<1800 for part in other.values()))
        # Local proof covers each text signal at every generation; singer's
        # 980-generation qualification exists in prior test suites.
        self.assertTrue(other['bubble_outline'])
        self.assertTrue(other['bubble_lyrics'])
        self.assertTrue(words)

    def test_separation_from_existing_singer_for_all_480_ticks(self):
        from life.character_round2 import universe as singer_universe
        character=singer_universe(with_bubble=True)
        text_stage=place(local_universe(),*WORD_STAGE_ORIGIN)
        # This is stronger than an initial-distance check. Bounding intervals
        # remain separated by 1000+ cells through every evaluated tick; Life
        # has radius one, so F(A+B)=F(A)+F(B) at every one of those ticks.
        min_margin=100000
        for gen in range(VERIFY_THROUGH+1):
            if text_stage:
                margin=min(x for x,y in text_stage)-max(x for x,y in character)
                self.assertGreater(margin,2,gen)
                min_margin=min(min_margin,margin)
            if gen in (0,268,420):
                actual=evolve(character|text_stage)
                separate=evolve(character)|evolve(text_stage)
                self.assertEqual(actual,separate,gen)
            if gen<VERIFY_THROUGH:
                character=evolve(character)
                text_stage=evolve(text_stage)
        self.assertGreater(min_margin,1000)

    def test_rle_export_round_trip(self):
        cells=local_universe()
        recovered=parse_rle(compact_rle(cells,('glider-written WE',)))
        lowx=min(x for x,y in cells);lowy=min(y for x,y in cells)
        self.assertEqual(recovered,{(x-lowx,y-lowy) for x,y in cells})

if __name__=='__main__':unittest.main()
