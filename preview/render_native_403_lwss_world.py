"""REAL-CELL full-song Made of Maybe bubbleless LWSS film.

One physically preloaded 101863-cell g0 B3/S23 universe:
- original native singer plus WE, MADE via original 90-degree converters;
- subsequent 401 original-Suno words as genuine WEST-bound LWSS glyph pixels;
- 28 persistent physical fishhooks; original W/V mouth only in 20s pilot.

This is a genuine native CELL rendering, NOT the older block-Life optical
karaoke. It is still NOT the final assignment: the remaining 401 words
have NOT yet been supplied through their original south-to-west converters,
and Suno W/V mouth behavior has not been physically wired over the full song.

At 24fps, g=8*f. All Suno sources are 4-phase, and each source's native
fishhook reaction occurs at local g37..39, restoring precisely at g40.
Therefore no sample-frame is inside a receiver reaction: genuine Life cells
are exactly the live LWSS phase or the already-restored fishhook. The
singer is independently C++ evolved through g4096 and frozen ONLY once
native one-step stability is checked. No runtime changes to Life world.
"""
from __future__ import annotations
import argparse,bisect,json,struct,subprocess
from pathlib import Path
from PIL import Image,ImageDraw
from life.core import evolve
from life.full_song_lwss_readhead import (
    X_ANCHOR,Y_ANCHOR,ROW_PITCH,PITCH,eaters,row_events,
    singer_parts,verify_train_geometry,source_seeds)
from life.phrase_crawler_eater import LWSS

W,H=1280,720
FPS,GPS=24,192
FRAMES=5733
BACKGROUND=(5,10,24)

def snapshots(path):
    with Path(path).open('rb') as f:
        while h:=f.read(8):
            g,n=struct.unpack('<iI',h)
            payload=f.read(8*n)
            if len(payload)!=8*n:raise ValueError('incomplete native source frame')
            yield g,set(struct.iter_unpack('<ii',payload))

def camera(g):
    t=g/GPS
    u=min(1.,max(0.,t/25.))
    u=u*u*(3-2*u)
    return ((1680-130*u,-980+5*u),.66+.04*u)

def coords(x,y,center,zoom):
    return (round((x-center[0])*zoom+W/2),
            round((y-center[1])*zoom+H/2))

def visible(x,y,center,zoom):
    return (abs(x-center[0]) < W/(2*zoom)+3
            and abs(y-center[1]) < H/(2*zoom)+3)

def draw_singer(draw,points,center,zoom):
    for x,y in points:
        if not visible(x,y,center,zoom):continue
        lx=x-1071;ly=y+1019
        if 335<=lx<=475 and 105<=ly<=240:c=(243,191,118)
        elif -390<=lx<=350 and -455<=ly<=355:
            if abs(lx)>195 or ly<-205:c=(183,143,226)
            elif -20<ly<125 and abs(lx)<130:c=(248,146,189)
            else:c=(221,227,238)
        else:c=(144,201,216)
        draw.point(coords(x,y,center,zoom),fill=c)

def draw_cells(draw,points,center,zoom,tint):
    for x,y in points:
        if visible(x,y,center,zoom):
            draw.point(coords(x,y,center,zoom),fill=tint)

def arrivals():
    out=[]
    for y,records in row_events().items():
        for t,word,col,row in records:
            out.append((t,y,word,col,row))
    out.sort()
    return out

def draw_active_ships(draw,g,events,times,center,zoom):
    # All events are native LWSS phase-0 at g divisible by eight. The
    # 37..39-generation eater collision never occupies a movie sample.
    left=bisect.bisect_left(times,g-36)
    right=bisect.bisect_right(times,g+round(2*(center[0]+W/(2*zoom)-X_ANCHOR))+15)
    for t,y,word,col,row in events[left:right]:
        if g>t+36:continue
        x=X_ANCHOR+(t-g)//2
        if not visible(x,y,center,zoom):continue
        draw_cells(draw,((x+dx,y+dy) for dx,dy in LWSS),
                   center,zoom,(150,240,206))

