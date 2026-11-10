"""Three-state phrase gate INTENT from original native Life karaoke events.

Phrase START=MEDIUM; eligible source word onsets alternate MEDIUM/OPEN;
lyric LINE CLEAR=CLOSED. Lines without a physically meaningful break stay
in one phrase. Only real karaoke make/clear generations are used. This
compiler neither edits Life cells nor certifies the existing singer wiring.
"""
from __future__ import annotations
from dataclasses import dataclass,asdict
from pathlib import Path
from .word_driven_expression import score
from .full_song_karaoke import ALIGNMENT_FILE,GPS

STATES=('closed','medium','open')
DEFAULT_SWITCH_G=96

@dataclass(frozen=True)
class PhraseCue:
    generation:int
    state:str
    action:str
    source_kind:str
    source_line:int
    source_word:int|None
    text:str
    phrase:int

def phrase_groups(path=ALIGNMENT_FILE,*,min_switch_g=DEFAULT_SWITCH_G):
    """Do not close and reopen at adjacent line breaks under min_switch_g."""
    if min_switch_g<48 or min_switch_g%4:
        raise ValueError('min_switch_g must be a multiple of 4, at least 48')
    lines=score(path)
    if not lines:return ()
    groups=[];pending=[lines[0]]
    for previous,current in zip(lines,lines[1:]):
        if current.words[0].make_g-previous.clear_g<min_switch_g:
            pending.append(current)
        else:
            groups.append(tuple(pending));pending=[current]
    groups.append(tuple(pending))
    return tuple(groups)

def phrase_cues(path=ALIGNMENT_FILE,*,min_switch_g=DEFAULT_SWITCH_G):
    """Only source word MAKE / line CLEAR; no independent mouth clock.

    Min switch distance is necessary but NOT sufficient for native physical
    glider routing/clearance of the complete lip bank.
    """
    groups=phrase_groups(path,min_switch_g=min_switch_g)
    cues=[]
    for pi,group in enumerate(groups):
        words=sorted((w for line in group for w in line.words),
                     key=lambda w:(w.make_g,w.word_index))
        start=words[0];ending=max(group,key=lambda line:line.clear_g)
        if ending.clear_g-start.make_g<min_switch_g:
            raise ValueError('phrase too short for physical start+close')
        cues.append(PhraseCue(start.make_g,'medium','start','word_make',
                              group[0].line_index,start.word_index,start.text,pi))
        last=start.make_g;state='medium'
        for w in words[1:]:
            if w.make_g-last<min_switch_g:continue
            if ending.clear_g-w.make_g<min_switch_g:continue
            state='open' if state=='medium' else 'medium'
            owner=next(line.line_index for line in group if w in line.words)
            cues.append(PhraseCue(w.make_g,state,'alternate','word_make',
                                  owner,w.word_index,w.text,pi))
            last=w.make_g
        cues.append(PhraseCue(ending.clear_g,'closed','close','line_clear',
                              ending.line_index,None,ending.text,pi))
    if any(b.generation-a.generation<min_switch_g for a,b in zip(cues,cues[1:])):
        raise AssertionError('phrase gate contains rapid switches')
    if any(a.state==b.state for a,b in zip(cues,cues[1:])):
        raise AssertionError('no-op switch emitted')
    return tuple(cues)

def state_at(generation,path=ALIGNMENT_FILE,*,min_switch_g=DEFAULT_SWITCH_G):
    """Readout for gate tests, NOT a renderer expression mask."""
    if generation<0:raise ValueError('generation must be nonnegative')
    current='closed'
    for cue in phrase_cues(path,min_switch_g=min_switch_g):
        if cue.generation>generation:break
        current=cue.state
    return current

def audit(path=ALIGNMENT_FILE,*,min_switch_g=DEFAULT_SWITCH_G):
    lines=score(path)
    cues=phrase_cues(path,min_switch_g=min_switch_g)
    groups=phrase_groups(path,min_switch_g=min_switch_g)
    return {'gps':GPS,'source':Path(path).name,
            'karaoke_words':sum(len(l.words) for l in lines),
            'karaoke_lines':len(lines),'sung_phrases':len(groups),
            'phrase_starts':sum(c.action=='start' for c in cues),
            'medium_open_alternations':sum(c.action=='alternate' for c in cues),
            'phrase_closures':sum(c.action=='close' for c in cues),
            'total_mouth_transitions':len(cues),
            'min_switch_generations':min_switch_g,
            'smallest_actual_transition_gap_g':min((b.generation-a.generation for a,b in zip(cues,cues[1:])),default=None),
            'source_events_only':True,'independent_mouth_oscillator':False,
            'phonemization':False,'native_life_full_lip_gate_connected':False,
            'events':[asdict(c) for c in cues]}
