"""Turn the qualified entire-song Life universe into an optical karaoke film.

The only sung lettering in the video is sampled from the TRUE 2x2 live-cell
blocks of preloaded, isolated B3/S23 glider machines. We use a proved
sparse-state solver instead of stepping 345,855 cells 45,865 times. At the
reaction windows we evaluate actual B3/S23 cells, not just source captions.

One stage/camera at a time. All other sung lines still physically coexist
in the initial Conway world, but are outside the video camera.

Requires Pillow and ffmpeg. Original audio is OPTIONAL and never altered:
  python preview/render_full_song_karaoke.py --audio made_of_maybe.wav

Without --audio, produces a silent 24fps MP4 ready for user-supplied audio.
Run --fixture for the first two sung lines without the full alignment JSON.
"""
from __future__ import annotations
import argparse
from bisect import bisect_right
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
import json
import math
import shutil
import subprocess
import sys
import tempfile

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from PIL import Image, ImageDraw, ImageFont, ImageFilter

from life.full_song_karaoke import (
    ALIGNMENT_FILE, GPS, compile_plan, physical_targets, stats,
)
from life.life_cell_sampler import block_alive_at
from life.lyric_cues import read_alignment

SONG_DURATION = 238.88
DEFAULT_SIZE=(1280,720)
BG=(7,13,25); FG=(235,247,245); LIGHT=(133,234,209)
FADED=(68,125,136); MUTED=(122,154,173); WARM=(239,204,153)


def font(size:int,bold:bool=False):
    names=(['DejaVuSans-Bold.ttf','/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf']
           if bold else ['DejaVuSans.ttf','/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'])
    for name in names:
        try:return ImageFont.truetype(name,size)
        except OSError:pass
    return ImageFont.load_default()


