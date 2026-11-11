"""Finite-horizon qualification: a real lyric glider triggers an existing lip tile.

This is a *single-connection* proof, not a 403-word mouth-controller claim.
All observations read B3/S23 live cells, including counterfactual source ablation.
"""
import io
import unittest
from life.core import evolve, place, parse_rle
from life.glider_controlled_mouth import BLOCK
from life.first_line_singing_character import dynamic_seed, art_seed
from life.first_line_karaoke import score, ERASE_GENERATION, GPS, components as lyrics
from life.physical_lip_splitter_bridge import (
    LIP_NAME, LIP_TARGET, SINGER_TRANSLATION, SPLITTER_ORIENTATION,
    SPLITTER_LOCAL_ORIGIN, REFERENCE_SPLIT_OUTPUT_G, CAUSAL_WORD_G,
    FULL_CHECK_G, ABLATED_VALID_THROUGH_G, replaced_word_glider,
    replaced_lip_glider, split_input, splitter_catalysts, complete_world_seed,
    bridge_unit_seed, word_and_lip_at, spatial_certificate,
    assert_portrait_protected, assert_exact_signal_match,
)
from life.export_full_song_karaoke import sparse_rle_stream


class PhysicalLipSplitterBridgeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # One single replay under BOTH counterfactuals; save checkpoints.
        # The seven-word world's other pixels are separately bounded by the
        # finite-horizon spatial certificate below.
        cls.qualified = (2152, 2156, 2188, 2296, 2300, 2312, 2350,
                         2456, 2554, 2578, 2700, FULL_CHECK_G)
        on = bridge_unit_seed(source_enabled=True)
        off = bridge_unit_seed(source_enabled=False)
        baseline = place(dynamic_seed(), *SINGER_TRANSLATION)
        catalyst = place(splitter_catalysts(), *SINGER_TRANSLATION)
        cls.observed = {}
        for g in range(FULL_CHECK_G + 1):
            if g in cls.qualified:
                cls.observed[g] = {
                    'on': word_and_lip_at(on),
                    'off': word_and_lip_at(off) if g <= ABLATED_VALID_THROUGH_G else None,
                    'on_matches_original_plus_catalyst': on == baseline | catalyst,
                    'on_cells': len(on),
                }
            if g < FULL_CHECK_G:
                on = evolve(on)
                baseline = evolve(baseline)
                if g < ABLATED_VALID_THROUGH_G:
                    off = evolve(off)

    def test_same_single_source_replaces_exact_original_word_and_lip_gliders(self):
        exact = assert_exact_signal_match()
        self.assertEqual(exact['native_g'], REFERENCE_SPLIT_OUTPUT_G)
        self.assertEqual(exact['shared_initial_input_gliders'], 1)
        self.assertEqual(len(split_input()), 5)
        self.assertEqual(len(splitter_catalysts()), 84)
        self.assertEqual(CAUSAL_WORD_G, score()[0].make_g)
        self.assertEqual(GPS, 192)
        self.assertEqual(LIP_NAME, 'lower_medium_0')
        self.assertTrue(replaced_word_glider() <= lyrics()['WE_0_pixel_000'])
        self.assertEqual(len(replaced_lip_glider()), 5)

    def test_source_ablation_changes_both_real_outputs(self):
        on = self.observed[CAUSAL_WORD_G]['on']
        off = self.observed[CAUSAL_WORD_G]['off']
        self.assertTrue(on[0], 'physical WE 2x2 glyph pixel must exist at its cue')
        self.assertFalse(off[0], 'without shared source WE pixel must be absent')
        on = self.observed[2312]['on']
        off = self.observed[2312]['off']
        self.assertFalse(on[1], 'shared source physically erases the existing lip tile')
        self.assertTrue(off[1], 'with source ablated original lip tile persists')
        self.assertTrue(on[0])
        self.assertFalse(off[0])
        self.assertTrue(self.observed[2188]['on'][1])

    def test_original_expression_recovers_and_all_bridge_debris_clears(self):
        self.assertTrue(self.observed[2456]['on'][1], 'lip tile is rebuilt later')
        self.assertFalse(self.observed[2554]['on'][1], 'lip tile is erased later')
        self.assertTrue(self.observed[2578]['on_matches_original_plus_catalyst'])
        self.assertTrue(self.observed[2700]['on_matches_original_plus_catalyst'])
        self.assertTrue(self.observed[FULL_CHECK_G]['on_matches_original_plus_catalyst'])
        self.assertEqual(self.observed[2578]['on'], (False, False))
        self.assertEqual(FULL_CHECK_G, 3068)

    def test_static_hair_eyes_eyebrows_face_and_jewelry_are_protected(self):
        checked = assert_portrait_protected(end=FULL_CHECK_G)
        self.assertEqual(checked['verified_native_generations'], FULL_CHECK_G)
        self.assertEqual(checked['unchanged_art_cells'], len(art_seed()))
        self.assertGreater(checked['unchanged_art_cells'], 4500)
        self.assertEqual(evolve(set(art_seed())), set(art_seed()))

    def test_other_360_lyric_pixels_have_independent_cleared_corridors(self):
        report = spatial_certificate()
        self.assertEqual(report['other_lyric_pixel_count'], 360)
        self.assertGreater(report['minimum_guaranteed_life_cell_clearance'], 2)
        self.assertFalse(report['completed_full_song_lip_wiring'])
        self.assertEqual(ERASE_GENERATION, 2578)

    def test_one_world_golly_export_roundtrips_and_has_no_seed_overlap(self):
        seed = complete_world_seed(source_enabled=True)
        sink = io.StringIO()
        report = sparse_rle_stream(iter(seed), sink, comments=('Single input controls WE glyph pixel and real lower lip tile.',))
        parsed = parse_rle(sink.getvalue())
        self.assertEqual(parsed, place(seed, -report['origin_x'], -report['origin_y']))
        self.assertEqual(report['cells'], len(seed))


if __name__ == '__main__':
    unittest.main()
