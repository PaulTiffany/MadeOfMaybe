"""Native B3/S23 pilot: actual held-vocal jaw poses plus word lip accent.

Reuses the EXISTING physical glider synthesis/erase mouth. Every jaw make
is a two-glider coincidence: a constant clock glider and an independently
supplied VOCAL source glider. WORD independently gates a small lip accent.
No Life cells are introduced after g0; no cinematic pose substitutions.

Both sources are finite synthetic presence/absence fixtures, NOT yet the
extracted 238.88s Suno vocal envelope. This is NOT a reusable controller
or a causal connection to the full singer and rounded speech bubble.
"""
from __future__ import annotations
from .core import evolve,place
from .glider_controlled_mouth import (
    SYNTH_GLIDER_NW,SYNTH_GLIDER_SW,block_erase_at,rotate,ROUTING,
    BANK_SCHEDULES,MEDIUM_TARGETS,OPEN_TARGETS,BLOCK,UPPER_LIP
)
ATTACK_TARGET=(-120,200)
ATTACK_MAKE_DIRECTION=2
ATTACK_ERASE_DIRECTION=5
CHECKPOINTS=(60,180,288,420,540,680,778)
VOICE_POSE={60:'closed',180:'medium',288:'open',420:'medium',
            540:'closed',680:'open',778:'closed'}

def split_make(t,direction):
    """Split the original 10-cell synthesis into two REAL signal gliders."""
    if t<4 or t%4:raise ValueError('Life make generation must be 4 mod 4')
    n=(t-4)//4
    clock=rotate(place(SYNTH_GLIDER_NW,4+n,2+n),direction)
    signal=rotate(place(SYNTH_GLIDER_SW,4+n,2-n),direction)
    if clock&signal:raise AssertionError('source gliders overlap at g0')
    return clock,signal

def seed(word,vocal):
    """Physically conditional source packets; no Boolean output cell edits."""
    parts=[]
    for bank in ('medium','open'):
        targets=MEDIUM_TARGETS if bank=='medium' else OPEN_TARGETS
        for i,(x,y) in enumerate(targets):
            delay,make_direction,erase_direction=ROUTING[bank,i]
            for operation,t in BANK_SCHEDULES[bank]:
                if operation=='make':
                    clock,source=split_make(t+delay,make_direction)
                    parts.append(place(clock,x,y))
                    if vocal:parts.append(place(source,x,y))
                else:
                    parts.append(place(rotate(block_erase_at(t+delay),
                                              erase_direction),x,y))
    x,y=ATTACK_TARGET
    clock,source=split_make(124,ATTACK_MAKE_DIRECTION)
    parts.append(place(clock,x,y))
    if word:parts.append(place(source,x,y))
    parts.append(place(rotate(block_erase_at(246),
                              ATTACK_ERASE_DIRECTION),x,y))
    signals=set().union(*parts)
    if len(signals)!=sum(map(len,parts)) or signals&UPPER_LIP:
        raise AssertionError('initial glider/upper lip overlap')
    return signals|set(UPPER_LIP)

def state(cells):
    return {
        'medium':all(place(BLOCK,*p)<=cells for p in MEDIUM_TARGETS),
        'open':all(place(BLOCK,*p)<=cells for p in OPEN_TARGETS),
        'word_accent':place(BLOCK,*ATTACK_TARGET)<=cells,
    }

def qualify():
    report={}
    for word in (False,True):
        for vocal in (False,True):
            cells=seed(word,vocal)
            trace={}
            for g in range(785):
                if g in CHECKPOINTS:trace[g]=state(cells)
                if g<784:cells=evolve(cells)
            for g,pose in VOICE_POSE.items():
                observed=trace[g]
                if observed['medium']!=bool(vocal and pose=='medium'):
                    raise AssertionError((word,vocal,g,'medium',observed))
                if observed['open']!=bool(vocal and pose=='open'):
                    raise AssertionError((word,vocal,g,'open',observed))
                if observed['word_accent']!=bool(word and g==180):
                    raise AssertionError((word,vocal,g,'word',observed))
            report[f'{int(word)}{int(vocal)}']={
                'initial_population':len(seed(word,vocal)),
                'final_population':len(cells),
                'checkpoint_poses':trace,
            }
            if word and vocal and cells!=set(UPPER_LIP):
                raise AssertionError('full-input test left unwanted native cells')
    return {'rule':'B3/S23',
            'four_source_truth_table_cases':report,
            'real_four_pixel_medium_bank':True,
            'real_four_pixel_open_bank':True,
            'word_accent_is_real_physical_Life_block':True,
            'real_upper_lip_retained':True,
            'g540_vocal_sustain_gap_known':True,
            'whole_song_stem_embedded':False,
            'repeatable_priority_gate_qualified':False,
            'mouth_physically_integrated_with_singer':False}
