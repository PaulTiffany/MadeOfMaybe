"""Reproducible source-signal → lyric pixel AND mouth 3-state causal tests."""
from __future__ import annotations
import unittest

from life.core import evolve, place, parse_rle
from life.export_operational import compact_rle
from life.glider_controlled_mouth import BLOCK
from life.full_song_karaoke import ALIGNMENT_FILE, GPS, compile_plan
from life.lyric_cues import read_alignment
from life.lyric_mouth_fanout import (
    PRIMARY_INPUT,CATALYSTS,NORTHWEST_GLIDER,SOUTHEAST_GLIDER,SPLIT_G,
    CLOSED_PORT,OPEN_PORT,CHECKPOINTS,FINAL_QUALIFICATION_G,
    events,universe,mouth_state,formed_word_pixels,full_song_mouth_intent,
)


def at_tick(seed, g):
    live=set(seed)
    for _ in range(g):live=evolve(live)
    return live


class SharedPhysicalFanoutTests(unittest.TestCase):
    def test_one_input_becomes_exactly_two_gliders_and_restores_apparatus(self):
        self.assertEqual(len(CATALYSTS),84)
        self.assertEqual(len(PRIMARY_INPUT),5)
        self.assertEqual(evolve(set(CATALYSTS)),set(CATALYSTS))
        # No input: there is no output, because the whole apparatus is stable.
        live=set(CATALYSTS)|set(PRIMARY_INPUT)
        for g in range(SPLIT_G+1):
            if g==SPLIT_G:
                self.assertEqual(live,set(CATALYSTS)|set(NORTHWEST_GLIDER)|set(SOUTHEAST_GLIDER))
            if g<SPLIT_G:live=evolve(live)
        self.assertEqual(len(live-set(CATALYSTS)),10)

    def test_real_circuit_repeats_with_two_inputs_400_generations_apart(self):
        live=set(CATALYSTS)|set(PRIMARY_INPUT)|place(set(PRIMARY_INPUT),-100,-100)
        for g in range(741):
            if g==740:
                self.assertTrue(CATALYSTS<=live)
                self.assertEqual(len(live-set(CATALYSTS)),20)  # 4 output gliders
            if g<740:live=evolve(live)

    def test_shared_score_is_karaoke_clock_not_separate_mouth_timer(self):
        first=events()
        self.assertEqual([e.word for e in first],['WE','MADE','A','WINDOW'])
        self.assertEqual([e.make_g for e in first],[2156,2204,2272,2296])
        self.assertEqual(GPS,192)
        self.assertEqual([e.action for e in first],['erase','make','erase','make'])
        self.assertEqual([e.mouth_port for e in first],['closed','open','open','closed'])
        for e in first:
            self.assertEqual(e.trigger_generation%4,0)
            self.assertEqual(e.trigger_generation+600+4*e.flight_steps,e.make_g)
        plan=full_song_mouth_intent()
        self.assertEqual([p['generation'] for p in plan[:4]],[e.make_g for e in first])
        self.assertEqual([p['target_state'] for p in plan[:4]],
                         ['medium','open','medium','closed'])
        if ALIGNMENT_FILE.exists():
            self.assertEqual(len(plan),403)  # exact connected Suno alignment
        else:
            self.assertEqual(len(plan),14)  # explicitly labelled fixture only

    def test_four_independent_causal_event_triggers_cycle_three_modes(self):
        live=universe()
        observed={}
        for g in range(FINAL_QUALIFICATION_G+1):
            if g in CHECKPOINTS:
                observed[g]=(mouth_state(live),formed_word_pixels(live))
                self.assertEqual(observed[g][0],CHECKPOINTS[g],f'mouth at generation {g}')
            if g<FINAL_QUALIFICATION_G:live=evolve(live)
        self.assertEqual(list(observed),list(CHECKPOINTS))
        for g,(_,pixels) in observed.items():
            self.assertEqual(sum(pixels.values()),sum(e.make_g<=g for e in events()))
        expected=set().union(*(place(set(CATALYSTS),*e.splitter_translation) for e in events()))
        expected |= place(BLOCK,*CLOSED_PORT)
        for e in events():expected |= place(BLOCK,*e.word_pixel)
        # All eight outputs have been consumed. No uncontrolled glider debris.
        self.assertEqual(live,expected)
        self.assertEqual(len(live),4*84 + 5*4)

    def test_trigger_knockout_destroys_both_the_word_pixel_and_mouth_transition(self):
        expected_states=('closed','medium','open','medium')
        for i,e in enumerate(events()):
            with self.subTest(missing_input=e.word):
                # No runtime intervention: the trigger glider is simply absent
                # from the alternative initial world. All partners remain.
                live=at_tick(universe(frozenset({i})),e.make_g+12)
                self.assertFalse(formed_word_pixels(live)[e.word])
                self.assertEqual(mouth_state(live),expected_states[i])

    def test_golly_rle_roundtrip_contains_only_real_initial_cells(self):
        seed=universe()
        recovered=parse_rle(compact_rle(seed))
        x0=min(x for x,y in seed);y0=min(y for x,y in seed)
        self.assertEqual(recovered,place(seed,-x0,-y0))
        self.assertEqual(len(seed),390)

if __name__=='__main__': unittest.main()
