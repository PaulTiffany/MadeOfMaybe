"""New face styling on genuine one-board 980-generation B3/S23 performance.

Only actual live cells are rendered as solid marks. Optional blooms are
optical presentation, not additional Life pixels; no runtime injection.
"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from PIL import Image,ImageDraw,ImageFont,ImageFilter
from life.core import evolve
from life.styled_singer import components,universe,QUALIFICATION_END
from life.expressive_mouth import EXPRESSIVE_CHECKPOINTS,START_LINE
from life.symmetric_full_mouth import target_blocks
from life.glider_controlled_mouth import BLOCK
from life.core import place
from life.export_operational import compact_rle

HERE=Path(__file__).resolve().parent
BG=(7,16,30);SIGNAL=(23,44,56);INK=(208,239,237)
COLOR={
    'art_contour':(206,236,235),'art_hair':(171,224,237),
    'art_brows':(249,196,178),'art_eye_liner':(240,246,241),
    'art_iris':(110,238,217),'art_nose':(222,188,183),
    'art_cheekbones':(249,158,172),
    'left_eye_glint':(248,245,210),'right_eye_glint':(248,245,210),
    'bubble_outline':(210,220,235),'bubble_lyrics':(251,219,157),
    'pulsar':(153,180,242),
}
LIPS=(255,133,173);BAND=(255,211,179)
W,H=1700,920;OX,OY=475,455;SX,SY=1.9,1.52
try:
    BOLD=ImageFont.truetype('DejaVuSans-Bold.ttf',29)
    SMALL=ImageFont.truetype('DejaVuSans.ttf',18)
except OSError:
    BOLD=SMALL=ImageFont.load_default()

# Identify only actual COMPLETE controlled blocks to apply lip color.
TILES={state:[place(BLOCK,x,y) for x,y in sorted(target_blocks(state))
               if (x-1,y) not in target_blocks(state) and
                  (x,y-1) not in target_blocks(state)]
       for state in ('medium','open')}
LINE=[place(BLOCK,*p) for p in START_LINE]


def pixel(x,y):return int(OX+SX*x),int(OY+SY*y)


def cells_dots(d,cells,color,extra=0):
    for x,y in cells:
        X,Y=pixel(x,y)
        if -4<=X<W+4 and -4<=Y<H+4:
            w=max(2,int(SX)+extra);h=max(2,int(SY)+extra)
            d.rectangle((X,Y,X+w-1,Y+h-1),fill=color)


def render(world,parts,g,legend=True):
    img=Image.new('RGB',(W,H),BG)
    d=ImageDraw.Draw(img)
    # Control gliders remain real cells; they are deliberately dimmed so
    # the true lip and static facial structure can be read at normal size.
    cells_dots(d,world,SIGNAL)
    for kind,color in COLOR.items():
        if kind in parts:
            cells_dots(d,parts[kind],color,extra=1 if kind in ('art_eye_liner','art_brows') else 0)
    lips=set()
    for tiles in TILES.values():
        for tile in tiles:
            if tile<=world:lips|=tile
    line=set()
    for tile in LINE:
        if tile<=world:line|=tile
    # Soft optical bloom is camera presentation, does NOT add live cells.
    if lips or line:
        glow=Image.new('RGBA',(W,H),(0,0,0,0))
        gd=ImageDraw.Draw(glow)
        for x,y in lips|line:
            X,Y=pixel(x,y)
            gd.ellipse((X-5,Y-5,X+5,Y+5),fill=(255,90,141,110))
        bloom=glow.filter(ImageFilter.GaussianBlur(5))
        img=Image.alpha_composite(img.convert('RGBA'),bloom).convert('RGB')
    d=ImageDraw.Draw(img)
    cells_dots(d,lips,LIPS,extra=1)
    cells_dots(d,line,BAND,extra=1)
    if legend:
        label=EXPRESSIVE_CHECKPOINTS.get(g,'in motion').upper()
        d.text((42,22),f'{label}   /   G{g:04}',font=BOLD,fill=INK)
        d.text((44,62),'Stylized face, genuine Life cells • 1 constant generation clock',font=SMALL,fill=(156,177,193))
        d.text((1075,809),'MADE OF MAYBE  /  SINGER TEST',font=BOLD,fill=INK)
        d.text((1075,846),'Bubble lettering still static • no karaoke timing yet',font=SMALL,fill=(156,177,193))
    return img


def main():
    world=universe(True);parts=components(True);shots={};frames=[]
    for g in range(QUALIFICATION_END):
        if g in EXPRESSIVE_CHECKPOINTS:
            shots[g]=(set(world),{k:set(v) for k,v in parts.items()})
        if g in (0,60,120,180,240,288,360,420,540,680,778,960):
            frames.append(render(world,parts,g).resize((850,460),Image.Resampling.LANCZOS))
        if g%200==0:print('Simulated',g,flush=True)
        parts={k:evolve(v) for k,v in parts.items()}
        world=evolve(world)
    print('Simulation complete; saving checkpoints',flush=True)
    for g in (60,180,288,420,680,960):
        w,p=shots[g]
        render(w,p,g).save(HERE/f'styled_singer_g{g:03}.png',optimize=True)
    # Crop to face for readable visual comparison, actual Life cells untouched.
    coords=(46,18,880,864)
    sample=(60,180,288,960)
    pw,ph=coords[2]-coords[0],coords[3]-coords[1]
    panel=Image.new('RGB',(pw*2,ph*2),BG)
    for n,g in enumerate(sample):
        w,p=shots[g]
        frame=render(w,p,g,legend=False).crop(coords)
        dd=ImageDraw.Draw(frame)
        dd.rectangle((9,8,255,52),fill=BG)
        dd.text((19,13),f'{EXPRESSIVE_CHECKPOINTS[g].upper()} • G{g}',font=BOLD,fill=INK)
        panel.paste(frame,((n%2)*pw,(n//2)*ph))
    panel.save(HERE/'styled_singer_four_states.png',optimize=True)
    print('Saving GIF',flush=True)
    frames[0].save(HERE/'styled_singer_native_life.gif',save_all=True,
                   append_images=frames[1:],duration=120,loop=0,optimize=True)
    print('Saving RLE',flush=True)
    pats=HERE.parent/'patterns';pats.mkdir(exist_ok=True)
    (pats/'styled_singer_glider_world.rle').write_text(compact_rle(universe(True),(
        'Conway Made of Maybe singer: oval head, brows, almond eyes and true glider-controlled mouth',
        'All cells preloaded in generation zero. Bubble lyrics still static.',
    )),encoding='utf-8')
    print('Saved four checkpoint contact sheet, six full frames, actual-Life GIF, and Golly RLE')

if __name__=='__main__':main()
