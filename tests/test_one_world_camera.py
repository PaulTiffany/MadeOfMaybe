"""First source must be camera-centered UNTIL actual native collision."""
import unittest
from life.core import place,evolve
from life.physical_lip_splitter_bridge import split_input
from life.relocated_singer_anchor import TRANSLATION,relocated_anchor
from life.full_song_karaoke import GPS
from preview.one_world_camera import camera_at,projected

class OneWorldCameraTests(unittest.TestCase):
    def test_camera_centers_actual_first_glider_before_collision(self):
        universe=place(relocated_anchor(),-TRANSLATION[0],-TRANSLATION[1])
        source=split_input()
        # actual physically translated full source world uses singer-local origin
        # = old source local + (new source position - original source position).
        glider=place(source,*TRANSLATION)
        world=relocated_anchor()
        for g in range(145):
            if g%8==0:
                self.assertTrue(glider<=world,('input no longer isolated',g))
                x=sum(x for x,y in glider)/5
                y=sum(y for x,y in glider)/5
                px,py=projected(x-TRANSLATION[0],y-TRANSLATION[1],g/GPS)
                self.assertLess(abs(px-640),20)
                self.assertLess(abs(py-360),20)
            if g<144:
                glider=evolve(glider);world=evolve(world)
    def test_locks_on_actual_catalyst_then_reveals_singer(self):
        self.assertAlmostEqual(camera_at(0)[0],420.2)
        self.assertAlmostEqual(camera_at(.75)[0],384.2)
        x,y,s=camera_at(2.)
        self.assertAlmostEqual(x,382.)
        self.assertAlmostEqual(y,169.5)
        self.assertAlmostEqual(s,7.3)
        x,y,s=camera_at(11.)
        self.assertAlmostEqual(x,200.)
        self.assertAlmostEqual(y,-8.)
        self.assertAlmostEqual(s,1.055)
        self.assertEqual(camera_at(100),camera_at(11))
        with self.assertRaises(ValueError):camera_at(-.1)

if __name__=='__main__':unittest.main()
