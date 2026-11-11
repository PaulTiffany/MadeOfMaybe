"""Export the operational glider-driven singer in a compact Golly RLE.

    python -m life.export_operational > patterns/operational_three_state_mouth.rle
"""
from __future__ import annotations
from collections import defaultdict
from itertools import groupby
from .glider_controlled_mouth import universe


def compact_rle(cells, comments=()):
    if not cells:
        return 'x = 0, y = 0, rule = B3/S23\n!\n'
    xmin=min(x for x,y in cells); xmax=max(x for x,y in cells)
    ymin=min(y for x,y in cells); ymax=max(y for x,y in cells)
    rows=defaultdict(list)
    for x,y in cells:
        rows[y-ymin].append(x-xmin)
    tokens=[]
    last_y=-1
    for y in range(ymax-ymin+1):
        xs=sorted(rows[y])
        if not xs:continue
        if last_y>=0:
            delta=y-last_y
            tokens.append((str(delta) if delta>1 else '')+'$')
        elif y>0:
            tokens.append((str(y) if y>1 else '')+'$')
        cursor=0
        for _,group in groupby(enumerate(xs),lambda q:q[1]-q[0]):
            points=[v for _,v in group]
            start,end=points[0],points[-1]
            gap=start-cursor
            if gap:tokens.append((str(gap) if gap>1 else '')+'b')
            run=end-start+1
            tokens.append((str(run) if run>1 else '')+'o')
            cursor=end+1
        last_y=y
    tokens.append('!')
    lines=[f'#C {comment}' for comment in comments]
    lines.append(f'x = {xmax-xmin+1}, y = {ymax-ymin+1}, rule = B3/S23')
    acc=''
    for token in tokens:
        if len(acc)+len(token)>70:
            lines.append(acc)
            acc=''
        acc+=token
    if acc:lines.append(acc)
    return '\n'.join(lines)+'\n'


if __name__=='__main__':
    print(compact_rle(universe(),(
        'MadeOfMaybe: three-state glider-controlled singer, untouched bubble/lyrics + pulsar',
        'State samples: G60 CLOSED / G180 MEDIUM / G288 OPEN / G420 MEDIUM',
        'G540 CLOSED / G680 OPEN (direct skip) / G778 CLOSED',
        'Native B3/S23; every control glider present at generation zero; no cell edits',
        'Sources: https://conwaylife.com/wiki/Block',
        'https://github.com/MartinSA04/GameOfLifeText (2-glider block synthesis)',
    )),end='')
