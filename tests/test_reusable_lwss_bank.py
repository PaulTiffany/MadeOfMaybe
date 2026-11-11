"""Real multi-lane native source/sink reset and original-Suno timing capacity."""
import unittest
from life.core import evolve, place
from life.reusable_lwss_bank import (
    EATER, FIXED, MIN_GAP_G, LANE_PITCH,
    delayed_glider, reference_westbound, qualify_sample,
    full_song_schedule, schedule_audit
)

class ReusableLWSSBankTests(unittest.TestCase):
    def test_112_cell_fishhook_and_converter_are_stationary(self):
        self.assertEqual(len(EATER), 7)
        self.assertEqual(len(FIXED), 112)
        self.assertEqual(evolve(set(FIXED)), set(FIXED))
        ship = reference_westbound()
        self.assertEqual(len(ship), 12)

    def test_three_lanes_eight_shots_native_reset_every_generation(self):
        cert = qualify_sample(lanes=3, shots=8, end_g=1700)
        self.assertEqual(cert['initial_population'], 456)
        self.assertEqual(cert['terminal_population'], 336)
        self.assertEqual(tuple(cert['first_outputs_present']), (True, True, True))
        self.assertTrue(cert['eater_and_converter_exactly_restored'])
        self.assertFalse(cert['full_song_word_display_built'])

    def test_independent_source_ablation_is_a_real_cell_removal_at_g0(self):
        cert = qualify_sample(lanes=3, shots=8, omit=(1,0), end_g=1700)
        self.assertEqual(cert['initial_population'], 451)
        self.assertEqual(tuple(cert['first_outputs_present']), (True, False, True))
        self.assertEqual(cert['terminal_population'], 336)

    def test_g0_launch_phases_and_full_song_slot_capacity(self):
        requests, lanes = full_song_schedule()
        self.assertEqual(len({r.word_index for r in requests}), 403)
        self.assertEqual(len(requests), 10366)
        self.assertGreater(lanes, 40)
        self.assertLess(lanes, len(requests))
        self.assertEqual(len(delayed_glider(requests[0].generation,
                                            requests[0].lane)), 5)
        cert = schedule_audit()
        self.assertEqual(cert['song_pixel_requests'], len(requests))
        self.assertEqual(cert['spaced_input_generation_gap'], MIN_GAP_G)
        self.assertTrue(cert['g0_source_cells_are_all_nonoverlapping'])
        self.assertFalse(cert['outputs_arranged_as_3x4_words'])
        self.assertFalse(cert['full_native_song_film_qualified'])

if __name__ == '__main__':
    unittest.main()
