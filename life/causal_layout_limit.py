"""Necessary B3/S23 light-cone bounds for one glider cue and fixed singer.

A *single localized input glider at g0* can only influence positions inside a
radius-g square by native generation g (Life causal speed <= 1 cell/g).
Therefore two events at positions A and B and times gA,gB cannot have one
localized g0 source if their Chebyshev distance exceeds gA+gB. At glider
transport speeds <= c/4, the operational bound is even stricter, but the
native cellular speed-of-light bound suffices for a rigorous impossibility.

This says nothing about distributed initial conditions, additional local
singers, phase-shifted preloaded sources, or a redesigned compact lyric stage.
"""
from __future__ import annotations
from dataclasses import dataclass,asdict
from pathlib import Path
from .full_song_karaoke import ALIGNMENT_FILE,compile_plan,physical_targets
from .lyric_cues import read_alignment
from .physical_lip_splitter_bridge import LIP_TARGET,SINGER_TRANSLATION


@dataclass(frozen=True)
class ConeCheck:
    line_index:int
    word:str
    first_glyph_target:tuple[int,int]
    lip_target:tuple[int,int]
    word_generation:int
    assumed_lip_generation:int
    distance_L_infty:int
    maximum_life_cone_sum:int
    single_g0_source_causally_possible:bool


def audit(path:Path=ALIGNMENT_FILE,*,lip_xy=None):
    if lip_xy is None:
        lip_xy=(LIP_TARGET[0]+SINGER_TRANSLATION[0],
                LIP_TARGET[1]+SINGER_TRANSLATION[1])
    lines=compile_plan(read_alignment(path))
    checks=[]
    for line in lines:
        word=line.words[0]
        target=next(physical_targets(line,word))
        gap=max(abs(target[0]-lip_xy[0]),abs(target[1]-lip_xy[1]))
        # Assume the lip changes at the onset: optimistic upper bound.
        limit=word.make_g+word.make_g
        checks.append(ConeCheck(line.line_index,word.text,target,lip_xy,
                                word.make_g,word.make_g,gap,limit,gap<=limit))
    return checks


def report(path:Path=ALIGNMENT_FILE):
    checks=audit(path)
    return {'source_alignment':path.name,'rule':'B3/S23',
      'scope':'ONE localized source at generation zero / ONE unchanged fixed actor',
      'word_line_count':len(checks),
      'lines_exceeding_absolute_causality_bound':sum(not c.single_g0_source_causally_possible for c in checks),
      'first_two_lines':[asdict(x) for x in checks[:2]],
      'implication':'Sparse remote lyric stages cannot share one glider source with an unchanged fixed actor at their aligned times; compact or distributed layout required.',
      'does_not_refute':'Independent distributed preloaded scores, physically replicated actors near stages, or redesigned delayed compact routing.'}
