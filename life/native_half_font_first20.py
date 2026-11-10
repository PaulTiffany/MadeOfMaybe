"""One native B3/S23 singer world with physically reduced 3x4 moving-LWSS font.

The original full 5x7 WE uses 35 spaced LWSS pixels. This version samples
actual 5x7 glyphs to 3x4 (with a W adjustment), yielding 17 real pixels.
We preserve the previously qualified 36-cell turner clearance. No optical
scaling, inserted pixels, fake mouth poses or camera cuts.
"""
from __future__ import annotations
from pathlib import Path
import json
from .core import place,encode_rle
from .lyric_font import GLYPHS
from .native_word_vocal_link import components as old_components,provenance
from .native_congruent_first20 import FIRST_WORD_G,WE_SHIFT
from .relocated_singer_anchor import SINGER_TRANSLATION
from .vertical_lwss_corner import STATION,INPUT
from .staggered_word_mesh import EATER_NORTHEAST,EATER_SOUTHWEST,EATER_TEXT,reference_output

GLYPH_PITCH=36
STATION_PITCH=36
MINI_ROWS=4

def compact_glyphs():
    f={ch:tuple(''.join(GLYPHS[ch][r][c] for c in (0,2,4))
           for r in (0,2,4,6)) for ch in GLYPHS
           if len(GLYPHS[ch])==7 and len(GLYPHS[ch][0])>=5}
    f['W']=('101','101','111','101')
    return f

def lit_pixels(word='WE'):
    f=compact_glyphs()
    return tuple((4*i+c,r) for i,ch in enumerate(word)
        for r,row in enumerate(f[ch]) for c,v in enumerate(row) if v=='1')

def routes(word='WE',target_g=FIRST_WORD_G):
    if target_g%4 or target_g<400:raise ValueError('bad time phase')
    for i,(col,row) in enumerate(lit_pixels(word)):
        x=152+STATION_PITCH*i;y=GLYPH_PITCH*row
        n=1+GLYPH_PITCH*col-x+43+(target_g-200)//2
        if n%2 or n<2:raise ValueError('unreachable music-time corner')
        yield i,col,row,x,y,n//2

def word_parts():
    parts=[]
    for _,col,row,x,y,k in routes():
        parts.append(place(STATION,x,y)|place(INPUT,x,y-2*k)
                     |place(EATER_NORTHEAST,x,y)|place(EATER_SOUTHWEST,x,y))
    parts.append(set().union(*(place(EATER_TEXT,0,36*r)
                               for r in range(MINI_ROWS))))
    assert len(set().union(*parts))==sum(map(len,parts))
    return tuple(parts)

def components():
    parts=list(old_components())
    pixels=set().union(*word_parts())
    parts[2]=place(pixels,WE_SHIFT[0]+SINGER_TRANSLATION[0],
                         WE_SHIFT[1]+SINGER_TRANSLATION[1])
    assert list(map(len,parts))==[6408,648,742,240,52]
    assert len(set().union(*parts))==8090
    return tuple(parts)

def universe():
    return set().union(*components())

def expected_word(dx=0):
    p=reference_output()
    return set().union(*(place(p,44+36*c+WE_SHIFT[0]+SINGER_TRANSLATION[0]+dx,
                        36*r+WE_SHIFT[1]+SINGER_TRANSLATION[1])
                       for c,r in lit_pixels()))

def export(dest):
    dest=Path(dest);dest.mkdir(parents=True,exist_ok=True)
    parts=components();cells=set().union(*parts)
    with (dest/'mini_word_seed.tsv').open('w') as f:
        for x,y in sorted(cells):f.write(f'{x} {y}\n')
    with (dest/'mini_word_parts.tsv').open('w') as f:
        f.write(f'{len(parts)}\n')
        for i,part in enumerate(parts):
            for x,y in sorted(part):f.write(f'{i} {x} {y}\n')
    (dest/'mini_word_seed.rle').write_text(encode_rle(cells,(
        'One actual B3/S23 singer: physically smaller 3x4 moving LWSS glyphs.',
        '17 real WE pixel ships form at Suno g2156; original W/V lip connected.',
        'Same original 19-cell corner stations and physical row eaters.'
    )),encoding='utf8')
    result={'rule':'B3/S23','initial_population':8090,
       'old_5x7_pixels':35,'new_3x4_pixels':17,
       'old_nominal_box_cells':[396,252],
       'new_nominal_box_cells':[252,144],
       'same_station_pitch_cells':36,
       'first_word_generation':FIRST_WORD_G,
       'Suno_vocal_stem_id':provenance()['vocal_stem_id'],
       'full_song_native_karaoke_qualified':False}
    (dest/'mini_geometry.json').write_text(json.dumps(result,indent=2)+'\n')
    return result

if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('--out',required=True)
    args=parser.parse_args()
    print(json.dumps(export(args.out),indent=2))
