"""A Life word-marker LWSS and a Suno vocal signal physically form a lip cell."""
import unittest
from life.core import evolve,place
from life.native_word_vocal_link import (
    marker_to_mouth,MOUTH_CORNER,MARKER_STATION,FIRST_WORD_G,
    UPSTREAM_PERIODS,components,world)
from life.glider_controlled_mouth import BLOCK,UPPER_LIP
from life.relocated_singer_anchor import SINGER_TRANSLATION
from life.vertical_lwss_corner import STATION,INPUT

class NativeWordVocalLinkTests(unittest.TestCase):
    def test_one_real_world_and_preserved_upper_lip(self):
        p=components()
        self.assertEqual(list(map(len,p)),[6408,648,1519,240,52])
        self.assertEqual(len(world()),8867)
        self.assertEqual(sum(map(len,p)),len(world()))
        self.assertTrue(place(UPPER_LIP,SINGER_TRANSLATION[0],
                        SINGER_TRANSLATION[1]+32)<=p[0])

    def test_native_two_source_word_marker_and_vocal_lip_truth_table(self):
        for word in (False,True):
            for vocal in (False,True):
                live=marker_to_mouth(word=word,vocal=vocal)
                for _ in range(FIRST_WORD_G):live=evolve(live)
                self.assertEqual(place(BLOCK,*MOUTH_CORNER)<=live,
                                 word and vocal,(word,vocal))
                if word and vocal:
                    for _ in range(144):live=evolve(live)
                    self.assertFalse(place(BLOCK,*MOUTH_CORNER)<=live)

    def test_real_word_source_is_original_19_cell_turner_and_LWSS(self):
        p=marker_to_mouth(word=True,vocal=False)
        x,y=MARKER_STATION
        self.assertTrue(place(STATION,x,y)<=p)
        self.assertTrue(place(INPUT,x,y-2*UPSTREAM_PERIODS)<=p)
        self.assertEqual(len(p),47)
        self.assertEqual(len(marker_to_mouth(word=False,vocal=True)),43)
        self.assertEqual(len(marker_to_mouth(word=False,vocal=False)),38)
if __name__=='__main__':unittest.main()
