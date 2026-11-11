"""Protect the difference between real shared control and a video overlay."""
import unittest
from preview.render_first_line_singer import make_image
from life.first_line_karaoke import score,GPS,PITCH
from life.physical_lip_splitter_bridge import CAUSAL_WORD_G,CAUSAL_LIP_G

class CausalFirstLineCameraTests(unittest.TestCase):
    def test_first_original_life_glyph_pixel_follows_actual_shared_source(self):
        g=CAUSAL_WORD_G
        self.assertEqual(GPS,192)
        self.assertEqual(score()[0].targets[0],(0,0))
        on=make_image(g,set(),{},first_glyph_pixel_alive=True)
        off=make_image(g,set(),{},first_glyph_pixel_alive=False)
        # The two views differ precisely in the rectangle representing the
        # original first WE block, not in the rest of the letters.
        self.assertEqual(on.size,off.size)
        self.assertEqual(on.getpixel((50,50)),off.getpixel((50,50)))
        diff=[]
        for y in range(260,320):
            for x in range(580,700):
                if on.getpixel((x,y))!=off.getpixel((x,y)):diff.append((x,y))
        self.assertGreater(len(diff),8)
        self.assertLess(len(diff),90)

    def test_causal_event_times_come_from_current_native_line(self):
        self.assertEqual(CAUSAL_WORD_G,score()[0].make_g)
        self.assertGreater(CAUSAL_LIP_G,CAUSAL_WORD_G)
        self.assertEqual(CAUSAL_LIP_G-CAUSAL_WORD_G,156)

if __name__=='__main__':unittest.main()
