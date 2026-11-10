"""Phrase transitions are only existing real karaoke Life events."""
import unittest
from pathlib import Path
from life.phrase_mouth_gate import phrase_groups,phrase_cues,phrase_gate_edges,state_at,audit,STATES
from life.word_driven_expression import score
from life.full_song_karaoke import ALIGNMENT_FILE,GPS

FIXTURE=Path(__file__).resolve().parents[1]/'data'/'first_verse_alignment_fixture.json'

class PhraseMouthGateTests(unittest.TestCase):
    def test_first_two_phrase_cycles(self):
        events=phrase_cues(FIXTURE)
        self.assertEqual([(c.generation,c.state) for c in events[:4]],
                         [(2156,'medium'),(2272,'open'),(2416,'medium'),(2578,'closed')])
        self.assertEqual([(c.generation,c.state) for c in events[4:]],
                         [(2976,'medium'),(3084,'open'),(3208,'medium'),(3402,'closed')])
        self.assertEqual(state_at(2152,FIXTURE),'closed')
        self.assertEqual(state_at(2156,FIXTURE),'medium')
        self.assertEqual(state_at(2312,FIXTURE),'open')
        self.assertEqual(state_at(2578,FIXTURE),'closed')
        self.assertEqual(state_at(2900,FIXTURE),'closed')
    def test_switches_are_actual_word_make_or_line_clear_generations(self):
        lines=score(FIXTURE)
        valid_word={(line.line_index,w.word_index,w.make_g) for line in lines for w in line.words}
        valid_clear={(line.line_index,line.clear_g) for line in lines}
        cues=phrase_cues(FIXTURE)
        for c in cues:
            self.assertIn(c.state,STATES)
            if c.source_kind=='word_make':
                self.assertIn((c.source_line,c.source_word,c.generation),valid_word)
                self.assertNotEqual(c.state,'closed')
            else:
                self.assertEqual(c.action,'close')
                self.assertIn((c.source_line,c.generation),valid_clear)
                self.assertEqual(c.state,'closed')
        self.assertTrue(all(b.generation-a.generation>=96 for a,b in zip(cues,cues[1:])))
        self.assertTrue(all(a.state!=b.state for a,b in zip(cues,cues[1:])))
    def test_short_line_gaps_are_one_long_sung_phrase(self):
        if not ALIGNMENT_FILE.exists():self.skipTest('full song absent')
        groups=phrase_groups(ALIGNMENT_FILE)
        self.assertTrue(any(len(g)>1 for g in groups))
        for a,b in zip(groups,groups[1:]):
            self.assertGreaterEqual(b[0].words[0].make_g-max(x.clear_g for x in a),96)
        for group in groups:
            for a,b in zip(group,group[1:]):
                self.assertLess(b.words[0].make_g-a.clear_g,96)
    def test_minimal_external_loop_interface_is_two_edges_per_phrase(self):
        edges=phrase_gate_edges(FIXTURE)
        self.assertEqual([(c.action,c.state) for c in edges],
                         [('start','medium'),('close','closed'),
                          ('start','medium'),('close','closed')])
        self.assertEqual(len(edges),4)
    def test_rejects_unrealistic_response_bounds(self):
        for n in (0,7,24,47,49,95):
            with self.subTest(n=n),self.assertRaises(ValueError):
                phrase_cues(FIXTURE,min_switch_g=n)
        self.assertEqual(GPS,192)
    @unittest.skipUnless(ALIGNMENT_FILE.exists(),'full alignment absent')
    def test_full_song_35_phrases_not_403_independent_mouth_rigs(self):
        r=audit(ALIGNMENT_FILE)
        for key,value in {'karaoke_words':403,'karaoke_lines':66,
                          'sung_phrases':35,'phrase_starts':35,
                          'medium_open_alternations':148,'phrase_closures':35,
                          'total_mouth_transitions':218,
                          'external_phrase_gate_events':70}.items():
            self.assertEqual(r[key],value,key)
        self.assertGreaterEqual(r['smallest_actual_transition_gap_g'],96)
        self.assertTrue(r['source_events_only'])
        self.assertFalse(r['independent_mouth_oscillator'])
        self.assertFalse(r['repeat_loop_physically_qualified'])
        self.assertFalse(r['native_life_full_lip_gate_connected'])

if __name__=='__main__':unittest.main()
