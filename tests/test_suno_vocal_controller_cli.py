"""Offline fixture: verifies actual WAV decoding and provenance, never fake stem."""
import math,struct,tempfile,unittest,wave
from pathlib import Path
from tools.compile_suno_vocal_controller import prepare,VOCAL_STEM_IDS
class IsolatedStemCompilerTests(unittest.TestCase):
    def test_synthetic_vocal_tail_keeps_mouth_request_alive(self):
        with tempfile.TemporaryDirectory() as tmp:
            stem=Path(tmp)/'SYNTHETIC_VOCAL_TEST.wav'
            out=Path(tmp)/'score.json'
            with wave.open(str(stem),'wb') as writer:
                writer.setnchannels(1);writer.setsampwidth(2)
                writer.setframerate(16000)
                for k in range(16000*16):
                    second=k/16000
                    amplitude=8000 if 11.1<=second<=14.8 else 0
                    writer.writeframesraw(struct.pack('<h',
                        amplitude if k%4<2 else -amplitude))
            result=prepare(stem,out)
            self.assertEqual(result['word_count'],403)
            self.assertGreater(result['vocal_only_generations'],0)
            self.assertGreater(result['vocal_episodes'],0)
            self.assertEqual(result['stem_id'],VOCAL_STEM_IDS[0])
            self.assertFalse(result['native_B3S23_control_circuit_qualified'])
            self.assertTrue(out.exists())
    def test_unknown_stem_id_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError):
                prepare(Path(tmp)/'missing.wav',Path(tmp)/'output.json',
                        stem_id='fabricated-id')
if __name__=='__main__':unittest.main()
