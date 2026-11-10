"""Native one-shot B3/S23 dual-input signal gate: real gliders, real output blocks.

WORD and VOCAL are independent physical five-cell input gliders. Each has
a separate constant-clock glider that creates a real stable indicator
block only when the input is present. At the third site, word and vocal
gliders collide directly: the output block is their TRUE native Life AND.
No software computed AND output is placed into the initial universe.

This qualifies a physical decision primitive. Reusable fanout, cleanup,
a clock generator, the 3-pose mouth actuator, and single-world singer
routing are NOT built here.
"""
from __future__ import annotations
from .core import evolve,place
from .glider_controlled_mouth import SYNTH_GLIDER_NW,SYNTH_GLIDER_SW,BLOCK

WORD_SITE=(-320,0)
VOCAL_SITE=(320,0)
BOTH_SITE=(0,300)
READ_GENERATION=124

def clock_and_input(time=READ_GENERATION, *, position=(0,0)):
    """Return the physical clock and input gliders for one clocked AND."""
    if time<4 or time%4:
        raise ValueError('output generation must be 4 mod 4')
    n=(time-4)//4
    x,y=position
    clock=place(SYNTH_GLIDER_NW,x+4+n,y+2+n)
    signal=place(SYNTH_GLIDER_SW,x+4+n,y+2-n)
    if clock&signal:raise AssertionError('source collision at g0')
    return frozenset(clock),frozenset(signal)

def world(word:bool,vocal:bool,*,time=READ_GENERATION):
    """Actual B3/S23 g0 pattern; all four independent source cases."""
    parts=[]
    for target,enable in ((WORD_SITE,word),(VOCAL_SITE,vocal)):
        clock,signal=clock_and_input(time,position=target)
        parts.append(set(clock))
        if enable:parts.append(set(signal))
    # Both indicator is a genuine two-input Life collision.
    # NEVER place an output conditional on computing word AND vocal here.
    a,b=clock_and_input(time,position=BOTH_SITE)
    if word:parts.append(set(a))
    if vocal:parts.append(set(b))
    seed=set().union(*parts)
    if sum(map(len,parts))!=len(seed):
        raise AssertionError('physical input tracks overlap at g0')
    return seed

def readout(cells):
    return tuple(place(BLOCK,*p)<=cells for p in
                 (WORD_SITE,VOCAL_SITE,BOTH_SITE))

def qualify(*,time=READ_GENERATION,postflight=100):
    """Check four source combinations through real native Life evolution."""
    cases=[]
    for word in (False,True):
        for vocal in (False,True):
            state=world(word,vocal,time=time)
            for _ in range(time):state=evolve(state)
            expected=(word,vocal,word and vocal)
            if readout(state)!=expected:
                raise AssertionError(f'wrong native truth table at {expected}')
            for _ in range(postflight):state=evolve(state)
            if readout(state)!=expected:
                raise AssertionError('output block did not persist')
            cases.append({'word':word,'vocal':vocal,
                          'native_output_blocks':readout(state)})
    return {'rule':'B3/S23','physical_two_glider_AND':True,
            'output_generation':time,'truth_table':cases,
            'lip_actuator_physically_connected':False,
            'physical_fanout':False,'repeatable_gate':False}
