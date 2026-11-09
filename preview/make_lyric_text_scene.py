"""First real 7-word native lyric controller — two fixed Life caption pages.

The whole Life universe advances; only the *camera crop* changes after the
second caption's first word. All cyan/amber/pink squares are actual B3/S23
cells. Page label, timecode and indicator legend are presentation overlays.

Requires Pillow, no other rendering dependencies.
Usage: python preview/make_lyric_text_scene.py
"""
from __future__ import annotations
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from PIL import Image,ImageDraw,ImageFont
from life.core import evolve
from life.lyric_text_scene import (
    components,universe,ALL_LAMPS,selected_page,caption_by_page,
)
from life.export_operational import compact_rle
from life.lyric_text_pilot import lamp_target

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'preview';PAT=ROOT/'patterns';PAT.mkdir(exist_ok=True)
(PAT/'seven_word_glider_timed_captions.rle').write_text(
    compact_rle(universe(),(
        'Seven words of MadeOfMaybe; two static caption pages and 7 physically controlled word lamps.',
        '24 Life generations per second; all gliders at gen 0, fixed B3/S23.',
        'Camera selected preview only; lyrics do not yet change dynamically.',
    )),encoding='utf-8')

INK=(224,245,239);YELLOW=(252,199,117);PINK=(255,120,158);GLIDER=(174,153,239)
BG=(12,19,32);PANEL=(17,28,43);BORDER=(95,192,172);SUB=(146,162,177)
fontdir='/usr/share/fonts/truetype/dejavu/'
try:
    title=ImageFont.truetype(fontdir+'DejaVuSans-Bold.ttf',29)
    body=ImageFont.truetype(fontdir+'DejaVuSans.ttf',17)
    small=ImageFont.truetype(fontdir+'DejaVuSans.ttf',15)
except OSError:
    title=body=small=ImageFont.load_default()

PARTS=components()
frame=(PARTS['bubble_outline'],PARTS['bubble_2_outline'])
lyrics=(PARTS['caption_stable_5x7'],PARTS['bubble_2_caption_5x7'])
all_targets=set().union(*(lamp_target(l) for l in ALL_LAMPS))
SCALE=3.05
W,H=1090,740
CAMERA_X=(225,825)
CAMERA_Y=-195
HEADER=120


def render(world,gen,page=None):
    if page is None: page=selected_page(gen)
    image=Image.new('RGB',(W,H),BG)
    d=ImageDraw.Draw(image)
    d.text((40,20),'MADE OF MAYBE  /  NATIVE LYRIC TIMING',font=title,fill=INK)
    d.text((42,67),f'{gen/24:06.3f}s  /  Life generation {gen:04d}  /  page {page+1} of 2',
           font=body,fill=SUB)
    d.rectangle((25,105,W-25,650),fill=PANEL)
    boxx=CAMERA_X[page]
    xmin,xmax=boxx,boxx+350
    ymin,ymax=CAMERA_Y,CAMERA_Y+179
    visible=[(x,y) for x,y in world if xmin<=x<xmax and ymin<=y<ymax]
    fixed_border=frame[page];fixed_words=lyrics[page]
    for x,y in visible:
        px=30+int((x-xmin)*SCALE)
        py=120+int((y-ymin)*SCALE)
        if (x,y) in all_targets:
            color=PINK
        elif (x,y) in fixed_words:
            color=YELLOW
        elif (x,y) in fixed_border:
            color=BORDER
        else:
            color=GLIDER
        cell=max(2,round(SCALE))
        d.rectangle((px,py,px+cell-1,py+cell-1),fill=color)
    shown=ALL_LAMPS[:4] if page==0 else ALL_LAMPS[4:]
    statuses=[]
    for l in shown:
        active=lamp_target(l)<=world
        statuses.append(f'{l.word}:{"ON" if active else "off"}')
    d.text((40,671),'  |  '.join(statuses),font=body,fill=PINK)
    d.text((40,707),'Only the pink cue pixels toggle. Text is stable Life; camera page selection is a preview edit.',
           font=small,fill=SUB)
    return image


def main():
    cells=universe()
    samples={}
    frames=[]
    gens=(260,268,276,288,300,304,308,312,320,326,342)
    for gen in range(350):
        if gen in gens:
            samples[gen]=render(cells,gen)
        if 260<=gen<=338 and gen%2==0:
            frames.append(render(cells,gen).resize((872,592),Image.Resampling.NEAREST))
        cells=evolve(cells)
    frames[0].save(OUT/'seven_word_native_life_cues.gif',save_all=True,
                   append_images=frames[1:],duration=84,loop=0,optimize=True)
    chosen=(268,288,304,312,326,342)
    sheet=Image.new('RGB',(2*W,3*H),BG)
    for i,g in enumerate(chosen):
        sheet.paste(samples[g],((i%2)*W,(i//2)*H))
    sheet.save(OUT/'seven_word_cue_contact_sheet.png',optimize=True)
    samples[312].save(OUT/'seven_word_second_page.png',optimize=True)
    print('Rendered 7 native glider word cues over 2 static caption pages, RLE and GIF.')

if __name__=='__main__':main()
