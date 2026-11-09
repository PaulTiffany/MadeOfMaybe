"""No bitmap/subtitle substitution: exact native Life packet state sampling."""
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

from life.core import evolve
from life.full_song_karaoke import (compile_plan,pixel_seed,physical_targets,GPS)
from life.glider_controlled_mouth import BLOCK
from life.life_cell_sampler import (block_alive_at,make_trace,erase_trace)
from life.lyric_cues import read_alignment
from preview.render_full_song_karaoke import (build_frame_intervals,
         sampled_signature,render,word_targets)

ROOT=Path(__file__).resolve().parents[1]
FIXTURE=ROOT/'data'/'first_verse_alignment_fixture.json'


class LifeCellSamplingTests(unittest.TestCase):
    def test_make_and_erase_are_exact_conway_reactions(self):
        self.assertEqual(len(make_trace()),41)
        self.assertEqual(len(erase_trace()),41)
        self.assertEqual(sum(make_trace()),1)
        self.assertEqual(erase_trace()[-1],False)
        self.assertEqual(erase_trace()[0],True)

    def test_sampler_matches_actual_302_step_b3s23_simulation(self):
        make,erase=200,302
        world=set(pixel_seed(make,erase))
        for g in range(erase+8):
            self.assertEqual(block_alive_at(make,erase,g),BLOCK<=world,
                             f'full Life disagreed at generation {g}')
            world=evolve(world)
        self.assertFalse(world)

    def test_first_actual_suno_word_trajectory(self):
        plans=compile_plan(read_alignment(FIXTURE))
        word=plans[0].words[0]
        m,e=word.make_g,plans[0].clear_g
        world=set(pixel_seed(m,e))
        picks={m-1,m,m+1,e-4,e-3,e-2,e-1,e,e+1}
        for g in range(e+2):
            if g in picks:
                self.assertEqual(block_alive_at(m,e,g),BLOCK<=world,
                                 f'Suno word full Life mismatch at generation {g}')
            world=evolve(world)

    def test_projected_pixel_positions_are_exact_stage_targets(self):
        line=compile_plan(read_alignment(FIXTURE))[0]
        targets=word_targets(line)
        self.assertEqual(len(targets),len(line.words))
        for w,blockcoords in zip(line.words,targets):
            self.assertEqual(len(blockcoords),w.pixel_count)
            for (logical_x,logical_y),(x,y) in zip(blockcoords,physical_targets(line,w)):
                self.assertEqual(x,logical_x*line.pitch)
                self.assertEqual(y,line.y_origin+logical_y*line.pitch)

    def test_frame_event_sequence_matches_physical_generations(self):
        lines=compile_plan(read_alignment(FIXTURE))
        events=build_frame_intervals(lines,10.5,19.,24)
        self.assertEqual(events[0]['line_index'],None)
        self.assertEqual(events[-1]['live_words'],[])
        self.assertEqual(events[-1]['line_index'],None)
        self.assertEqual(events[0]['first_frame'],252)
        self.assertEqual(events[-1]['last_frame_exclusive'],456)
        self.assertEqual(sum(ev['last_frame_exclusive']-ev['first_frame'] for ev in events),204)
        for ev in events:
            g=round(ev['first_frame']*GPS/24)
            idx,flags=sampled_signature(lines,[l.start_s for l in lines],g)
            self.assertEqual((idx,list(flags)),(ev['line_index'],ev['live_words']))

    @unittest.skipUnless(shutil.which('ffmpeg') and shutil.which('ffprobe'),'ffmpeg required')
    def test_video_is_native_life_projection_with_valid_duration(self):
        lines=compile_plan(read_alignment(FIXTURE))
        with tempfile.TemporaryDirectory() as tmp:
            target=Path(tmp)/'sample.mp4'
            result=render(lines,target,fps=24,size=(640,360),
                          clip_start=11.,clip_end=12.5)
            self.assertTrue(target.exists() and target.stat().st_size>1000)
            self.assertFalse(result['audio_included'])
            self.assertGreater(result['true_scene_events'],1)
            probe=subprocess.check_output(['ffprobe','-v','error','-show_entries',
                              'format=duration','-of','default=noprint_wrappers=1:nokey=1',str(target)],
                              text=True).strip()
            self.assertLess(abs(float(probe)-1.5),.05)

if __name__=='__main__':unittest.main()
