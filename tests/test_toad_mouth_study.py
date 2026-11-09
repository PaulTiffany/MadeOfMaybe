"""Verified native toad visual study; no claims of glider-controlled timing."""
import unittest
from life.core import evolve
from life.toad_mouth_study import FACE,MOUTH_BAND,MOUTH_OPEN,initial

class ToadMouthStudyTests(unittest.TestCase):
    def test_stable_surrounding_face(self):
        self.assertEqual(evolve(FACE),FACE)

    def test_true_two_phase_shape_change(self):
        self.assertNotEqual(MOUTH_BAND,MOUTH_OPEN)
        self.assertEqual(evolve(MOUTH_BAND),MOUTH_OPEN)
        self.assertEqual(evolve(MOUTH_OPEN),MOUTH_BAND)
        self.assertEqual(len({y for _,y in MOUTH_BAND}),2)
        self.assertEqual(len({y for _,y in MOUTH_OPEN}),4)

    def test_genuine_independence_100_generations(self):
        board=initial()
        mouth=MOUTH_BAND
        for gen in range(100):
            self.assertEqual(board,FACE|mouth,gen)
            board=evolve(board)
            mouth=evolve(mouth)
