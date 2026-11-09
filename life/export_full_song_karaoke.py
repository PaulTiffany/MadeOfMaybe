"""Export the complete song as one RLE of preloaded Life gliders.

Usage:
    python -m life.export_full_song_karaoke \
        --alignment data/made_of_maybe_suno_alignment.json \
        --out patterns/made_of_maybe_full_song_native_life.rle \
        --score output/made_of_maybe_full_karaoke_score.json

RLE writer iterates only occupied rows. The board spans millions of empty
cells, so a naive row-by-row encoder would never finish.
"""
from __future__ import annotations
import argparse
from collections import defaultdict
from itertools import groupby
import json
from pathlib import Path

from .full_song_karaoke import compile_plan, seeded_lines, manifest, stats, GPS, ALIGNMENT_FILE
from .lyric_cues import read_alignment


def sparse_rle_stream(cells, out, *, comments=()):
    """Streaming compressed RLE using sparse rows; supports huge Life coordinates."""
    rows=defaultdict(list)
    xmin=ymin=None
    xmax=ymax=None
    count=0
    for x,y in cells:
        rows[y].append(x);count+=1
        xmin=x if xmin is None else min(xmin,x)
        xmax=x if xmax is None else max(xmax,x)
        ymin=y if ymin is None else min(ymin,y)
        ymax=y if ymax is None else max(ymax,y)
    if count==0:
        out.write('x = 0, y = 0, rule = B3/S23\n!\n')
        return {'cells':0,'width':0,'height':0,'origin_x':0,'origin_y':0}
    for c in comments:
        out.write(f'#C {c}\n')
    out.write(f'x = {xmax-xmin+1}, y = {ymax-ymin+1}, rule = B3/S23\n')
    current_y=-1
    buffer=''
    def emit(token):
        nonlocal buffer
        if len(buffer)+len(token)>70:
            out.write(buffer+'\n');buffer=''
        buffer+=token
    for y in sorted(rows):
        rel_y=y-ymin
        if current_y>=0:
            gap=rel_y-current_y
            emit((str(gap) if gap>1 else '')+'$')
        elif rel_y>0:
            emit((str(rel_y) if rel_y>1 else '')+'$')
        xs=sorted(set(rows[y]))
        cursor=0
        for _,group in groupby(enumerate(xs),lambda it:it[1]-it[0]):
            group=list(group)
            a,b=group[0][1]-xmin,group[-1][1]-xmin
            blank=a-cursor
            if blank:emit((str(blank) if blank>1 else '')+'b')
            live=b-a+1
            emit((str(live) if live>1 else '')+'o')
            cursor=b+1
        current_y=rel_y
    emit('!')
    if buffer:out.write(buffer+'\n')
    return {'cells':count,'width':xmax-xmin+1,'height':ymax-ymin+1,
            'origin_x':xmin,'origin_y':ymin}


def main(argv=None):
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--alignment',type=Path,default=ALIGNMENT_FILE)
    ap.add_argument('--out',type=Path,default=Path('patterns/made_of_maybe_full_song_native_life.rle'))
    ap.add_argument('--score',type=Path,default=Path('output/made_of_maybe_full_karaoke_score.json'))
    args=ap.parse_args(argv)
    lines=compile_plan(read_alignment(args.alignment))
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.score.parent.mkdir(parents=True,exist_ok=True)
    with args.out.open('w',encoding='ascii') as out:
        dimensions=sparse_rle_stream(seeded_lines(lines),out,comments=[
            'Made of Maybe: FULL SONG karaoke, one B3/S23 universe; 192 generations/second.',
            '3 preloaded Life gliders per text pixel: MAKE 2, ERASE 1.',
            'Each sung line is a separate spatial stage; camera follows stage.',
            'Song tempo unaffected. No runtime cells inserted or text substituted.',
            'Source alignment: Suno song 53610991-7381-4749-96e1-79b8e3b1c28b.',
        ])
    data=manifest(lines)
    data['export']=dimensions
    args.score.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'rle':str(args.out),'score':str(args.score),
                      'export':dimensions,**data['stats']},indent=2))

if __name__=='__main__':main()
