"""Single native B3/S23 g0 world for the first 20s of MADE OF MAYBE.

Uses previously qualified LWSS turners, 2-glider mouth block make/erase,
rounded singer bubble and two independently scored source timelines.
All gliders exist at g0. Masks describe fixed 2x2 tiles omitted at
construction, not operations performed during playback. Finite pilot.
"""
import json
from pathlib import Path
from .core import evolve,place,encode_rle
from .glider_controlled_mouth import (BLOCK,UPPER_LIP,MEDIUM_TARGETS,OPEN_TARGETS,
 ROUTING,SYNTH_GLIDER_NW,SYNTH_GLIDER_SW,block_make_at,block_erase_at,rotate)
from .refined_singer_candidate import qualified_layout,LIP_DROP_Y
from .relocated_singer_anchor import SINGER_TRANSLATION
from .rounded_bubble_edge_candidate import rim
from .vertical_lwss_corner import STATION,INPUT
from .staggered_word_mesh import EATER_NORTHEAST,EATER_SOUTHWEST,EATER_TEXT
from .lyric_font import GLYPHS
from .full_song_karaoke import GPS,ALIGNMENT_FILE,compile_plan
from .lyric_cues import read_alignment
ROOT=Path(__file__).resolve().parents[1]
FIRST_WORD_G=2156
LAST_G=3840
WE_SHIFT=(440,-323)
VOICE_EVENTS=((700,'medium',822),(824,'open',1682),(2160,'open',2650),(2960,'medium',3966))

def provenance():
    raw=json.loads((ROOT/'data/made_of_maybe_vocal_gate_take1_v0.json').read_text())
    a=raw['intervals_seconds']
    assert raw['song_id']=='53610991-7381-4749-96e1-79b8e3b1c28b'
    assert raw['vocal_stem_id']=='bee52d16-b01b-4224-bd4c-5c51081d813b'
    assert (a[0][0],a[5][1])==(3.5,8.74)
    assert tuple(a[6])==(10.96,13.5) and a[7][0]==15.24
    assert raw['dry_wet_separation_qualified'] is False
    word=compile_plan(read_alignment(ALIGNMENT_FILE))[0].words[0]
    assert (word.text,word.make_g)==('WE',FIRST_WORD_G) and GPS==192
    return raw

def word_routes():
    pixels=[(6*i+c,r) for i,ch in enumerate('WE')
            for r,row in enumerate(GLYPHS[ch])
            for c,v in enumerate(row) if v=='1']
    assert len(pixels)==35
    for i,(col,row) in enumerate(pixels):
        x=152+36*i;y=36*row
        numerator=1+36*col-x+43+(FIRST_WORD_G-200)//2
        assert numerator%2==0
        k=numerator//2;assert k>=0
        yield i,col,row,x,y,k

def word():
    parts=[]
    for _,_,_,x,y,k in word_routes():
        parts.append(place(STATION,x,y)|place(INPUT,x,y-2*k)
                     |place(EATER_NORTHEAST,x,y)|place(EATER_SOUTHWEST,x,y))
    parts.append(set().union(*(place(EATER_TEXT,0,36*r) for r in range(7))))
    out=set().union(*parts)
    assert len(out)==sum(map(len,parts))==1519
    return out

def vocal_gliders():
    parts=[]
    for on,bank,off in VOICE_EVENTS:
        targets=MEDIUM_TARGETS if bank=='medium' else OPEN_TARGETS
        for i,(x,y) in enumerate(targets):
            delay,md,ed=ROUTING[bank,i]
            parts.append(place(rotate(block_make_at(on+delay),md),x,y+LIP_DROP_Y))
            parts.append(place(rotate(block_erase_at(off+delay),ed),x,y+LIP_DROP_Y))
    out=set().union(*parts)
    assert len(out)==sum(map(len,parts))==240
    return out

def word_accent(*,w=True,v=True):
    n=(FIRST_WORD_G-4)//4
    ga=rotate(place(SYNTH_GLIDER_NW,4+n,2+n),7)
    gb=rotate(place(SYNTH_GLIDER_SW,4+n,2-n),7)
    parts=[place(rotate(block_erase_at(2278),5),0,100)]
    if w:parts.append(place(ga,0,100))
    if v:parts.append(place(gb,0,100))
    out=set().union(*parts)
    assert len(out)==sum(map(len,parts))
    return out

def remove_tiles(cells,origins):
    out=set(cells)
    for x,y in origins:
        block=place(BLOCK,x,y)
        assert block<=out,(x,y)
        out.difference_update(block)
    assert evolve(out)==out
    return out

def components():
    provenance()
    mask=json.loads((ROOT/'data/native_first20_removed_tiles.json').read_text())
    assert (len(mask['art']),len(mask['rim']))==(80,50)
    art=set().union(*qualified_layout()['art'].values())
    singer=place(remove_tiles(art,mask['art'])|place(UPPER_LIP,0,LIP_DROP_Y),*SINGER_TRANSLATION)
    bubble=place(remove_tiles(set(rim()),mask['rim']),*SINGER_TRANSLATION)
    letters=place(word(),WE_SHIFT[0]+SINGER_TRANSLATION[0],WE_SHIFT[1]+SINGER_TRANSLATION[1])
    vocals=place(vocal_gliders(),*SINGER_TRANSLATION)
    accent=place(word_accent(),*SINGER_TRANSLATION)
    parts=(singer,bubble,letters,vocals,accent)
    assert list(map(len,parts))==[6500,652,1519,240,15]
    assert len(set().union(*parts))==sum(map(len,parts))==8926
    return parts

def export(dest):
    dest=Path(dest);dest.mkdir(parents=True,exist_ok=True)
    parts=components();world=set().union(*parts)
    with (dest/'native_first20_seed.tsv').open('w') as f:
        for x,y in sorted(world):f.write(f'{x} {y}\n')
    with (dest/'native_first20_parts.tsv').open('w') as f:
        f.write(f'{len(parts)}\n')
        for i,p in enumerate(parts):
            for x,y in sorted(p):f.write(f'{i} {x} {y}\n')
    (dest/'native_first20.rle').write_text(encode_rle(world,(
        'One 8926-cell g0 Life universe, song word W and isolated vocal V.',
        '35 existing LWSS turners assemble WE at g2156; four jaw events.',
        'Word accent is independently timed, not routed from moving text.',
    )),encoding='utf8')
    return {'g0_population':8926,'component_sizes':list(map(len,parts)),
            'vocal_score_events':VOICE_EVENTS,'word_onset_g':FIRST_WORD_G,
            'one_shot_song_fixture':True,'full_song_qualified':False,
            'letter_to_mouth_signal_physically_branched':False}
if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--out',required=True)
    a=p.parse_args();print(json.dumps(export(a.out),indent=2))
