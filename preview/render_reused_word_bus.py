"""Inspection only: two sung WE onsets occupy one REAL Conway glyph location.

All displayed colored cells come from native B3/S23 evolution. The graphic
uses separate optical crops for the singer and the single glyph sink; these
are not adjacent in the actual physical world. The remaining full lettering
is NOT reconstructed by this narrow two-line hardware pilot.
"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from PIL import Image,ImageDraw,ImageFont
from life.core import evolve,place
from life.first_line_singing_character import safe_art
from life.physical_lip_splitter_bridge import SINGER_TRANSLATION,WORD_PIXEL
from life.reusable_word_cue import character_world_with_second_lip,line_times,SECOND_LIP_GLOBAL
from life.glider_controlled_mouth import BLOCK
from preview.make_character_round2 import PALETTE

ROOT=Path(__file__).resolve().parents[1]
W,H=1360,980
BG=(7,11,23)
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
def font(size,bold=False):
    path='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf' if bold else FONT
    return ImageFont.truetype(path,size)


def render(path=ROOT/'preview/reused_word_bus_two_lines.png'):
    times=line_times();wanted=[times[0][0],times[0][1],times[1][0],times[1][1]]
    still={};live=character_world_with_second_lip()
    for g in range(wanted[-1]+1):
        if g in wanted:still[g]=set(live)
        if g<wanted[-1]:live=evolve(live)
    art=safe_art()
    canvas=Image.new('RGB',(W,H),BG);d=ImageDraw.Draw(canvas)
    d.text((27,16),'ONE SPLITTER. TWO SONG LINES. TWO REAL LIP ACTIONS.',font=font(23,True),fill=(240,222,248))
    d.text((28,48),'Original singer protected; first WE pixel reused at its exact native B3/S23 coordinates',font=font(15),fill=(167,191,219))
    notes=[('FIRST WE / WORD ON',True),('FIRST LINE / ERASED',False),('SECOND WE / WORD ON',True),('SECOND LINE / ERASED',False)]
    for i,g in enumerate(wanted):
        col=i%2;row=i//2
        left=25+col*672;top=92+row*438
        right=left+640;bottom=top+408
        d.rounded_rectangle((left,top,right,bottom),radius=14,fill=(16,22,43),outline=(55,70,102),width=2)
        note,expected=notes[i]
        d.text((left+18,top+12),note,font=font(18,True),fill=(128,238,205) if expected else (242,169,188))
        d.text((left+18,top+39),f'g={g}     audio={g/192:.3f}s',font=font(14),fill=(183,197,220))
        pixels=still[g]
        ax,ay=SINGER_TRANSLATION
        xoff=left+207;yoff=top+226
        sx=.45;sy=.45
        # Singer face stays the source's authentic Life art, not an AI drawing.
        for x,y in pixels:
            xx=x-ax;yy=y-ay
            if -395<xx<395 and -415<yy<400:
                u=xoff+int(xx*sx);v=yoff+int(yy*sy)
                if left+4<u<left+405 and top+65<v<bottom-8:
                    d.rectangle((u,v,u+1,v+1),fill=(238,119,170))
        for name,cells in art.items():
            color=PALETTE.get(name,(210,212,239))
            for xx,yy in cells:
                if -395<xx<395 and -415<yy<400:
                    u=xoff+int(xx*sx);v=yoff+int(yy*sy)
                    if left+4<u<left+405 and top+65<v<bottom-8:
                        d.rectangle((u,v,u+2,v+2),fill=color)
        # Optical zoom of EXACT SAME 2x2 lyric anchor in both lines.
        bx=left+438;by=top+121
        d.rounded_rectangle((bx-13,by-31,bx+170,by+166),radius=9,fill=(23,33,54),outline=(87,96,139),width=1)
        d.text((bx,by-25),'GLYPH ANCHOR',font=font(12,True),fill=(208,224,244))
        d.text((bx,by-5),'same cell (0,0)',font=font(11),fill=(155,174,198))
        block=place(BLOCK,*WORD_PIXEL)
        on=block<=pixels
        # a 14x14 raw Life-cell crop enlarged to exact rectangular pixels
        for x,y in pixels:
            if -6<=x<=7 and -6<=y<=7:
                ux=bx+12+(x+6)*8;vy=by+24+(y+6)*8
                d.rectangle((ux,vy,ux+6,vy+6),fill=(112,246,213))
        d.text((bx,by+150),'ON' if on else 'OFF',font=font(16,True),fill=(112,246,213) if on else (246,165,178))
        if i==2:
            d.text((left+18,bottom-29),'SECOND LIP TILE: waiting for causal ERASE at g3152',font=font(11),fill=(188,192,234))
        elif i==3:
            d.text((left+18,bottom-29),'SECOND LIP TILE: erased by the SAME WORD SOURCE',font=font(11),fill=(188,192,234))
        if on!=expected:
            raise AssertionError(f'wrong native anchor occupancy at g{g}: {on} != {expected}')
    d.text((28,H-29),'CAMERA CROPS ONLY  |  One unchanged Life universe  |  Complete 403-word and three-state lip fanout still pending',
           font=font(13),fill=(163,182,202))
    path.parent.mkdir(parents=True,exist_ok=True);canvas.save(path,optimize=True)
    print('Wrote',path,'bytes',path.stat().st_size)
    return path

if __name__=='__main__':render()
