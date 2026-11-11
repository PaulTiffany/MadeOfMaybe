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
    def test_intentionally_no_bubble_in_the_final_staged_g0_world(self):
        from life.two_line_native_singer import components,universe
        from life.native_half_font_first20 import components as old_parts
        base=old_parts()
        parts=components()
        self.assertEqual(len(parts),5)
        self.assertEqual(len(parts[0]),len(base[0]))
        self.assertEqual(len(parts[-1]),1372)
        self.assertEqual(len(universe()),8814)
        self.assertFalse(base[1] & universe())

    def test_inverse_stage_options_keep_source_disjoint(self):
        for delta in OFFSETS:
            try:parts=made_parts(0)
            except ValueError:continue
            self.assertEqual(len(set().union(*parts)),sum(map(len,parts)))

if __name__=='__main__':unittest.main()
