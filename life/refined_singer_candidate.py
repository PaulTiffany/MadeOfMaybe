"""Real B3/S23 narrower/lower mouth candidate.

This is an alternative singer, not yet a replacement for the causal
WE-to-lower_medium_0 bridge: the old outer channel is removed. Retained
glider packets still do the physical mouth motion. Full static art tiles are
pruned only when their 2-cell spacetime guard hits a moved glider.
No runtime cell injection or optical scaling is used.
"""
from __future__ import annotations
from functools import lru_cache
from .core import evolve, place
from .glider_controlled_mouth import BLOCK
from .character_round2 import components as original_components
from .symmetric_full_mouth import MEDIUM_TARGETS, OPEN_TARGETS, target_blocks
from .restored_centerline import START_LINE

LIP_DROP_Y = 32
MAX_MEDIUM_HALF_WIDTH = 53
MAX_OPEN_HALF_WIDTH = 49
CHECKPOINTS = {60:'closed',180:'medium',288:'open',420:'medium',
               540:'breath',680:'open',960:'closed'}


def _lip_moved_component(name):
    if name.startswith(('upper_', 'lower_')):
        p=name.split('_'); bank=p[1]
        index=int(p[-1])+(4 if 'extra' in p else 0)
        x=(MEDIUM_TARGETS if bank=='medium' else OPEN_TARGETS)[index][0]
        bound=MAX_MEDIUM_HALF_WIDTH if bank=='medium' else MAX_OPEN_HALF_WIDTH
        return abs(x)<=bound, LIP_DROP_Y
    if name.startswith('line_'):return True,LIP_DROP_Y
    return True,0


def new_moving_components():
    moving={}
    for k,cells in original_components(False).items():
        if k.startswith('art_'):continue
        keep,dy=_lip_moved_component(k)
        if keep:moving[k]=place(cells,0,dy)
    return moving


def new_target_cells(state):
    cells=target_blocks(state)
    sites={(x,y) for x,y in cells
           if (x-1,y) not in cells and (x,y-1) not in cells}
    cap=MAX_MEDIUM_HALF_WIDTH if state=='medium' else MAX_OPEN_HALF_WIDTH
    kept={p for p in sites if abs(p[0])<=cap}
    return set().union(*(place(BLOCK,x,y+LIP_DROP_Y) for x,y in kept)) if kept else set()


@lru_cache(maxsize=1)
def qualified_layout():
    base=original_components(False)
    original_art={k:set(v) for k,v in base.items() if k.startswith('art_')}
    moving=new_moving_components()
    world=set().union(*moving.values())
    if sum(map(len,moving.values()))!=len(world):
        raise AssertionError('refined lip packets overlap at generation zero')
    shadow=set();observed={}
    for gen in range(981):
        if gen in CHECKPOINTS:
            observed[gen]={s:new_target_cells(s)<=world for s in ('medium','open')}
            observed[gen]['centerline']=all(place(BLOCK,x,y+LIP_DROP_Y)<=world
                                             for x,y in START_LINE)
        if world!=set().union(*moving.values()):
            raise AssertionError(f'refined glider packets interact at g{gen}')
        if gen==980:break
        for x,y in world:
            if -350<=x<=350 and -430<=y<=370:
                shadow.update((x+dx,y+dy) for dx in range(-2,3)
                                            for dy in range(-2,3))
        moving={k:evolve(v) for k,v in moving.items()}
        world=evolve(world)
    for state,gens in {'medium':(180,420),'open':(288,680)}.items():
        for g in gens:
            if not observed[g][state]:raise AssertionError((g,state,'missing real mouth'))
    if not observed[60]['centerline'] or not observed[960]['centerline']:
        raise AssertionError('resting lip did not recover')
    art={};removed={}
    for key,cells in original_art.items():
        origins={(x,y) for x,y in cells if (x-1,y) not in cells
                 and (x,y-1) not in cells and place(BLOCK,x,y)<=cells}
        kept={p for p in origins if not place(BLOCK,*p)&shadow}
        art[key]=frozenset().union(*(place(BLOCK,*p) for p in kept)) if kept else frozenset()
        removed[key]=len(origins)-len(kept)
        if evolve(art[key])!=art[key]:raise AssertionError(f'unstable art {key}')
    all_art=set().union(*art.values())
    if evolve(all_art)!=all_art or all_art&shadow:
        raise AssertionError('static portrait and moving mouth not independent')
    old_cheeks=len(original_art['art_cheekbones'])//4
    new_cheeks=len(art['art_cheekbones'])//4
    if new_cheeks<old_cheeks-2:raise AssertionError('cheeks not preserved')
    return {'rule':'B3/S23','native_generations_checked':980,
            'mouth_delta_y':LIP_DROP_Y,
            'max_medium_half_width':MAX_MEDIUM_HALF_WIDTH,
            'max_open_half_width':MAX_OPEN_HALF_WIDTH,
            'original_art_cells':sum(map(len,original_art.values())),
            'preserved_art_cells':len(all_art),
            'preserved_cheek_tiles':new_cheeks,
            'original_cheek_tiles':old_cheeks,
            'removed_art_blocks':removed,
            'native_dynamic_channel_independence':True,
            'strict_two_cell_spacetime_guard':True,
            'checkpoint_poses':observed,
            'new_mouth_causal_lyric_bridge_qualified':False,
            'art':art}


def seed():
    q=qualified_layout()
    return set().union(*new_moving_components().values())|set().union(*q['art'].values())
