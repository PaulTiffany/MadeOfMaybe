"""Render first-line singer whose WE glyph and lip share ONE actual glider.

The word/lip signal comes from life.physical_lip_splitter_bridge, not the
previous, independently timed character world. All other lyric pixels still
use the earlier native-Life qualified optical sampler. The image shows Life
states, with color, zoom and framing only. This is a first-line pilot, *not*
proof of full-song or 40-tile causal fanout.
"""
from __future__ import annotations
import argparse,json,subprocess,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from PIL import Image,ImageDraw
from life.core import evolve,place
from life.first_line_karaoke import GPS
from life.first_line_singing_character import safe_art
from life.physical_lip_splitter_bridge import (
    bridge_unit_seed,word_and_lip_at,SINGER_TRANSLATION,CAUSAL_WORD_G,
    CAUSAL_LIP_G,FULL_CHECK_G)
from preview.render_first_line_singer import make_image,W,H,BG,font


def causal_frame(g,live,art):
    word,lip=word_and_lip_at(live)
    # Camera uses dynamic cells from the exact causally coupled world, not
    # original separately authored singer gliders. Translate to portrait local.
    singer_local=place(live,-SINGER_TRANSLATION[0],-SINGER_TRANSLATION[1])
    im=make_image(g,singer_local,art,first_glyph_pixel_alive=word)
    d=ImageDraw.Draw(im)
    # Optical annotation only: these labels DO NOT modify Life geometry.
    d.text((606,595),f'SHARED GLIDER: WE PIXEL {"ON" if word else "OFF"}  /  LIP TILE {"ON" if lip else "OFF"}',
           font=font(16,True),fill=(245,196,170))
    return im


def render(out:Path,*,start_s=10.93,end_s=15.43,fps=24,audio=None):
    if GPS%fps:raise ValueError('fps must divide native Life generation rate')
    start_frame=round(start_s*fps);end_frame=round(end_s*fps)
    first_g=start_frame*(GPS//fps)
    last_g=(end_frame-1)*(GPS//fps)
    if last_g>FULL_CHECK_G:raise ValueError('requested preview exceeds qualified B3/S23 horizon')
    world=bridge_unit_seed(source_enabled=True)
    for _ in range(first_g):world=evolve(world)
    art=safe_art()
    out.parent.mkdir(parents=True,exist_ok=True)
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo',
         '-pixel_format','rgb24','-video_size',f'{W}x{H}',
         '-framerate',str(fps),'-i','pipe:0']
    if audio:cmd+=['-ss',str(start_s),'-i',str(audio),'-map','0:v','-map','1:a',
                  '-c:a','aac','-b:a','192k','-shortest']
    cmd+=['-c:v','libx264','-preset','veryfast','-crf','22','-pix_fmt','yuv420p',
          '-movflags','+faststart',str(out)]
    p=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
    checkpoints={};samples={first_g,CAUSAL_WORD_G,CAUSAL_LIP_G,last_g}
    try:
        for i in range(start_frame,end_frame):
            g=i*(GPS//fps)
            if g in samples:checkpoints[g]=word_and_lip_at(world)
            frame=causal_frame(g,world,art)
            p.stdin.write(frame.tobytes())
            if i==start_frame+32:frame.save(out.parent/'causal_firstline_character_frame.png')
            if i<end_frame-1:
                for _ in range(GPS//fps):world=evolve(world)
        p.stdin.close();err=p.stderr.read().decode(errors='replace')
        if p.wait():raise RuntimeError('ffmpeg rendering failed: '+err[-2000:])
    except Exception:
        p.kill();raise
    result={
      'start_s':start_s,'end_s':end_s,'fps':fps,'frames':end_frame-start_frame,
      'audio_included':bool(audio),'original_song_unchanged':True,'GPS':GPS,
      'life_source':'life.physical_lip_splitter_bridge.bridge_unit_seed',
      'source_gliders_at_initialization':1,'physically_coupled_lyric_pixels':1,
      'physically_coupled_lip_tiles':1,'full_lip_fanout':False,
      'source_word_generation':CAUSAL_WORD_G,'source_lip_generation':CAUSAL_LIP_G,
      'remaining_360_glyph_pixels':'verified native-Life optical sampler',
      'checkpoint_native_observations':{str(k):list(v) for k,v in checkpoints.items()},
      'basis':'B3/S23 native evolution for singer + shared glyph pixel; other glyphs finite-horizon certified independent',
    }
    (out.parent/'causal_firstline_singer_metadata.json').write_text(json.dumps(result,indent=2)+'\n')
    return result


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--out',type=Path,default=Path('preview/causal_firstline_singer.mp4'))
    p.add_argument('--audio',type=Path)
    p.add_argument('--start',type=float,default=10.93)
    p.add_argument('--end',type=float,default=15.43)
    args=p.parse_args()
    print(json.dumps(render(args.out,start_s=args.start,end_s=args.end,audio=args.audio),indent=2))

if __name__=='__main__':main()
