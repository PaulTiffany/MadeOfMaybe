"""Exact B3/S23 native probe, NOT a full-song qualification.

Station x translation changes the actual converter arrival time while
keeping the desired westbound MADE readout fixed. Compare alternate
physical initial conditions; preserve the source g2204 target.
"""
from __future__ import annotations
from pathlib import Path
from life.core import place
from life.gondry_corner_backtrace import backtrace
from life.vertical_lwss_corner import STATION,INPUT
from life.staggered_word_mesh import EATER_NORTHEAST,EATER_SOUTHWEST,EATER_TEXT

OFFSETS=(-240,-192,-160,-128,-96,-80,-64,-48,-32,-16,16,32,48,64,80,96,128,160,192,224,240)

def parts_at_offset(offset):
    if offset%2:raise ValueError('period-four alignment requires even x')
    plans=backtrace('MADE',2204)
    parts=[]
    for p in plans:
        # x_station increases by delta; to keep output x the same at
        # g2204, incoming k decreases by delta/2, source y increases delta.
        k=p.incoming_advance_periods-offset//2
        if k<2 or 200+4*k>2204:
            raise ValueError('unreachable converter phase')
        x=p.station_x+offset;y=p.station_y
        parts.append(place(STATION,x,y)|place(INPUT,x,y-2*k)
            |place(EATER_NORTHEAST,x,y)|place(EATER_SOUTHWEST,x,y))
    parts.append(set().union(*(place(EATER_TEXT,0,36*r) for r in range(4))))
    if len(set().union(*parts))!=sum(map(len,parts)):
        raise ValueError('initial converter/source overlap')
    return tuple(parts)

def export(folder):
    folder=Path(folder);folder.mkdir(parents=True,exist_ok=True)
    good=[]
    for offset in OFFSETS:
        try:parts=parts_at_offset(offset)
        except ValueError as exc:
            print(f'offset={offset} invalid: {exc}')
            continue
        target=folder/f'made_offset_{offset}_parts.tsv'
        with target.open('w') as f:
            f.write(f'{len(parts)}\n')
            for i,group in enumerate(parts):
                for x,y in sorted(group):f.write(f'{i} {x} {y}\n')
        good.append(offset)
    print('candidates',good)
    return good
if __name__=='__main__':
    import sys
    export(sys.argv[1])
