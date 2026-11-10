"""Truth-table test of a PHYSICAL two-input Life collision, not software AND."""
import unittest
from life.core import evolve
from life.glider_controlled_mouth import BLOCK
from life.dual_source_native_gate import (
    clock_and_input,world,readout,qualify
)
class NativeDualGateTests(unittest.TestCase):
    def test_two_gliders_are_both_required(self):
        clock,signal=clock_and_input()
        for a,b,expected in ((0,0,False),(1,0,False),(0,1,False),(1,1,True)):
            state=(set(clock) if a else set())|(set(signal) if b else set())
            for _ in range(124):state=evolve(state)
            self.assertEqual(BLOCK<=state,expected)
    def test_four_combined_world_truth_table_and_life_persistence(self):
        certificate=qualify(postflight=56)
        self.assertEqual(len(certificate['truth_table']),4)
        self.assertTrue(certificate['physical_two_glider_AND'])
        self.assertFalse(certificate['lip_actuator_physically_connected'])
    def test_initial_world_is_real_gliders_not_injected_outputs(self):
        self.assertEqual([len(world(a,b)) for a,b in
            [(False,False),(True,False),(False,True),(True,True)]],
            [10,20,20,30])
        for a,b in [(False,False),(False,True),(True,False),(True,True)]:
            self.assertEqual(readout(world(a,b)),(False,False,False))
    def test_bad_glider_phases_rejected(self):
        with self.assertRaises(ValueError):clock_and_input(123)
if __name__=='__main__':unittest.main()
