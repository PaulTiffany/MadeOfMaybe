"""Continuous, unedited B3/S23 native camera over rounded bubble candidate."""
from __future__ import annotations
import math
from pathlib import Path
from . import render_one_world_native_no_cuts as base
old=base.camera
def camera(t):
    if t<=2:return old(t)
    if t<=11:
        u=base.ease((t-2)/9)
        return (382+(350-382)*u,
                169.5+(-125-169.5)*u,
                7.3*math.exp(math.log(.85/7.3)*u))
    return (350.,-125.,.85)
old_color=base.fixed_color
def fixed_color(x,y):
    lx=x-1071;ly=y+1019
    if 300<lx<1015 and -370<ly<105:return (129,223,215)
    return old_color(x,y)
base.camera=camera
base.fixed_color=fixed_color
if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser()
    p.add_argument('--frames',type=Path,required=True)
    p.add_argument('--out',type=Path,required=True)
    p.add_argument('--stills',type=Path)
    a=p.parse_args()
    print(base.render(a.frames,a.out,still_dir=a.stills))
