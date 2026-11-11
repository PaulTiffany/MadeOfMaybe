"""Compile every aligned lyric into ONE preloaded Conway Life (B3/S23) universe.

The song audio is fixed. The entire cellular universe evolves at one fixed
192 generations per audio second. Every visible letter-pixel is a 2x2 block
constructed by two initially placed gliders and erased by a third glider.

Each SUNG LINE has a separate physical stage, and a camera follows the stage.
No runtime cell edits, words imposed by renderer, or changing global tick rate.

This intentionally favors a certifiable sparse layout over compact geometry.
The gigantic RLE coordinates require Hashlife/Golly; DO NOT use the naive
per-cell RLE encoder from core.py or try to render the entire world as pixels.
"""
from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP
from functools import lru_cache
from itertools import groupby
from math import ceil
from pathlib import Path
from typing import Iterable, Iterator

from .glider_controlled_mouth import BLOCK, block_make_at, block_erase_at
from .lyric_clock import nearest_phase
from .lyric_cues import LyricWord, aligned_words, read_alignment
from .lyric_font import GLYPHS
from .core import place

GPS = 192
# Conservative opening and closing separation. Some last tokens are only ~70ms.
MIN_HOLD_GENERATIONS = 42
# Margin includes all three gliders and intermediate collision shapes.
ENVELOPE_MARGIN = 24
SPACE_MARGIN = 12
ALIGNMENT_FILE = Path(__file__).resolve().parents[1] / 'data' / 'made_of_maybe_suno_alignment.json'


@dataclass(frozen=True)
class WordPlan:
    word_index: int
    text: str
    start_s: float
    end_s: float
    make_g: int
    source_tokens: tuple[int, ...]
    flagged: bool
    char_start: int
    pixel_count: int


@dataclass(frozen=True)
class LinePlan:
    line_index: int
    source_line: int
    section: str
    text: str
    start_s: float
    end_s: float
    clear_g: int
    radius: int
    pitch: int
    y_origin: int
    glyph_columns: int
    pixel_count: int
    words: tuple[WordPlan, ...]

    @property
    def box(self) -> tuple[int, int, int, int]:
        """Guaranteed (conditional on primitive-envelope) footprint: minx,miny,maxx,maxy."""
        return (-self.radius, self.y_origin-self.radius,
                self.glyph_columns*self.pitch+self.radius,
                self.y_origin+6*self.pitch+self.radius)

    @property
    def word_makes(self) -> dict[int, int]:
        return {w.word_index:w.make_g for w in self.words}


def _phase_at_or_after(g: int, residue: int) -> int:
    return g + (residue - g) % 4


def glyph_pixels(text: str) -> tuple[tuple[int,int], ...]:
    """Return one set of logical text pixels without any simulated overlay."""
    pixels = []
    for ci, ch in enumerate(text):
        try:
            glyph = GLYPHS[ch]
        except KeyError as exc:
            raise ValueError(f'unsupported lyric glyph {ch!r} in {text!r}') from exc
        for row, mask in enumerate(glyph):
            for column, bit in enumerate(mask):
                if bit == '1':
                    pixels.append((ci*6+column, row))
    return tuple(pixels)


def lyric_lines(words: Iterable[LyricWord]) -> list[tuple[LyricWord, ...]]:
    """Keep Suno's actual printed line breaks; no dropped sung words."""
    return [tuple(group) for _, group in groupby(words, key=lambda w: w.line)]


def compile_plan(raw: dict, gps: int = GPS) -> tuple[LinePlan, ...]:
    if gps <= 0 or gps % 4:
        raise ValueError('constant generation rate must be positive and divisible by 4')
    words = aligned_words(raw)
    if not words:
        raise ValueError('full alignment has no sung words')
    result = []
    next_origin_y = 0
    previous_bottom = None
    global_word_idx = 0
    for line_num, group in enumerate(lyric_lines(words)):
        text = ' '.join(w.text for w in group)
        pixel_count = len(glyph_pixels(text))
        starts = [nearest_phase(w.start_s,gps,0) for w in group]
        source_end=max(w.end_s for w in group)
        clear_g = _phase_at_or_after(max(nearest_phase(source_end,gps,2),
                                          max(starts)+MIN_HOLD_GENERATIONS), 2)
        # Every seed glider lies in a square with radius ~ g/4+O(1) around
        # its target. We deliberately use a larger *conservative* bound.
        r=ceil(clear_g/4)+ENVELOPE_MARGIN
        pitch=2*r+SPACE_MARGIN
        if previous_bottom is not None:
            next_origin_y=previous_bottom + r + SPACE_MARGIN
        offset=0
        subwords=[]
        for w,start_g in zip(group,starts):
            subwords.append(WordPlan(global_word_idx,w.text,w.start_s,w.end_s,
                                     start_g,w.source_tokens,w.flagged,offset,
                                     len(glyph_pixels(w.text))))
            global_word_idx+=1
            offset+=len(w.text)+1
        plan=LinePlan(line_num,group[0].line,group[0].section,text,
                     group[0].start_s,source_end,clear_g,r,pitch,
                     next_origin_y,6*len(text),pixel_count,tuple(subwords))
        result.append(plan)
        previous_bottom=plan.box[3]
    validate_layout(result)
    return tuple(result)


