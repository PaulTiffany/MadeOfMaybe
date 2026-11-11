"""Film boundary and provenance must never conflate optical and native."""
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
from preview.assemble_bubbleless_screening import FPS,OPENING_FRAMES,SONG_END_FRAMES,command

class ScreeningBoundaryTests(unittest.TestCase):
    def test_correct_frame_exact_boundary_and_optional_audio(self):
        with TemporaryDirectory() as d:
            a=Path(d)/'native.mp4';b=Path(d)/'optical.mp4'
            a.write_bytes(b'pilot');b.write_bytes(b'lyrics')
            with patch('shutil.which',return_value='/usr/bin/ffmpeg'):
                cmd=command(a,b,Path(d)/'out.mp4')
                joined=' '.join(cmd)
                self.assertIn(f'end_frame={OPENING_FRAMES}',joined)
                self.assertIn(f'end={SONG_END_FRAMES/FPS:.9f}',joined)
                self.assertIn('concat=n=2:v=1:a=0',joined)
                self.assertEqual(cmd[-1],str(Path(d)/'out.mp4'))
                self.assertIn('-an',cmd)

if __name__=='__main__':unittest.main()
