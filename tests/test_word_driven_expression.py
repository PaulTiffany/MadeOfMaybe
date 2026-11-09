"""Full-song source-linked mouth score is only an intent, never fake Life."""
import unittest
from pathlib import Path
from life.full_song_karaoke import GPS,ALIGNMENT_FILE
FIXTURE=Path(__file__).resolve().parents[1]/"data"/"first_verse_alignment_fixture.json"
from life.word_driven_expression import (score,source_cues,qualified_intent,rate_limited_candidate,audit,STATES)

class WordDrivenExpressionTests(unittest.TestCase):
    def test_every_word_and_line_clear_reuses_exact_real_native_lyric_cues(self):
        lines=score(FIXTURE);raw=source_cues(FIXTURE)
        self.assertEqual(len(lines),2)
        self.assertEqual(sum(c.cause=='word_make' for c in raw),14)
        self.assertEqual(sum(c.cause=='line_clear' for c in raw),2)
        word_cues={c.word_index:c for c in raw if c.cause=='word_make'}
        for line in lines:
            self.assertIn((line.line_index,line.clear_g),
                          {(c.line_index,c.generation) for c in raw if c.cause=='line_clear'})
            for w in line.words:
                self.assertEqual(word_cues[w.word_index].generation,w.make_g)
                self.assertEqual(word_cues[w.word_index].line_index,line.line_index)
        self.assertEqual(GPS,192)

    def test_only_three_states_and_no_independent_micro_clock(self):
        events=qualified_intent(FIXTURE)
        self.assertTrue(all(c.state in STATES for c in events))
        self.assertEqual(events[0].state,'medium')
        self.assertEqual(events[0].generation,score(FIXTURE)[0].words[0].make_g)
        self.assertTrue(all(a.state!=b.state for a,b in zip(events,events[1:])))
        report=audit(FIXTURE)
        self.assertTrue(report['word_source_only'])
        self.assertFalse(report['phonemization'])
        self.assertFalse(report['physical_full_lip_wiring_verified'])
        self.assertGreater(report['state_changes_requested'],5)
        self.assertGreater(report['gaps_under_48_generations'],0)

    def test_thinned_state_changes_are_only_actual_word_or_clear_events(self):
        requested=source_cues(FIXTURE)
        proposed=rate_limited_candidate(FIXTURE,min_spacing_g=48)
        self.assertGreater(len(proposed),0)
        self.assertLess(len(proposed),len(requested))
        self.assertTrue(set(proposed)<=set(requested))
        self.assertTrue(all(b.generation-a.generation>=48
            for a,b in zip(proposed,proposed[1:])))
        self.assertTrue(all(a.state!=b.state for a,b in zip(proposed,proposed[1:])))
        with self.assertRaises(ValueError):
            rate_limited_candidate(FIXTURE,min_spacing_g=7)

    @unittest.skipUnless(ALIGNMENT_FILE.exists(), "GitHub's full Suno alignment is absent in local fixture-only checkout")
    def test_full_song_all_403_words_and_66_lines(self):
        report=audit(ALIGNMENT_FILE)
        self.assertEqual(report['word_events'],403)
        self.assertEqual(report['line_clear_events'],66)
        self.assertEqual(len(score(ALIGNMENT_FILE)),66)
        self.assertTrue(all(x['state'] in STATES for x in report['all_cues']))
        self.assertLess(report['smallest_change_gap_generations'],48)

if __name__=='__main__':unittest.main()