def validate_layout(lines: Iterable[LinePlan]) -> None:
    lines=tuple(lines)
    for line in lines:
        if line.pitch - 2*line.radius < 3:
            raise AssertionError('not enough pixel spacing')
        if line.clear_g <= max(w.make_g for w in line.words)+24:
            raise AssertionError('not enough hold before the clear glider')
        if sum(w.pixel_count for w in line.words)!=line.pixel_count:
            raise AssertionError('glyph pixel counts disagree')
    for a,b in zip(lines,lines[1:]):
        if b.box[1]-a.box[3] <= 2:
            raise AssertionError('separate song-line stages could interact')


@lru_cache(maxsize=1024)
def pixel_seed(make_g: int, erase_g: int) -> frozenset[tuple[int,int]]:
    """Two phased MAKE gliders and one clean ERASE glider, all at generation 0."""
    return frozenset(block_make_at(make_g)|block_erase_at(erase_g))


def physical_targets(line: LinePlan, word: WordPlan) -> Iterator[tuple[int,int]]:
    for ci,char in enumerate(word.text):
        glyph=GLYPHS[char]
        for row,mask in enumerate(glyph):
            for col,lit in enumerate(mask):
                if lit=='1':
                    yield ((word.char_start+ci)*6*line.pitch+col*line.pitch,
                           line.y_origin+row*line.pitch)


def seeded_lines(lines: Iterable[LinePlan]) -> Iterator[tuple[int, int]]:
    """Generate all glider cells without allocating the entire universe twice."""
    for line in lines:
        for word in line.words:
            gliders=pixel_seed(word.make_g,line.clear_g)
            for x,y in physical_targets(line,word):
                for gx,gy in gliders:
                    yield (x+gx,y+gy)


def stats(lines: Iterable[LinePlan]) -> dict:
    lines=tuple(lines)
    words=[w for l in lines for w in l.words]
    return {'song':'Made of Maybe','audio_duration_s':238.88,'rule':'B3/S23','gps':GPS,
            'line_count':len(lines),'word_count':len(words),
            'source_token_count':len({i for w in words for i in w.source_tokens}),
            'glider_controlled_pixels':sum(l.pixel_count for l in lines),
            'glider_count':3*sum(l.pixel_count for l in lines),
            'seed_cell_count':15*sum(l.pixel_count for l in lines),
            'flagged_merged_words':sum(w.flagged for w in words),
            'worst_word_onset_error_ms':round(max(abs(w.make_g/GPS-w.start_s)
               for w in words)*1000,3),
            'worst_line_clear_error_ms':round(max(abs(l.clear_g/GPS-l.end_s)
               for l in lines)*1000,3),
            'last_event_generation':max(l.clear_g for l in lines),
            'separation':'Conservative nonoverlapping axis-aligned event envelopes; conditioned on primitive flight bounds',
            'runtime_cell_edits':False,'camera_switching_native_life':False,
            'audio_tempo_unchanged':True,'frame_swapped_lyrics':False}


def manifest(lines: Iterable[LinePlan]) -> dict:
    lines=tuple(lines)
    return {'stats':stats(lines),'source':str(ALIGNMENT_FILE.name),
      'lines':[
       {'line':p.line_index,'source_line':p.source_line,'section':p.section,
        'text':p.text,'start_s':p.start_s,'end_s':p.end_s,
        'erase_s':round(p.clear_g/GPS,4),'clear_g':p.clear_g,
        'bbox':p.box,'pitch':p.pitch,'radius':p.radius,
        'camera_target':{'x0':0,'y0':p.y_origin,
                         'width_columns':p.glyph_columns,'height_rows':7,
                         'pixel_pitch':p.pitch},
        'pixel_count':p.pixel_count,
        'words':[
         {'index':w.word_index,'text':w.text,'start_s':w.start_s,'end_s':w.end_s,
          'make_g':w.make_g,'real_start_s':round(w.make_g/GPS,4),
          'pixel_count':w.pixel_count,'start_char':w.char_start,
          'source_tokens':list(w.source_tokens),'alignment_flagged':w.flagged}
         for w in p.words]}
       for p in lines]}


def local_line_seed(line: LinePlan) -> set[tuple[int,int]]:
    """A complete independently runnable line, for bounded pilot tests."""
    return set(seeded_lines([line]))


def real_word_count(world:set[tuple[int,int]],line:LinePlan,word:WordPlan) -> int:
    """Count actual 2x2 Life still-lifes, not calculated animation frames."""
    return sum(place(BLOCK,x,y)<=world for x,y in physical_targets(line,word))

