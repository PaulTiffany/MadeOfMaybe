"""Independent B3/S23 checks of the one-board mouth-toggle experiment."""
import unittest
from life.core import evolve
from life.singer_pilot import APPARATUS, MOUTH_BLOCK, face_cells, initial_state


class ActuatorProof(unittest.TestCase):
    def test_apparatus_and_face_are_stationary(self):
        base = APPARATUS | face_cells()
        self.assertEqual(evolve(base), base)
        self.assertFalse(MOUTH_BLOCK & base)

    def test_three_signals_alternate_and_recover(self):
        base = APPARATUS | face_cells()
        cells = initial_state()
        for generation in range(575):
            if generation in (170, 362, 554):
                self.assertEqual(MOUTH_BLOCK.issubset(cells), generation != 362)
            cells = evolve(cells)
        self.assertEqual(cells, base | MOUTH_BLOCK)
        self.assertEqual(evolve(cells), cells)

    def test_two_signals_return_exactly_to_original(self):
        cells = initial_state(pulses=2, face=False)
        for generation in range(395):
            cells = evolve(cells)
        self.assertEqual(cells, APPARATUS)


if __name__ == "__main__":
    unittest.main()
