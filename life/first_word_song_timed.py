"""Song-timed first moving WE from compact native B3/S23 turning stations.

At 192 generations/second the first SUNO-aligned WE is at generation
2156. This stages all 35 existing independently verified physical LWSS
turners to form a moving WE at exactly that generation, using the SAME
36-cell station/glyph spacing as the g6000 full-word proof.
The seven shared text eaters consume the word by g3500. No renderer edits.
"""
from __future__ import annotations
from dataclasses import replace,asdict
from pathlib import Path
import json
from .core import evolve,place
from .vertical_lwss_corner import STATION,INPUT
from .export_operational import compact_rle
from .compact_full_word_mesh import (
    routes as base_routes,expected_word,expected_final as unused_final,
    fixed_eaters,catcher_bank,FORMATION_G as BASE_G,STATION_X0 as BASE_X,
    EATER_NORTHEAST,EATER_SOUTHWEST
)
from .full_song_karaoke import GPS

WORD='WE'
ONSET_G=2156
CLEARANCE_END_G=3500
STATION_X0=152
STATION_OFFSET_X=STATION_X0-BASE_X
DELAY_REDUCTION=(BASE_G-ONSET_G)//4+STATION_OFFSET_X//2

def routes():
    if (BASE_G-ONSET_G)%4 or STATION_OFFSET_X%2:
        raise AssertionError('phase offset is not c/2 compatible')
    rs=[]
    for r in base_routes(WORD):
        k=r.source_delay_4gens-DELAY_REDUCTION
        if k<0:raise AssertionError('song onset cannot be reached from g0')
        result=replace(r,station_x=r.station_x+STATION_OFFSET_X,
                       source_delay_4gens=k,
                       output_reference_generation=200+4*k)
        travel=(ONSET_G-result.output_reference_generation)//4
        if result.station_x-43-2*travel!=result.final_x:
            raise AssertionError('timed LWSS does not land on glyph')
        rs.append(result)
    return tuple(rs)

def components(*,omit_index=None):
    rs=routes()
    if omit_index is not None and not 0<=omit_index<len(rs):
        raise ValueError('bad source index')
    out=[]
    for r in rs:
        fixed=place(STATION,r.station_x,r.station_y)
        fixed|=place(EATER_NORTHEAST,r.station_x,r.station_y)
        fixed|=place(EATER_SOUTHWEST,r.station_x,r.station_y)
        if omit_index!=r.ordinal:
            fixed|=place(INPUT,r.station_x,r.station_y-2*r.source_delay_4gens)
        out.append(fixed)
    out.append(catcher_bank())
    if len(set().union(*out))!=sum(map(len,out)):
        raise AssertionError('first-word input hardware overlaps at g0')
    return tuple(out)

def universe(*,omit_index=None):
    return set().union(*components(omit_index=omit_index))

def final_eaters(*,omit_index=None):
    fixed=fixed_eaters(routes())
    if omit_index is not None:
        r=routes()[omit_index]
        fixed|=place(STATION,r.station_x,r.station_y)
    return fixed

def read_snapshot(path):
    with open(path,encoding='utf8') as f:
        return {tuple(map(int,line.split())) for line in f if line.strip()}

def verify_snapshots(onset,final,*,omit_index=None):
    word=expected_word(WORD,omit_index=omit_index)
    fixed=final_eaters(omit_index=omit_index)
    expected_pop=987 if omit_index is None else 994
    if len(onset)!=expected_pop or not word<=onset or len(word)!=(35-(omit_index is not None))*12:
        raise AssertionError('native g2156 WE did not assemble correctly')
    if omit_index is not None:
        missing=expected_word(WORD)-word
        if missing & onset:raise AssertionError('ablated pixel unexpectedly present')
    if len(onset-(word|fixed))!=28:
        raise AssertionError('unqualified transient corner byproduct')
    after=set(onset)
    for _ in range(24):after=evolve(after)
    if not place(word,-12,0)<=after:
        raise AssertionError('complete word failed to crawl at native c/2')
    if final!=fixed or evolve(final)!=final:
        raise AssertionError('source hardware/eaters not fully reset')
    return {'rule':'B3/S23','word':WORD,'gps':GPS,
            'song_first_word_onset_g':ONSET_G,
            'song_first_word_onset_seconds':round(ONSET_G/GPS,6),
            'native_cleanup_g':CLEARANCE_END_G,
            'vertical_sources':35-(omit_index is not None),
            'one_shot_turners':35,'output_lwss_pixels':35-(omit_index is not None),
            'input_ablation_index':omit_index,
            'initial_population':len(universe(omit_index=omit_index)),
            'onset_population':len(onset),'final_population':len(final),
            'all_outputs_at_suno_generation':True,
            'moving_c2_evolution_verified_through_generation':ONSET_G+24,
            'exact_no_ash_native_cleanup':True,
            'independent_components_until_onset':'checked by native C++ qualification',
            'full_song_connected':False,'mouth_physically_connected':False}

def export(directory,*,omit_index=None):
    directory=Path(directory);directory.mkdir(parents=True,exist_ok=True)
    name='suno_first_we' if omit_index is None else f'suno_first_we_ablate_{omit_index}'
    parts=components(omit_index=omit_index)
    world=set().union(*parts)
    (directory/(name+'.rle')).write_text(compact_rle(world,(
        'Song-timed WE: native 35 LWSS corners, target g2156 (11.229s @192 GPS).',
        'All source gliders preloaded; whole word moves and is eaten by g3500.',
        'Separate from singer; no complete song lip/highlight link yet.'
    )),encoding='utf8')
    with (directory/(name+'_parts.tsv')).open('w',encoding='utf8') as f:
        f.write(f'{len(parts)}\n')
        for i,part in enumerate(parts):
            for x,y in sorted(part):f.write(f'{i} {x} {y}\n')
    (directory/(name+'_routes.json')).write_text(
        json.dumps([asdict(r) for r in routes()],indent=2)+'\n')
    return world

if __name__=='__main__':export('output/song_timed_moving_we')
