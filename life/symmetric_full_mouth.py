"""Symmetric moving lips in one B3/S23 universe, using preloaded gliders.

The verified dense lower lip is mirrored across y=50. Both lip edges are
actively made/erased by glider reactions, while a short central resting line
remains static (not yet a glider-controlled closed-mouth state).
Facial still-life blocks are placed outside the entire glider trajectory.
"""
from __future__ import annotations
import math
from functools import lru_cache
from .core import evolve, place
from .dense_glider_mouth import (
    signal_components as old_signal_components,
    DENSE_MEDIUM_TARGETS, DENSE_OPEN_TARGETS,
    FULL_DURATION, POSE_SAMPLES, BLOCK,
)

MIDLINE=50
MEDIUM_INDICES=tuple(range(7))
OPEN_INDICES=tuple(range(13))
MEDIUM_TARGETS=tuple(DENSE_MEDIUM_TARGETS[i] for i in MEDIUM_INDICES)
OPEN_TARGETS=tuple(DENSE_OPEN_TARGETS[i] for i in OPEN_INDICES)
REST_LINE=frozenset().union(*(place(BLOCK,x,MIDLINE-1)
                              for x in range(-32,33,8)))

def reflect(cells):
    return {(x,2*MIDLINE-y) for x,y in cells}

def signal_components():
    original=old_signal_components()
    kept={}
    for key,cells in original.items():
        bank='medium' if key.startswith('medium') else 'open'
        index=int(key.rsplit('_',1)[1])
        if '_extra_' in key:
            index+=4
        selected=MEDIUM_INDICES if bank=='medium' else OPEN_INDICES
        if index not in selected:
            continue
        kept['lower_'+key]=set(cells)
        kept['upper_'+key]=reflect(cells)
    return kept

def target_blocks(state):
    if state not in ('closed','medium','open'):
        raise ValueError(state)
    out=set()
    targets=MEDIUM_TARGETS if state=='medium' else OPEN_TARGETS if state=='open' else ()
    for pt in targets:
        b=place(BLOCK,*pt)
        out |= b|reflect(b)
    return out

def face_outline_points():
    pts=set()
    for y in range(-25,29):
        fraction=(y-1)/28
        if abs(fraction)>=1:
            continue
        radius=int(round(26.5*math.sqrt(1-fraction*fraction)))
        pts |= {(-radius*8,y*8),(radius*8,y*8)}
    return pts

def feature_points():
    pts=set()
    for c in (-56,56):
        for dx in (-24,-16,-8,0,8,16,24):
            pts.add((c+dx,-174+(abs(dx)//16)*8))
        for dx in (-16,-8,0,8,16):
            pts.add((c+dx,-143+(abs(dx)//16)*8))
        for dx in (-8,0,8):
            pts.add((c+dx,-127))
        pts.add((c,-135))
    pts.update({(-8,-104),(0,-104),(0,-96),(8,-96)})
    pts.update({(-112,MIDLINE-1),(112,MIDLINE-1)})
    return pts

def guard(cells,radius=2):
    for x,y in cells:
        for dx in range(-radius,radius+1):
            for dy in range(-radius,radius+1):
                yield x+dx,y+dy

@lru_cache(maxsize=1)
def prepared_art():
    """One-time layout: avoid two-cell shadow of every signal at every tick."""
    moving=signal_components()
    forbidden=set(guard(REST_LINE))
    for _ in range(FULL_DURATION):
        for key,cells in moving.items():
            forbidden.update(guard(cells))
            moving[key]=evolve(cells)
    outline=set()
    features=set()
    for p in face_outline_points():
        b=place(BLOCK,*p)
        if not b&forbidden:
            outline |= b
    outline_guard=set(guard(outline))
    for p in feature_points():
        b=place(BLOCK,*p)
        if not b&forbidden and not b&outline_guard:
            features |= b
    return frozenset(outline),frozenset(features)

def components(with_bubble=True):
    outline,features=prepared_art()
    parts={'outline':set(outline),'eyes_nose':set(features),
           'rest_line':set(REST_LINE),**signal_components()}
    if with_bubble:
        from .composition import bubble_parts,symbol
        border,text=bubble_parts()
        parts['bubble_outline']=place(border,160,-90)
        parts['bubble_lyrics']=place(text,160,-90)
        parts['pulsar']=place(symbol(),300,90)
    return parts

def universe(with_bubble=True):
    return set().union(*components(with_bubble).values())
