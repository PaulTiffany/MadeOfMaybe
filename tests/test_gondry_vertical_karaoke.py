"""Backward from the physical movie frame, then forward in native B3/S23."""
import unittest
from life.core import evolve,place
from life.gondry_vertical_karaoke import (
    SHIP,EATER,PITCH_X,PITCH_Y,SONG_END_G,ship_phases,eater_reaction,
    word_plan,select_words,pixel_origins,receiver_cells,seed_cells,
    word_at_readout,verify_pulse_lanes,snapshot,certificate,lane_stride
)

class BackwardsStagedConwayFilmTests(unittest.TestCase):
    def test_real_southbound_LWSS_and_reusable_eater(self):
        self.assertEqual(len(SHIP),9)
        self.assertEqual(len(EATER),7)
        self.assertEqual(evolve(EATER),set(EATER))
        self.assertEqual(evolve(set(ship_phases()[3])),place(SHIP,0,2))
        self.assertEqual(eater_reaction()[40],EATER)
        self.assertEqual(len(eater_reaction()),41)

    def test_all_403_original_suno_words_backtraced_from_actual_onsets(self):
        words=word_plan()
        self.assertEqual(len(words),403)
        self.assertEqual(words[0].text,'WE')
        self.assertEqual(words[0].onset_g,2156)
        self.assertEqual(words[1].text,'MADE')
        self.assertEqual(words[1].onset_g,2204)
        self.assertNotEqual(words[0].lane,words[1].lane)
        self.assertEqual(sum(w.pixel_count for w in words),10366)
        self.assertGreater(lane_stride(),PITCH_X*words[0].max_column)
        self.assertEqual(SONG_END_G,45864)

    def test_inductive_all_song_collision_and_receiver_certificate(self):
        report=certificate()
        self.assertTrue(report['conveyor_arrives_physically_from_above'])
        self.assertTrue(report['full_song_exact_lyrics_backtraced'])
        self.assertTrue(report['song_end_snapshot_exactly_receiver_bank'])
        self.assertGreater(report['source_population_at_g0'],90000)
        self.assertFalse(report['native_singing_character_integrated'])
        self.assertFalse(report['full_native_singing_music_video_finished'])

    def test_actual_first_two_words_and_ablation_in_one_native_world(self):
        words=select_words(2)
        bank=receiver_cells(words)
        world=seed_cells(words)
        self.assertEqual(world,snapshot(0,words))
        probes={0,1,7,36,37,38,39,40,100,2160,2208,2456,2480,2520,2599}
        probes|={w.onset_g for w in words}
        for g in range(2601):
            if g in probes or g%16==0:
                self.assertEqual(world,snapshot(g,words),f'native mismatch at g{g}')
            if g==words[0].onset_g:
                self.assertTrue(word_at_readout(words[0])<=world)
            if g==words[1].onset_g:
                self.assertTrue(word_at_readout(words[1])<=world)
            if g<2600:world=evolve(world)
        self.assertEqual(world,bank)
        self.assertEqual(evolve(world),world)

        # Source ablation is literal deletion of first word's g0 ships.
        ablated=seed_cells(words,omit=words[0].index)
        self.assertEqual(len(world),len(bank))
        self.assertEqual(len(seed_cells(words))-len(ablated),9*words[0].pixel_count)
        for g in range(2601):
            if g==words[0].onset_g:
                self.assertFalse(word_at_readout(words[0]) <= ablated)
            if g==words[1].onset_g:
                self.assertTrue(word_at_readout(words[1]) <= ablated)
            if g<2600:ablated=evolve(ablated)
        self.assertEqual(ablated,bank)

if __name__ == '__main__':unittest.main()
