"""Actual-cell preview of the denser, one-world, glider-timed singer.

Pillow is needed only for presentation; simulation remains pure Python.
Run: python preview/make_dense_mouth.py
"""
from __future__ import annotations
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))

from PIL import Image,ImageDraw,ImageFont
from life.core import evolve
from life.export_operational import compact_rle
from life.dense_glider_mouth import (
    BLOCK,FULL_DURATION,POSE_SAMPLES,
    DENSE_MEDIUM_TARGETS,DENSE_OPEN_TARGETS,
    prepared_art,universe,components,
)

OUT=Path(__file__).resolve().parent
BG=(12,22,36); FACE=(205,238,232); LIP=(255,167,168)
SIGNAL=(43,72,91); TEXT=(233,243,247); SUB=(134,166,186)
try:
    TITLE=ImageFont.truetype('DejaVuSans-Bold.ttf',33)
    SMALL=ImageFont.truetype('DejaVuSans.ttf',19)
except OSError:
    TITLE=SMALL=ImageFont.load_default()

HEAD,UPPER=map(set,prepared_art())
MOUTH=set().union(*(
    {(x+dx,y+dy) for dx,dy in BLOCK}
    for x,y in DENSE_MEDIUM_TARGETS+DENSE_OPEN_TARGETS
))

def shot(cells,g,width=720,height=730,scale=1.34):
    im=Image.new('RGB',(width,height),BG)
    draw=ImageDraw.Draw(im)
    ox,oy=width//2,height//2+14
    for x,y in cells:
        X=round(ox+x*scale);Y=round(oy+y*scale)
        if 0<=X<width-4 and 0<=Y<height-4:
            color=(FACE if (x,y) in HEAD else
                   LIP if (x,y) in UPPER or (x,y) in MOUTH else SIGNAL)
            sz=max(2,round(scale*2))
            draw.rectangle((X,Y,X+sz-1,Y+sz-1),fill=color)
    draw.text((26,21),f'{POSE_SAMPLES.get(g,"LIFE").upper()}  ·  G{g}',
              fill=TEXT,font=TITLE)
    draw.text((29,64),'One universe · native glider signals',
              fill=SUB,font=SMALL)
    return im

def stage(cells,g,decorations):
    width,height,scale=1512,900,1.45
    im=Image.new('RGB',(width,height),BG)
    draw=ImageDraw.Draw(im)
    ox,oy=510,472
    bubble,pulsar=decorations
    for x,y in cells:
        X=round(ox+x*scale);Y=round(oy+y*scale)
        if 0<=X<width-4 and 0<=Y<height-4:
            color=(FACE if (x,y) in HEAD else
                   LIP if (x,y) in UPPER or (x,y) in MOUTH else
                   (225,217,154) if (x,y) in bubble else
                   (166,175,234) if (x,y) in pulsar else SIGNAL)
            sz=max(2,round(scale*2))
            draw.rectangle((X,Y,X+sz-1,Y+sz-1),fill=color)
    draw.text((34,23),'MADE OF MAYBE  /  B3/S23',
              font=TITLE,fill=TEXT)
    draw.text((34,70),f'Generation {g} · one initial universe · native gliders',
              font=SMALL,fill=SUB)
    return im

def main():
    root=OUT.parent
    pattern=root/'patterns'/'dense_three_state_singer.rle'
    pattern.parent.mkdir(exist_ok=True)
    pattern.write_text(compact_rle(universe(),(
        'B3/S23: glider-controlled denser three-state singer; one universe',
        'CLOSED MEDIUM OPEN MEDIUM CLOSED OPEN CLOSED with direct skip',
        'All control gliders preloaded; no playback edits',
    )),encoding='utf-8')
    parts=components()
    decorations=(parts['bubble_outline']|parts['bubble_lyrics'],parts['pulsar'])
    world=universe();near=[];full=[];snapshots={};full_snaps={}
    for gen in range(FULL_DURATION):
        if gen in (60,180,288):
            snapshots[gen]=shot(world,gen)
            full_snaps[gen]=stage(world,gen,decorations)
        if gen%12==0:
            near.append(shot(world,gen).resize((540,548),Image.Resampling.NEAREST))
        if gen%18==0:
            full.append(stage(world,gen,decorations).resize(
                (1134,675),Image.Resampling.NEAREST))
        world=evolve(world)
    sheet=Image.new('RGB',(2160,730),BG)
    for i,gen in enumerate((60,180,288)):
        sheet.paste(snapshots[gen],(i*720,0))
        full_snaps[gen].save(OUT/f'dense_stage_g{gen}.png',optimize=True)
    sheet.save(OUT/'dense_mouth_three_states.png',optimize=True)
    near[0].save(OUT/'dense_mouth_glider_control.gif',save_all=True,
                 append_images=near[1:],duration=120,loop=0,optimize=True)
    full[0].save(OUT/'dense_singer_bubble_stage.gif',save_all=True,
                 append_images=full[1:],duration=150,loop=0,optimize=True)
    print('Rendered genuine B3/S23 three-state mouth, stage GIF and full RLE.')

if __name__=='__main__':
    main()