def verify_singer_clearance(frames):
    # Full speaker portrait moves until g4096. A 20-cell one-world
    # spacetime guard around all 28 lyric rows remains EMPTY at each
    # eight-generation checkpoint. Light cones from any possible
    # intermediate interaction cannot traverse this guard within 8g.
    _,lanes=__import__('life.full_song_lwss_readhead',
        fromlist=['layout']).layout()
    miny=Y_ANCHOR-20
    maxy=Y_ANCHOR+ROW_PITCH*(lanes-1)+PITCH*3+20
    singer_at_4096=None
    for g,world in frames:
        if any(x>=X_ANCHOR-38 and miny<=y<=maxy for x,y in world):
            raise AssertionError(('singer crosses REAL lyric corridor',g))
        if g==4096:
            if evolve(world)!=world:
                raise AssertionError('singer not stationary at g4096')
            singer_at_4096=frozenset(world)
            break
    if singer_at_4096 is None:
        raise AssertionError('singer native C++ frames must reach g4096')
    return singer_at_4096

def render(singer_path,out):
    qual=verify_train_geometry()
    events=arrivals()
    times=[x[0] for x in events]
    if len(events)!=10317:
        raise AssertionError('complete original Suno real LWSS train changed')
    original=tuple(snapshots(singer_path))
    if len(original)!=513 or tuple(g for g,_ in original)!=(tuple(range(0,4097,8))):
        raise AssertionError('not a continuous native 513-frame singer')
    assert sum(len(p) for p in singer_parts())==8814
    if original[0][1]!=set().union(*singer_parts()):
        raise AssertionError('movie is using the wrong original singer')
    resting=verify_singer_clearance(original)
    # stable camera/face from 25s after the initial gently moving camera.
    center,zoom=camera(25*GPS)
    static=Image.new('RGB',(W,H),BACKGROUND)
    d=ImageDraw.Draw(static)
    draw_singer(d,resting,center,zoom)
    fishhooks=eaters()
    draw_cells(d,fishhooks,center,zoom,(132,148,181))
    out=Path(out);out.parent.mkdir(parents=True,exist_ok=True)
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y',
        '-f','rawvideo','-pixel_format','rgb24','-video_size',f'{W}x{H}',
        '-framerate',str(FPS),'-i','pipe:0','-c:v','libx264',
        '-preset','ultrafast','-crf','21','-pix_fmt','yuv420p',
        '-movflags','+faststart',str(out)]
    proc=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
    try:
        for frame in range(FRAMES):
            g=frame*GPS//FPS
            center,zoom=camera(g)
            if g<=4096 or g<=25*GPS:
                im=Image.new('RGB',(W,H),BACKGROUND);draw=ImageDraw.Draw(im)
                singer=original[g//8][1] if g<=4096 else resting
                draw_singer(draw,singer,center,zoom)
                draw_cells(draw,fishhooks,center,zoom,(132,148,181))
            else:
                im=static.copy();draw=ImageDraw.Draw(im)
            draw_active_ships(draw,g,events,times,center,zoom)
            proc.stdin.write(im.tobytes())
        proc.stdin.close()
        err=proc.stderr.read().decode(errors='replace')
        if proc.wait():raise RuntimeError('ffmpeg: '+err[-2000:])
    except Exception:
        proc.kill();raise
    result={
      'status':'native full-song WEST-LWSS workprint, not finished full original-converter video',
      'source_song':'Made of Maybe','source_song_id':
         '53610991-7381-4749-96e1-79b8e3b1c28b',
      'duration_s':FRAMES/FPS,'frames':FRAMES,'fps':FPS,'resolution':[W,H],
      'native_singer_source_frames':513,'singer_resting_g4096':True,
      'native_generation_zero_cells':qual['true_source_g0_population'],
      'original_suno_words':403,'native_3x4_WE_MADE_actual_90deg_converters':True,
      'full_401_later_native_WEST_moving_words':True,
      'later_401_south_to_WEST_converters_missing':True,
      'original_WV_physical_mouth_full_song_missing':True,
      'video_has_original_audio':False,
      'word_source_uses_real_B3S23_LWSS_cells':True,
      'receiver_reset_g40_not_optical_dissolve':True,
      'native_physical_bubble_present':False,
      'per_frame_cell_injection':False,'screen_typography_overlay':False,
      'camera_cuts':0,'symbolics':False,'nuke':False}
    out.with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--singer',required=True,type=Path)
    p.add_argument('--out',required=True,type=Path)
    a=p.parse_args()
    print(json.dumps(render(a.singer,a.out),indent=2))
