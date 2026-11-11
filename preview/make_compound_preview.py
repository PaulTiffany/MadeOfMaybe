"""Render only genuinely simulated B3/S23 cells; Pillow for presentation only.

python preview/make_compound_preview.py
The GIF is accelerated for review and is NOT synchronized to the song.
"""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from PIL import Image, ImageDraw, ImageFont
from life.core import evolve, encode_rle
from life.composition import components, scene
from life.catalog import CATALOG, pattern
from life.singer_pilot import MOUTH_BLOCK

OUT=Path(__file__).resolve().parent
PATTERNS=OUT.parent/'patterns'
OUT.mkdir(exist_ok=True,parents=True)
PATTERNS.mkdir(exist_ok=True,parents=True)

COLORS={'mouth_actuator':'#2f8977','face':'#5cdbbd',
        'bubble_outline':'#d2ddf6','bubble_lyrics':'#ffd58b',
        'pulsar':'#e68ebf'}
DARK='#09101f'; PALE='#d9e4fb'; MUTED='#9baac7'; BOLD='#f8dba6'
try:
    font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',18)
    small=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',14)
    heavy=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',24)
except OSError:
    font=small=heavy=ImageFont.load_default()

W,H=1500,760
SCALE=3; X0,Y0=-55,-100; OX,OY=80,130

def draw_scene(parts,gen):
    im=Image.new('RGB',(W,H),DARK)
    d=ImageDraw.Draw(im)
    d.text((80,44),'MADE OF MAYBE',font=heavy,fill=PALE)
    d.text((80,78),'One B3/S23 universe · constant clock · no frame swaps',font=small,fill=MUTED)
    for name,color in COLORS.items():
        for x,y in parts[name]:
            px,py=OX+(x-X0)*SCALE,OY+(y-Y0)*SCALE
            if 0<=px<W-2 and 0<=py<H-2:
                d.rectangle((px,py,px+SCALE-1,py+SCALE-1),fill=color)
    active=MOUTH_BLOCK.issubset(parts['mouth_actuator'])
    d.line((80,690,1420,690),fill='#39465e',width=1)
    d.text((80,711),f'GEN {gen:03d}',font=font,fill=BOLD)
    d.text((265,711),f'MOUTH TOGGLE: {"ON" if active else "OFF"}',
           font=font,fill=BOLD if active else MUTED)
    d.text((695,711),'CYAN: singer   •   GOLD: words   •   ROSE: pulsar',
           font=small,fill=MUTED)
    return im

parts=components()
frames=[];keyframes={}
for gen in range(611):
    if gen%16==0 or gen in (170,362,554):
        shot=draw_scene(parts,gen)
        if gen%16==0:
            frames.append(shot.resize((1125,570),Image.Resampling.NEAREST))
        if gen in (170,362,554):
            keyframes[gen]=shot
    parts={name:evolve(cells) for name,cells in parts.items()}

frames[0].save(OUT/'singer_bubble_life.gif',save_all=True,
               append_images=frames[1:],duration=140,loop=0,optimize=True)
for gen,shot in keyframes.items():
    shot.save(OUT/f'singer_bubble_gen{gen}.png',optimize=True)

rle=encode_rle(scene(),[
    'MadeOfMaybe singer + stable bubble + pulsar; 3 preloaded signal gliders',
    'Actuator Luke Kiernan (2023) https://conwaylife.com/wiki/Glider_to_block'
])
(PATTERNS/'singer_bubble_pulsar.rle').write_text(rle,encoding='utf-8')

# This is an audition CONTACT SHEET, not a four-pattern composed universe.
names=['pulsar','heart','smiley','gosper_gun']
CW,CH=520,390
sheet=Image.new('RGB',(CW*2,CH*2),DARK)
for i,name in enumerate(names):
    cells=pattern(name)
    panel=Image.new('RGB',(CW,CH),DARK)
    d=ImageDraw.Draw(panel)
    d.text((26,18),name.replace('_',' ').upper(),font=heavy,fill=PALE)
    meta=CATALOG[name]
    d.text((26,56),f"{meta['kind']} · period {meta['period']}",
           font=small,fill=MUTED)
    d.text((26,320),meta['lyric'],font=small,fill=BOLD)
    for _ in range(90 if name=='gosper_gun' else meta['period']-1):
        cells=evolve(cells)
    xs=[x for x,y in cells];ys=[y for x,y in cells]
    xmin,xmax=min(xs),max(xs);ymin,ymax=min(ys),max(ys)
    scale=max(3,min(13,min(440//(xmax-xmin+1),220//(ymax-ymin+1))))
    xo=260-(xmax-xmin+1)*scale//2
    yo=190-(ymax-ymin+1)*scale//2
    for x,y in cells:
        px=xo+(x-xmin)*scale;py=yo+(y-ymin)*scale
        d.rectangle((px,py,px+scale-1,py+scale-1),
                    fill=['#e7a8ef','#e28a9f','#7edbc9','#a7c5ff'][i])
    sheet.paste(panel,((i%2)*CW,(i//2)*CH))
sheet.save(OUT/'symbol_auditions.png',optimize=True)
print('Wrote GIF, 3 checkpoint PNGs, symbol auditions PNG, and RLE.')
