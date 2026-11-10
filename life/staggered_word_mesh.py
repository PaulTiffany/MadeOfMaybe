"""Native B3/S23 staggered mesh: vertical LWSS -> leftgoing moving WE -> eaters.

35 independently timed one-shot right-angle turners form all 35 lit 5x7
letter pixels at generation 6000. Two glider eaters accompany each corner;
seven shared row eaters consume the complete moving word by generation 7600.
No runtime insertion, optical glyph swapping or additional music clock.
The 35 one-shot turners are consumed and NOT reusable yet.
"""
from __future__ import annotations
from dataclasses import dataclass,asdict
from functools import lru_cache
from pathlib import Path
import json
from .core import place,evolve
from .export_operational import compact_rle
from .lyric_font import GLYPHS
from .vertical_lwss_corner import STATION,INPUT,outgoing_lwss

WORD='WE'
PIXEL_PITCH=64
STATION_PITCH=80
STATION_X0=300
FORMATION_G=6000
CLEANUP_G=7600
TURN_REFERENCE_G=200
OUTPUT_REFERENCE_MIN_X=-43
OUTPUT_REFERENCE_MIN_Y=12

# Actual stable eater-1s verified against all native corner byproducts.
EATER_NORTHEAST=frozenset({(-12,-7),(-12,-6),(-11,-8),(-11,-6),
                           (-10,-8),(-9,-9),(-9,-8)})
EATER_SOUTHWEST=frozenset({(-79,69),(-79,70),(-78,69),(-77,67),
                           (-77,69),(-76,67),(-76,68)})
EATER_TEXT=frozenset({(-57,8),(-56,8),(-56,9),(-56,10),
                      (-55,11),(-54,10),(-54,11)})

@dataclass(frozen=True)
class PixelRoute:
    ordinal:int
    column:int
    row:int
    station_x:int
    station_y:int
    incoming_delay_4gens:int
    output_ref_arrives_at_g:int
    assembled_x:int
    assembled_y:int

def lit_pixels(word=WORD):
    result=[]
    for i,char in enumerate(word.upper()):
        if char not in GLYPHS:
            raise ValueError(f'unsupported letter {char!r}')
        for row,mask in enumerate(GLYPHS[char]):
            for col,bit in enumerate(mask):
                if bit=='1':
                    result.append((6*i+col,row))
    if not result:
        raise ValueError('word needs at least one lit pixel')
    return tuple(result)

def routes(word=WORD,*,formation_g=FORMATION_G):
    if formation_g<200 or formation_g%4:
        raise ValueError('formation_g must be multiple of four >=200')
    result=[]
    for i,(col,row) in enumerate(lit_pixels(word)):
        X=STATION_X0+STATION_PITCH*i
        Y=PIXEL_PITCH*row
        target_x=1+PIXEL_PITCH*col
        target_y=OUTPUT_REFERENCE_MIN_Y+Y
        # x_final = X -43 - (T-200-4k)/2
        numerator=target_x-X-OUTPUT_REFERENCE_MIN_X+(formation_g-200)//2
        if numerator%2:
            raise AssertionError('cannot phase-match 4-gen LWSS')
        k=numerator//2
        if k<0 or formation_g<TURN_REFERENCE_G+4*k:
            raise ValueError('unreachable output deadline')
        result.append(PixelRoute(i,col,row,X,Y,k,
                                 TURN_REFERENCE_G+4*k,target_x,target_y))
    return tuple(result)

def catcher_bank():
    return set().union(*(place(EATER_TEXT,0,PIXEL_PITCH*r) for r in range(7)))

def persistent_eaters(route_set=None):
    route_set=routes() if route_set is None else route_set
    return (set().union(*(place(EATER_NORTHEAST,r.station_x,r.station_y)|
                          place(EATER_SOUTHWEST,r.station_x,r.station_y)
                          for r in route_set))|catcher_bank())

def component_seed(route,*,include_source=True):
    fixed=place(STATION,route.station_x,route.station_y)
    eaters=(place(EATER_NORTHEAST,route.station_x,route.station_y)|
            place(EATER_SOUTHWEST,route.station_x,route.station_y))
    if not include_source:
        return fixed|eaters
    source=place(INPUT,route.station_x,
                 route.station_y-2*route.incoming_delay_4gens)
    return fixed|eaters|source

