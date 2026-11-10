"""Compact 35-corner native B3/S23 moving WE, geometrically staggered.

35 one-shot native LWSS turners spaced 36 cells apart, seven output
rows pitched 36 cells apart. At g6000 all output ships form a moving
word, at g7600 only the 77 stationary eaters remain. No camera glyphs.
"""
from __future__ import annotations
from dataclasses import dataclass,asdict
from pathlib import Path
import json
from .core import evolve,place
from .vertical_lwss_corner import STATION,INPUT
from .lyric_font import GLYPHS
from .export_operational import compact_rle
from .staggered_word_mesh import (
    EATER_NORTHEAST,EATER_SOUTHWEST,EATER_TEXT,
    reference_output,OUTPUT_REFERENCE_MIN_X,OUTPUT_REFERENCE_MIN_Y
)

WORD='WE'
STATION_PITCH=36
PIXEL_PITCH=36
STATION_X0=300
FORMATION_G=6000
CLEANUP_G=7600
TURN_REFERENCE_G=200

@dataclass(frozen=True)
class PixelRoute:
    ordinal:int
    column:int
    row:int
    station_x:int
    station_y:int
    source_delay_4gens:int
    output_reference_generation:int
    final_x:int
    final_y:int

def lit_pixels(word=WORD):
    out=[]
    for ci,char in enumerate(word.upper()):
        if char not in GLYPHS:
            raise ValueError(f'unsupported glyph {char!r}')
        for row,bits in enumerate(GLYPHS[char]):
            for col,v in enumerate(bits):
                if v=='1':out.append((6*ci+col,row))
    if not out:raise ValueError('no lit pixels')
    return tuple(out)

def routes(word=WORD,*,formation_g=FORMATION_G):
    if formation_g<TURN_REFERENCE_G or formation_g%4:
        raise ValueError('formation must be multiple of 4 >= 200')
    result=[]
    for i,(col,row) in enumerate(lit_pixels(word)):
        station_x=STATION_X0+STATION_PITCH*i
        station_y=PIXEL_PITCH*row
        final_x=1+PIXEL_PITCH*col
        final_y=OUTPUT_REFERENCE_MIN_Y+station_y
        numerator=final_x-station_x-OUTPUT_REFERENCE_MIN_X+(formation_g-TURN_REFERENCE_G)//2
        if numerator%2:raise ValueError(f'bad LWSS phase at pixel {i}')
        k=numerator//2
        if k<0 or TURN_REFERENCE_G+4*k>formation_g:
            raise ValueError(f'pixel {i} cannot reach reading line in time')
        result.append(PixelRoute(i,col,row,station_x,station_y,k,
                            TURN_REFERENCE_G+4*k,final_x,final_y))
    return tuple(result)

def catcher_bank():
    return set().union(*(place(EATER_TEXT,0,PIXEL_PITCH*r) for r in range(7)))

def fixed_eaters(rs=None):
    rs=routes() if rs is None else rs
    return (set().union(*(place(EATER_NORTHEAST,r.station_x,r.station_y)|
                          place(EATER_SOUTHWEST,r.station_x,r.station_y)
                          for r in rs))|catcher_bank())

def components(word=WORD,*,omit_index=None):
    rs=routes(word)
    if omit_index is not None and not 0<=omit_index<len(rs):
        raise ValueError('invalid ablation ordinal')
    parts=[]
    for r in rs:
        cells=(place(STATION,r.station_x,r.station_y)|
               place(EATER_NORTHEAST,r.station_x,r.station_y)|
               place(EATER_SOUTHWEST,r.station_x,r.station_y))
        if r.ordinal!=omit_index:
            cells|=place(INPUT,r.station_x,
                         r.station_y-2*r.source_delay_4gens)
        parts.append(cells)
    parts.append(catcher_bank())
    if len(set().union(*parts))!=sum(map(len,parts)):
        raise AssertionError('initial hardware overlaps')
    return tuple(parts)