# Proof-checkable glider fast-forward for the complete 4-minute performance.
# We verify an initially seeded GLIDER TRIPLE, not a renderer animation.
# Each individual glider has c/4 diagonal movement under B3/S23. For the
# certified isolated-flight prefix, replace four actual timesteps with one
# unit translation, checking its 4 successive cell phases for crosstalk.
from .glider_controlled_mouth import (SYNTH_GLIDER_NW, SYNTH_GLIDER_SW,
                                       INPUT_GLIDER)
from .core import evolve

_GLIDERS=(SYNTH_GLIDER_NW,SYNTH_GLIDER_SW,INPUT_GLIDER)
_VELOCITY=((-1,-1),(-1,1),(1,1))

@lru_cache(maxsize=1)
def _glider_phases():
    all_phases=[]
    for base,vel in zip(_GLIDERS,_VELOCITY):
        shapes=[set(base)]
        for _ in range(3):shapes.append(evolve(shapes[-1]))
        if evolve(shapes[-1])!=place(set(base),*vel):
            raise AssertionError('assumed glider c/4 velocity failed')
        all_phases.append(tuple(tuple(sorted(s)) for s in shapes))
    return tuple(all_phases)


def _glider_origin(make_g:int,erase_g:int)->tuple[tuple[int,int],...]:
    nm=(make_g-4)//4;ne=(erase_g-22)//4
    return ((4+nm,2+nm),(4+nm,2-nm),(-8-ne,-8-ne))


def isolated_triple(make_g:int,erase_g:int,g:int) -> tuple[set[tuple[int,int]],...]:
    """Three exact Life glider states at g, provided no earlier interaction."""
    k,r=divmod(g,4)
    positions=_glider_origin(make_g,erase_g)
    shapes=_glider_phases()
    return tuple({(x+orig[0]+vel[0]*k,y+orig[1]+vel[1]*k)
        for x,y in shapes[i][r]} for i,(orig,vel) in enumerate(zip(positions,_VELOCITY)))


def _strictly_disjoint_neighborhood(a,b) -> bool:
    ax0=min(x for x,y in a);ax1=max(x for x,y in a)
    ay0=min(y for x,y in a);ay1=max(y for x,y in a)
    bx0=min(x for x,y in b);bx1=max(x for x,y in b)
    by0=min(y for x,y in b);by1=max(y for x,y in b)
    return ax1+2<bx0 or bx1+2<ax0 or ay1+2<by0 or by1+2<ay0


def verify_native_packet(make_g:int,erase_g:int, *, verify_prefix:bool=True) -> dict:
    """Inductively certify isolated flight and exactly simulate both reactions.

    Tests ALL four Life phases of all three gliders, every generation before
    the final 40 generations before construction. During that phase the three
    gliders are separated (Moore neighborhoods do not overlap); by induction
    their independent c/4 phase positions are identical to the global world.
    The remaining generations, including both collisions and held block,
    are evolved with *actual* B3/S23. Nothing gets placed at runtime.
    """
    if make_g%4 or erase_g%4!=2 or erase_g-make_g<MIN_HOLD_GENERATIONS:
        raise ValueError('invalid construction / erasure schedule')
    cutoff=max(0,make_g-40)
    cutoff-=cutoff%4
    if verify_prefix:
        # Bounding boxes of 5-cell gliders; entirely sufficient separation.
        for g in range(0,cutoff):
            trio=isolated_triple(make_g,erase_g,g)
            if any(not _strictly_disjoint_neighborhood(trio[i],trio[j])
                   for i,j in ((0,1),(0,2),(1,2))):
                raise AssertionError(f'early glider interaction at g={g} for {make_g},{erase_g}')
    trio=isolated_triple(make_g,erase_g,cutoff)
    world=set().union(*trio)
    # Compare against true seed exactly at cutoff for short preflights.
    if cutoff==0 and world!=set(pixel_seed(make_g,erase_g)):
        raise AssertionError('glider phase decomposition invalid')
    first_seen=None
    max_radius=0
    for g in range(cutoff,erase_g+1):
        if world:
            max_radius=max(max_radius,max(max(abs(x),abs(y)) for x,y in world))
        if g==make_g:
            if not BLOCK<=world:
                raise AssertionError(f'block failed to appear at g{g}')
            first_seen=g
        if make_g+4 <= g < erase_g-16 and not BLOCK<=world:
            raise AssertionError(f'block failed to hold from MAKE until ERASE: g{g}')
        if g==erase_g and world:
            raise AssertionError(f'erasure left {len(world)} debris cells at g{g}')
        if g<erase_g:world=evolve(world)
    return {'make_g':make_g,'erase_g':erase_g,'preflight_g':cutoff,
            'appeared_g':first_seen,'final_population':len(world),
            'near_collision_max_abs_coordinate':max_radius}