def word_targets(line):
    """Project *physical target coordinates*, not rendered glyph strings."""
    return [tuple(((x//line.pitch),((y-line.y_origin)//line.pitch))
                  for x,y in physical_targets(line,w)) for w in line.words]


def sampled_signature(lines, starts, gen):
    """Exact occupancy signature for all target block pixels at given tick."""
    t=gen/GPS
    li=bisect_right(starts,t)-1
    if li<0:return None,()
    line=lines[li]
    if gen>=line.clear_g:return None,()
    return li,tuple(block_alive_at(w.make_g,line.clear_g,gen) for w in line.words)


def cell_frame_background(size):
    w,h=size
    im=Image.new('RGB',size,BG)
    draw=ImageDraw.Draw(im)
    # Cinematic background and rail system: these are screen graphics, NOT Life
    # cells or lyric characters. Every singer-word pixel is drawn separately.
    for y in range(h):
        dy=abs((y-h*0.45)/(h*0.55))
        r=int(11+9*(1-dy)**2)
        g=int(20+14*(1-dy)**2)
        b=int(35+23*(1-dy)**2)
        draw.line((0,y,w,y),fill=(r,g,b))
    draw.line((58,int(h*.18),w-58,int(h*.18)),fill=(49,76,92),width=1)
    draw.line((58,int(h*.79),w-58,int(h*.79)),fill=(49,76,92),width=1)
    # Side trims are unrelated to Life glyphs, merely composition framing.
    return im


def draw_sung_frame(line,signature,gen,*,size,base,targets_cache,total_lines=66,show_debug=False):
    w,h=size
    im=base.copy()
    d=ImageDraw.Draw(im)
    s=min(w/1280,h/720)
    left=lambda p:int(p*s)
    f_title=font(max(16,left(26)),True)
    f_meta=font(max(12,left(16)))
    f_section=font(max(12,left(14)),True)
    f_small=font(max(11,left(14)))
    d.text((left(59),left(49)),'MADE OF MAYBE',font=f_title,fill=FG)
    d.text((w-left(59),left(61)),'CONWAY // B3/S23',font=f_section,
           fill=LIGHT,anchor='ra')
    if line is not None:
        section=line.section.upper().replace('—',' / ')
        if len(section)>60:section=section[:57]+'...'
        d.text((left(60),left(102)),section,font=f_meta,fill=MUTED)
        cells=[]
        glyph_cols=line.glyph_columns
        # Optical mapping rescales the *actual 2x2 block sites* out of the
        # enormous independently routed Life stage. No bitmap letters drawn
        # by PIL fonts in the lyric area.
        # Keep Life cells readable on small screens by moving a true linear
        # camera across each spatially large lyric stage, rather than shrinking
        # a long sentence to illegible pinpoints. All coordinates of a word
        # retain their exact affine distances in this optical projection.
        pitch=max(8,min(13,round(w/105)))
        tw=glyph_cols*pitch
        visible_cols=(w-left(132))/pitch
        active_index=max((i for i,on in enumerate(signature) if on),default=0)
        active_word=line.words[active_index]
        desired_center=(active_word.char_start+(len(active_word.text)-1)*.5)*6+2.5
        # Leave the first words steady until the score naturally approaches
        # the right edge; then pan the camera to keep the singer's words in view.
        if glyph_cols>visible_cols:
            center=max(visible_cols/2,min(desired_center,glyph_cols-visible_cols/2))
            tx=int(w/2-center*pitch)
        else:
            tx=(w-tw)//2
        ty=int(h*.47)-3.5*pitch
        for word_i,alive in enumerate(signature):
            if not alive:continue
            c=LIGHT if word_i==sum(bool(x) for x in signature)-1 else FADED
            for x,y in targets_cache[line.line_index][word_i]:
                xx=tx+x*pitch; yy=ty+y*pitch
                if -pitch <= xx <= w and -pitch <= yy <= h:
                    cells.append((xx,yy,c))
        # Optical halos glow from *live* block sites only; completely cosmetic.
        if cells:
            veil=Image.new('RGBA',size,(0,0,0,0))
            vd=ImageDraw.Draw(veil)
            for x,y,c in cells:
                vd.rectangle((x-1,y-1,x+pitch,y+pitch),fill=(c[0],c[1],c[2],85))
            glow=veil.filter(ImageFilter.GaussianBlur(max(3,pitch//2)))
            im=Image.alpha_composite(im.convert('RGBA'),glow).convert('RGB')
            d=ImageDraw.Draw(im)
            for x,y,c in cells:
                d.rounded_rectangle((x,y,x+max(2,pitch-2),y+max(2,pitch-2)),
                                    radius=max(0,pitch//5),fill=c)
        # Tiny printed statistics are *presentation information*, not lyrics.
        label=f'{len(cells):,} PHYSICAL 2×2 BLOCKS ALIVE'
        d.text((w//2,int(h*.71)),label,font=f_small,fill=MUTED,anchor='mm')
        d.text((left(60),int(h*.825)),f'LYRIC STAGE {line.line_index+1:02d}  /  {total_lines:02d}',
               font=f_section,fill=LIGHT)
    else:
        d.text((w//2,int(h*.49)),'· · ·',font=font(max(20,left(55))),fill=FADED,anchor='mm')
        d.text((left(60),int(h*.825)),'AWAITING NEXT LYRIC',font=f_section,fill=MUTED)
    time_s=gen/GPS
    minute=int(time_s//60);sec=time_s-60*minute
    d.text((w-left(60),int(h*.825)),f'{minute:02}:{sec:05.2f}  /  03:58.88',
           font=f_meta,fill=FG,anchor='ra')
    # Tempo of the original recording stays fixed. No audio is transformed.
    bar0=left(60);bar1=w-left(60)
    progress=min(1.,max(0.,time_s/SONG_DURATION))
    d.line((bar0,int(h*.883),bar1,int(h*.883)),fill=(55,82,97),width=4)
    d.line((bar0,int(h*.883),int(bar0+(bar1-bar0)*progress),int(h*.883)),
           fill=LIGHT,width=4)
    d.text((left(60),int(h*.920)),'ONE UNINTERRUPTED LIFE WORLD  ·  192 GENERATIONS / AUDIO SECOND',
           font=f_small,fill=MUTED)
    if show_debug:
        d.text((w-left(60),int(h*.920)),f'g{gen:,}',font=f_small,fill=WARM,anchor='ra')
    return im


def build_frame_intervals(lines,clip_start,clip_end,fps):
    """Collapse unchanged *real-cell occupancy* into repeated-video intervals.

    The video remains constant-FPS, and event timestamps are sampled on each
    video's audio-frame boundary. We never interpolate Life glyph cells.
    """
    start=round(clip_start*fps)
    finish=round(clip_end*fps)
    starts=tuple(l.start_s for l in lines)
    intervals=[];old=None
    for frame in range(start,finish):
        gen=int(round(frame*GPS/fps))
        signature=sampled_signature(lines,starts,gen)
        # Also update purely presentational clock/progress rail each second.
        event_key=(signature,frame//fps)
        if event_key!=old:
            intervals.append({'first_frame':frame,'last_frame_exclusive':frame+1,
                              'generation':gen,'line_index':signature[0],
                              'live_words':list(signature[1])})
            old=event_key
        else:
            intervals[-1]['last_frame_exclusive']=frame+1
    return intervals


def ffmpeg_concat(image_paths,frame_intervals,output,fps,clip_start,clip_end,*,audio=None):
    if shutil.which('ffmpeg') is None:
        raise RuntimeError('ffmpeg required to encode MP4')
    plist=output.parent/'_frame_schedule.ffconcat'
    with plist.open('w',encoding='utf-8') as file:
        file.write('ffconcat version 1.0\n')
        for i,(path,event) in enumerate(zip(image_paths,frame_intervals)):
            duration=(event['last_frame_exclusive']-event['first_frame'])/fps
            file.write("file '"+path.absolute().as_posix().replace("'","'\\''")+"'\n")
            file.write(f'duration {duration:.9f}\n')
        # ffmpeg concat needs the final image repeated to honor last duration.
        file.write("file '"+image_paths[-1].absolute().as_posix()+"'\n")
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y',
         '-safe','0','-f','concat','-i',str(plist)]
    if audio is not None:
        cmd+=['-ss',str(clip_start),'-i',str(audio),'-map','0:v:0','-map','1:a:0']
    cmd+=['-fps_mode','cfr','-r',str(fps),'-c:v','libx264','-preset','fast',
          '-crf','22','-pix_fmt','yuv420p','-movflags','+faststart']
    if audio is not None:
        cmd+=['-c:a','aac','-b:a','192k','-shortest']
    else:
        cmd+=['-an']
    cmd+=['-t',f'{clip_end-clip_start:.6f}',str(output)]
    run=subprocess.run(cmd,text=True,capture_output=True)
    if run.returncode:
        raise RuntimeError('ffmpeg failed: '+run.stderr[-3000:])
    plist.unlink(missing_ok=True)


def render(lines,output,*,fps=24,size=DEFAULT_SIZE,clip_start=0.,clip_end=SONG_DURATION,
           audio=None,thumbnail=None,metadata=None):
    if fps<=0 or 192%fps:
        raise ValueError('FPS must be a positive divisor of 192 Life generations/s')
    if size[0]<480 or size[1]<280 or size[0]%2 or size[1]%2:
        raise ValueError('video dimensions must be even and at least 480×280')
    if not (0 <= clip_start < clip_end <= SONG_DURATION):
        raise ValueError('invalid clip interval')
    if audio is not None and not Path(audio).is_file():
        raise FileNotFoundError('audio WAV/MP3 not found')
    output=Path(output);output.parent.mkdir(parents=True,exist_ok=True)
    intervals=build_frame_intervals(lines,clip_start,clip_end,fps)
    base=cell_frame_background(size)
    targets_cache={l.line_index:[tuple(((x//l.pitch),(y-l.y_origin)//l.pitch)
        for x,y in physical_targets(l,w)) for w in l.words] for l in lines}
    with tempfile.TemporaryDirectory(prefix='conway_lyric_frames_') as tmp:
        pngs=[]
        for i,row in enumerate(intervals):
            line=lines[row['line_index']] if row['line_index'] is not None else None
            im=draw_sung_frame(line,row['live_words'],row['generation'],
                   size=size,base=base,targets_cache=targets_cache,total_lines=len(lines))
            path=Path(tmp)/f'frame_{i:04d}.png'
            im.save(path,optimize=False)
            pngs.append(path)
            if thumbnail and (i==min(len(intervals)-1,max(1,len(intervals)//5))):
                Path(thumbnail).parent.mkdir(parents=True,exist_ok=True)
                im.save(thumbnail)
        ffmpeg_concat(pngs,intervals,output,fps,clip_start,clip_end,audio=audio)
    payload={
        'video':output.name,'fps':fps,'resolution':size,
        'duration_s':round(clip_end-clip_start,3),
        'song_duration_s':SONG_DURATION,
        'initial_universe':'preloaded Life gliders; no runtime cell changes',
        'pixel_source':'true B3/S23 2x2-block occupancy; exact native collision windows; certified phase flight',
        'true_scene_events':len(intervals),
        'source_alignment':'Suno alignment normalized into independent Life word circuits',
        'line_count':len(lines),
        'word_count':sum(len(l.words) for l in lines),
        'audio_included':audio is not None,
        'audio_rate_modified':False,
        'video_camera':'lyric-stage crop/projection; original full-world coordinates are not modified',
        'caveat':'optically projected target blocks only; background control gliders are outside the camera crop',
        'first_events':intervals[:5],
        'last_events':intervals[-3:],
    }
    if metadata:
        Path(metadata).parent.mkdir(parents=True,exist_ok=True)
        Path(metadata).write_text(json.dumps(payload,indent=2)+'\n',encoding='utf-8')
    return payload


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--alignment',type=Path,default=ALIGNMENT_FILE)
    parser.add_argument('--fixture',action='store_true',help='Use bundled two-line test alignment')
    parser.add_argument('--out',type=Path,default=Path('output/made_of_maybe_conway_karaoke_silent.mp4'))
    parser.add_argument('--preview',action='store_true',help='Render 10.5–19s first-verse teaser')
    parser.add_argument('--fps',type=int,default=24)
    parser.add_argument('--width',type=int,default=1280)
    parser.add_argument('--height',type=int,default=720)
    parser.add_argument('--audio',type=Path)
    parser.add_argument('--thumbnail',type=Path)
    parser.add_argument('--metadata',type=Path)
    args=parser.parse_args()
    if args.fixture:
        args.alignment=Path(__file__).resolve().parents[1]/'data'/'first_verse_alignment_fixture.json'
    lines=compile_plan(read_alignment(args.alignment))
    t0,t1=(10.5,19.0) if args.preview else (0.,SONG_DURATION)
    result=render(lines,args.out,fps=args.fps,size=(args.width,args.height),
           clip_start=t0,clip_end=t1,audio=args.audio,
           thumbnail=args.thumbnail,metadata=args.metadata)
    print(json.dumps({'lines':len(lines),'words':sum(len(l.words) for l in lines),
          **result},indent=2))

if __name__=='__main__':main()
