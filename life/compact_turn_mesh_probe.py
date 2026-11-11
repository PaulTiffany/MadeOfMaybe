"""Minimal stagger test for seven genuine B3/S23 vertical-to-left LWSS turns.

Slightly separate the 17-cell-tall one-shot stations: row pitch 18, with
36-cell horizontal staircase. Input spaceships are staged upstream by the
corresponding c/2 travel time, so all seven emerge horizontally aligned.
This is one seven-pixel column, NOT yet the full 35-pixel WE mechanism.
"""
from __future__ import annotations
from .core import evolve,place
from .vertical_lwss_corner import STATION,INPUT,outgoing_lwss

ROW_COUNT=7
ROW_PITCH=18
X_STEP=-36
ASSEMBLED_G=800
REPLAY_END_G=3200

def components(*,row_pitch=ROW_PITCH,x_step=X_STEP,offsets=None,enabled=None):
    if row_pitch<=0 or x_step%2:
        raise ValueError('invalid phase-compatible geometry')
    xs=[x_step*i for i in range(ROW_COUNT)] if offsets is None else list(offsets)
    if len(xs)!=ROW_COUNT or any(x%2 for x in xs):
        raise ValueError('seven phase-compatible x offsets required')
    if enabled is None:enabled=range(ROW_COUNT)
    enabled=set(enabled)
    if any(i<0 or i>=ROW_COUNT for i in enabled):
        raise ValueError('bad enabled row')
    farthest=max(xs)
    parts=[]
    for i,x in enumerate(xs):
        y=row_pitch*i
        fixed=place(STATION,x,y)
        # For a c/2 downward incoming LWSS, moving its initial position
        # up by d cells delays its collision by 2d Life generations.
        delay=farthest-x
        source=place(INPUT,x,y-delay) if i in enabled else set()
        parts.append(fixed|source)
    return tuple(parts)

def first_interference(*,row_pitch=ROW_PITCH,x_step=X_STEP,offsets=None,
                       until=400):
    parts=list(map(set,components(row_pitch=row_pitch,x_step=x_step,offsets=offsets)))
    world=set().union(*parts)
    if len(world)!=sum(map(len,parts)):return 0
    for g in range(until+1):
        if world!=set().union(*parts):return g
        if g<until:
            world=evolve(world)
            parts=[evolve(p) for p in parts]
    return None

def qualify(*,row_pitch=ROW_PITCH,x_step=X_STEP,
            until=REPLAY_END_G,enabled=None):
    """Exact native Life whole-world equality at EVERY tick and real LWSS output."""
    if until<ASSEMBLED_G+100:
        raise ValueError('replay must include post-assembly flight')
    parts=list(map(set,components(row_pitch=row_pitch,x_step=x_step,
                                  enabled=enabled)))
    world=set().union(*parts)
    if len(world)!=sum(map(len,parts)):
        raise AssertionError('g0 stationary/ship overlap')
    snapshots={}
    for g in range(until+1):
        if world!=set().union(*parts):
            raise AssertionError(f'unintended cross-channel reaction at g{g}')
        if g in (ASSEMBLED_G,ASSEMBLED_G+100):
            found={}
            for i,part in enumerate(parts):
                ship=outgoing_lwss(part)
                if ship:
                    found[i]=[min(x for x,y in ship), min(y for x,y in ship),
                              max(x for x,y in ship),max(y for x,y in ship),
                              len(ship)]
            snapshots[g]=found
        if g<until:
            world=evolve(world)
            parts=[evolve(p) for p in parts]
    expected=set(range(ROW_COUNT)) if enabled is None else set(enabled)
    rows=snapshots[ASSEMBLED_G]
    if set(rows)!=expected:raise AssertionError(('unexpected output rows',rows))
    for i,b in rows.items():
        if b!=[-343,12+row_pitch*i,-339,15+row_pitch*i,12]:
            raise AssertionError(('unmatched output phase/position',i,b))
        next_b=snapshots[ASSEMBLED_G+100].get(i)
        if next_b!=[b[0]-50,b[1],b[2]-50,b[3],12]:
            raise AssertionError(('outgoing ship not c/2',i,next_b))
    return {'rule':'B3/S23','status':'finite native-Life qualification',
            'row_count':ROW_COUNT,'station_cells_each':len(STATION),
            'input_cells_each':len(INPUT),'row_pitch':row_pitch,
            'horizontal_step_per_row':x_step,
            'input_delay_per_row_generations':-2*x_step,
            'native_generations_checked':until,
            'whole_world_equals_independent_rows_at_each_tick':True,
            'aligned_output_generation':ASSEMBLED_G,
            'output_rows':{str(k):v for k,v in rows.items()},
            'final_population_at_replay_end':len(world),
            'corner_is_reusable':False,'cleanup_qualified':False,
            'complete_word_compacted':False}
