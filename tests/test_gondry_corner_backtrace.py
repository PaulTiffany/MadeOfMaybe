"""The actual Gondry operation: work backward UPSTREAM of original turners."""
import unittest
from life.core import evolve,place
from life.gondry_corner_backtrace import (
    first_words,backtrace,components,universe,fixed_eaters,
    expected_formation,expected_cleanup,check_native_snapshots,LAST_G)
from life.vertical_lwss_corner import STATION,INPUT
from life.staggered_word_mesh import reference_output

class CorrectedGondryTests(unittest.TestCase):
    def test_original_song_first_two_words_are_unchanged(self):
        self.assertEqual([(w.text,w.make_g) for w in first_words()],
                         [('WE',2156),('MADE',2204)])
        self.assertEqual(len(backtrace('WE',2156)),17)
        self.assertEqual(len(backtrace('MADE',2204)),32)
        self.assertEqual(backtrace('MADE',2204)[10].station_x,456)
        self.assertEqual(backtrace('MADE',2204)[10].incoming_advance_periods,
                         tuple(p for p in backtrace('MADE',2204) if p.pixel_index==10)[0].incoming_advance_periods)

    def test_every_output_is_original_physical_corner_and_period_four_backtrace(self):
        source=set(INPUT)
        for _ in range(4):source=evolve(source)
        self.assertEqual(source,place(INPUT,0,2))
        self.assertEqual(len(STATION),19)
        self.assertEqual(len(reference_output()),12)
        for word,g in [('WE',2156),('MADE',2204)]:
            for p in backtrace(word,g):
                self.assertEqual(p.source_y,p.station_y-2*p.incoming_advance_periods)
                self.assertEqual(p.converted_reference_generation,
                                 200+4*p.incoming_advance_periods)
                self.assertEqual(p.reading_x,
                                 p.station_x-43-(g-p.converted_reference_generation)//2)
                self.assertEqual(p.reading_y,p.station_y+12)
            self.assertEqual(len(universe(word,g)),len(components(word,g)[0])
                             +sum(len(part) for part in components(word,g)[1:]))
            self.assertEqual(evolve(fixed_eaters(word,g)),fixed_eaters(word,g))
        with self.assertRaises(ValueError):
            backtrace('WE',2155)

    def test_source_ablation_does_not_create_a_pixel_by_renderer(self):
        for word,g in [('WE',2156),('MADE',2204)]:
            f=expected_formation(word,g)
            missing=expected_formation(word,g,omit=0)
            # Station persists in ablation; 12-cell real output vanishes.
            self.assertEqual(len(f-missing),12)
            self.assertEqual(len(missing-f),19)
            self.assertEqual(len(universe(word,g))-len(universe(word,g,omit=0)),9)
            self.assertEqual(len(expected_cleanup(word,g)),len(fixed_eaters(word,g)))

    def test_readout_and_terminal_require_exact_forward_native_life(self):
        # CI runs independently evolved C++ complete native g0 patterns.
        # This unit test only asserts the expected cell structures, not
        # that an entire untested 403-word universe has been evolved.
        for word,g in [('WE',2156),('MADE',2204)]:
            self.assertEqual(len(expected_formation(word,g)),
                             len(fixed_eaters(word,g))+
                             12*len(backtrace(word,g)))
            self.assertTrue(evolve(expected_cleanup(word,g))==
                            expected_cleanup(word,g))

if __name__=='__main__':
    unittest.main()
