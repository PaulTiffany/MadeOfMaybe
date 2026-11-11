"""No accounting tricks: actual Suno words, actual 90-degree Life catalysts."""
import unittest
from life.complete_native_converter_score import (
    source_words,assemble,compiler_audit,SONG_WORDS,SONG_GLYPH_PIXELS,
    STAGE_PITCH)
from life.native_half_font_first20 import lit_pixels
from life.gondry_corner_backtrace import backtrace

class FullConverterSourceTests(unittest.TestCase):
    def test_original_403_words_are_the_same_suno_music(self):
        words=source_words()
        self.assertEqual(len(words),SONG_WORDS)
        self.assertEqual((words[0].text,words[0].make_g),('WE',2156))
        self.assertEqual((words[1].text,words[1].make_g),('MADE',2204))
        self.assertEqual(sum(len(lit_pixels(w.text)) for w in words),
                         SONG_GLYPH_PIXELS)
    def test_first_two_physical_words_still_use_original_turners(self):
        self.assertEqual(len(backtrace('WE',2156)),17)
        self.assertEqual(len(backtrace('MADE',2204)),32)
        groups,stages,failures=assemble(2)
        self.assertFalse(failures)
        self.assertEqual(len(groups),5)
        self.assertEqual(len(stages),2)
        self.assertEqual(len(set().union(*groups)),sum(map(len,groups)))
        self.assertEqual(len(set().union(*groups)),8814)
    def test_sources_for_first_complete_sentence_or_report_failures(self):
        groups,stages,failures=assemble(7)
        result=compiler_audit(groups,stages,failures,7)
        if failures:
            self.fail(f'original first lyric sentence not staged: {failures}')
        self.assertEqual(len(stages),7)
        self.assertEqual(len(groups),10)
        self.assertEqual(result['physical_bubble_cells'],0)

if __name__=='__main__':unittest.main()
