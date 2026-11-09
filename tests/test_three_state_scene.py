"""Verify reuse of the unchanged bubble with each stable singer pose."""
import unittest
from life.core import evolve
from life.three_state_mouth import STATES
from life.three_state_scene import parts,universe

class ThreeStateCompositeTests(unittest.TestCase):
    def test_each_candidate_is_independent_from_bubble_and_symbol(self):
        for state in STATES:
            with self.subTest(state=state):
                individual=parts(state)
                actual=universe(state)
                for generation in range(12):
                    self.assertEqual(actual,set().union(*individual.values()),generation)
                    actual=evolve(actual)
                    individual={name:evolve(c) for name,c in individual.items()}
                self.assertEqual(actual,universe(state))

if __name__=='__main__':
    unittest.main()
