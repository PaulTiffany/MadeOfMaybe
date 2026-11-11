"""Physical native B3/S23 W+V at an actual corner of the singer's mouth.

W originates in a companion word-marker LWSS travelling down through
the SAME existing 19-cell 90-degree turner as our lyric glyphs. The turn
emits a real southwest-going glider. The V glider is independently
timed from the Suno-isolated vocal envelope. Their native collision
forms a four-cell 2x2 block at the mouth corner at generation 2156.

The 35 WE glyph LWSS turners, vocal-glider jaw banks, singer and rounded
bubble all coexist in this same generation-zero universe. The marker is
an extra word lane, NOT a splitter tapped from one of the 35 glyph pixels.
Finite song-derived proof, not a rearming four-minute control circuit.
"""
from __future__ import annotations
import json
from pathlib import Path
from .core import evolve,place
from .glider_controlled_mouth import BLOCK,SYNTH_GLIDER_NW,rotate,block_erase_at,UPPER_LIP
from .vertical_lwss_corner import STATION,INPUT
from .staggered_word_mesh import EATER_NORTHEAST,EATER_TEXT
from .relocated_singer_anchor import SINGER_TRANSLATION
from .native_congruent_first20 import (FIRST_WORD_G,LAST_G,
    components as earlier_components,provenance)
from .export_operational import compact_rle

ROOT=Path(__file__).resolve().parents[1]
CLEARANCE_FILE=ROOT/'data'/'native_word_vocal_link_clearance.json'
MOUTH_CORNER=(120,72)
MARKER_STATION=(522,-320)
UPSTREAM_PERIODS=130
W_V_ORIENTATION=3
ERASE_G=2278

def marker_to_mouth(*,word=True,vocal=True):
    """A real source-ablated 2-input glider collision, never an output overlay."""
    sx,sy=MARKER_STATION;tx,ty=MOUTH_CORNER
    cells=(place(STATION,sx,sy)|place(EATER_NORTHEAST,sx,sy)
           |place(EATER_TEXT,sx-232,sy))
    if word:cells|=place(INPUT,sx,sy-2*UPSTREAM_PERIODS)
    if vocal:
        n=(FIRST_WORD_G-4)//4
        cells|=place(rotate(place(SYNTH_GLIDER_NW,4+n,2+n),
                            W_V_ORIENTATION),tx,ty)
    cells|=place(rotate(block_erase_at(ERASE_G),0),tx,ty)
    if len(cells)!=38+9*bool(word)+5*bool(vocal):
        raise AssertionError('initial glider/turner overlap')
    return cells

def actual_lip_accent(cells):
    return place(BLOCK,*MOUTH_CORNER)<=cells

def _drop_fixed_tiles(cells,tiles):
    out=set(cells)
    for x,y in tiles:
        tile=place(BLOCK,x+SINGER_TRANSLATION[0],y+SINGER_TRANSLATION[1])
        if not tile<=out:raise AssertionError(f'not an original 2x2 Life tile: {(x,y)}')
        out-=tile
    if evolve(out)!=out:raise AssertionError('initial clearance not stable')
    return out

def components():
    source=provenance()
    assert tuple(source['intervals_seconds'][6])==(10.96,13.5)
    parts=list(earlier_components()[:4])
    tiles=json.loads(CLEARANCE_FILE.read_text(encoding='utf8'))
    assert (len(tiles['0']),len(tiles['1']))==(23,1)
    for i in (0,1):parts[i]=_drop_fixed_tiles(parts[i],tiles[str(i)])
    if not place(UPPER_LIP,SINGER_TRANSLATION[0],
                 SINGER_TRANSLATION[1]+32)<=parts[0]:
        raise AssertionError('upper lip was altered by geometric clearance')
    parts.append(place(marker_to_mouth(),*SINGER_TRANSLATION))
    sizes=list(map(len,parts))
    if sizes!=[6408,648,1519,240,52]:
        raise AssertionError(('unexpected initial world',sizes))
    if len(set().union(*parts))!=sum(sizes):
        raise AssertionError('initial component overlap')
    return tuple(parts)

def world():
    return set().union(*components())

def export(destination):
    destination=Path(destination);destination.mkdir(parents=True,exist_ok=True)
    parts=components();cells=set().union(*parts)
    (destination/'real_W_marker_V_mouth_seed.rle').write_text(compact_rle(cells,(
       'Single native B3/S23 8867-cell W+V singer initial condition.',
       'Actual LWSS 90-degree redirector supplies diagonal W glider.',
       'Independent Suno V glider collides with W at mouth on g2156.',
       'Finite one-word proof; no per-frame cells inserted or removed.',
    )),encoding='utf8')
    with (destination/'real_W_marker_V_mouth_parts.tsv').open('w',encoding='utf8') as f:
        f.write(f'{len(parts)}\n')
        for i,group in enumerate(parts):
            for x,y in sorted(group):f.write(f'{i} {x} {y}\n')
    with (destination/'real_W_marker_V_mouth_seed.tsv').open('w',encoding='utf8') as f:
        for x,y in sorted(cells):f.write(f'{x} {y}\n')
    return {'rule':'B3/S23','initial_population':8867,
        'word_g':FIRST_WORD_G,'word_glyph_lwss':35,
        'physical_W_is_turner_emitted_glider':True,
        'source_V_stem_id':provenance()['vocal_stem_id'],
        'additional_g0_still_life_tiles_omitted':[23,1],
        'word_marker_is_extra_LWSS_lane':True,
        'glyph_to_mouth_specific_pixel_splitter':False,
        'whole_song_reusable_gate':False}

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--out',required=True)
    print(json.dumps(export(p.parse_args().out),indent=2))
