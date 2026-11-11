"""Source geometry tests; C++ independent whole-world simulation in CI."""
import unittest
from life.core import evolve
from life.two_line_native_singer import ROW_Y,OFFSETS,made_parts,made_fixed,made_at_g2204
from life.gondry_corner_backtrace import backtrace
from life.native_half_font_first20 import expected_word

class NativeTwoLineStageTests(unittest.TestCase):
    def test_second_physical_word_preserves_native_3x4_pixel_count(self):
        self.assertEqual(ROW_Y,144)
        self.assertEqual(len(backtrace('MADE',2204)),32)
        self.assertEqual(len(made_parts()),33)
        self.assertEqual(len(expected_word()),17*12)
        self.assertEqual(len(made_at_g2204()),32*12)
        self.assertEqual(len(made_fixed()),(32*2+4)*7)
        self.assertEqual(evolve(made_fixed()),made_fixed())
    def test_inverse_stage_options_keep_source_disjoint(self):
        for delta in OFFSETS:
            try:parts=made_parts(delta)
            except ValueError:continue
            self.assertEqual(len(set().union(*parts)),sum(map(len,parts)))

if __name__=='__main__':unittest.main()
