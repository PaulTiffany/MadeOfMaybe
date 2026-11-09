"""Denser real B3/S23 glider-controlled mouth.

Extends the qualified 4-pixel-per-bank pilot with 15 independently routed
glider synthesis/deletion channels. One starting universe, fixed clock, no
runtime cell injection, no picture swaps. This is a tested fixed score; new
timing requires new routing and full-world requalification.
"""
from __future__ import annotations
from functools import lru_cache
from .core import evolve, place
from .glider_controlled_mouth import (
    BLOCK, FULL_DURATION, POSE_SAMPLES, BANK_SCHEDULES,
    MEDIUM_TARGETS, OPEN_TARGETS, UPPER_LIP,
    block_make_at, block_erase_at, rotate,
    signal_components as base_signals,
)
from .three_state_mouth import face_pixels

# Each entry: target (x,y), arrival shift in generations,
# D4 orientation for synthesis and clean deletion.
ADDITIONAL_ROUTING = {
    'medium': (
        ((-52, 71), 0, 2, 4),
        ((0, 82), 32, 2, 6),
        ((52, 71), -32, 7, 4),
        ((-67, 71), -24, 7, 6),
        ((67, 55), -24, 2, 3),
        ((37, 76), 0, 2, 4),
    ),
    'open': (
        ((0, 130), 8, 7, 4),
        ((-48, 112), -48, 2, 5),
        ((48, 112), -32, 2, 3),
        ((-67, 98), 0, 2, 5),
        ((67, 98), -48, 2, 3),
        ((-37, 111), 0, 7, 6),
        ((37, 111), -8, 7, 4),
        ((-12, 129), -8, 2, 5),
        ((12, 129), 32, 2, 5),
    ),
}

DENSE_MEDIUM_TARGETS = MEDIUM_TARGETS + tuple(x[0] for x in ADDITIONAL_ROUTING['medium'])
DENSE_OPEN_TARGETS = OPEN_TARGETS + tuple(x[0] for x in ADDITIONAL_ROUTING['open'])

def _packet(bank, target, shift, make_dir, erase_dir):
    seed=set()
    for action,t in BANK_SCHEDULES[bank]:
        packet = (rotate(block_make_at(t+shift),make_dir)
                  if action=='make' else
                  rotate(block_erase_at(t+shift),erase_dir))
        seed |= place(packet,*target)
    return seed

def signal_components():
    packets=base_signals()
    for bank,entries in ADDITIONAL_ROUTING.items():
        for i,(target,shift,make_dir,erase_dir) in enumerate(entries):
            packets[f'{bank}_extra_{i}']=_packet(bank,target,shift,make_dir,erase_dir)
    return packets

def shadow(cells,radius=2):
    return {(x+dx,y+dy) for x,y in cells
            for dx in range(-radius,radius+1)
            for dy in range(-radius,radius+1)}

@lru_cache(maxsize=1)
def prepared_art():
    """Prepare permanent still-life face/lip with full-timeline clearance.

    This layout step precedes generation zero; no runtime masking occurs.
    """
    interference=shadow(UPPER_LIP)
    packets=signal_components()
    for _ in range(FULL_DURATION):
        for key,live in packets.items():
            interference.update(shadow(live))
            packets[key]=evolve(live)
    old_origins=set(range(-105,106,12))
    extra_lip=set()
    for x in range(-105,104,4):
        if x in old_origins:continue
        block=place(BLOCK,x,30)
        if block & interference:continue
        extra_lip |= block
    upper=set(UPPER_LIP)|extra_lip
    interference.update(shadow(upper))
    face=set()
    for x,y in face_pixels():
        tile=place(BLOCK,8*x,8*y)
        if not tile & interference:
            face |= tile
    return frozenset(face),frozenset(upper)

def active_pixels(state):
    if state not in ('closed','medium','open'):
        raise ValueError(state)
    if state=='closed':return set()
    targets=DENSE_MEDIUM_TARGETS if state=='medium' else DENSE_OPEN_TARGETS
    return set().union(*(place(BLOCK,*p) for p in targets))

def components(with_bubble=True):
    face,lip=prepared_art()
    parts={'upper_lip':set(lip),'fixed_face':set(face),**signal_components()}
    if with_bubble:
        from .composition import bubble_parts, symbol
        outline,letters=bubble_parts()
        # Same bubble and lyrics, simply placed nearer the face. All output
        # corridors are verified against these positions for 785 generations.
        parts['bubble_outline']=place(outline,160,-90)
        parts['bubble_lyrics']=place(letters,160,-90)
        parts['pulsar']=place(symbol(),300,90)
    return parts

def universe(with_bubble=True):
    return set().union(*components(with_bubble).values())
