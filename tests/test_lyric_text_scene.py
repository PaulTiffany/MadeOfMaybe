"""Exact qualification for full seven-word first-line word-alignment pilot."""
import unittest
from life.core import evolve,parse_rle
from life.lyric_cues import make_generation
from life.lyric_text_scene import (
    FIRST_LAMPS,SECOND_LAMPS,ALL_LAMPS,END_GENERATION,
    components,universe,second_caption_cells,status,caption_by_page,
)
from life.lyric_text_pilot import caption_cells,lamp_seed,lamp_target
from life.export_operational import compact_rle

class FullFirstLineLifeTests(unittest.TestCase):
    def test_all_seven_aligned_words_have_real_signal_packets(self):
        self.assertEqual(tuple(l.word for l in ALL_LAMPS),
                         ('WE','MADE','A','WINDOW','OUT','OF','SAND'))
        for lamp in ALL_LAMPS:
            self.assertLessEqual(abs(lamp.activation_generation/24 - lamp.lyric_start_s),.085)
            state=lamp_seed(lamp)
            target=lamp_target(lamp)
            for gen in range(345):
                if gen in (lamp.activation_generation-1,lamp.activation_generation,320,326,344):
                    expected=lamp.activation_generation<=gen<END_GENERATION
                    self.assertEqual(target<=state,expected,(lamp.word,gen))
                state=evolve(state)
            self.assertFalse(state, lamp.word)

    def test_static_pages_are_real_still_lifes(self):
        p=components()
        self.assertEqual(evolve(second_caption_cells()),second_caption_cells())
        self.assertEqual(evolve(p['bubble_2_outline']),p['bubble_2_outline'])
        for line in (caption_cells(),second_caption_cells()):
            self.assertTrue(line)
        self.assertEqual(caption_by_page(1),('OUT OF','SAND'))

    def test_export_roundtrip(self):
        initial=universe()
        pattern=compact_rle(initial,('seven word lyric cue pilot',))
        reconstructed=parse_rle(pattern)
        xmin=min(x for x,y in initial);ymin=min(y for x,y in initial)
        self.assertEqual(reconstructed,{(x-xmin,y-ymin) for x,y in initial})

    def test_350_generations_full_universe_superposition(self):
        parts=components()
        # Verifies unchanged singer, two genuine Life caption pages, and all
        # seven independently scheduled make/erase lamps simultaneously.
        whole=universe()
        checkpoints={268:(1,0,0,0,0,0,0),
                     276:(1,1,0,0,0,0,0),
                     284:(1,1,1,0,0,0,0),
                     288:(1,1,1,1,0,0,0),
                     304:(1,1,1,1,1,0,0),
                     312:(1,1,1,1,1,1,1),
                     320:(1,1,1,1,1,1,1),
                     326:(0,0,0,0,0,0,0),
                     344:(0,0,0,0,0,0,0)}
        for g in range(350):
            independent=set().union(*parts.values())
            self.assertEqual(whole,independent,f'cross-component interaction gen {g}')
            if g in checkpoints:
                self.assertEqual(tuple(int(v) for v in status(whole).values()),checkpoints[g],g)
            whole=evolve(whole)
            parts={name:evolve(c) for name,c in parts.items()}

if __name__=='__main__': unittest.main()
