"""A single fixed camera observing B3/S23 LWSS cells for the full song.

No optical words, caption switching, edit cuts, mouth, singer, or runtime
cell changes. All ships are present at generation zero. To avoid running a
93k-cell universe for 450k generations, evaluate the exact 4-phase period
of the LWSS's B3/S23 native orbit. Because the compiler establishes all
10,366 ship neighborhoods are disjoint at each phase, the union of their
freely translated orbits is the exact full-world Game of Life evolution.
"""
from __future__ import annotations
import argparse, subprocess, sys, time
from pathlib import Path
import numpy as np
from compile_karaoke import compile_score,GPS,FPS,SONG_DURATION

W,H=960,540
SCALE=5
CENTER_X=40
CAMERA_Y=14
BG=(7,13,27)


def render(output, audio, *, silent=False):
    words,ships,phases=compile_score()
    points=np.asarray(ships,dtype=np.int32)
    xinit=points[:,0]
    phases=[np.asarray(phase,dtype=np.int32) for phase in phases]
    out=Path(output);out.parent.mkdir(parents=True,exist_ok=True)
    silentpath=out.with_name('LWSS_one_line_silent.mp4')
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo',
         '-pixel_format','rgb24','-video_size',f'{W}x{H}',
         '-framerate',str(FPS),'-i','pipe:0','-c:v','libx264',
         '-preset','ultrafast','-crf','25','-pix_fmt','yuv420p',
         '-movflags','+faststart',str(silentpath)]
    pipe=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
    ambient=np.full((H,W,3),BG,dtype=np.uint8)
    # A subtle *background gradient*, never a substitute for a cell.
    ys=np.arange(H,dtype=np.int32)
    v=-(abs(ys-(H//2))//70)
    ambient[:,:,1]=np.clip(BG[1]+7+v,0,255).astype(np.uint8)[:,None]
    ambient[:,:,2]=np.clip(BG[2]+12+2*v,0,255).astype(np.uint8)[:,None]
    nframes=round(SONG_DURATION*FPS)
    assert nframes==11466
    step=GPS//FPS
    assert step%4==0
    started=time.monotonic()
    try:
        for frame in range(nframes):
            # Native B3/S23 phase, not a timed word/title/caption decision.
            g=frame*step
            k,r=divmod(g,4)
            # At 4 native ticks all LWSSs translate west by exactly 2 cells.
            dx=-2*k
            minx=CENTER_X-W//(2*SCALE)-8-dx
            maxx=CENTER_X+W//(2*SCALE)+8-dx
            i=np.searchsorted(xinit,minx,side='left')
            j=np.searchsorted(xinit,maxx,side='right')
            canvas=ambient.copy()
            if j>i:
                sprite=points[i:j,None,:]+phases[r][None,:,:]
                xs=((sprite[:,:,0]+dx-CENTER_X)*SCALE+W//2).reshape(-1)
                ys=((sprite[:,:,1]-CAMERA_Y)*SCALE+H//2).reshape(-1)
                okay=(xs>=4)&(xs<W-8)&(ys>=4)&(ys<H-8)
                xs=xs[okay];ys=ys[okay]
                if len(xs):
                    # Glow and live points are purely color transforms of
                    # actual 9-cell LWSS native B3/S23 positions.
                    for oy in range(-3,7):
                        for ox in range(-3,7):
                            canvas[ys+oy,xs+ox]=(26,61,65)
                    for oy in range(0,5):
                        for ox in range(0,5):
                            canvas[ys+oy,xs+ox]=(108,232,203)
                    canvas[ys+1,xs+1]=(224,255,245)
            pipe.stdin.write(canvas.tobytes())
            if frame and frame%2400==0:
                print(f'Native one-line film {frame}/{nframes} frames, {time.monotonic()-started:.1f}s',flush=True)
        pipe.stdin.close()
        err=pipe.stderr.read().decode(errors='replace')
        if pipe.wait():raise RuntimeError('ffmpeg encode: '+err[-2000:])
    except Exception:
        pipe.kill();raise
    if not silent:
        if audio is None:
            raise ValueError('Provide --original-audio path or use --silent')
        subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y',
                        '-i',str(silentpath),'-i',str(audio),'-map','0:v:0',
                        '-map','1:a:0','-c:v','copy','-c:a','aac',
                        '-b:a','128k','-t',str(SONG_DURATION),
                        '-movflags','+faststart',str(out)],check=True)
        silentpath.unlink()
    else:
        silentpath.replace(out)
    print('FILM COMPLETE',out,'bytes',out.stat().st_size,'seconds',time.monotonic()-started)
    return out

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--out',default='output/MadeOfMaybe_ONE_LINE_403_LWSS_FULL_SONG.mp4')
    p.add_argument('--original-audio',default=None, help='Local original Suno song recording (MP3, M4A or MP4)')
    p.add_argument('--silent',action='store_true')
    a=p.parse_args()
    render(a.out,a.original_audio,silent=a.silent)
