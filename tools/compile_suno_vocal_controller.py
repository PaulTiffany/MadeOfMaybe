"""Compile the ACTUAL isolated Suno vocal stem + 403 source-word events.

Produces an AUDITABLE request score. It must not be used to replace native
Life mouth pixels in the renderer. The native glider gate is a separate
one-shot primitive until an actual voice/word-to-lip circuit is qualified.

Example:
 python -m tools.compile_suno_vocal_controller --vocals vocals_take1.mp3 --output output/vocal_requests.json
"""
from __future__ import annotations
import argparse,hashlib,json,shutil,subprocess,tempfile
from pathlib import Path
from life.dual_channel_mouth_logic import vocal_activity_from_wav,compile_score

SONG_ID='53610991-7381-4749-96e1-79b8e3b1c28b'
VOCAL_STEM_IDS=(
    'bee52d16-b01b-4224-bd4c-5c51081d813b',
    '8375d878-79aa-4460-9b68-897281642ca2'
)

def prepare(vocals,output,*,stem_id=VOCAL_STEM_IDS[0],threshold=.14):
    vocals=Path(vocals);output=Path(output)
    if stem_id not in VOCAL_STEM_IDS:
        raise ValueError('unknown Suno vocal stem')
    if not vocals.is_file():raise FileNotFoundError(vocals)
    if not shutil.which('ffmpeg'):
        raise RuntimeError('ffmpeg executable is required for audio decoding')
    with tempfile.TemporaryDirectory(prefix='conway_isolated_vocals_') as temp:
        wav=Path(temp)/'voice.wav'
        subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y',
            '-i',str(vocals),'-map','0:a:0','-vn','-ac','1',
            '-ar','16000','-c:a','pcm_s16le',str(wav)],check=True)
        intervals=vocal_activity_from_wav(wav,relative_threshold=threshold)
    digest=hashlib.sha256(vocals.read_bytes()).hexdigest()
    provenance={'song_id':SONG_ID,'vocal_stem_id':stem_id,
                'file_sha256':digest,'source_kind':'isolated-Suno-vocals',
                'threshold':threshold}
    score=compile_score(intervals,
                        provenance=json.dumps(provenance,sort_keys=True))
    score['vocal_activity_intervals_seconds']=intervals
    score['song_id']=SONG_ID
    score['stem_id']=stem_id
    score['source_sha256']=digest
    score['requires_native_actuator_integration']=True
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(score,indent=2)+'\n',encoding='utf8')
    return score

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--vocals',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--stem-id',choices=VOCAL_STEM_IDS,default=VOCAL_STEM_IDS[0])
    p.add_argument('--threshold',type=float,default=.14)
    a=p.parse_args()
    report=prepare(a.vocals,a.output,stem_id=a.stem_id,threshold=a.threshold)
    print(json.dumps({'word_count':report['word_count'],
        'vocal_episodes':report['vocal_episodes'],
        'vocal_only_generations':report['vocal_only_generations'],
        'physical_gate_built':report['physical_gate_built'],
        'native_mouth_connected':report['native_B3S23_control_circuit_qualified'],
        'file':str(a.output)},indent=2))
if __name__=='__main__':main()
