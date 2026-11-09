"""Conway first-line character integration, including source-derived delay."""
import unittest
import io
from life.core import evolve,place,parse_rle
from life.glider_controlled_mouth import BLOCK
from life.character_round2 import universe as original_universe
from life.first_line_karaoke import score, ERASE_GENERATION
from life.first_line_singing_character import (
    anchor_delay, dynamic_seed, original_dynamic_components,
    safe_art, art_seed, character_seed, combined_seed, singer_coordinates_at,
    timed_checkpoints, spatial_certificate, CHARACTER_X,
)
from life.symmetric_full_mouth import target_blocks
from life.expressive_mouth import START_LINE


class FirstLineSingingCharacterTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.delay=anchor_delay();cls.art=art_seed()

    def test_karaoke_event_is_the_only_performance_anchor(self):
        self.assertEqual(self.delay,ERASE_GENERATION-490)
        self.assertEqual(self.delay,2088)
        self.assertEqual(timed_checkpoints()[self.delay+180],'medium')
        self.assertLess(self.delay+420,ERASE_GENERATION)
        self.assertEqual(len(score()),7)

    def test_backstepped_life_gliders_recover_exact_original_dynamics(self):
        original=set().union(*original_dynamic_components().values())
        moving=singer_coordinates_at(self.delay,include_art=False)
        self.assertEqual(moving,original)

    def test_static_character_art_is_unchanged_across_glider_performance(self):
        self.assertGreater(len(self.art),4500)
        self.assertEqual(evolve(set(self.art)),set(self.art))
        self.assertGreaterEqual(len(safe_art()['art_hair_mass']),1500)

    def test_native_multi_tile_lips_follow_lyric_anchored_checkpoints(self):
        samples={self.delay+g for g in (60,180,288,420,540,680,960)}
        moving=set(dynamic_seed())
        observed={}
        for g in range(max(samples)+1):
            if g in samples:observed[g]=set(moving)
            if g<max(samples):moving=evolve(moving)
        for old,state in ((60,'closed'),(180,'medium'),(288,'open'),
                          (420,'medium'),(540,'breath'),(680,'open'),(960,'closed')):
            world=observed[self.delay+old]
            medium=sum(place(BLOCK,x,y)<=world for x,y in target_blocks('medium')
                       if (x-1,y) not in target_blocks('medium') and (x,y-1) not in target_blocks('medium'))
            opened=sum(place(BLOCK,x,y)<=world for x,y in target_blocks('open')
                       if (x-1,y) not in target_blocks('open') and (x,y-1) not in target_blocks('open'))
            center=sum(place(BLOCK,*xy)<=world for xy in START_LINE)
            if state=='medium':
                self.assertGreaterEqual(medium,8)
                self.assertEqual(opened,0)
            elif state=='open':
                self.assertGreaterEqual(opened,14)
                self.assertEqual(medium,0)
            elif state=='closed':
                self.assertEqual(medium,0);self.assertEqual(opened,0)
                self.assertEqual(center,5)

    def test_sparse_rle_round_trip_of_complete_single_world(self):
        from life.export_full_song_karaoke import sparse_rle_stream
        initial=combined_seed();sink=io.StringIO()
        envelope=sparse_rle_stream(iter(initial),sink)
        decoded=parse_rle(sink.getvalue())
        self.assertEqual(decoded,place(initial,-envelope['origin_x'],-envelope['origin_y']))
        self.assertEqual(envelope['cells'],len(initial))

    def test_singer_and_real_word_gliders_share_one_initial_universe(self):
        cert=spatial_certificate()
        self.assertGreater(cert['initial_x_separation'],1000)
        self.assertFalse(cert['physical_shared_duplicator_connected'])
        self.assertEqual(len(combined_seed()),cert['combined_initial_cells'])

if __name__=='__main__':unittest.main()
