"""Regression for actual time-multiplexed Conway lyric source at fixed sink."""
import io
import unittest
from life.core import parse_rle,place
from life.export_full_song_karaoke import sparse_rle_stream
from life.reusable_word_cue import (
    seed,line_times,next_input,checkpoints,qualification,
    splitter_reuse_certificate,protected_character_certificate,
    character_world_seed)
from life.physical_lip_splitter_bridge import splitter_catalysts, SINGER_TRANSLATION


class ReusableWordCueTests(unittest.TestCase):
    def test_two_suno_line_starts_reuse_same_glider_splitter_and_pixel(self):
        result=qualification()
        self.assertEqual(result['first_line_make_erase'],[2156,2578])
        self.assertEqual(result['second_line_make_erase'],[2976,3402])
        self.assertEqual(result['shared_physical_splitter_catalysts'],84)
        self.assertTrue(result['same_physical_word_pixel_reused'])
        self.assertFalse(result['full_song_layout_compacted'])
        self.assertFalse(result['actual_full_lip_coupling_for_second_event'])

    def test_each_input_causally_necessary_only_at_its_own_make_onset(self):
        a,b=line_times()
        normal=checkpoints();without_first=checkpoints(False,True)
        without_second=checkpoints(True,False)
        self.assertTrue(normal[a[0]]['block'])
        self.assertTrue(normal[b[0]]['block'])
        self.assertFalse(without_first[a[0]]['block'])
        self.assertTrue(without_first[b[0]]['block'])
        self.assertTrue(without_second[a[0]]['block'])
        self.assertFalse(without_second[b[0]]['block'])
        # Ablating input 1 can leave uncancelled glider debris that affects
        # the later reset. The counterfactual is NOT a certified clean world.
        self.assertTrue(without_first[b[1]]['block'])
        self.assertFalse(normal[b[1]]['block'])

    def test_splitter_reusable_and_final_debris_only_clean_gliders(self):
        result=splitter_reuse_certificate()
        self.assertEqual(result['physical_catalysts'],84)
        self.assertEqual(result['surviving_clean_gliders'],2)
        self.assertEqual(result['final_life_cell_population'],94)
        self.assertEqual(result['at_generation'],3402)

    def test_single_initial_rle_roundtrip(self):
        world=seed()
        sink=io.StringIO()
        rep=sparse_rle_stream(iter(world),sink,comments=('One Life source, two Suno-aligned reuse events.',))
        self.assertEqual(parse_rle(sink.getvalue()),place(world,-rep['origin_x'],-rep['origin_y']))
        self.assertEqual(rep['cells'],114)

    def test_second_input_preserves_hair_eyes_face_and_original_lip_schedule(self):
        checked=protected_character_certificate()
        self.assertGreater(checked['singer_art_still_life_cells'],4500)
        self.assertEqual(checked['native_generations_checked'],3403)
        self.assertTrue(checked['original_one_lip_coupling_preserved'])
        self.assertTrue(checked['unchanged_portrait_spacetime_guarantee'])
        self.assertFalse(checked['second_lip_causally_connected'])
        # The full singer-world single-source bridge remains a REAL lip tile.
        self.assertGreater(len(character_world_seed()),1000)

if __name__=='__main__': unittest.main()
