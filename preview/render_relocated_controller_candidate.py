"""Display face, speech bubble and relocated controller at their REAL Life coordinates."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from PIL import Image,ImageDraw,ImageFont
from life.core import evolve,place
from life.glider_controlled_mouth import BLOCK,rotate
from life.relocated_singer_anchor import (
    RELOCATED_SPLITTER_LOCAL,RELOCATED_GLYPH_ORIGIN,relocated_anchor,qualified_integration)
from life.refined_singer_candidate import qualified_layout,new_moving_components,new_target_cells,LIP_DROP_Y
from life.physical_lip_splitter_bridge import SINGER_TRANSLATION
from life.composition import bubble_parts
from life.lyric_mouth_fanout import CATALYSTS
from life.restored_centerline import START_LINE
from preview.make_character_round2 import PALETTE
W,H=1550,1160;BG=(7,13,28);SCALE=1.6;OX,OY=586,570
def font(n,bold=False):
    try:return ImageFont.truetype('DejaVuSans-Bold.ttf' if bold else 'DejaVuSans.ttf',n)
    except OSError:return ImageFont.load_default()
def mark(d,cells,fill,size=2):
    for x,y in cells:
        px=round(OX+x*SCALE);py=round(OY+y*SCALE)
        if 3<px<W-3 and 105<py<H-8:
            d.rectangle((px,py,px+size,py+size),fill=fill)
def frame(gen,anchor,moving,art,bubble):
    im=Image.new('RGB',(W,H),BG);d=ImageDraw.Draw(im)
    d.text((35,19),'MADE OF MAYBE',font=font(30,True),fill=(241,227,250))
    d.text((37,61),f'ONE NATIVE WORLD / g{gen} / SINGER + BUBBLE + MOVED SPLITTER',
           font=font(16),fill=(149,212,200))
    local_anchor=place(anchor,-SINGER_TRANSLATION[0],-SINGER_TRANSLATION[1])
    mark(d,local_anchor|moving,(25,38,58),1)
    mark(d,bubble,(197,212,240),3)
    for k,cells in art.items():mark(d,cells,PALETTE.get(k,(220,227,243)),3)
    lips=set().union(*(new_target_cells(state)&moving for state in ('medium','open')))
    mark(d,lips,(250,121,172),4)
    closed=set().union(*(place(BLOCK,x,y+LIP_DROP_Y) for x,y in START_LINE))
    mark(d,closed&moving,(247,207,169),4)
    actual_catalysts=place(rotate(CATALYSTS,2),*RELOCATED_SPLITTER_LOCAL)
    mark(d,actual_catalysts&local_anchor,(119,248,208),4)
    px=round(OX+375*SCALE);py=round(OY+210*SCALE)
    d.text((px+8,py+3),'PHYSICAL 84-CELL SPLITTER',font=font(14,True),fill=(142,239,212))
    on=place(BLOCK,*RELOCATED_GLYPH_ORIGIN)<=anchor
    d.rounded_rectangle((1110,870,1500,1065),radius=15,fill=(17,28,51),outline=(75,104,128),width=2)
    d.text((1130,893),'RELOCATED NATIVE WORD PIXEL',font=font(15,True),fill=(189,228,228))
    d.text((1130,926),'Actual Life coordinate: '+str(RELOCATED_GLYPH_ORIGIN),
           font=font(13),fill=(166,189,215))
    d.text((1130,963),'WE: '+'PRESENT' if on else 'WE: ABSENT',
           font=font(23,True),fill=(111,236,201) if on else (245,157,181))
    d.text((1130,1011),'Lip movement not yet word-driven',font=font(12),fill=(145,160,186))
    return im
def main():
    qualified_integration()
    art=qualified_layout()['art']
    border,words=bubble_parts();bubble=place(border|words,160,-90)
    anchor=relocated_anchor();moving=set().union(*new_moving_components().values())
    shots={}
    for gen in range(2157):
        if gen in (288,2156):shots[gen]=frame(gen,anchor,moving,art,bubble)
        if gen<2156:anchor=evolve(anchor);moving=evolve(moving)
    dest=Path('preview/relocated_controller_real_life.png')
    dest.parent.mkdir(parents=True,exist_ok=True)
    shots[288].save(dest,optimize=True)
    shots[2156].save(dest.with_name('relocated_controller_word_on.png'),optimize=True)
    print('Wrote real-coordinate controller camera',dest)
if __name__=='__main__':main()
