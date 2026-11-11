"""Exact B3/S23 demonstration of a real LWSS corner (not a renderer turn)."""
import unittest
from life.vertical_lwss_corner import (
    STATION,INPUT,evolve,drift,shifted,outgoing_lwss,qualify
)
from life.core import encode_rle,parse_rle,place

class VerticalLwssCornerTests(unittest.TestCase):
    def test_incoming_ship_is_physically_vertical(self):
        self.assertEqual(len(INPUT),9)
        self.assertEqual(drift(INPUT,4),shifted(INPUT,0,2))
        self.assertEqual(len(STATION),19)
        self.assertEqual(evolve(STATION),set(STATION))

    def test_native_collision_makes_outgoing_horizontal_ship(self):
        r=qualify()
        self.assertEqual(r['rule'],'B3/S23')
        self.assertTrue(r['source_ablation_prevents_output'])
        self.assertFalse(r['station_reusable'])
        ship=outgoing_lwss(drift(STATION|INPUT,200))
        self.assertEqual(drift(ship,40),shifted(ship,-20,0))

    def test_golly_export_roundtrip(self):
        src=STATION|INPUT
        txt=encode_rle(src,('One-shot true LWSS right-angle turn: incoming from above, output left.',))
        got=parse_rle(txt)
        x0=min(x for x,y in src);y0=min(y for x,y in src)
        self.assertEqual(got,place(src,-x0,-y0))

if __name__=='__main__':unittest.main()
