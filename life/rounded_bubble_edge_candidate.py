"""Physically rounded B3/S23 singer speech bubble using EXISTING LWSS turner.

This is a carefully measured optional scene candidate, NOT a newly invented
redirector. The turner emits one pixel, not the finished 403-word karaoke.
The tail is an actual 2x2-block Life mosaic; it is not yet a mouth wire.
"""
from __future__ import annotations
from functools import lru_cache
from math import cos,sin,pi
from .core import evolve,place
from .relocated_singer_anchor import relocated_anchor,portrait,SINGER_TRANSLATION
from .vertical_lwss_corner import STATION,INPUT
from .staggered_word_mesh import EATER_NORTHEAST,EATER_SOUTHWEST,EATER_TEXT
from .blank_bubble_redirector import OUTPUT_G,FLIGHT_DELAY

CENTER=(655,-170)
RADII=(350,185)
STATION_LOCAL=(925,-125)
CATCHER_X=348
BLOCK={(0,0),(1,0),(0,1),(1,1)}

def _blocks(points):
    world=set()
    for x,y in points:
        b=place(BLOCK,x,y)
        if world&b:raise AssertionError('overlapping native bubble tiles')
        world|=b
    if evolve(world)!=world:
        raise AssertionError('native rounded bubble is not a stable Life pattern')
    return world

@lru_cache(maxsize=1)
def rim():
    cx,cy=CENTER;rx,ry=RADII;pts=set()
    for i in range(420):
        angle=2*pi*i/420
        x=8*round((cx+rx*cos(angle))/8)
        y=8*round((cy+ry*sin(angle))/8)
        # Existing downward LWSS enters through a physically missing set
        # of 2x2 tiles; not a film mask.
        if abs(x-STATION_LOCAL[0])<=64 and y<-245:continue
        # Actual controller-to-tail aperture also avoids a native corridor
        # traversed by the already-present singer glider.
        if 480<=x<=730 and y>=-60:continue
        pts.add((x,y))
    def add_segment(a,b):
        count=max(2,round(max(abs(b[0]-a[0]),abs(b[1]-a[1]))/8))
        for i in range(count+1):
            t=i/count
            x=8*round((a[0]+(b[0]-a[0])*t)/8)
            y=8*round((a[1]+(b[1]-a[1])*t)/8)
            pts.add((x,y))
    # Native still-life tail; this is a spatial reservation, not a wire.
    add_segment((608,0),(584,80))
    add_segment((720,0),(584,80))
    return frozenset(_blocks(pts))

@lru_cache(maxsize=1)
def device():
    x,y=STATION_LOCAL
    return frozenset(place(STATION,x,y)|
                     place(INPUT,x,y-2*FLIGHT_DELAY)|
                     place(EATER_NORTHEAST,x,y)|
                     place(EATER_SOUTHWEST,x,y)|
                     place(EATER_TEXT,CATCHER_X+57,y))

def components():
    base=relocated_anchor()|portrait()
    border=place(rim(),*SINGER_TRANSLATION)
    actuator=place(device(),*SINGER_TRANSLATION)
    if base&border or base&actuator or border&actuator:
        raise AssertionError('frame or original turner overlaps singer at g0')
    return (frozenset(base),frozenset(border),frozenset(actuator))

def universe():
    return set().union(*components())
