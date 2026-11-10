"""One continuous 24fps camera over a single exact, native B3/S23 world.

NO drawn text, mouth substitutions, subtitle sprites, boxes, borders,
hard camera cuts, extra symbolic content or renderer-driven state changes.
Only native cells from complete-world snapshots are shown. Coloring is a
fixed world-coordinate camera palette, not a physical RGB switch.
This is a 19s mechanically certified opening, NOT full-song karaoke.
"""
from __future__ import annotations
import argparse,math,struct,subprocess
from pathlib import Path
from PIL import Image,ImageDraw
GPS=192
FPS=24
WIDTH,HEIGHT=1280,720
SINGER_ORIGIN=(1071,-1019)
BACKGROUND=(5,10,24)

def ease(v):
    v=max(0.,min(1.,v))
    return v*v*(3-2*v)

def camera(t):
    """One continuous affine camera, same world at every time."""
    if t<0:raise ValueError('negative time')
    if t<=.75:return (420.2-48*t,121.2+48*t,15.)
    if t<=2:
        u=ease((t-.75)/1.25)
        return (384.2+(382-384.2)*u,
                157.2+(169.5-157.2)*u,
                15.*math.exp(math.log(7.3/15.)*u))
    if t<=11:
        u=ease((t-2)/9.)
        return (382+(200-382)*u,
                169.5+(-8-169.5)*u,
                7.3*math.exp(math.log(1.055/7.3)*u))
    return (200.,-8.,1.055)

def color(x,y):
    """Display tint from fixed world coordinates ONLY, never lyric state."""
    lx=x-SINGER_ORIGIN[0];ly=y-SINGER_ORIGIN[1]
    if 155<=lx<=570 and -255<=ly<=-20:return (136,236,216)
    if 335<=lx<=475 and 105<=ly<=240:return (243,191,118)
    if -390<=lx<=350 and -455<=ly<=355:
        if abs(lx)>195 or ly<-205:return (183,143,226)
        if -20<ly<125 and abs(lx)<130:return (248,146,189)
        return (221,227,238)
    return (144,201,216)

def source_frames(path):
    with open(path,'rb') as f:
        while True:
            header=f.read(8)
            if not header:break
            if len(header)!=8:raise ValueError('truncated native header')
            gen,n=struct.unpack('<iI',header)
            payload=f.read(n*8)
            if len(payload)!=n*8:raise ValueError('truncated native world')
            yield gen,struct.iter_unpack('<ii',payload)

def draw(g,cells):
    cx,cy,s=camera(g/GPS)
    ox=WIDTH/2-cx*s-SINGER_ORIGIN[0]*s
    oy=HEIGHT/2-cy*s-SINGER_ORIGIN[1]*s
    size=max(2,round(s))
    xl=(0-ox)/s-2;xh=(WIDTH-ox)/s+2
    yl=(0-oy)/s-2;yh=(HEIGHT-oy)/s+2
    image=Image.new('RGB',(WIDTH,HEIGHT),BACKGROUND)
    canvas=ImageDraw.Draw(image)
    for x,y in cells:
        if not(xl<=x<=xh and yl<=y<=yh):continue
        px=round(ox+x*s);py=round(oy+y*s)
        canvas.rectangle((px,py,px+size-1,py+size-1),fill=color(x,y))
    return image

def render(frames,out,*,stills=None):
    out=Path(out);out.parent.mkdir(parents=True,exist_ok=True)
    cmd=['ffmpeg','-y','-hide_banner','-loglevel','error',
         '-f','rawvideo','-pixel_format','rgb24',
         '-video_size',f'{WIDTH}x{HEIGHT}','-framerate',str(FPS),
         '-i','pipe:0','-c:v','libx264','-preset','veryfast','-crf','21',
         '-pix_fmt','yuv420p','-movflags','+faststart',str(out)]
    p=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
    previous=-8;count=0
    if stills:
        stills=Path(stills);stills.mkdir(parents=True,exist_ok=True)
    try:
        for g,world in source_frames(frames):
            if g!=previous+GPS//FPS:raise ValueError('missing native generation')
            previous=g
            image=draw(g,world)
            if stills and g in (0,200,384,960,2104,2400,3440):
                image.save(stills/f'full_world_g{g:04d}.png')
            p.stdin.write(image.tobytes())
            count+=1
        p.stdin.close()
        err=p.stderr.read().decode(errors='replace')
        if p.wait():raise RuntimeError('ffmpeg failed: '+err[-800:])
    finally:
        if p.poll() is None:p.kill();p.wait()
    return {'frames':count,'seconds':count/FPS,
            'rule':'B3/S23','native_world_frames':True,
            'screen_overlay_count':0,'independent_video_layers':0,
            'hard_camera_cuts':0,'full_song_qualified':False}

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--frames',type=Path,required=True)
    p.add_argument('--out',type=Path,required=True)
    p.add_argument('--stills',type=Path)
    a=p.parse_args()
    print(render(a.frames,a.out,stills=a.stills))
