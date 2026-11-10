"""Independent vocal source + real word timing + finite jaw dwell tests."""
import math,struct,tempfile,unittest,wave
from pathlib import Path
from life.dual_channel_mouth_logic import (
    DEFAULT_DWELL_G,time_to_g,vocal_activity_from_wav,compile_score
)
class DualChannelMouthTests(unittest.TestCase):
    def test_no_vocal_stem_does_not_fabricate_activity(self):
        s=compile_score([],end_s=239,provenance='NO VOCAL STEM')
        self.assertEqual((s['word_count'],s['vocal_episodes'],s['vocal_only_generations']),(403,0,0))
        self.assertFalse(s['physical_gate_built'])
    def test_long_held_vocal_after_word_creates_alternation(self):
        s=compile_score([(11.2,14.5)],end_s=15,provenance='SYNTHETIC TEST ONLY')
        es=s['transitions']
        self.assertEqual(time_to_g(11.224),2156)
        self.assertTrue(any(e['state']=='medium' and e['voice_active'] for e in es))
        self.assertTrue(any(e['state']=='open' and e['voice_active'] for e in es))
        self.assertTrue(any(e['state']=='closed' and not e['voice_active'] for e in es))
        self.assertGreater(s['vocal_only_generations'],0)
        self.assertTrue(all(b['generation']-a['generation']>=DEFAULT_DWELL_G
                            for a,b in zip(es,es[1:])))
        self.assertFalse(s['lip_actuation_qualified'])
    def test_vocal_intro_can_open_before_first_word(self):
        s=compile_score([(1.,2.1)],end_s=3,provenance='SYNTHETIC TEST ONLY')
        es=s['transitions']
        self.assertEqual((es[0]['generation'],es[0]['state']),(192,'open'))
        self.assertTrue(any(e['state']=='medium' for e in es))
        self.assertTrue(any(e['state']=='closed' for e in es))
    def test_wav_stem_gate_is_actual_audio_based(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'synthetic.wav';rate=16000
            with wave.open(str(p),'wb') as f:
                f.setnchannels(1);f.setsampwidth(2);f.setframerate(rate)
                for k in range(rate*3):
                    t=k/rate;amp=13000 if 1<=t<2 else 0
                    f.writeframesraw(struct.pack('<h',int(amp*math.sin(2*math.pi*220*t))))
            spans=vocal_activity_from_wav(p)
            self.assertEqual(len(spans),1)
            self.assertLess(abs(spans[0][0]-1.),.03)
            self.assertLess(abs(spans[0][1]-2.),.03)
    def test_bad_time_rejected(self):
        with self.assertRaises(ValueError):time_to_g(-.1)
        with self.assertRaises(ValueError):compile_score([(2,3),(1,2)],end_s=4)
        with self.assertRaises(ValueError):compile_score([(1,1)],end_s=4)
        with self.assertRaises(ValueError):compile_score([],end_s=4,dwell_g=100.5)
if __name__=='__main__':unittest.main()
