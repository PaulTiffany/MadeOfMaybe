"""BUBBLE-FREE whole-song SCREENING WORKPRINT, not a native 403-corner proof.

Compose:
  0–20.0417s: genuine one-world B3/S23 singer + WE + MADE, real converters.
  thereafter: existing full-song 2x2 block-Life *optical* karaoke viewport.

The latter is NOT equivalent to the desired full-song 90-degree-converter
production. This is a deliberately labeled editorial screening cut to
inspect the complete Suno timing BEFORE constructing the physical bubble.

With the already exported workflow artifacts:
  python preview/assemble_bubbleless_screening.py \
    --pilot path/to/two_words_native_singer.mp4 \
    --lyrics path/to/made_of_maybe_conway_karaoke_silent.mp4 \
    --out output/bubbleless_screening_silent.mp4
Optionally pass --audio path/to/original_suno.mp3 for original music.
"""
from __future__ import annotations
import argparse
import json
import shutil
import subprocess
from pathlib import Path

FPS=24
OPENING_FRAMES=481
SONG_END_FRAMES=5733
SONG_DURATION=238.88

def command(pilot:Path,lyrics:Path,out:Path,audio=None):
    if not shutil.which('ffmpeg'):raise RuntimeError('ffmpeg required')
    paths=[pilot,lyrics]+([audio] if audio else [])
    if any(not Path(p).is_file() for p in paths):
        raise FileNotFoundError('supply both verified workflow clips, optionally the original Suno audio')
    border=OPENING_FRAMES/FPS
    last=SONG_END_FRAMES/FPS
    chain=(f'[0:v]trim=start_frame=0:end_frame={OPENING_FRAMES},'
           'setpts=PTS-STARTPTS[a];'
           f'[1:v]trim=start={border:.9f}:end={last:.9f},'
           'setpts=PTS-STARTPTS[b];'
           '[a][b]concat=n=2:v=1:a=0[v]')
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y',
         '-i',str(pilot),'-i',str(lyrics)]
    if audio:
        cmd+=['-i',str(audio)]
    cmd+=['-filter_complex',chain,'-map','[v]']
    if audio:
        cmd+=['-map','2:a:0','-c:a','aac','-b:a','192k','-shortest']
    else:
        cmd+=['-an']
    cmd+=['-r',str(FPS),'-frames:v',str(SONG_END_FRAMES),
          '-c:v','libx264','-preset','veryfast','-crf','21',
          '-pix_fmt','yuv420p','-movflags','+faststart',str(out)]
    return cmd

def assemble(pilot,lyrics,out,audio=None):
    pilot=Path(pilot);lyrics=Path(lyrics);out=Path(out)
    out.parent.mkdir(parents=True,exist_ok=True)
    subprocess.run(command(pilot,lyrics,out,Path(audio) if audio else None),
                   check=True)
    manifest={
      'status':'SCREENING WORKPRINT ONLY',
      'nominal_song_seconds':SONG_DURATION,
      'rendered_duration_seconds':SONG_END_FRAMES/FPS,
      'fps':FPS,'frame_count':SONG_END_FRAMES,
      'physical_bubble_present':False,
      'native_b3s23_singer_and_actual_original_90deg_converters_first_frames':OPENING_FRAMES,
      'post_opening_mechanism':'older certified optical 2x2 block-Life karaoke, NOT native 90-degree LWSS converter',
      'all_403_words_displayed_after_intro':'older optical full song, NOT native 403-corner conversion',
      'physical_native_403_song_proven':False,
      'source_suno_audio_muxed':bool(audio),
      'symbolics_included':False,'final_nuke_included':False,
      'next_production_gate':'full-word converter mechanics + native singer through all 403 words, then physically add rim to empty space',
      'no_automatic_runtime_cell_edits_in_original_native_segment':True,
    }
    path=out.with_suffix('.json')
    path.write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf8')
    return manifest

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--pilot',type=Path,required=True)
    p.add_argument('--lyrics',type=Path,required=True)
    p.add_argument('--out',type=Path,required=True)
    p.add_argument('--audio',type=Path)
    a=p.parse_args()
    print(json.dumps(assemble(a.pilot,a.lyrics,a.out,a.audio),indent=2))