def components(word=WORD,*,omit_index=None):
    rs=routes(word)
    if omit_index is not None and not(0<=omit_index<len(rs)):
        raise ValueError('invalid source-ablation index')
    parts=[component_seed(r,include_source=(r.ordinal!=omit_index)) for r in rs]
    parts.append(catcher_bank())
    if len(set().union(*parts))!=sum(map(len,parts)):
        raise AssertionError('initial hardware overlaps')
    return tuple(parts)

def universe(word=WORD,*,omit_index=None):
    return set().union(*components(word,omit_index=omit_index))

@lru_cache(maxsize=1)
def reference_output():
    live=set(STATION|INPUT)
    for _ in range(TURN_REFERENCE_G):
        live=evolve(live)
    output=outgoing_lwss(live)
    if output is None or len(output)!=12:
        raise AssertionError('missing native turned LWSS 12-cell phase')
    if (min(x for x,y in output),min(y for x,y in output))!=(-43,12):
        raise AssertionError('reference LWSS phase changed')
    return frozenset(output)

def expected_word_at_formation(word=WORD,*,omit_index=None):
    cells=set()
    for route in routes(word):
        if route.ordinal!=omit_index:
            cells|=place(reference_output(),
                         route.assembled_x-OUTPUT_REFERENCE_MIN_X,
                         route.assembled_y-OUTPUT_REFERENCE_MIN_Y)
    return cells

def expected_formation_world(word=WORD,*,omit_index=None):
    cells=expected_word_at_formation(word,omit_index=omit_index)|persistent_eaters(routes(word))
    if omit_index is not None:
        r=routes(word)[omit_index]
        cells|=place(STATION,r.station_x,r.station_y)
    return cells

def verify_snapshots(snapshot,last,word=WORD,*,omit_index=None):
    expected=expected_formation_world(word,omit_index=omit_index)
    if set(snapshot)!=expected:
        raise AssertionError(f'formation mismatch: {len(set(snapshot)^expected)} cells')
    fixed=persistent_eaters(routes(word))
    if omit_index is not None:
        r=routes(word)[omit_index]
        fixed|=place(STATION,r.station_x,r.station_y)
    if set(last)!=fixed:
        raise AssertionError(f'cleanup left debris: {len(set(last)^fixed)} cells')
    if evolve(set(last))!=set(last):
        raise AssertionError('cleanup world is not stationary')
    return {'rule':'B3/S23','word':word,'source_ablation':omit_index,
            'formation_g':FORMATION_G,'cleanup_g':CLEANUP_G,
            'one_shot_turners':len(routes(word)),
            'vertical_source_ships':len(routes(word))-(omit_index is not None),
            'moving_glyph_spaceships':len(lit_pixels(word))-(omit_index is not None),
            'reusable_side_glider_eaters':2*len(routes(word)),
            'shared_row_eaters':7,'initial_population':len(universe(word,omit_index=omit_index)),
            'formation_population':len(snapshot),'final_population':len(last),
            'all_word_pixels_exact_at_generation_6000':True,
            'all_output_ships_eaten_by_generation_7600':True,
            'whole_world_ends_in_exact_stationary_eaters':True,
            'turners_reusable':False,'full_song_implemented':False}

def read_seed_file(path):
    with open(path) as f:
        return {tuple(map(int,l.split())) for l in f if l.strip()}

def export(directory,word=WORD,*,omit_index=None):
    directory=Path(directory);directory.mkdir(parents=True,exist_ok=True)
    parts=components(word,omit_index=omit_index)
    slug=word.lower().replace(' ','_')+('_ablate_'+str(omit_index) if omit_index is not None else '')
    pat=directory/(slug+'_mesh.rle')
    pat.write_text(compact_rle(set().union(*parts),(
        'Geometrically staggered vertical LWSS turners form WE at g6000.',
        '35 actual corners, 70 diagonal eaters, 7 shared row eaters.',
        'All moving text is eaten by g7600. All source ships preloaded.'
    )),encoding='utf-8')
    tsv=directory/(slug+'_components.tsv')
    with tsv.open('w') as f:
        f.write(str(len(parts))+'\n')
        for i,part in enumerate(parts):
            for x,y in sorted(part):f.write(f'{i} {x} {y}\n')
    (directory/(slug+'_routes.json')).write_text(json.dumps([asdict(r) for r in routes(word)],indent=2)+'\n')
    return pat,tsv

if __name__=='__main__':
    print(export('output/staggered_word_mesh'))
