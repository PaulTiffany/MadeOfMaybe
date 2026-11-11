"""Quick native Life word-mesh checks; entire 7600-gen replay runs in C++ CI."""
import unittest
from life.core import evolve,place
from life.staggered_word_mesh import (
    WORD,FORMATION_G,CLEANUP_G,STATION,INPUT,routes,lit_pixels,components,
    universe,reference_output,EATER_NORTHEAST,EATER_SOUTHWEST,EATER_TEXT,
    persistent_eaters,expected_word_at_formation,expected_formation_world
)

class StaggeredMeshTests(unittest.TestCase):
    def test_staggered_seven_row_35_pixel_geometry(self):
        self.assertEqual(WORD,'WE')
        rs=routes()
        self.assertEqual(len(rs),35)
        self.assertEqual(len({r.row for r in rs}),7)
        self.assertEqual(len({r.station_x for r in rs}),35)
        self.assertEqual(len(components()),36)
        self.assertEqual(len(universe()),1519)
        for r in rs:
            self.assertGreaterEqual(FORMATION_G,r.output_ref_arrives_at_g)
            travel=(FORMATION_G-r.output_ref_arrives_at_g)//4
            self.assertEqual(-43+r.station_x-2*travel,r.assembled_x)
            self.assertEqual(12+r.station_y,r.assembled_y)
            self.assertEqual(r.output_ref_arrives_at_g,200+4*r.incoming_delay_4gens)
        # The farther stations produce their output earlier.
        self.assertLess(rs[-1].output_ref_arrives_at_g,rs[0].output_ref_arrives_at_g)

    def test_real_corner_and_all_three_fishhook_types(self):
        self.assertEqual(len(STATION),19)
        self.assertEqual(len(INPUT),9)
        self.assertEqual(len(reference_output()),12)
        for eater in (EATER_NORTHEAST,EATER_SOUTHWEST,EATER_TEXT):
            self.assertEqual(len(eater),7)
            self.assertEqual(evolve(eater),set(eater))
        self.assertEqual(len(persistent_eaters()),539)
        self.assertEqual(len(expected_word_at_formation()),35*12)
        self.assertEqual(len(expected_formation_world()),959)
        self.assertEqual(CLEANUP_G-FORMATION_G,1600)

    def test_source_ablation_removes_only_one_intended_ship(self):
        self.assertEqual(len(universe(omit_index=34)),1510)
        removed=expected_word_at_formation()-expected_word_at_formation(omit_index=34)
        self.assertEqual(removed,place(reference_output(),
            routes()[34].assembled_x+43,routes()[34].assembled_y-12))
        self.assertEqual(len(expected_formation_world(omit_index=34)),966)
        with self.assertRaises(ValueError):components(omit_index=99)
        with self.assertRaises(ValueError):routes(formation_g=100)

if __name__=='__main__':unittest.main()
