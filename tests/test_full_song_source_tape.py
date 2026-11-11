"""Whole four-minute W/V source only; not a claim about karaoke actuation."""
import unittest
from life.core import place,evolve
from life.singer_pilot import INPUT_GLIDER
from life.full_song_source_tape import (
    source_events,packets,packet_cells,tape_cells,certify,SONG_END_G
)

class NativeSongSourceTapeTests(unittest.TestCase):
    def test_correct_independent_song_events(self):
        ev=source_events()
        self.assertEqual(len(ev),509)
        self.assertEqual(sum(k=='W' for k,*_ in ev),403)
        self.assertEqual(sum(k=='V+' for k,*_ in ev),53)
        self.assertEqual(sum(k=='V-' for k,*_ in ev),53)
        self.assertEqual(SONG_END_G,45864)
    def test_each_packet_is_five_cell_native_spaceship(self):
        g=set(INPUT_GLIDER)
        for _ in range(4):g=evolve(g)
        self.assertEqual(g,place(INPUT_GLIDER,1,1))
        self.assertEqual(len(packet_cells(packets()[0])),5)
    def test_reused_lanes_collision_free_and_scene_causally_separated(self):
        v=certify()
        self.assertEqual(len(tape_cells()),2545)
        self.assertTrue(v['source_rails_disjoint_from_singer_at_all_song_ticks_by_finite_speed'])
        self.assertFalse(v['all_sources_connected_to_physical_singer_controller'])
        self.assertFalse(v['four_minute_film_complete'])

if __name__=='__main__':unittest.main()
