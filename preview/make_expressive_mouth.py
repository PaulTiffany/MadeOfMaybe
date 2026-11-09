"""Render a LIFE-driven singer with a physically cleared inner mouth.

Requires Pillow. Everything structural is extracted from actual B3/S23
live cells. The glow, contrast and 1.52x camera stretch are presentation
choices, not changes to physics or cell insertions.

Run: python preview/make_expressive_mouth.py
"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from PIL import Image,ImageDraw,ImageFont,ImageFilter
from life.core import evolve
from life.export_operational import compact_rle
from life.expressive_mouth import (
    components,universe,LINE_CELLS,EXPRESSIVE_CHECKPOINTS,
    QUALIFICATION_END,START_LINE
)
from life.symmetric_full_mouth import target_blocks
from life.glider_controlled_mouth import BLOCK
from life.core import place

HERE=Path(__file__).resolve().parent
PATS=HERE.parent/'patterns'
PATS.mkdir(exist_ok=True,parents=True)
RENDER_RLE=PATS/'expressive_singer_glider_performance.rle'
RENDER_RLE.write_text(compact_rle(universe(True),(
    'One B3/S23 universe; five central line blocks erased at g98 and restored by g932.',
    'CLOSED / MEDIUM / OPEN / MEDIUM / BREATH / OPEN / BREATH / CLOSED',
    'g540 and g778 are BREATH, NOT closed. Dynamic open poses have no fixed teeth.',
    'Glider controls preloaded at generation zero. Two independent period-2 eye glints.',
)),encoding='utf-8')

DARK=(8,16,31)
FLESH=(221,241,243)
EYES=(243,251,248)
LIP=(255,136,153)
GLOW=(240,89,133)
BREATH=(255,217,171)
SIGNAL=(36,65,80)
BUBBLE=(235,211,142)
PULSAR=(169,188,228)
SUB=(141,163,181)
try:
    FONT=ImageFont.truetype('DejaVuSans.ttf',20)
    SMALL=ImageFont.truetype('DejaVuSans.ttf',16)
    BOLD=ImageFont.truetype('DejaVuSans-Bold.ttf',28)
except OSError: FONT=SMALL=BOLD=ImageFont.load_default()

W,H=950,680
SX,SY=1.95,1.28
OX,OY=475,326

TARGETS={state:target_blocks(state) for state in ('medium','open')}
TILES={}
for state,ps in TARGETS.items():
    tiles=[]
    for x,y in ps:
        b=place(BLOCK,x,y)
        # Each tile's top-left is a point with no same-set member above or left.
        if (x-1,y) not in ps and (x,y-1) not in ps:
            tiles.append(b)
    TILES[state]=tiles
LINE_TILES=[place(BLOCK,*pt) for pt in START_LINE]


def pixel(x,y,offset=(0,0)):
    return round(OX+SX*x+offset[0]),round(OY+SY*y+offset[1])


def paint_cells(canvas,cells,color,offset=(0,0),dot_size=None):
    d=ImageDraw.Draw(canvas)
    w=dot_size or max(2,round(SX));h=dot_size or max(2,round(SY))
    for x,y in cells:
        X,Y=pixel(x,y,offset)
        if -2<=X<canvas.width+2 and -2<=Y<canvas.height+2:
            d.rectangle((X,Y,X+w-1,Y+h-1),fill=color)


def render(world,parts,gen,detail=True):
    # Source-of-truth is world evolved from one starting board.
    img=Image.new('RGB',(W,H),DARK)
    static=set(parts.get('outline',set()))|set(parts.get('eyes_nose',set()))
    color_map={}
    for pt in parts['outline']:color_map[pt]=FLESH
    for pt in parts['eyes_nose']:color_map[pt]=EYES
    live_mouth=set()
    for tiles in TILES.values():
        for t in tiles:
            if t<=world:live_mouth.update(t)
    live_closed=set()
    for tile in LINE_TILES:
        if tile<=world:live_closed.update(tile)
    active=live_mouth|live_closed
    # All cells, even in-transit gliders, are drawn, but gliders are dim.
    paint_cells(img,world,SIGNAL)
    paint_cells(img,static,FLESH)
    paint_cells(img,parts['eyes_nose'],EYES)
    paint_cells(img,parts['left_eye_glint'],(147,239,226),dot_size=4)
    paint_cells(img,parts['right_eye_glint'],(147,239,226),dot_size=4)
    # A renderer's soft optical bloom; never adds a Life cell.
    if detail and active:
        layer=Image.new('RGBA',(W,H),(0,0,0,0))
        d=ImageDraw.Draw(layer)
        for x,y in active:
            X,Y=pixel(x,y)
            d.ellipse((X-7,Y-7,X+7,Y+7),fill=(255,115,150,180))
        blur=layer.filter(ImageFilter.GaussianBlur(7))
        img=Image.alpha_composite(img.convert('RGBA'),blur).convert('RGB')
    paint_cells(img,live_mouth,LIP,dot_size=3)
    paint_cells(img,live_closed,BREATH,dot_size=3)
    d=ImageDraw.Draw(img)
    name=EXPRESSIVE_CHECKPOINTS.get(gen,'in motion').upper()
    d.rectangle((0,0,W,92),fill=DARK)
    d.text((25,16),f'{name}   •   G{gen:04}',font=BOLD,fill=(243,248,251))
    d.text((27,58),'Real Conway Life  ·  1.52× horizontal camera  ·  optical glow',font=SMALL,fill=SUB)
    return img


def render_stage(world,parts,g):
    # All Life cells drawn, including unchanged bubble, lettering and pulsar.
    w,h=1750,780
    im=Image.new('RGB',(w,h),DARK)
    p=render(world,parts,g)
    im.paste(p,(0,40))
    d=ImageDraw.Draw(im)
    for k,col in (('bubble_outline',BUBBLE),('bubble_lyrics',BUBBLE),('pulsar',PULSAR)):
        for x,y in parts[k]:
            X=round(490+1.65*x)
            Y=round(335+1.30*y)
            if 930<=X<w-3 and 20<=Y<h-3:
                d.rectangle((X,Y,X+2,Y+2),fill=col)
    d.text((1010,30),'SINGER  +  SPEECH BUBBLE',font=BOLD,fill=FLESH)
    d.text((1010,73),'One uninterrupted Game of Life world',font=SMALL,fill=SUB)
    return im


def main():
    parts=components(with_bubble=True)
    world=universe(with_bubble=True)
    shots={};gif=[]
    frames_needed=set(EXPRESSIVE_CHECKPOINTS)
    for g in range(QUALIFICATION_END):
        if g in frames_needed:
            shots[g]=(set(world),{k:set(v) for k,v in parts.items()})
        if g%29==0:
            gif.append(render(world,parts,g,detail=True).resize((570,408),Image.Resampling.LANCZOS))
        world=evolve(world)
        parts={k:evolve(v) for k,v in parts.items()}
    # Six checkpoints from one exact Life run, no edits between snapshots.
    cols=[60,180,288,420,680,960]
    sheet=Image.new('RGB',(3*W,2*H),DARK)
    for n,g in enumerate(cols):
        src,sep=shots[g]
        sheet.paste(render(src,sep,g),((n%3)*W,(n//3)*H))
    sheet.save(HERE/'expressive_mouth_contact_sheet.png',optimize=True)
    src,part=shots[288]
    render_stage(src,part,288).save(HERE/'expressive_singer_bubble.png',optimize=True)
    gif[0].save(HERE/'expressive_glider_singer.gif',save_all=True,
                append_images=gif[1:],duration=115,loop=0,optimize=True)
    print('Rendered 6 actual Life checkpoints, staged scene, GIF, and real-universe RLE.')

if __name__=='__main__':main()
