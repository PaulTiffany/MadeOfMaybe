"""Clock conversion and phase contracts for audio-locked Life signals."""
import unittest
from life.lyric_clock import (nearest_phase,plan_we,retimed_routes,
                              physical_initial,mouth_timing_targets)
from life.glider_controlled_mouth import block_make_at,block_erase_at
from life.native_lyric_word import routes

class LyricClockTests(unittest.TestCase):
    def test_half_up_phases(self):
        self.assertEqual(nearest_phase(11.224,48,0),540)
        self.assertEqual(nearest_phase(11.224,192,0),2156)
        self.assertEqual(nearest_phase(11.224,192,2),2154)
        self.assertRaises(ValueError,nearest_phase,-1,48,0)
        self.assertRaises(ValueError,nearest_phase,2,0,0)
        self.assertRaises(ValueError,nearest_phase,2,48,4)

    def test_musical_onsets_and_physical_writing_windows(self):
        plans=[plan_we(gps) for gps in (48,96,192)]
        for p in plans:
            self.assertLessEqual(abs(p.onset_error_s),2/p.gps+1e-9)
            self.assertLessEqual(abs(p.clear_error_s),2/p.gps+1e-9)
            self.assertEqual(p.make_at%4,0)
            self.assertEqual(p.erase_by%4,2)
        self.assertAlmostEqual(plans[0].preroll_s,1.0,places=6)
        self.assertAlmostEqual(plans[2].preroll_s,.25,places=6)
        self.assertAlmostEqual(plans[2].erase_tail_s,68/192,places=6)

    def test_all_retimed_routes_remain_native_glider_phase_legal(self):
        for gps in (48,96,192):
            p=plan_we(gps)
            rr=retimed_routes(p)
            self.assertEqual(len(rr),35)
            self.assertEqual(set((r.x,r.y) for r in rr),
                             set((r.x,r.y) for r in routes()))
            for r in rr:
                self.assertEqual(r.make_tick%4,0)
                self.assertEqual(r.erase_tick%4,2)
                self.assertTrue(block_make_at(r.make_tick))
                self.assertTrue(block_erase_at(r.erase_tick))
            self.assertTrue(physical_initial(p))

    def test_mouth_audio_is_unchanged_when_rate_changes(self):
        a=mouth_timing_targets(24,192)
        self.assertEqual(a['medium'][0]['audio_s'],124/24)
        self.assertEqual(a['open'][0]['target_generation'],248*8)
        self.assertNotEqual(a['medium'][0]['target_generation'],124)

    def test_needs_line_hold_not_end_of_each_token(self):
        # The first word's duration is 255 ms; our *current* erase spread
        # alone is 68 generations (1.42 s even at 2x).
        a=plan_we(48)
        self.assertGreater(a.erase_tail_s,.255)
        self.assertLess(plan_we(192).preroll_s,.30)
        self.assertRaises(ValueError,plan_we,48,11.225)

class PhysicalClockQualificationTests(unittest.TestCase):
    def test_real_word_works_at_fixed_faster_clocks_with_isolated_corridors(self):
        """A rigorous rescore test: no fake images, no cell injection, no bubble.

        We must enlarge *physical* pixel pitch when extending arrival delays;
        simply backstepping old pitch-20 gliders causes new collisions.
        """
        from life.core import evolve
        from life.lyric_clock import physical_components,physical_targets
        for rate,pitch in ((48,80),(96,80),(192,160)):
            with self.subTest(rate=rate,pitch=pitch):
                p=plan_we(rate)
                parts=physical_components(p,pitch)
                targets=physical_targets(p,pitch)
                self.assertEqual(len(parts),35)
                self.assertEqual(len(set().union(*targets)),140)
                world=set().union(*parts.values())
                for gen in range(p.erase_by+17):
                    self.assertEqual(world,set().union(*parts.values()),
                                     f'{rate} gps: crosstalk at g{gen}')
                    if gen==p.first_make-1:
                        self.assertFalse(any(c<=world for c in targets))
                    if gen==p.make_at:
                        self.assertTrue(all(c<=world for c in targets))
                    if gen==p.make_at+16:
                        self.assertTrue(all(c<=world for c in targets))
                    if gen==p.erase_by:
                        self.assertEqual(world,set())
                    if gen < p.erase_by+16:
                        world=evolve(world)
                        parts={name:evolve(cells) for name,cells in parts.items()}
                self.assertEqual(world,set())

    def test_retiming_requires_corridor_requalification(self):
        """Naively reusing the old pixel pitch physically collides."""
        from life.core import evolve
        from life.lyric_clock import physical_components
        p=plan_we(96)
        parts=physical_components(p,pitch=20)
        world=set().union(*parts.values())
        for gen in range(10):
            if world != set().union(*parts.values()):
                return
            world=evolve(world)
            parts={name:evolve(cells) for name,cells in parts.items()}
        self.fail('Expected the documented near-instant crosstalk from naive 96 gps scaling')

if __name__=='__main__': unittest.main()
