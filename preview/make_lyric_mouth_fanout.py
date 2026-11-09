"""Visualize ACTUAL B3/S23 state for a shared lyric/mouth glider splitter pilot.

The physical universe is never altered. The diagram arranges sampled 2x2
output ports side-by-side for inspection; the labels and UI are NOT Life cells
and the ports occupy their real dispersed positions in the RLE.
"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from PIL import Image, ImageDraw, ImageFont
from life.core import evolve,place
from life.glider_controlled_mouth import BLOCK
from life.lyric_mouth_fanout import (events,universe,mouth_state,
    CLOSED_PORT,OPEN_PORT,CATALYSTS,FINAL_QUALIFICATION_G,GPS)

OUT=Path(__file__).resolve().parent
BG=(8,15,32);PANEL=(19,30,54);WHITE=(235,240,255)
VIOLET=(187,153,255);CYAN=(91,224,238);PINK=(255,129,183)
FONT_DIRS=['/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
           '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf']
try:
    NORMAL=ImageFont.truetype(FONT_DIRS[0],22)
    SMALL=ImageFont.truetype(FONT_DIRS[0],17)
    BOLD=ImageFont.truetype(FONT_DIRS[1],28)
    TITLE=ImageFont.truetype(FONT_DIRS[1],37)
except OSError:
    NORMAL=SMALL=BOLD=TITLE=ImageFont.load_default()

EVENTS=events()


def tile(d,live,pos,cx,cy,accent,size=17):
    px=place(BLOCK,*pos)
    d.rounded_rectangle((cx-24,cy-24,cx+53,cy+53),radius=12,fill=(12,25,48),outline=(62,80,108),width=2)
    on=px<=live
    for x in (0,1):
        for y in (0,1):
            sx=cx+x*(size+2)
            sy=cy+y*(size+2)
            d.rounded_rectangle((sx,sy,sx+size,sy+size),radius=3,
                                fill=accent if (pos[0]+x,pos[1]+y) in live else (40,53,74))
    return on


def apparatus(d,x0,y0,scale=2.6):
    for x,y in CATALYSTS:
        sx=x0+x*scale;sy=y0+y*scale
        d.rectangle((sx,sy,sx+scale*.72,sy+scale*.72),fill=(112,139,199))


def frame(live,g):
    W,H=1180,620
    im=Image.new('RGB',(W,H),BG)
    d=ImageDraw.Draw(im)
    d.text((42,29),'MADE OF MAYBE',fill=WHITE,font=TITLE)
    d.text((43,85),'One Life glider  →  two physical consequences',fill=VIOLET,font=NORMAL)
    d.text((873,35),f'G{g:04d}   {g/GPS:6.3f}s',fill=CYAN,font=BOLD)
    d.rounded_rectangle((34,137,1147,561),radius=22,fill=PANEL)

    # Actual native-Life catalysts are displayed as a magnified tilemap.
    d.text((58,166),'GLIDER DUPLICATOR',fill=CYAN,font=NORMAL)
    apparatus(d,86,224,3)
    d.text((68,429),'84 stationary Life cells',fill=WHITE,font=SMALL)
    d.text((68,453),'4 copies in one universe',fill=(164,176,201),font=SMALL)
    d.line((316,190,316,530),fill=(59,77,106),width=2)

    state=mouth_state(live)
    d.text((345,161),'THREE-STATE MOUTH REGISTER',fill=PINK,font=BOLD)
    d.text((353,222),'CLOSED PORT',fill=(185,197,217),font=SMALL)
    c=tile(d,live,CLOSED_PORT,412,260,PINK)
    d.text((580,222),'OPEN PORT',fill=(185,197,217),font=SMALL)
    o=tile(d,live,OPEN_PORT,635,260,CYAN)
    d.text((783,239),state.upper(),fill=(255,214,227) if state=='closed' else CYAN,font=TITLE)
    d.text((355,340),'Both empty = MEDIUM   ·   C only = CLOSED   ·   O only = OPEN',
           fill=(183,191,212),font=SMALL)
    d.line((343,382,1113,382),fill=(59,77,106),width=2)
    d.text((349,398),'KARAOKE OUTPUT:  ONE VERIFIED 2×2 LYRIC PIXEL PER WORD',fill=VIOLET,font=SMALL)
    for i,e in enumerate(EVENTS):
        x=371+i*185
        d.text((x,443),e.word,fill=WHITE,font=SMALL)
        enabled=tile(d,live,e.word_pixel,x+27,477,VIOLET,size=10)
        d.text((x+77,486),'ON' if enabled else '·',fill=CYAN if enabled else (104,113,134),font=SMALL)
    d.text((43,580),'Actual B3/S23 live-cell occupancy. Ports optically arranged for inspection; no in-simulation cell edits.',
           fill=(158,174,197),font=SMALL)
    return im


def main():
    samples=[0,2152,2156,2164,2196,2200,2204,2212,2268,2272,2280,2292,2296,2304,2320]
    samples=set(samples)
    live=universe()
    saved={}
    for g in range(FINAL_QUALIFICATION_G+1):
        if g in samples: saved[g]=frame(live,g)
        if g<FINAL_QUALIFICATION_G: live=evolve(live)
    panels=[saved[g] for g in (0,2164,2212,2280,2304)]
    # 5 genuine physical checkpoints, arranged as a single presentation sheet.
    width,height=850,450
    contact=Image.new('RGB',(3*width,2*height),BG)
    for i,p in enumerate(panels):
        contact.paste(p.resize((width,height),Image.Resampling.LANCZOS),((i%3)*width,(i//3)*height))
    contact.save(OUT/'lyric_mouth_shared_fanout_five_states.png',optimize=True)
    gif_frames=[saved[g].resize((885,465),Image.Resampling.LANCZOS) for g in sorted(samples)]
    gif_frames[0].save(OUT/'lyric_mouth_shared_fanout.gif',save_all=True,
                       append_images=gif_frames[1:],duration=[650,230,400,550,180,230,500,550,180,530,540,250,580,500,750],
                       optimize=True,loop=0)
    print('Wrote verified optical register preview: five states and GIF')

if __name__=='__main__':main()
