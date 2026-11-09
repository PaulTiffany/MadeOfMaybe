"""Proof of native Life three-state mouth control, with skip and reversals."""
import unittest

from life.core import evolve, parse_rle
from life.glider_controlled_mouth import (
    BLOCK, UPPER_LIP, MEDIUM_TARGETS, OPEN_TARGETS,
    POSE_SAMPLES, FULL_DURATION, ROUTING, BANK_SCHEDULES,
    block_make_at, block_erase_at, active_pixels, prepared_face,
    signal_components, components, universe,
)
from life.export_operational import compact_rle


class PrimitiveTests(unittest.TestCase):
    def test_clean_two_glider_synthesis_at_fixed_clock(self):
        for t in (4,40,124,244):
            with self.subTest(t=t):
                cells=block_make_at(t)
                self.assertEqual(len(cells),10)
                for g in range(t):cells=evolve(cells)
                self.assertEqual(cells,BLOCK)
                self.assertEqual(evolve(cells),cells)

    def test_clean_one_glider_block_deletion_at_fixed_clock(self):
        for t in (22,46,246):
            with self.subTest(t=t):
                cells=BLOCK|block_erase_at(t)
                self.assertEqual(len(cells),9)
                for g in range(t):cells=evolve(cells)
                self.assertEqual(cells,set())

    def test_empty_destination_is_noop(self):
        self.assertEqual(evolve(set()),set())


class ThreeStateGliderControl(unittest.TestCase):
    def test_face_and_upper_lip_permanently_stable(self):
        self.assertEqual(evolve(UPPER_LIP),UPPER_LIP)
        self.assertEqual(evolve(set(prepared_face())),set(prepared_face()))
        self.assertEqual(evolve(UPPER_LIP|set(prepared_face())),
                         UPPER_LIP|set(prepared_face()))

    def test_785_life_circuit_state_transitions_and_composability(self):
        """Every frame is the result of one full Life step, no cell injection."""
        parts=components()
        world=universe()
        constant=UPPER_LIP | set(prepared_face())
        for g in range(FULL_DURATION):
            self.assertEqual(world,set().union(*parts.values()),
                             f'extraneous Life interaction at G{g}')
            self.assertTrue(constant <= world, f'permanent face changed G{g}')
            if g in POSE_SAMPLES:
                state=POSE_SAMPLES[g]
                expected_m=4 if state=='medium' else 0
                expected_o=4 if state=='open' else 0
                present_m=sum({(tx+dx,ty+dy) for dx,dy in BLOCK} <= world
                              for tx,ty in MEDIUM_TARGETS)
                present_o=sum({(tx+dx,ty+dy) for dx,dy in BLOCK} <= world
                              for tx,ty in OPEN_TARGETS)
                self.assertEqual((present_m,present_o),(expected_m,expected_o),
                                 (g,state))
                self.assertTrue(active_pixels(state)<=world)
            # Direct skip section has no medium lip after last close.
            if 550 <= g <= 778:
                self.assertFalse(any(
                    {(tx+dx,ty+dy) for dx,dy in BLOCK} <= world
                    for tx,ty in MEDIUM_TARGETS),f'medium appeared during skip G{g}')
            world=evolve(world)
            parts={name:evolve(cells) for name,cells in parts.items()}

    def test_export_roundtrip_preserves_every_initial_cell(self):
        initial=universe()
        restored=parse_rle(compact_rle(initial,('native 3-state mouth',)))
        xmin=min(x for x,y in initial);ymin=min(y for x,y in initial)
        self.assertEqual(restored,{(x-xmin,y-ymin) for x,y in initial})
        self.assertLess(len(compact_rle(initial)),30000)

    def test_gliders_only_at_initial_generation(self):
        # Checks packet makeup, not merely the rendered frames.
        self.assertEqual(len(signal_components()),8)
        self.assertEqual(sum(len(x) for x in signal_components().values()),240)
        self.assertEqual(set(ROUTING),{(bank,i) for bank in ('medium','open')
                                      for i in range(4)})
        self.assertEqual(len(BANK_SCHEDULES['medium']),4)
        self.assertEqual(len(BANK_SCHEDULES['open']),4)


if __name__=='__main__':
    unittest.main()