def universe(word=WORD,*,omit_index=None):
    return set().union(*components(word,omit_index=omit_index))

def expected_word(word=WORD,*,omit_index=None):
    phase=reference_output()
    return set().union(*(place(phase,r.final_x-OUTPUT_REFERENCE_MIN_X,
                          r.final_y-OUTPUT_REFERENCE_MIN_Y)
                          for r in routes(word) if r.ordinal!=omit_index))

def expected_formation(word=WORD,*,omit_index=None):
    rs=routes(word)
    fixed=fixed_eaters(rs)
    if omit_index is not None:
        r=rs[omit_index]
        fixed|=place(STATION,r.station_x,r.station_y)
    return expected_word(word,omit_index=omit_index)|fixed

def expected_final(word=WORD,*,omit_index=None):
    rs=routes(word)
    fixed=fixed_eaters(rs)
    if omit_index is not None:
        r=rs[omit_index]
        fixed|=place(STATION,r.station_x,r.station_y)
    return fixed

def read_snapshot(path):
    with open(path,encoding='utf8') as f:
        return {tuple(map(int,l.split())) for l in f if l.strip()}

def verify_snapshots(formation,final,*,word=WORD,omit_index=None,cleanup_generation=CLEANUP_G):
    expected=expected_formation(word,omit_index=omit_index)
    rest=expected_final(word,omit_index=omit_index)
    if formation!=expected:
        raise AssertionError(f'g{FORMATION_G} moving word differs: {len(formation^expected)} wrong cells')
    if final!=rest:
        raise AssertionError(f'g{CLEANUP_G} cleanup differs: {len(final^rest)} wrong cells')
    if evolve(final)!=final:
        raise AssertionError('postcleanup world is not a still life')
    rs=routes(word)
    return {
      'rule':'B3/S23','word':word,'source_ablation':omit_index,
      'formation_generation':FORMATION_G,'cleanup_generation':cleanup_generation,
      'corners':len(rs),'vertical_inputs':len(rs)-(omit_index is not None),
      'outgoing_lwss_pixels':len(rs)-(omit_index is not None),
      'station_pitch_x':STATION_PITCH,'row_and_glyph_pitch':PIXEL_PITCH,
      'original_station_pitch_x':80,'original_glyph_pitch':64,
      'initial_population':len(universe(word,omit_index=omit_index)),
      'formation_population':len(formation),'cleanup_population':len(final),
      'all_moving_pixels_aligned_at_g6000':True,
      'all_outgoing_pixels_eaten_by_g7600':True,
      'intact_77_eaters_only':omit_index is None,
      'native_world_interference_gate':'C++ run checks every g<=6000',
      'corner_reused':False,'full_403_word_song_qualified':False,
    }

def export(folder,word=WORD,*,omit_index=None):
    folder=Path(folder);folder.mkdir(parents=True,exist_ok=True)
    base='compact_'+word.lower().replace(' ','_')
    slug=base if omit_index is None else f'{base}_ablate_{omit_index}'
    parts=components(word,omit_index=omit_index)
    rle=folder/(slug+'.rle')
    rle.write_text(compact_rle(set().union(*parts),(
        f'Native B3/S23 compact {len(routes(word))}-corner {word}, staged from above.',
        'All moving LWSS pixels meet at g6000 and are eaten by g7600.',
        'One-shot stations; no full-song or native switch claim.'
    )),encoding='utf8')
    tsv=folder/(slug+'_parts.tsv')
    with tsv.open('w',encoding='utf8') as f:
        f.write(f'{len(parts)}\n')
        for i,part in enumerate(parts):
            for x,y in sorted(part):
                f.write(f'{i} {x} {y}\n')
    (folder/(slug+'_routes.json')).write_text(
        json.dumps([asdict(r) for r in routes(word)],indent=2)+'\n',
        encoding='utf8')
    return rle,tsv

if __name__=='__main__':export('output/compact_full_word_mesh')
