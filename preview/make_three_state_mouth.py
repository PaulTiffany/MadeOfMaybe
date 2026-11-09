"""Render the three separate B3/S23 stable mouth *targets*.

This is a three-alternative-state contact sheet; NOT a switched Life run.
"""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from PIL import Image,ImageDraw,ImageFont
from life.core import encode_rle
from life.three_state_mouth import STATES, FACE, mouth, scene

OUT=Path(__file__).resolve().parent
PATTERNS=OUT.parent/'patterns';PATTERNS.mkdir(exist_ok=True)
C=(13,21,33);BG=(21,32,46);INK=(231,243,238);LIP=(243,158,168);ACCENT=(125,199,185)
try:
    FONT=ImageFont.truetype('DejaVuSans.ttf',22)
    LABEL=ImageFont.truetype('DejaVuSans-Bold.ttf',35)
    SUB=ImageFont.truetype('DejaVuSans.ttf',19)
except OSError:
    FONT=LABEL=SUB=ImageFont.load_default()

W,H=580,955
CANVAS=Image.new('RGB',(3*W,H),C)

def draw_cells(draw,cells,origin,scale,color):
    ox,oy=origin
    for x,y in cells:
        X=int(ox+x*scale);Y=int(oy+y*scale)
        ww=max(1,int(scale))
        draw.rectangle((X,Y,X+ww-1,Y+ww-1),fill=color)

for i,name in enumerate(STATES):
    pane=Image.new('RGB',(W,H),BG)
    d=ImageDraw.Draw(pane)
    d.text((28,20),name.upper(),fill=INK,font=LABEL)
    description={'closed':'Quiet / consonants','medium':'Ordinary syllables',
                 'open':'Sustained vowels'}[name]
    d.text((30,73),description,fill=ACCENT,font=SUB)
    scale=2.28
    ox,oy=W/2,350
    draw_cells(d, FACE, (ox,oy),scale,INK)
    draw_cells(d, mouth(name),(ox,oy),scale,LIP)
    d.line((30,690,W-30,690),fill=(67,83,101),width=2)
    d.text((30,702),'MOUTH — ACTUAL LIVE CELLS',fill=ACCENT,font=SUB)
    mout=mouth(name)
    scale2=3.3
    lip_center_x=0
    lip_center_y=9*4
    draw_cells(d,mout,(W/2-lip_center_x*scale2,824-lip_center_y*scale2),
               scale2,LIP)
    CANVAS.paste(pane,(i*W,0))
    (PATTERNS/f'singer_mouth_{name}_stable.rle').write_text(
        encode_rle(scene(name),[
            f'MadeOfMaybe face with {name.upper()} Life-stable mouth pose',
            'This is a static pose target, not a glider-controlled transition.',
            'B3/S23 only. Each live pixel is an actual 2x2 Life block.',
        ]),encoding='utf-8')

CANVAS.save(OUT/'three_state_mouth_contact_sheet.png',optimize=True)
print('Rendered three genuine stable Life mouth poses, exported 3 RLEs.')
