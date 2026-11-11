"""Physically moved splitter + two real lyric events + refined singer in one Life world.

The 84-cell splitter is physically below the actual native speech bubble.
Both source gliders and glyph partner-glider hardware are translated with it,
so the first two native WE events still make/erase a REAL 2x2 lyric pixel at
2156/2578 and 2976/3402 generations.  The lip output is NOT YET CONNECTED
to the narrower/lower singer's newly retained lip lanes.
"""
from __future__ import annotations
from functools import lru_cache
from .core import evolve,place
from .glider_controlled_mouth import BLOCK
from .physical_lip_splitter_bridge import (
    SINGER_TRANSLATION,SPLITTER_LOCAL_ORIGIN,splitter_catalysts)
from .reusable_word_cue import seed as word_source_seed,line_times
from .refined_singer_candidate import seed as singer_seed,qualified_layout,new_moving_components
from .composition import bubble_parts

RELOCATED_SPLITTER_LOCAL=(420,120)
TRANSLATION=(RELOCATED_SPLITTER_LOCAL[0]-SPLITTER_LOCAL_ORIGIN[0],
             RELOCATED_SPLITTER_LOCAL[1]-SPLITTER_LOCAL_ORIGIN[1])
RELOCATED_GLYPH_ORIGIN=TRANSLATION
LAST_NATIVE_G=3402


def relocated_anchor(*,first=True,second=True):
    return place(word_source_seed(first,second),*TRANSLATION)


def static_bubble():
    border,letters=bubble_parts()
    return place(border|letters,160+SINGER_TRANSLATION[0],
                 -90+SINGER_TRANSLATION[1])


def portrait():
    return place(singer_seed(),*SINGER_TRANSLATION)


def universe(*,first=True,second=True):
    anchor=relocated_anchor(first=first,second=second)
    singer=portrait()
    bubble=static_bubble()
    if len(anchor|singer|bubble)!=len(anchor)+len(singer)+len(bubble):
        raise AssertionError('physical initial universe overlaps')
    return anchor|singer|bubble


def _two_cell_shadow_collision(cells,other):
    return any((x+dx,y+dy) in other for x,y in cells
               for dx in range(-2,3) for dy in range(-2,3))


@lru_cache(maxsize=1)
def qualified_integration():
    """3403 exact-generation finite clearance and real-glyph verification."""
    art=place(set().union(*qualified_layout()['art'].values()),*SINGER_TRANSLATION)
    bubble=static_bubble()
    if evolve(bubble)!=bubble:raise AssertionError('speech bubble unstable')
    stable=art|bubble
    if evolve(stable)!=stable:raise AssertionError('static world not stable')
    device=place(splitter_catalysts(),SINGER_TRANSLATION[0]+TRANSLATION[0],
                 SINGER_TRANSLATION[1]+TRANSLATION[1])
    local_device=place(device,-SINGER_TRANSLATION[0],-SINGER_TRANSLATION[1])
    local_bubble=place(bubble,-SINGER_TRANSLATION[0],-SINGER_TRANSLATION[1])
    bx0,bx1=min(x for x,y in local_bubble),max(x for x,y in local_bubble)
    by1=max(y for x,y in local_bubble)
    x0,x1=min(x for x,y in local_device),max(x for x,y in local_device)
    y0,y1=min(y for x,y in local_device),max(y for x,y in local_device)
    if not (bx0<x0<x1<bx1 and y0>by1+2):
        raise AssertionError('controller is not physically below bubble')
    anchor=relocated_anchor()
    moving=place(set().union(*new_moving_components().values()),*SINGER_TRANSLATION)
    block=place(BLOCK,*RELOCATED_GLYPH_ORIGIN)
    times=line_times()
    expected={times[0][0]:True,times[0][1]:False,
              times[1][0]:True,times[1][1]:False}
    observed={}
    for gen in range(LAST_NATIVE_G+1):
        if _two_cell_shadow_collision(anchor,stable|moving):
            raise AssertionError(f'controller/glyph hits protected singer/bubble g{gen}')
        if gen in expected:
            observed[gen]={'word_live':block<=anchor,'catalysts_restored':device<=anchor}
            if observed[gen]['word_live']!=expected[gen]:
                raise AssertionError(f'causal glyph switch wrong at g{gen}')
        if gen<LAST_NATIVE_G:
            anchor=evolve(anchor)
            moving=evolve(moving)
    if len(device)!=84 or not device<=anchor:
        raise AssertionError('relocated catalysts failed to reset')
    if len(universe())<6500:raise AssertionError('missing native portrait')
    return {'rule':'B3/S23',
            'splitter_original_local':SPLITTER_LOCAL_ORIGIN,
            'splitter_relocated_local':RELOCATED_SPLITTER_LOCAL,
            'controller_is_physically_below_real_bubble':True,
            'catalyst_cells':len(device),
            'catalyst_local_bbox':[x0,x1,y0,y1],
            'bubble_local_ymax':by1,
            'relocated_native_lyric_anchor':RELOCATED_GLYPH_ORIGIN,
            'source_events':[times[0],times[1]],
            'real_life_generations_replayed':LAST_NATIVE_G+1,
            'static_portrait_and_bubble_unchanged':True,
            'two_cell_spacetime_clearance':True,
            'checkpoints':observed,
            'old_lips_still_autonomously_timed':True,
            'new_mouth_expression_fanout_connected':False,
            'all_403_word_routes_connected':False}
