"""5x7 full-alphabet captions are real Life still lifes, not video overlays."""
import unittest
from life.core import evolve
from life.lyric_font import GLYPHS,line_cells,bubble_lyric_cells,width_of
from life.styled_singer import components

class LyricFontQualification(unittest.TestCase):
    def test_all_supported_glyphs_are_seven_rows_by_five(self):
        self.assertGreaterEqual(len(GLYPHS),37)
        for char,lines in GLYPHS.items():
            with self.subTest(char=char):
                self.assertEqual(len(lines),7)
                self.assertTrue(all(len(s)==5 and set(s)<=set('01') for s in lines))

    def test_bubble_text_and_alternate_short_lines_are_stable(self):
        for pair in (('MADE OF','MAYBE'),('I SEE','YOU'),('NOW','NOW')):
            with self.subTest(pair=pair):
                cells=bubble_lyric_cells(pair)
                self.assertEqual(evolve(cells),cells)
                parts=components(caption_lines=pair)
                self.assertEqual(parts['bubble_lyrics'],cells)
                self.assertEqual(evolve(parts['bubble_outline']|cells),parts['bubble_outline']|cells)

    def test_long_line_refused_rather_than_clipped(self):
        with self.assertRaises(ValueError):bubble_lyric_cells(('A VERY VERY LONG LINE',))
        with self.assertRaises(ValueError):line_cells('?',(0,0),pitch=3)
        with self.assertRaises(ValueError):line_cells('🚀',(0,0))

if __name__=='__main__':unittest.main()
