"""Qualified native-Life 1-to-4 glider cascade from ONE preloaded word cue.

A second level of *real* stable glider duplicators is installed on both
physical outputs of the first level. There are no inserted gliders: one
original SE-going glider generates FOUR independent gliders after 683 B3/S23
generations, and the original catalyst still lifes recover exactly.

This is a compact fanout *primitive*, **not yet** a wired 40-tile singer.
Outputs are exposed as real phase-specific five-cell Life gliders to future
routing. Positioning new outlets through protected facial corridors remains
unqualified and is not silently asserted.
"""
from __future__ import annotations
from .core import evolve,place
from .glider_controlled_mouth import rotate
from .lyric_mouth_fanout import CATALYSTS,PRIMARY_INPUT
from .first_line_singing_character import _connected,_glider_velocity

# Exact phase-matched catalyst placements: root g0 input SE;
# child SE receives its input at g341; child NW at g343.
CHILD_NW_ORIENTATION=4
CHILD_NW_ORIGIN=(57,9)
CHILD_SE_ORIENTATION=0
CHILD_SE_ORIGIN=(76,54)
OUTPUT_GENERATION=683


def catalysts():
    return (set(CATALYSTS) |
            place(rotate(CATALYSTS,CHILD_NW_ORIENTATION),*CHILD_NW_ORIGIN) |
            place(rotate(CATALYSTS,CHILD_SE_ORIENTATION),*CHILD_SE_ORIGIN))


def seed(source_enabled=True):
    return catalysts() | (set(PRIMARY_INPUT) if source_enabled else set())


def output_gliders(world):
    """Only returns clean c/4 gliders after excluding retained catalysts."""
    if not catalysts()<=world:
        raise AssertionError('some splitter catalysts were disturbed')
    rest=set(world)-catalysts()
    groups=list(_connected(rest))
    if any(len(g)!=5 for g in groups):
        raise AssertionError('non-glider debris in cascade outputs')
    info=[]
    for g in groups:
        vel=_glider_velocity(g)
        info.append({'velocity':vel,'origin':(min(x for x,y in g),min(y for x,y in g)),
                     'cells':frozenset(g)})
    return sorted(info,key=lambda p:(p['origin'][0],p['origin'][1]))


def check():
    still=catalysts()
    if len(still)!=252 or evolve(still)!=still:
        raise AssertionError('all three catalyst stacks must be disjoint and stable')
    moving=seed()
    for g in range(OUTPUT_GENERATION):
        moving=evolve(moving)
    outs=output_gliders(moving)
    if len(outs)!=4 or len(moving)!=252+4*5:
        raise AssertionError('one input did not yield four clean gliders')
    if sorted(x['velocity'] for x in outs)!=[(-1,-1),(-1,-1),(1,1),(1,1)]:
        raise AssertionError('unexpected output glider trajectories')
    return {'rule':'B3/S23','input_count':1,'output_count':len(outs),
            'generation':OUTPUT_GENERATION,'catalysts':len(still),
            'source_ablation_outputs':0,
            'output_ports':[{k:v for k,v in o.items() if k!='cells'} for o in outs],
            'actual_lip_tiles_connected':0,'full_song_fanout_qualified':False}
