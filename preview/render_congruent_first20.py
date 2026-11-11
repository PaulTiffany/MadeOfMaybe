"""One continuous camera over ONLY true 192g/s B3/S23 occupied cells.

No optical lyric dots, lip poses, HUD, border, cut or inserted cell.
"""
from pathlib import Path
import math
from . import render_one_world_native_no_cuts as base

def camera(t):
    if t<0:raise ValueError('negative music time')
    if t<=1.5:return (628.,-1301.+96*t,11.)
    if t<=11:
        s=base.ease((t-1.5)/9.5)
        start_y=-1301.+96*1.5
        return (628.+(350.-628.)*s,start_y+(-125.-start_y)*s,
                11.*math.exp(math.log(.84/11.)*s))
    return (350.,-125.,.84)

old_color=base.color
def color(x,y):
    lx=x-base.SINGER_ORIGIN[0];ly=y-base.SINGER_ORIGIN[1]
    if 290<lx<1010 and -370<ly<110:
        if 390<lx<925 and -310<ly<-80:return (224,230,196)
        return (110,223,212)
    return old_color(x,y)

base.camera=camera
base.color=color

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser()
    p.add_argument('--frames',type=Path,required=True)
    p.add_argument('--out',type=Path,required=True)
    p.add_argument('--stills',type=Path)
    a=p.parse_args()
    print(base.render(a.frames,a.out,stills=a.stills))
