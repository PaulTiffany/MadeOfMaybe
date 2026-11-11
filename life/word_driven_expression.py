"""Single-source, full-song 3-state mouth INTENT derived from native lyric cues.

The compiler does NOT inject Life cells. It supplies a source-linked control
score to the future physical glider-router. It deliberately does not claim that
these 403 word signals have all been routed through the character or that
8-tick changes are attainable by the existing 40-element mouth.

Two independent facts are preserved: every event is exactly a real lyric MAKE
or line ERASE generation, and its destination is one of CLOSED/MEDIUM/OPEN.
No phonemization, derived vocal pitch, secondary music clock, or arbitrary
waveform-driven lip edits are present.
"""
from __future__ import annotations
from dataclasses import dataclass,asdict
from functools import lru_cache
from .full_song_karaoke import ALIGNMENT_FILE,GPS,compile_plan
from .lyric_cues import read_alignment

STATES=('closed','medium','open')
# Every first word of a line engages MEDIUM. The remaining words alternate
# MEDIUM/OPEN, giving a legible expression target without phonemization.
# Physical hardware remains subject to a separate response/clearance gate.

@dataclass(frozen=True)
class MouthCue:
    generation:int
    state:str
    cause:str
    line_index:int
    word_index:int|None
    source_text:str

@lru_cache(maxsize=1)
def score(path=ALIGNMENT_FILE):
    return compile_plan(read_alignment(path))

@lru_cache(maxsize=1)
def source_cues(path=ALIGNMENT_FILE):
    cues=[]
    for line in score(path):
        for wi,w in enumerate(line.words):
            state='medium' if wi%2==0 else 'open'
            cues.append(MouthCue(w.make_g,state,'word_make',line.line_index,
                                 w.word_index,w.text))
        cues.append(MouthCue(line.clear_g,'closed','line_clear',line.line_index,
                             None,line.text))
    # Stable ordering: at coincident ticks, line_clear wins over word onset,
    # but next line's onset takes precedence if same-generation.
    return tuple(sorted(cues,key=lambda c:(c.generation,c.line_index,
                   0 if c.cause=='line_clear' else 1)))

def qualified_intent(path=ALIGNMENT_FILE):
    """Filter no-op repeats; retain every source cue in source_cues()."""
    out=[];current='closed'
    for cue in source_cues(path):
        if cue.state!=current:
            out.append(cue)
            current=cue.state
    return tuple(out)

def rate_limited_candidate(path=ALIGNMENT_FILE, *, min_spacing_g=48):
    """Event-only thinning proposal for a bounded-response physical router.

    This **does not certify** 40 physical lip elements. It merely omits state
    changes that would require less than min_spacing_g Life generations. No
    artificial delayed events are invented: outputs are a strict ordered
    subset of actual karaoke onset/clear events. A physically qualified mouth
    compiler must still prove its individual glider routes and reset behavior.
    """
    if min_spacing_g<0 or min_spacing_g%4:
        raise ValueError('minimum candidate response must be nonnegative, multiple of 4')
    out=[];current='closed'
    for cue in source_cues(path):
        if cue.state==current:continue
        if out and cue.generation-out[-1].generation<min_spacing_g:continue
        out.append(cue);current=cue.state
    return tuple(out)


def audit(path=ALIGNMENT_FILE):
    raw=source_cues(path); changed=qualified_intent(path)
    feasible_candidate=rate_limited_candidate(path)
    gaps=[b.generation-a.generation for a,b in zip(changed,changed[1:])]
    return {
      'gps':GPS,'source_alignment_file':path.name,'word_events':sum(x.cause=='word_make' for x in raw),
      'line_clear_events':sum(x.cause=='line_clear' for x in raw),
      'state_changes_requested':len(changed),
      'smallest_change_gap_generations':min(gaps) if gaps else None,
      'gaps_under_22_generations':sum(g<22 for g in gaps),
      'gaps_under_48_generations':sum(g<48 for g in gaps),
      'rate_limited_proposed_changes':len(feasible_candidate),
      'rate_limited_minimum_spacing_generations':48,
      'rate_limited_cues':[asdict(c) for c in feasible_candidate],
      'rate_limited_physical_hardware_certified':False,
      'word_source_only':True,'phonemization':False,
      'physical_full_lip_wiring_verified':False,
      'all_cues': [asdict(c) for c in changed]
    }
