"""Physical full 7-word line: all glyph pixels switch via native Life gliders."""
import unittest
from life.core import evolve
from life.first_line_karaoke import (GPS,LYRICS,PITCH,ERASE_GENERATION,
    score,signal_template,separation_certificate,universe,target_blocks)
from life.glider_controlled_mouth import BLOCK

class PhysicalSevenWordLine(unittest.TestCase):
    def test_all_seven_real_words_and_physical_timing(self):
        words=score()
        self.assertEqual(' '.join(w.text for w in words),LYRICS)
        self.assertEqual(len(words),7)
        self.assertEqual([len(w.targets) for w in words],[35,72,18,96,42,30,68])
        for w in words:
            self.assertEqual(w.make_g%4,0)
            self.assertLessEqual(abs(w.make_g/GPS-w.start_s),2/GPS+1e-9)
        self.assertLessEqual(abs(ERASE_GENERATION/GPS-13.420),2/GPS+1e-9)

    def test_all_pixel_reactions_real_and_holdable(self):
        # 7 unique input glider packet templates, one per word onset.
        for w in score():
            world=set(signal_template(w.make_g))
            for gen in range(ERASE_GENERATION+1):
                if gen==w.make_g:
                    self.assertEqual(world&BLOCK,BLOCK,w.text)
                if gen==w.make_g+8:
                    self.assertEqual(world&BLOCK,BLOCK,w.text)
                if gen<ERASE_GENERATION:world=evolve(world)
            self.assertFalse(world,w.text)

    def test_all_361_trajectories_have_rigorous_no_crosstalk_envelopes(self):
        cert=separation_certificate()
        self.assertEqual(cert['pixel_count'],361)
        self.assertEqual(cert['word_count'],7)
        self.assertLessEqual(cert['max_L_infty_footprint'],647)
        self.assertGreater(cert['minimum_guaranteed_cell_gap'],2)
        self.assertEqual(len(universe()),361*15)

if __name__=='__main__':unittest.main()

class ActualFullLineWorldTests(unittest.TestCase):
    def test_single_world_constructs_every_complete_word_at_the_right_generation(self):
        """No per-word overlays: iterate the full 5415-cell initial universe."""
        words=score()
        complete={w.make_g:i for i,w in enumerate(words)}
        live=universe()
        blocks=[target_blocks(w) for w in words]
        for gen in range(ERASE_GENERATION+1):
            if gen in complete:
                current=complete[gen]
                for i,parts in enumerate(blocks):
                    number=sum(p<=live for p in parts)
                    self.assertEqual(number, len(parts) if i<=current else 0,
                                     f'g{gen} word {i} {words[i].text}')
            if gen==ERASE_GENERATION:
                self.assertEqual(live,set(),'all gliders and all glyph pixels consumed')
            if gen<ERASE_GENERATION:live=evolve(live)

    def test_export_roundtrip(self):
        from life.export_operational import compact_rle
        from life.core import parse_rle
        seed=universe()
        parsed=parse_rle(compact_rle(seed,('native first lyric line',)))
        x0=min(x for x,y in seed);y0=min(y for x,y in seed)
        self.assertEqual(parsed,{(x-x0,y-y0) for x,y in seed})
