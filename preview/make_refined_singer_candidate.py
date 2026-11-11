"""Optical display of actual Life mouth candidate states, not control overlay."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from PIL import Image,ImageDraw,ImageFont
from life.core import evolve,place
from life.refined_singer_candidate import (
    qualified_layout,new_moving_components,new_target_cells,LIP_DROP_Y)
from life.restored_centerline import START_LINE
from life.glider_controlled_mouth import BLOCK
from preview.make_character_round2 import PALETTE
BG=(7,13,28); W=930;H=950; SX=SY=1.45; OX,OY=460,500
def font(n,bold=False):
    try:return ImageFont.truetype('DejaVuSans-Bold.ttf' if bold else 'DejaVuSans.ttf',n)
    except OSError:return ImageFont.load_default()
def plot(d,cells,color,size=2):
    for x,y in cells:
        px=int(OX+x*SX);py=int(OY+y*SY)
        if 12<px<W-12 and 100<py<H-12:
            d.rectangle((px,py,px+size,py+size),fill=color)
def render(world,art,gen,label):
    im=Image.new('RGB',(W,H),BG);d=ImageDraw.Draw(im)
    d.text((29,20),'MADE OF MAYBE',font=font(28,True),fill=(242,230,252))
    d.text((29,64),f'{label}   /   g{gen}   /   NATIVE B3/S23',
           font=font(16,True),fill=(150,219,205))
    plot(d,(p for p in world if -350<p[0]<350 and -350<p[1]<350),(24,34,56),1)
    for name,cells in art.items():plot(d,cells,PALETTE.get(name,(216,216,228)),3)
    lip=set()
    for state in ('medium','open'):
        lip|=new_target_cells(state)&world
    line=set().union(*(place(BLOCK,x,y+LIP_DROP_Y) for x,y in START_LINE))
    plot(d,lip,(255,119,170),4)
    plot(d,line&world,(255,205,153),4)
    d.text((28,H-34),'STYLE CANDIDATE / WORD-CAUSAL REROUTE PENDING',
           font=font(13),fill=(149,163,196))
    return im
def main():
    art=qualified_layout()['art'];world=set().union(*new_moving_components().values())
    samples={60:'REST / CLOSED',180:'MEDIUM',288:'OPEN',420:'MEDIUM',960:'RESTORED CLOSED'}
    shots={}
    for g in range(max(samples)+1):
        if g in samples:shots[g]=render(world,art,g,samples[g])
        if g<max(samples):world=evolve(world)
    dest=Path('preview/refined_singer_qualified_candidate.png')
    cw,ch=570,580;out=Image.new('RGB',(cw*2,ch*2),BG)
    for i,g in enumerate((60,180,288,960)):
        out.paste(shots[g].resize((cw,ch),Image.Resampling.LANCZOS),
                  ((i%2)*cw,(i//2)*ch))
    dest.parent.mkdir(parents=True,exist_ok=True)
    out.save(dest,optimize=True)
    shots[288].save('preview/refined_singer_open_closeup.png',optimize=True)
    print('Created',dest)
if __name__=='__main__':main()
