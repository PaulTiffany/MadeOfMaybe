"""Four real glider inputs, one reusable 105-cell Life converter."""
import unittest
from life.core import evolve
from life.reusable_glider_to_lwss_2023 import hardware,qualify

class ReusableGtoLWSSTests(unittest.TestCase):
    def test_exact_stable_hardware(self):
        self.assertEqual(len(hardware()),105)
        self.assertEqual(evolve(set(hardware())),set(hardware()))
    def test_four_real_westbound_ships_and_restored_station(self):
        cert=qualify(n=4)
        self.assertEqual(cert['output_LWSS_count'],4)
        self.assertEqual(cert['terminal_population'],153)
        self.assertTrue(cert['hardware_restored'])
        self.assertFalse(cert['whole_song_converter_array_built'])
    def test_ablate_one_input_no_spurious_ship(self):
        cert=qualify(n=3)
        self.assertEqual(cert['output_LWSS_count'],3)
        self.assertEqual(cert['terminal_population'],141)

if __name__=='__main__':unittest.main()
