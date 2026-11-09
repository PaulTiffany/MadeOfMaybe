"""Experimental two-act native glider control of a five-block resting lip.

CLOSED line exists at start, is erased at generation 98 and is re-built via
five two-glider block syntheses no later than generation 932. The original
medium/open banks retain their previous fixed timing, so the intermediate
post-medium closed checkpoint at g540 does *not* yet display this line.
"""
from __future__ import annotations
from .core import place
from .glider_controlled_mouth import BLOCK, block_make_at, block_erase_at, rotate
from .symmetric_full_mouth import components as original_components

START_LINE = tuple((x,49) for x in (-16,-8,0,8,16))
ERASE_TIME = 98
RESTORE_ROUTES = (
    ((-16,49),800,0),
    ((-8,49),800,0),
    ((0,49),812,3),
    ((8,49),932,2),
    ((16,49),908,0),
)
QUALIFICATION_END=980

def components(with_bubble=True):
    p=original_components(with_bubble=with_bubble)
    p.pop('rest_line')
    for i,(x,y) in enumerate(START_LINE):
        p[f'line_erase_{i}']=(place(BLOCK,x,y) |
            place(rotate(block_erase_at(ERASE_TIME),1),x,y))
    for i,(origin,gen,direction) in enumerate(RESTORE_ROUTES):
        p[f'line_make_{i}']=place(rotate(block_make_at(gen),direction),*origin)
    return p

def universe(with_bubble=True):
    return set().union(*components(with_bubble).values())
