"""Tests prove cellular behavior, NOT artistic legibility of the face."""
import unittest
from life.core import evolve
from life.beehive_mouth import APPARATUS, FACE, OPEN, initial_state
from life.beehive_scene import components, scene

class BeehiveMouthTests(unittest.TestCase):
    def test_stable_parts(self):
        self.assertEqual(evolve(APPARATUS), APPARATUS)
        self.assertEqual(evolve(FACE), FACE)
        self.assertFalse(OPEN & FACE)

    def test_three_real_gliders_open_close_open(self):
        state=initial_state()
        samples={}
        for g in range(650):
            if g in (150,340,540):
                samples[g]=OPEN.issubset(state)
            state=evolve(state)
        self.assertEqual(samples,{150:True,340:False,540:True})
        self.assertEqual(state,APPARATUS|FACE|OPEN)

    def test_face_circuit_noninteraction(self):
        full=initial_state()
        circuit=full-FACE
        for g in range(610):
            self.assertEqual(full,circuit|FACE,g)
            full=evolve(full)
            circuit=evolve(circuit)

    def test_existing_bubble_and_pulsar_still_independent(self):
        individual=components()
        board=scene()
        for g in range(610):
            self.assertEqual(board,set().union(*individual.values()),g)
            board=evolve(board)
            individual={k:evolve(v) for k,v in individual.items()}

if __name__=='__main__':
    unittest.main()
