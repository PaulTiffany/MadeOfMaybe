"""Native rounded still-life bubble with only the prior 19-cell LWSS turner."""
import unittest
from life.core import evolve
from life.rounded_bubble_edge_candidate import (
 rim,device,components,universe,CENTER,RADII,STATION_LOCAL
)
from life.vertical_lwss_corner import STATION,INPUT
class RoundedBubbleTests(unittest.TestCase):
    def test_stable_round_bubble_and_real_native_tail(self):
        self.assertEqual((CENTER,RADII),((655,-170),(350,185)))
        self.assertEqual(len(rim()),852)
        self.assertEqual(evolve(set(rim())),set(rim()))
    def test_exact_existing_turner_and_physical_apertures(self):
        self.assertEqual(STATION_LOCAL,(925,-125))
        self.assertEqual((len(STATION),len(INPUT),len(device())),(19,9,49))
        self.assertEqual(list(map(len,components())),[7902,852,49])
        self.assertEqual(len(universe()),8803)
    def test_no_initial_overlap(self):
        parts=components()
        self.assertEqual(sum(map(len,parts)),len(set().union(*parts)))
if __name__=='__main__':unittest.main()
