"""Causal inspection of one physical word/lip fanout, from raw Life cells.

Each column is one identical seed except for the single source glider.
Art is drawn from identical protected static 2x2 Life still lifes, NOT a
painted face. Detail insets magnify actual B3/S23 live cells only.
"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from PIL import Image,ImageDraw,ImageFont
from life.core import evolve,place
from life.physical_lip_splitter_bridge import (
    bridge_unit_seed, SINGER_TRANSLATION, LIP_TARGET, word_and_lip_at)
from life.first_line_singing_character import safe_art
from life.glider_controlled_mouth import BLOCK
from preview.make_character_round2 import PALETTE

W=1380;H=1230
BG=(9,13,26)
CHECKS=[(2156,'WE starts / lyric pixel constructed'),
        (2312,'Shared source erases one real lip tile'),
        (2578,'Lyric cleared / original lips restored')]
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
def font(px):return ImageFont.truetype(FONT,px)

def plot_cell(d,x,y,transform,color,size=2):
    X,Y=transform(x,y)
    if 0<=X<W and 0<=Y<H:d.rectangle((X,Y,X+size,Y+size),fill=color)

def paint(world,art,g,source,frame,loc_x,loc_y):
    d=ImageDraw.Draw(frame)
    left=loc_x;top=loc_y
    d.rounded_rectangle((left,top,left+652,top+357),radius=10,
                         outline=(77,85,127),fill=(12,18,36),width=2)
    d.text((left+14,top+12),('SOURCE PRESENT' if source else 'SOURCE ABLATED'),
           font=font(17),fill=(111,235,206) if source else (247,164,177))
    d.text((left+14,top+37),f'g = {g}  |  {g/192:.3f} s',font=font(14),fill=(159,169,195))
    # Actual current character region, with the original portrait translation undone.
    ax,ay=SINGER_TRANSLATION
    def wholeface(x,y):return (int(left+173+x*.49),int(top+191+y*.49))
    for x,y in world:
        xx=x-ax;yy=y-ay
        if -300<xx<300 and -310<yy<320:
            plot_cell(d,xx,yy,wholeface,(53,56,82),1)
    for key,cells in art.items():
        color=PALETTE.get(key,(222,228,239))
        for x,y in cells:plot_cell(d,x,y,wholeface,color,1)
    # Inset: exact mouth tile. Deliberately shows unfiltered raw B3/S23 cells.
    zoom_x=left+352;zoom_y=top+99
    d.rounded_rectangle((zoom_x-8,zoom_y-30,zoom_x+278,zoom_y+115),radius=9,
                         fill=(22,27,48),outline=(92,80,124),width=1)
    d.text((zoom_x,zoom_y-26),'LOWER-LIP PIXEL (NATIVE LIFE)',font=font(12),fill=(226,205,230))
    lx,ly=LIP_TARGET
    for xx,yy in world:
        if -15<=xx-ax-lx<=15 and -9<=yy-ay-ly<=9:
            px=zoom_x+(xx-ax-lx+15)*8;py=zoom_y+(yy-ay-ly+9)*5
            d.rectangle((px,py,px+6,py+4),fill=(246,148,198))
    d.rectangle((zoom_x+15*8-2,zoom_y+9*5-3,zoom_x+16*8+12,zoom_y+10*5+7),
                outline=(250,225,141),width=2)
    w,lip=word_and_lip_at(world)
    d.text((left+353,top+220),f'WE glyph pixel: {"LIVE" if w else "ABSENT"}',
           font=font(16),fill=(129,226,204) if w else (210,156,170))
    d.text((left+353,top+250),f'Lip pixel: {"LIVE" if lip else "ABSENT"}',
           font=font(16),fill=(129,226,204) if lip else (210,156,170))
    d.text((left+353,top+294),'Visual emphasis is camera-only.',
           font=font(12),fill=(143,158,183))


def main():
    art=safe_art()
    alive=bridge_unit_seed(source_enabled=True)
    ablated=bridge_unit_seed(source_enabled=False)
    stills={}
    for g in range(CHECKS[-1][0]+1):
        if g in {k for k,_ in CHECKS}:
            stills[g]=(set(alive),set(ablated))
        if g<CHECKS[-1][0]:
            alive=evolve(alive)
            ablated=evolve(ablated)
    im=Image.new('RGB',(W,H),BG);d=ImageDraw.Draw(im)
    d.text((35,19),'ONE PHYSICAL SOURCE  /  REAL KARAOKE GLYPH + EXISTING LIP TILE',
           font=font(24),fill=(233,224,247))
    d.text((35,52),'Finite-horizon causal ablation; B3/S23; original facial art retained',
           font=font(15),fill=(177,188,209))
    for row,(g,label) in enumerate(CHECKS):
        y=90+row*377
        d.text((35,y-13),f'{row+1:02}.  {label}',font=font(17),fill=(239,188,226))
        A,B=stills[g]
        paint(A,art,g,True,im,22,y+18)
        paint(B,art,g,False,im,707,y+18)
    out=Path('preview/real_lip_shared_signal_ablation.png');out.parent.mkdir(parents=True,exist_ok=True)
    im.save(out,optimize=True)
    print('Created',out, 'bytes',out.stat().st_size)

if __name__=='__main__':main()
