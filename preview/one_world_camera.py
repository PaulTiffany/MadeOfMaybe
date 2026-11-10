"""One continuous Life-world camera: glider -> switch -> singer.

A camera trajectory ONLY: the native B3/S23 initial condition and the
audio-to-generation relationship are unmodified. Center the first *actual*
source glider for its first 0.75 seconds (144 generations), reframe its
first collision with the catalyst, then pull out into the full Life stage.

Use camera_at(generation / GPS) with any sampler of the single Life world.
Do not recomposite the singer or lyrics into separate screen panels.
"""
from __future__ import annotations
import math
from life.full_song_karaoke import GPS

OPENING_SECONDS=11.0
GLIDER_TRACK_END=.75
CIRCUIT_LOCK_END=2.
WORLD_REVEAL_END=11.
CIRCUIT_CENTER=(382.,169.5)
GLIDER_CENTER_G0=(420.2,121.2)
GLIDER_VELOCITY=(-48.,48.) # world cells / audio second, c/4 at GPS=192
FINAL_CENTER=(200.,-8.)
FINAL_ZOOM=1.055


def _ease(u):
    u=max(0.,min(1.,u))
    return u*u*(3-2*u)


def camera_at(t):
    """Return singer-local (center_x, center_y, pixels_per_Life_cell)."""
    if t<0:raise ValueError('time must be nonnegative')
    if t<=GLIDER_TRACK_END:
        return (GLIDER_CENTER_G0[0]+GLIDER_VELOCITY[0]*t,
                GLIDER_CENTER_G0[1]+GLIDER_VELOCITY[1]*t,15.)
    if t<=CIRCUIT_LOCK_END:
        u=_ease((t-GLIDER_TRACK_END)/(CIRCUIT_LOCK_END-GLIDER_TRACK_END))
        a=camera_at(GLIDER_TRACK_END)
        return (a[0]+(CIRCUIT_CENTER[0]-a[0])*u,
                a[1]+(CIRCUIT_CENTER[1]-a[1])*u,
                math.exp(math.log(15.)+(math.log(7.3)-math.log(15.))*u))
    u=_ease((t-CIRCUIT_LOCK_END)/(WORLD_REVEAL_END-CIRCUIT_LOCK_END))
    return (CIRCUIT_CENTER[0]+(FINAL_CENTER[0]-CIRCUIT_CENTER[0])*u,
            CIRCUIT_CENTER[1]+(FINAL_CENTER[1]-CIRCUIT_CENTER[1])*u,
            math.exp(math.log(7.3)+(math.log(FINAL_ZOOM)-math.log(7.3))*u))


def projected(x,y,t,*,width=1280,height=720):
    """Actual-world coordinate projection; never a Life-cell modification."""
    cx,cy,s=camera_at(t)
    return ((x-cx)*s+width/2,(y-cy)*s+height/2)
