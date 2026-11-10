"""Opening must have continuous camera and no screen-space captions."""
import inspect,unittest
from preview.render_one_world_native_no_cuts import camera,draw
class NativeUncutFilmTests(unittest.TestCase):
    def test_camera_continuous_through_all_stages(self):
        for t in (.75,2.,11.):
            before=camera(t-1e-6)
            after=camera(t+1e-6)
            self.assertLess(max(abs(a-b) for a,b in zip(before,after)),.001)
    def test_camera_stops_zooming_without_a_new_shot(self):
        self.assertEqual(camera(11),camera(19))
        with self.assertRaises(ValueError):camera(-.1)
    def test_renderer_contains_no_subtitles_or_pose_editor(self):
        src=inspect.getsource(draw)
        for forbidden in ('ImageFont','word_index','mouth_state','lyric',
                          'subtitle','glider_at','draw.text','draw.line'):
            self.assertNotIn(forbidden,src)
    def test_time_is_strictly_native_life_audio_mapping(self):
        self.assertEqual(192//24,8)

if __name__=='__main__':unittest.main()
