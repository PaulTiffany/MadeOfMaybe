"""Render the actual integrated native WE+MADE one-world frames, no cuts.

The frame input is *one full B3/S23 universe* sampled every 8 generations
at 192 generations per audio second. Only existing live cell positions are
plotted; color/scale are camera presentation, never scripted lip or text poses.

Reproduce (no CI):
 python -m life.integrated_we_made_second_w --out output/WE_MADE
 g++ -O3 -std=c++17 research/one_world_native_frames.cpp -o /tmp/native
 /tmp/native output/WE_MADE/we_made_two_WV_g0.tsv output/WE_MADE/life.bin 3840 8
 python preview/render_native_integrated_we_made.py \
    --frames output/WE_MADE/life.bin --original-audio /path/to/authorized_suno.mp4 \
    --out output/WE_MADE/WE_MADE_original_song.mp4
"""
from __future__ import annotations
import argparse,struct,subprocess
from pathlib import Path
import numpy as np

W,H=1920,1080
FPS,GPS=24,192
FRAMES=480
CAMERA_X,CAMERA_Y,ZOOM=1820.,-1040.,.78
BG=(5,10,24)

def render(native_frames,video_path):
    video_path=Path(video_path)
    video_path.parent.mkdir(parents=True,exist_ok=True)
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y',
         '-f','rawvideo','-pixel_format','rgb24','-video_size',f'{W}x{H}',
         '-framerate',str(FPS),'-i','pipe:0','-c:v','libx264',
         '-preset','veryfast','-crf','25','-pix_fmt','yuv420p',
         '-movflags','+faststart',str(video_path)]
    encoder=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
    try:
        with open(native_frames,'rb') as f:
            for frame in range(FRAMES):
                header=f.read(8)
                if len(header)!=8:raise ValueError('native world film ended early')
                generation,n=struct.unpack('<iI',header)
                if generation!=8*frame:raise ValueError(('native clock discontinuity',generation))
                payload=f.read(n*8)
                if len(payload)!=n*8:raise ValueError('truncated actual Life universe')
                points=np.frombuffer(payload,dtype='<i4').reshape(-1,2)
                x=np.rint((points[:,0]-CAMERA_X)*ZOOM+W*.5).astype(np.int32)
                y=np.rint((points[:,1]-CAMERA_Y)*ZOOM+H*.5).astype(np.int32)
                good=(x>=0)&(x<W-1)&(y>=0)&(y<H-1)
                xy=points[good];x=x[good];y=y[good]
                image=np.empty((H,W,3),dtype=np.uint8)
                image[:]=BG
                face=(xy[:,0]<1400)&(xy[:,1]>-1400)&(xy[:,1]<-650)
                lip=(xy[:,0]>968)&(xy[:,0]<1270)&(xy[:,1]>-1020)&(xy[:,1]<-856)
                we=(xy[:,0]>=1400)&(xy[:,0]<2340)&(xy[:,1]<-1195)
                made=(xy[:,0]>=2200)&(xy[:,1]>-1240)&(xy[:,1]<-990)
                for ox in (0,1):
                    for oy in (0,1):
                        image[y+oy,x+ox]=(142,221,207)
                        image[y[face]+oy,x[face]+ox]=(203,174,233)
                        image[y[we]+oy,x[we]+ox]=(143,231,212)
                        image[y[made]+oy,x[made]+ox]=(251,210,139)
                        image[y[lip]+oy,x[lip]+ox]=(249,125,165)
                encoder.stdin.write(image.tobytes())
        encoder.stdin.close()
        stderr=encoder.stderr.read().decode(errors='replace')
        if encoder.wait()!=0:raise RuntimeError(stderr[-2000:])
    except Exception:
        encoder.kill()
        raise
    return video_path

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--frames',type=Path,required=True)
    p.add_argument('--original-audio',type=Path,required=True,
                   help='Owner-authorized original Made of Maybe MP3/M4A or previously muxed film.')
    p.add_argument('--out',type=Path,required=True)
    a=p.parse_args()
    silence=a.out.with_name(a.out.stem+'_silent.mp4')
    render(a.frames,silence)
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y',
          '-i',str(silence),'-i',str(a.original_audio),
          '-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac',
          '-b:a','128k','-t','20','-movflags','+faststart',str(a.out)],check=True)
    silence.unlink()
    print(a.out)
if __name__=='__main__':main()
