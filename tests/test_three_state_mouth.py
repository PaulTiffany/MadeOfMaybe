"""Three-state pose *targets*: qualified still lifes, not a live controller."""
import unittest
from life.core import evolve,parse_rle,encode_rle
from life.three_state_mouth import (STATES, FACE, mouth, mouth_pixels, scene,
                                    MOUTH_Y, APERTURE, HALF_WIDTH)

class ThreePoseTests(unittest.TestCase):
    def test_each_pose_is_a_still_life(self):
        for name in STATES:
            with self.subTest(name=name):
                state=scene(name)
                self.assertEqual(evolve(state),state)
                self.assertEqual(evolve(mouth(name)),mouth(name))
                self.assertEqual(evolve(FACE),FACE)
                self.assertFalse(FACE & mouth(name))

    def test_all_mouths_have_same_anchored_corners(self):
        for name in STATES:
            self.assertIn((-HALF_WIDTH,MOUTH_Y), mouth_pixels(name))
            self.assertIn((HALF_WIDTH,MOUTH_Y), mouth_pixels(name))

    def test_apertures_are_distinct_and_progressive(self):
        top_and_bottom={}
        for name in STATES:
            ys=[y for x,y in mouth_pixels(name) if x==0]
            top_and_bottom[name] = max(ys)-min(ys)
        self.assertTrue(top_and_bottom['closed'] < top_and_bottom['medium']
                        < top_and_bottom['open'])
        self.assertEqual([top_and_bottom[s] for s in STATES],[2,8,16])

    def test_face_rle_round_trip(self):
        for name in STATES:
            cells=scene(name)
            rebuilt=parse_rle(encode_rle(cells,[name]))
            ox=min(x for x,y in cells); oy=min(y for x,y in cells)
            self.assertEqual(rebuilt,{(x-ox,y-oy) for x,y in cells})

    def test_arbitrary_same_pose_stays_stable(self):
        for name in STATES:
            current=scene(name)
            for _ in range(12):
                self.assertEqual(evolve(current),current)
                current=evolve(current)

if __name__=='__main__':
    unittest.main()
