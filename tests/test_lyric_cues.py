"""Word alignment -> deterministic generation/caption assertions."""
import unittest
from pathlib import Path
from life.lyric_cues import (
    read_alignment,aligned_words,caption_pages,cue_rows,generation,
    make_generation, MAX_BUBBLE_CHARS,
)
from life.lyric_font import line_cells,width_of
from life.character_round2 import components as singer_components

DATA=Path(__file__).resolve().parents[1]/'data'

class LyricAlignmentTests(unittest.TestCase):
    def test_first_verse_exact_suno_times(self):
        raw=read_alignment(DATA/'first_verse_alignment_fixture.json')
        words=aligned_words(raw)
        self.assertEqual([w.text for w in words[:7]],
            ['WE','MADE','A','WINDOW','OUT','OF','SAND'])
        self.assertEqual([w.start_s for w in words[:4]],
            [11.224,11.479,11.824,11.964])
        self.assertEqual([generation(w.start_s) for w in words[:4]],
            [269,275,284,287])
        self.assertEqual([make_generation(w.start_s) for w in words[:4]],
            [268,276,284,288])
        self.assertLessEqual(max(abs(make_generation(w.start_s)/24-w.start_s)
                                 for w in words[:4]),.06)
        # Avoid the historic double-rounding error: 12.909s must pick g308, not g312.
        self.assertEqual(make_generation(12.909),308)
        self.assertEqual(make_generation(12.968),312)

    def test_page_layout_does_not_drop_words_or_overflow_bubble(self):
        words=aligned_words(read_alignment(DATA/'first_verse_alignment_fixture.json'))
        pages=caption_pages(words)
        self.assertEqual(pages[0].lines,('WE MADE','A WINDOW'))
        self.assertEqual(pages[1].lines,('OUT OF','SAND'))
        self.assertEqual(pages[2].lines,('WE DREW','A SKY'))
        self.assertEqual(pages[3].lines,('UPON THE','GLASS'))
        self.assertEqual(tuple(w for p in pages for w in p.words),words)
        for page in pages:
            self.assertTrue(1<=len(page.lines)<=2)
            for line in page.lines:
                self.assertLessEqual(len(line),MAX_BUBBLE_CHARS)
                self.assertLessEqual(width_of(line),190)

    def test_punctuation_split_and_zero_length_preserve_provenance(self):
        raw={'words':[
            {'word':'[Chorus]\nI','start_s':54.061,'end_s':54.141,'success':True},
            {'word':"'",'start_s':54.150,'end_s':54.253,'success':True},
            {'word':'m','start_s':54.266,'end_s':54.325,'success':True},
            {'word':' made','start_s':54.325,'end_s':54.654,'success':True},
            {'word':' don','start_s':76.20,'end_s':76.30,'success':True},
            {'word':"'",'start_s':76.30,'end_s':76.35,'success':True},
            {'word':'t','start_s':76.35,'end_s':76.39,'success':True},
            {'word':' zero','start_s':76.40,'end_s':76.40,'success':True},
        ]}
        words=aligned_words(raw)
        self.assertEqual([w.text for w in words],["I'M",'MADE',"DON'T",'ZERO'])
        self.assertEqual(words[0].source_tokens,(0,1,2))
        self.assertTrue(words[-1].flagged)

    def test_prevent_invalid_alignment(self):
        import json,tempfile
        raw=read_alignment(DATA/'first_verse_alignment_fixture.json')
        raw['audio_id']='wrong'
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'bad.json';p.write_text(json.dumps(raw))
            with self.assertRaises(ValueError):read_alignment(p)

    def test_full_song_when_connected_alignment_is_present(self):
        source=DATA/'made_of_maybe_suno_alignment.json'
        if not source.exists():self.skipTest('Full Suno capture lives on PR branch')
        raw=read_alignment(source)
        self.assertEqual(len(raw['words']),468)
        self.assertEqual(sum(w['start_s']==w['end_s'] for w in raw['words']),3)
        words=aligned_words(raw)
        pages=caption_pages(words)
        self.assertGreater(len(words),250)
        self.assertGreater(len(pages),70)
        self.assertTrue(all(len(row)<=8 for page in pages for row in page.lines))

if __name__=='__main__':unittest.main()

class ExportedLyricArtifactTests(unittest.TestCase):
    def test_fixture_generates_reusable_csv_json_and_srt(self):
        import csv,json,tempfile
        from life.lyric_cues import compile_files,page_rows
        raw=read_alignment(DATA/'first_verse_alignment_fixture.json')
        with tempfile.TemporaryDirectory() as tmp:
            prefix=Path(tmp)/'verse'
            compile_files(raw,prefix)
            with (Path(tmp)/'verse_words.csv').open(encoding='utf-8') as f:
                ws=list(csv.DictReader(f))
            with (Path(tmp)/'verse_pages.csv').open(encoding='utf-8') as f:
                ps=list(csv.DictReader(f))
            pages=json.loads((Path(tmp)/'verse_pages.json').read_text())
            subtitles=(Path(tmp)/'verse_pages.srt').read_text()
            self.assertEqual(len(ws),14)
            self.assertEqual(len(ps),4)
            self.assertEqual(pages['native_life_switching'],
                             'NOT IMPLEMENTED FOR CAPTION PAGES')
            self.assertEqual(ws[0]['word'],'WE')
            self.assertEqual(ws[0]['make_generation'],'268')
            self.assertEqual(ps[0]['line1'],'WE MADE')
            self.assertEqual(ps[0]['line2'],'A WINDOW')
            self.assertIn('00:00:11,224 -->',subtitles)
            self.assertEqual(subtitles.count(' --> '),4)
            self.assertEqual(page_rows(raw)[0]['source_tokens'],'0;1;2;3')

    def test_trailing_end_header_does_not_relabel_last_word(self):
        from life.lyric_cues import aligned_words
        a=aligned_words({'words':[
            {'word':'[Outro]\nRight','start_s':231.0,'end_s':231.2},
            {'word':' now.\n\n[End]','start_s':231.2,'end_s':231.5},
        ]})
        self.assertEqual([x.section for x in a],['Outro','Outro'])
        self.assertEqual([x.text for x in a],['RIGHT','NOW.'])

    def test_full_alignment_with_real_bubble_pages(self):
        from life.lyric_cues import page_rows
        source=DATA/'made_of_maybe_suno_alignment.json'
        if not source.exists():
            self.skipTest('Full song captured on draft PR branch; CI runs this test')
        raw=read_alignment(source)
        pages=caption_pages(aligned_words(raw))
        self.assertGreater(len(pages),70)
        for page in pages:
            for line in page.lines:
                self.assertLessEqual(len(line),8)
                self.assertGreater(len(line_cells(line,(0,0))),0)
        self.assertEqual(len(page_rows(raw)),len(pages))
