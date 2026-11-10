"""Real one-world camera over native staggered WE mesh (accelerated demo).

Every moving pixel is an actual B3/S23 cell from native C++ evolution.
The 14-second proof compresses 7600 Life generations for inspection; it is
NOT the song-synchronized karaoke nor an optical letter animation.
"""
from __future__ import annotations
import argparse,bisect,struct,subprocess
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont

WIDTH,HEIGHT=1280,720
FPS=20
DURATION_S=14
KEYFRAMES=(
 (0.,0,1650.,-1250.,.35),
 (2.,1120,1640.,-750.,.40),
 (4.5,3200,1550.,-120.,.44),
 (6.7,4900,1100.,120.,.65),
 (8.3,6000,320.,190.,1.32),
 (10.,6400,290.,190.,1.32),
 (12.,7000,250.,190.,1.32),
 (14.,7600,250.,190.,1.32),
)

def font(size,bold=False):
    try:return ImageFont.truetype('DejaVuSans-Bold.ttf' if bold else 'DejaVuSans.ttf',size)
    except OSError:return ImageFont.load_default()

def read_frames(path):
    frames={}
    with open(path,'rb') as file:
        while True:
            header=file.read(8)
            if not header:break
            if len(header)!=8:raise RuntimeError('truncated frame header')
            generation,count=struct.unpack('<iI',header)
            payload=file.read(count*8)
            if len(payload)!=count*8:raise RuntimeError('truncated B3/S23 coordinates')
            frames[generation]=list(struct.iter_unpack('<ii',payload))
    if not frames or max(frames)<7600:
        raise RuntimeError('native g7600 checkpoint missing')
    return frames

def camera(t):
    if t<=KEYFRAMES[0][0]:return KEYFRAMES[0][1:]
    if t>=KEYFRAMES[-1][0]:return KEYFRAMES[-1][1:]
    for a,b in zip(KEYFRAMES,KEYFRAMES[1:]):
        if a[0]<=t<=b[0]:
            u=(t-a[0])/(b[0]-a[0])
            eased=u*u*(3-2*u)
            return tuple(v+(w-v)*eased for v,w in zip(a[1:],b[1:]))
    raise AssertionError('camera time unreachable')

def draw(cells,g,t):
    im=Image.new('RGB',(WIDTH,HEIGHT),(6,11,26))
    d=ImageDraw.Draw(im)
    _,cx,cy,scale=camera(t)
    for x,y in cells:
        px=int((x-cx)*scale+WIDTH/2)
        py=int((y-cy)*scale+HEIGHT/2)
        if -3<px<WIDTH+2 and -3<py<HEIGHT+2:
            radius=1 if scale<.8 else 2 if scale<1.3 else 3
            d.rectangle((px,py,px+radius,py+radius),fill=(123,230,214))
    d.text((32,20),'WE / STAGGERED CONWAY TURNING MESH',
           font=font(25,True),fill=(237,239,253))
    d.text((33,59),'ONE REAL B3/S23 WORLD   |   35 VERTICAL LWSS INPUTS  →  35 LEFTWARD LETTER PIXELS',
           font=font(13),fill=(167,191,217))
    if g<4000:label='VERTICAL APPROACH'
    elif g<5950:label='STAGGERED TURNING'
    elif g<7300:label='ALIGNED MOVING WORD  →  SEVEN EATER LANES'
    else:label='EVERY SHIP EATEN / STABLE EATERS REMAIN'
    d.text((34,HEIGHT-68),label,font=font(18,True),fill=(255,213,153))
    d.text((34,HEIGHT-38),
           f'native generation {g:,}    •    accelerated proof replay (not song tempo)',
           font=font(13),fill=(174,186,202))
    return im

def render(frames_path,output,*,thumbnail=None):
    frames=read_frames(frames_path)
    generations=sorted(frames)
    output=Path(output)
    output.parent.mkdir(parents=True,exist_ok=True)
    cmd=['ffmpeg','-y','-hide_banner','-loglevel','error',
         '-f','rawvideo','-pix_fmt','rgb24','-s',f'{WIDTH}x{HEIGHT}',
         '-r',str(FPS),'-i','-','-c:v','libx264','-preset','fast',
         '-crf','21','-pix_fmt','yuv420p','-movflags','+faststart',str(output)]
    process=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
    try:
        for n in range(round(FPS*DURATION_S)):
            t=n/FPS
            target=round(camera(t)[0])
            idx=bisect.bisect_left(generations,target)
            if idx==len(generations):idx-=1
            if idx>0 and abs(generations[idx-1]-target)<abs(generations[idx]-target):
                idx-=1
            g=generations[idx]
            image=draw(frames[g],g,t)
            if thumbnail is not None and n==round(FPS*8.3):
                Path(thumbnail).parent.mkdir(parents=True,exist_ok=True)
                image.save(thumbnail,optimize=True)
            process.stdin.write(image.tobytes())
        process.stdin.close()
        err=process.stderr.read().decode(errors='replace')
        if process.wait():
            raise RuntimeError('FFmpeg: '+err[-2000:])
    finally:
        if process.poll() is None:process.kill();process.wait()
    print('Wrote actual native Life video',output)
    return output

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--frames',type=Path,default=Path('output/staggered_word_mesh/we_frames.bin'))
    p.add_argument('--out',type=Path,default=Path('preview/staggered_word_we_native.mp4'))
    p.add_argument('--thumbnail',type=Path,default=Path('preview/staggered_word_we_native.png'))
    a=p.parse_args()
    render(a.frames,a.out,thumbnail=a.thumbnail)
