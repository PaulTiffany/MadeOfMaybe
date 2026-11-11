"""Native-Life signal relay and physical reachability qualification."""
import unittest
from life.core import evolve,place
from life.physical_glider_relay import (
    SNARK_CATALYST,SNARK_IN,relay_seed,
    snark_relay_certificate,proposed_relocation_feasibility,
    PROPOSED_SPLITTER_LOCAL_ORIGIN
)

class PhysicalGliderRelayTests(unittest.TestCase):
    def test_snark_is_stationary_until_activated(self):
        self.assertEqual(len(SNARK_CATALYST),49)
        self.assertEqual(len(SNARK_IN),5)
        self.assertEqual(evolve(set(SNARK_CATALYST)),set(SNARK_CATALYST))
        self.assertEqual(relay_seed(one=False,two=False),set(SNARK_CATALYST))

    def test_actual_two_pulse_relay_without_injection_or_glider_gun(self):
        r=snark_relay_certificate()
        self.assertEqual(r['stationary_cells'],49)
        self.assertEqual(r['source_separation_generations'],820)
        self.assertEqual(r['both_outputs_verified_by_native_life'],2)
        self.assertEqual(r['replays']['both'][920]['clean_output_gliders'],2)
        self.assertEqual(r['replays']['off'][920]['clean_output_gliders'],0)
        self.assertTrue(r['source_ablation_prevents_corresponding_output'])
        self.assertFalse(r['controller_relocation_qualified'])

    def test_requested_below_bubble_move_fails_existing_glider_deadline(self):
        f=proposed_relocation_feasibility()
        self.assertEqual(f['proposed_splitter_local_origin'],(380,120))
        self.assertEqual(f['old_lyric_anchor'],(0,0))
        self.assertEqual(f['required_min_x_axis_displacement'],1397)
        self.assertEqual(f['max_c4_axis_displacement_before_deadline'],454)
        self.assertFalse(f['old_lyric_anchor_reachable_by_c4'])
        self.assertFalse(f['controller_relocation_qualified'])

if __name__ == '__main__':unittest.main()
