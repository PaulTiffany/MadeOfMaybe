"""Full-song compiler and actual glider reaction checks (no image swapping)."""
import io
import json
from pathlib import Path
import unittest

from life.full_song_karaoke import (
 GPS, ALIGNMENT_FILE, MIN_HOLD_GENERATIONS, compile_plan,
 validate_layout, stats, seeded_lines, local_line_seed, physical_targets,
 pixel_seed, real_word_count, verify_native_packet, isolated_triple,
)
from life.export_full_song_karaoke import sparse_rle_stream
from life.lyric_cues import read_alignment
from life.core import parse_rle, evolve, place
from life.glider_controlled_mouth import BLOCK

FIXTURE=Path(__file__).resolve().parents[1]/'data'/'first_verse_alignment_fixture.json'

class FullSongCompilerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture=compile_plan(read_alignment(FIXTURE))

    def test_two_line_genuine_preloaded_world(self):
        lines=self.fixture
        self.assertEqual(len(lines),2)
        self.assertEqual([l.text for l in lines],
            ['WE MADE A WINDOW OUT OF SAND','WE DREW A SKY UPON THE GLASS'])
        self.assertEqual([len(l.words) for l in lines],[7,7])
        self.assertEqual([l.pixel_count for l in lines],[361,349])
        s=stats(lines)
        self.assertEqual(s['glider_count'],2130)
        self.assertEqual(s['seed_cell_count'],10650)
        self.assertLess(s['worst_word_onset_error_ms'],11)
        self.assertTrue(s['audio_tempo_unchanged'])
        self.assertFalse(s['runtime_cell_edits'])
        self.assertFalse(s['frame_swapped_lyrics'])
        self.assertEqual(len(set(seeded_lines(lines))),s['seed_cell_count'])

    def test_per_line_and_cross_line_spatial_clearance(self):
        lines=self.fixture
        validate_layout(lines)
        for l in lines:
            self.assertGreater(l.pitch-2*l.radius,2)
        self.assertGreater(lines[1].box[1]-lines[0].box[3],2)

    def test_true_sparse_rle_roundtrip_with_multi_line_large_coords(self):
        out=io.StringIO()
        dims=sparse_rle_stream(seeded_lines(self.fixture),out)
        cells=set(seeded_lines(self.fixture))
        recovered=parse_rle(out.getvalue())
        minx=min(x for x,y in cells); miny=min(y for x,y in cells)
        self.assertEqual(dims['cells'],len(cells))
        self.assertEqual(recovered,{(x-minx,y-miny) for x,y in cells})

    def test_no_per_pixel_preloaded_glider_overlap(self):
        for line in self.fixture:
            for w in line.words:
                p=pixel_seed(w.make_g,line.clear_g)
                self.assertEqual(len(p),15)
                self.assertGreater(line.clear_g-w.make_g,25)

    def test_real_life_write_hold_erase_on_representative_phases(self):
        for make,erase in ((2156,2578),(2756,3402),(44600,44702)):
            report=verify_native_packet(make,erase,verify_prefix=True)
            self.assertEqual(report['appeared_g'],make)
            self.assertEqual(report['final_population'],0)

    def test_real_subset_of_two_independent_lyric_pixels(self):
        line=self.fixture[0];w=line.words[0]
        origins=list(physical_targets(line,w))[:2]
        signal=set()
        for xy in origins:
            signal |= place(set(pixel_seed(w.make_g,line.clear_g)),*xy)
        checkpoints={w.make_g, w.make_g+4, line.clear_g}
        for g in range(line.clear_g+1):
            if g in checkpoints:
                visible=sum(place(BLOCK,*o)<=signal for o in origins)
                self.assertEqual(visible,2 if g!=line.clear_g else 0)
            if g<line.clear_g:signal=evolve(signal)
        self.assertFalse(signal)

    def test_full_song_alignment_if_available(self):
        if not ALIGNMENT_FILE.exists():
            self.skipTest('Suno full alignment included in GitHub repo; local fixture only')
        raw=read_alignment(ALIGNMENT_FILE)
        plans=compile_plan(raw)
        source_words={i for line in plans for w in line.words for i in w.source_tokens}
        self.assertGreaterEqual(len(plans),40)
        self.assertGreaterEqual(len(source_words),450)
        self.assertEqual(plans[0].text,'WE MADE A WINDOW OUT OF SAND')
        self.assertTrue(plans[-1].text.endswith('RIGHT NOW.'))
        self.assertLess(stats(plans)['worst_word_onset_error_ms'],11)
        self.assertLess(stats(plans)['worst_line_clear_error_ms'],240)
        validate_layout(plans)

if __name__=='__main__':unittest.main()
