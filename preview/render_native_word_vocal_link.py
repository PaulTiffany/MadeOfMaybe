"""Wider continuous camera over only true B3/S23 cells; no cuts or overlays."""
from pathlib import Path
import argparse,math,inspect
from . import render_one_world_native_no_cuts as base

def camera(t):
    if t<0:raise ValueError('negative time')
    if t<=1.5:return (628.,-1301.+96*t,11.)
    if t<=11:
        u=base.ease((t-1.5)/9.5)
        y=-1301.+96*1.5
        return (628.+(350.-628.)*u,y+(-125.-y)*u,
                11.*math.exp(math.log(.73/11.)*u))
    return (350.,-125.,.73)

original_color=base.color if hasattr(base,'color') else base.fixed_color
def static_world_tint(x,y):
    lx=x-base.SINGER_ORIGIN[0];ly=y-base.SINGER_ORIGIN[1]
    if 290<lx<1010 and -370<ly<110:
        if 390<lx<925 and -310<ly<-80:return (224,230,196)
        return (110,223,212)
    return original_color(x,y)

base.camera=camera
if hasattr(base,'color'):base.color=static_world_tint
else:base.fixed_color=static_world_tint

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--frames',type=Path,required=True)
    p.add_argument('--out',type=Path,required=True)
    p.add_argument('--stills',type=Path)
    a=p.parse_args()
    kw='stills' if 'stills' in inspect.signature(base.render).parameters else 'still_dir'
    base.render(a.frames,a.out,**{kw:a.stills})
