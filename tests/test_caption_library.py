"""Every bubble page is a real static Life shape, not text painted in post."""
import unittest
from pathlib import Path
import tempfile
from life.core import evolve,parse_rle
from life.caption_library import native_page,word_rows,bubble_frame,export_page_rles
from life.lyric_cues import read_alignment,caption_pages,aligned_words
from life.character_round2 import components as singer_components

DATA=Path(__file__).resolve().parents[1]/'data'

class NativeCaptionPages(unittest.TestCase):
    def test_unchanged_qualified_frame(self):
        self.assertEqual(bubble_frame(),singer_components()['bubble_outline'])

    def test_first_verse_pages_are_stable_life_and_fit(self):
        raw=read_alignment(DATA/'first_verse_alignment_fixture.json')
        pages=caption_pages(aligned_words(raw))
        self.assertEqual(len(pages),4)
        for i,page in enumerate(pages):
            with self.subTest(index=i,words=page.lines):
                cells=native_page(page)
                self.assertEqual(evolve(cells),cells)
                self.assertTrue(word_rows(page.lines))
                self.assertFalse(word_rows(page.lines)&bubble_frame())

    def test_one_column_too_wide_is_rejected(self):
        with self.assertRaises(ValueError):
            word_rows(('NOT FITTING IN BUBBLE',))

    def test_four_rle_assets_round_trip(self):
        raw=read_alignment(DATA/'first_verse_alignment_fixture.json')
        pages=caption_pages(aligned_words(raw))
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(export_page_rles(raw,d),len(pages))
            for i,p in enumerate(pages):
                cells=native_page(p)
                rle=parse_rle((Path(d)/f'page_{i:03d}.rle').read_text())
                xmin=min(x for x,y in cells);ymin=min(y for x,y in cells)
                self.assertEqual(rle,{(x-xmin,y-ymin) for x,y in cells})

    def test_full_song_pages_qualify_when_alignment_available(self):
        path=DATA/'made_of_maybe_suno_alignment.json'
        if not path.exists():
            self.skipTest('Full source file present on draft PR branch; verified by GitHub CI')
        pages=caption_pages(aligned_words(read_alignment(path)))
        for i,p in enumerate(pages):
            with self.subTest(page=i):native_page(p)

if __name__=='__main__':unittest.main()
