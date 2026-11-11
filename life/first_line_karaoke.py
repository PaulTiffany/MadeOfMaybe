"""Real glider-written FIRST SUNG LINE, text-only stage at fast global Life clock.

WE MADE A WINDOW OUT OF SAND is built word-by-word by native two-glider
synthesis of every 2x2 block, held through the line, and erased at its end.
All control gliders exist at generation zero in ONE B3/S23 universe.

We initially use deliberately enormous physical spacing (PITCH=1600) to
provide a rigorous separation certificate. The camera's optical magnification
is separate from the physical substrate; the final production compaction
problem is NOT solved by this intentionally spacious feasibility proof.
"""
from __future__ import annotations
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from .core import evolve,place
from .glider_controlled_mouth import BLOCK,block_make_at,block_erase_at
from .lyric_clock import nearest_phase
from .lyric_cues import read_alignment,aligned_words
from .lyric_font import GLYPHS

GPS=192
PITCH=1600  # > 2*647+2 cells of reaction-envelope width; conservative.
LINE_CLEAR_S=13.420
ERASE_GENERATION=nearest_phase(LINE_CLEAR_S,GPS,2) #2578
LYRICS='WE MADE A WINDOW OUT OF SAND'

@dataclass(frozen=True)
class Word:
    text:str
    start_s:float
    end_s:float
    make_g:int
    targets:tuple[tuple[int,int], ...] # physical target block ORIGINS


def _source_words():
    source=Path(__file__).resolve().parents[1]/'data'/'first_verse_alignment_fixture.json'
    first=aligned_words(read_alignment(source))[:7]
    assert ' '.join(x.text for x in first)==LYRICS
    return first


@lru_cache(maxsize=1)
def score()->tuple[Word,...]:
    out=[]; cursor=0; row_base=0
    for wi,w in enumerate(_source_words()):
        # Two real Life-cell text rows, not a renderer-only line break.
        if wi==4:
            cursor=0; row_base=10

        pts=[]
        for i,char in enumerate(w.text):
            for row,mask in enumerate(GLYPHS[char]):
                for col,bit in enumerate(mask):
                    if bit=='1':
                        pts.append(((6*(cursor+i)+col)*PITCH,(row_base+row)*PITCH))
        out.append(Word(w.text,w.start_s,w.end_s,
                        nearest_phase(w.start_s,GPS,0),tuple(pts)))
        cursor+=len(w.text)+1
    return tuple(out)


@lru_cache(maxsize=10)
def signal_template(make_g:int)->frozenset[tuple[int,int]]:
    return frozenset(block_make_at(make_g)|block_erase_at(ERASE_GENERATION))


def components()->dict[str,set[tuple[int,int]]]:
    return {f'{w.text}_{wi}_pixel_{p:03}':place(signal_template(w.make_g),x,y)
            for wi,w in enumerate(score()) for p,(x,y) in enumerate(w.targets)}


def universe()->set[tuple[int,int]]:
    return set().union(*components().values())


def target_blocks(word:Word)->tuple[set[tuple[int,int]],...]:
    return tuple(place(BLOCK,x,y) for x,y in word.targets)


def observed_words(world:set[tuple[int,int]])->dict[str,tuple[int,int]]:
    return {w.text:(sum(b<=world for b in target_blocks(w)),len(w.targets))
            for w in score()}


@lru_cache(maxsize=1)
def max_envelope_radius()->int:
    """Calculate exact maximum distance from a target over 7 native traces.

    All individual components have identical geometry modulo translations
    within one word. The measured radius + pitch separation mathematically
    certifies component independence throughout the finite lyric performance.
    """
    furthest=0
    for w in score():
        live=set(signal_template(w.make_g))
        for g in range(ERASE_GENERATION+1):
            if live:
                furthest=max(furthest,max(max(abs(x),abs(y)) for x,y in live))
            if g<ERASE_GENERATION:live=evolve(live)
        if live:raise AssertionError('one pixel left debris after line clear')
    return furthest


def separation_certificate()->dict:
    radius=max_envelope_radius()
    # Every target location differs from every other by at least PITCH in
    # at least one axis; each component stays within a radius-R square.
    points=[p for w in score() for p in w.targets]
    if len(points)!=len(set(points)):
        raise AssertionError('overlapping target cells')
    if PITCH-2*radius<=2:
        raise AssertionError('input glider trajectories can interact across pixels')
    return {'b3s23':'B3/S23','audio_gps':GPS,'physical_pitch':PITCH,
            'max_L_infty_footprint':radius,
            'minimum_guaranteed_cell_gap':PITCH-2*radius,
            'pixel_count':len(points),'word_count':len(score()),
            'all_gliders_present_at_generation_zero':True,
            'full_line_erase_generation':ERASE_GENERATION,
            'single_world_by_nonintersection':True}
