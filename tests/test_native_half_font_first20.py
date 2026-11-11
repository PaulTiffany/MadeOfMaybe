"""Native mini-glyph physical geometry, not a video-camera scaling claim."""
import unittest
from life.native_half_font_first20 import (
    compact_glyphs,lit_pixels,routes,components,universe,expected_word
)
from life.staggered_word_mesh import reference_output

class NativeHalfFontTests(unittest.TestCase):
    def test_3x4_font_reduces_real_life_components(self):
        font=compact_glyphs()
        self.assertEqual(font['W'],('101','101','111','101'))
        self.assertEqual(font['E'],('111','100','100','111'))
        self.assertEqual(len(lit_pixels()),17)
        self.assertEqual((max(x for x,y in lit_pixels())+1,
                          max(y for x,y in lit_pixels())+1),(7,4))
    def test_native_turners_keep_original_phases(self):
        self.assertEqual(len(list(routes())),17)
        self.assertEqual(len(reference_output()),12)
        self.assertEqual(len(expected_word()),204)
        self.assertEqual(list(map(len,components())),[6408,648,742,240,52])
        self.assertEqual(len(universe()),8090)
        self.assertEqual(len(universe()),sum(map(len,components())))
    def test_bad_time_rejected(self):
        with self.assertRaises(ValueError):list(routes(target_g=2155))

if __name__=='__main__':unittest.main()
