"""Compact 35-turner phase geometry, expected cells and ablation."""
import unittest
from life.core import evolve,place
from life.compact_full_word_mesh import (
    STATION_PITCH,PIXEL_PITCH,FORMATION_G,CLEANUP_G,
    lit_pixels,routes,components,universe,expected_word,
    expected_formation,expected_final,fixed_eaters
)
from life.staggered_word_mesh import (
    reference_output,OUTPUT_REFERENCE_MIN_X,OUTPUT_REFERENCE_MIN_Y
)
class CompactFullWordMeshTests(unittest.TestCase):
    def test_physical_station_mesh_is_smaller_and_separated_at_g0(self):
        self.assertEqual(len(lit_pixels()),35)
        self.assertEqual((STATION_PITCH,PIXEL_PITCH),(36,36))
        self.assertEqual((FORMATION_G,CLEANUP_G),(6000,7600))
        rs=routes()
        self.assertEqual(len(rs),35)
        self.assertEqual((min(r.station_x for r in rs),max(r.station_x for r in rs)),(300,1524))
        self.assertEqual((min(r.station_y for r in rs),max(r.station_y for r in rs)),(0,216))
        self.assertEqual(len(components()),36)
        self.assertEqual(len(universe()),1519)
        self.assertEqual(len(fixed_eaters()),539)

    def test_all_35_exact_native_lwss_phases_align_at_g6000(self):
        for r in routes():
            self.assertEqual(r.output_reference_generation,200+4*r.source_delay_4gens)
            travel=(FORMATION_G-r.output_reference_generation)//4
            self.assertEqual(r.station_x+OUTPUT_REFERENCE_MIN_X-2*travel,r.final_x)
            self.assertEqual(r.station_y+OUTPUT_REFERENCE_MIN_Y,r.final_y)
        self.assertEqual(len(expected_word()),35*12)
        self.assertEqual(len(expected_formation()),959)
        self.assertEqual(len(expected_final()),539)
        self.assertEqual(evolve(expected_final()),expected_final())
        self.assertEqual(len(reference_output()),12)

    def test_one_input_ablation_removes_one_and_only_one_formed_pixel(self):
        self.assertEqual(len(universe(omit_index=34)),1510)
        r=routes()[34]
        self.assertEqual(expected_word()-expected_word(omit_index=34),
                         place(reference_output(),
                         r.final_x-OUTPUT_REFERENCE_MIN_X,
                         r.final_y-OUTPUT_REFERENCE_MIN_Y))
        self.assertEqual(len(expected_formation(omit_index=34)),966)
        self.assertEqual(len(expected_final(omit_index=34)),558)
        with self.assertRaises(ValueError):components(omit_index=35)
        with self.assertRaises(ValueError):routes(formation_g=201)

if __name__=='__main__':unittest.main()
