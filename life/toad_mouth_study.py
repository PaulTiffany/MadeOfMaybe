"""Native period-2 Toad mouth visual study (not signal-gated).

The Toad changes from a two-row band to a four-row oval on successive
B3/S23 generations. This is a visual reference, not a mouth with holdable
open/closed states.
"""
from .core import evolve, place

TOAD={(1,0),(2,0),(3,0),(0,1),(1,1),(2,1)}
BLOCK={(0,0),(1,0),(0,1),(1,1)}
FACE_BLOCK_ORIGINS=[
 (-8,-12),(-4,-12),(0,-12),(4,-12),(8,-12),
 (-12,-8),(12,-8),(-12,-4),(12,-4),(-12,0),(12,0),
 (-12,4),(12,4),(-12,8),(12,8),
 (-8,12),(-4,12),(0,12),(4,12),(8,12),
 (-6,-6),(6,-6),(0,-2),
]
FACE=set().union(*(place(BLOCK,x,y) for x,y in FACE_BLOCK_ORIGINS))
MOUTH_BAND=place(TOAD,-1,4)
MOUTH_OPEN=evolve(MOUTH_BAND)

def initial():
    return FACE | MOUTH_BAND

def two_phases():
    a=initial()
    return a, evolve(a)
