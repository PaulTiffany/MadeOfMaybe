"""Exact physical 1→4 Life splitter qualification, not just a wiring diagram."""
import unittest
from life.core import evolve
from life.cascaded_lyric_splitter import (catalysts,seed,output_gliders,check,
    OUTPUT_GENERATION)

class CascadedLyricSplitterTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report=check()

    def test_one_input_produces_four_clean_gliders_without_extra_cells(self):
        self.assertEqual(self.report['input_count'],1)
        self.assertEqual(self.report['output_count'],4)
        self.assertEqual(self.report['generation'],683)
        self.assertEqual(self.report['catalysts'],252)
        self.assertEqual(sorted(x['velocity'] for x in self.report['output_ports']),
                         [(-1,-1),(-1,-1),(1,1),(1,1)])

    def test_absent_source_keeps_all_three_catalysts_without_outputs(self):
        off=seed(source_enabled=False)
        self.assertEqual(off,catalysts())
        self.assertEqual(evolve(off),off)
        self.assertEqual(output_gliders(off),[])

    def test_report_does_not_invent_full_lip_wiring(self):
        self.assertEqual(self.report['actual_lip_tiles_connected'],0)
        self.assertFalse(self.report['full_song_fanout_qualified'])

if __name__=='__main__':unittest.main()
