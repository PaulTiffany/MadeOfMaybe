"""Native one-world attempt: existing singer/rounded bubble/real W+V mouth,
plus a second REAL downward-LWSS -> 90-degree converter -> WEST word MADE.

Gondry inverse source staging moves the second converter x-position while
preserving every moving output-pixel position at original Suno g2204.
No renderer word substitution or independent studio layers.
"""
from __future__ import annotations
from pathlib import Path
import json
from .core import place
from .native_half_font_first20 import components as singer_parts,expected_word
from .gondry_corner_backtrace import backtrace
from .vertical_lwss_corner import STATION,INPUT
from .staggered_word_mesh import EATER_NORTHEAST,EATER_SOUTHWEST,EATER_TEXT,reference_output
from .native_congruent_first20 import WE_SHIFT
from .relocated_singer_anchor import SINGER_TRANSLATION
from .export_operational import compact_rle

ROW_Y=144
SHIFT=(WE_SHIFT[0]+SINGER_TRANSLATION[0],WE_SHIFT[1]+SINGER_TRANSLATION[1])
OFFSETS=(-90,-54,-18,0,18,54,90)

def made_parts(offset=0):
    if offset%2:raise ValueError('offset violates period four')
    parts=[]
    for p in backtrace('MADE',2204):
        x=p.station_x+offset;y=p.station_y+ROW_Y
        k=p.incoming_advance_periods-offset//2
        if k<2 or 200+4*k>2204:raise ValueError('unreachable converter')
        parts.append(place(STATION,x,y)|place(INPUT,x,y-2*k)
                   |place(EATER_NORTHEAST,x,y)|place(EATER_SOUTHWEST,x,y))
    parts.append(set().union(*(place(EATER_TEXT,0,ROW_Y+36*r) for r in range(4))))
    if len(set().union(*parts))!=sum(map(len,parts)):
        raise ValueError('second-stage initial overlap')
    return tuple(parts)

def components(offset=0):
    base=singer_parts()
    new=place(set().union(*made_parts(offset)),*SHIFT)
    if len(set().union(*base,new))!=sum(map(len,base))+len(new):
        raise ValueError('second stage overlaps original singer at g0')
    return tuple(base)+(new,)

def universe(offset=0):
    return set().union(*components(offset))

def made_at_g2204():
    out=set()
    for p in backtrace('MADE',2204):
        out|=place(reference_output(),
            SHIFT[0]+p.reading_x+43,SHIFT[1]+ROW_Y+p.reading_y-12)
    return out

def made_fixed(offset=0):
    parts=[]
    for p in backtrace('MADE',2204):
        x=p.station_x+offset;y=p.station_y+ROW_Y
        parts.append(place(EATER_NORTHEAST,x,y)|place(EATER_SOUTHWEST,x,y))
    parts.append(set().union(*(place(EATER_TEXT,0,ROW_Y+36*r)
        for r in range(4))))
    return place(set().union(*parts),*SHIFT)

def export_probe(folder):
    folder=Path(folder);folder.mkdir(parents=True,exist_ok=True)
    reports=[]
    for delta in OFFSETS:
        try: parts=components(delta)
        except ValueError as e:
            reports.append({'offset':delta,'valid_g0':False,'error':str(e)})
            continue
        path=folder/f'candidate_{delta}_parts.tsv'
        with path.open('w') as f:
            f.write(str(len(parts))+'\n')
            for i,p in enumerate(parts):
                for x,y in sorted(p):f.write(f'{i} {x} {y}\n')
        reports.append({'offset':delta,'valid_g0':True,
            'seed_population':sum(map(len,parts)), 'file':str(path)})
    (folder/'candidates.json').write_text(json.dumps(reports,indent=2)+'\n')
    return reports

def export_winner(delta,folder):
    folder=Path(folder);folder.mkdir(parents=True,exist_ok=True)
    live=universe(delta)
    with (folder/'winning_g0.tsv').open('w') as f:
        for x,y in sorted(live):f.write(f'{x} {y}\n')
    (folder/'winning_g0.rle').write_text(compact_rle(live,(
      'Real singer and two Suno lyric words, one B3/S23 g0 universe',
      'Downward LWSS turn WEST at actual original 19-cell converters',
      'Native seven-cell fishhook receivers; no inserted movie elements',
      'Second MADE has not yet been wired to the actual three-state mouth'
    )),encoding='utf8')
    report={'offset':delta,'seed_population':len(live),
      'WE_onset_generation':2156,'MADE_onset_generation':2204,
      'MADE_converted_3x4_glyph_LWSS':len(backtrace('MADE',2204)),
      'actual_original_W_to_V_lip_kept':True,
      'MADE_to_mouth_connected':False,
      'all_403_words_physically_integrated':False,
      'four_minute_one_bubble_movie_complete':False}
    (folder/'qualification_scope.json').write_text(json.dumps(report,indent=2)+'\n')
    return report

if __name__=='__main__':
    import sys
    print(json.dumps(export_probe(sys.argv[1]),indent=2))
