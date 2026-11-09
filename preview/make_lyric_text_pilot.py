"""Render exact native Life frames for 4 physically switched lyric progress lamps.

UI clock/word labels and cell color choices are presentation-only; the lyrics
in this experiment are physically STABLE. Lamps are actual native glider
collisions, not timed renderer insertions. Suno audio is not included.

Requires Pillow, numpy, scipy; runs with: python preview/make_lyric_text_pilot.py
"""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import numpy as np
from scipy.ndimage import convolve
from PIL import Image,ImageDraw,ImageFont
from life.lyric_text_pilot import components,LAMPS,universe,lamp_target
from life.lyric_cues import read_alignment,aligned_words,caption_pages
from life.export_operational import compact_rle

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'preview'
PAT=ROOT/'patterns';PAT.mkdir(exist_ok=True)
DATA=ROOT/'data'
(LIFE:=PAT/'first_lyric_glider_progress.rle').write_text(
    compact_rle(universe(),(
        'MadeOfMaybe Suno word cue proof: stable Life text, native glider-controlled 4-word progress lights',
        '24 Life generations/second; WE 268, MADE 276, A 284, WINDOW 288; all erase 326',
        'No runtime cell edits. The full caption is not dynamically constructed/removed yet.'
    )),encoding='utf-8')

parts=components()
face_art=set().union(*(v for key,v in parts.items() if key.startswith('art_')))
hair=set().union(*(v for key,v in parts.items() if 'hair' in key))
frame=parts['bubble_outline'];text=parts['caption_stable_5x7']
progress_targets=set().union(*(lamp_target(l) for l in LAMPS))
# Fixed crop of the actual universe. Only visible region is drawn; Life still
# evolves across a larger, padded, single board with all gliders intact.
LEFT,TOP=-500,-600
W,H=1700,1250
K=np.ones((3,3),dtype=np.uint8);K[1,1]=0
world=np.zeros((H,W),dtype=np.uint8)
for x,y in universe():world[y-TOP,x-LEFT]=1

def step(z):
    n=convolve(z,K,mode='constant',cval=0)
    return np.asarray((n==3)|((z>0)&(n==2)),dtype=np.uint8)

try:
    title=ImageFont.truetype('DejaVuSans-Bold.ttf',29)
    label=ImageFont.truetype('DejaVuSans.ttf',19)
    small=ImageFont.truetype('DejaVuSans.ttf',15)
except OSError:
    title=label=small=ImageFont.load_default()

BACKGROUND=(12,18,32)
PAPER=(223,237,247)
PLUM=(179,137,226)
WARM=(250,201,125)
INK=(166,236,226)
CORAL=(255,143,171)

# Same Life pixels, two presentation crops: stage and bubble close-up.
def draw_state(grid,g,closeup=False):
    if closeup:
        width,height=960,670
        x0,y0,scale=234,-205,2.57
    else:
        width,height=1320,815
        x0,y0,scale=-360,-390,1.38
    canvas=Image.new('RGB',(width,height),BACKGROUND)
    d=ImageDraw.Draw(canvas)
    d.text((30,15),'MADE OF MAYBE  /  LYRIC SIGNAL PILOT',font=title,fill=PAPER)
    d.text((30,60),f'{g/24:06.3f}s  •  generation {g}  •  B3/S23',font=label,fill=WARM)
    xmin=max(LEFT,int(x0-10));xmax=min(LEFT+W,int(x0+width/scale+10))
    ymin=max(TOP,int(y0-10));ymax=min(TOP+H,int(y0+height/scale+10))
    region=grid[ymin-TOP:ymax-TOP, xmin-LEFT:xmax-LEFT]
    yy,xx=np.nonzero(region)
    psize=max(2,round(scale+.55))
    for dx,dy in zip(xx,yy):
        x=dx+xmin;y=dy+ymin
        p=(int((x-x0)*scale),int((y-y0)*scale))
        if p[0]<0 or p[1]<0 or p[0]>=width or p[1]>=height:continue
        if (x,y) in progress_targets:color=CORAL
        elif (x,y) in text:color=WARM
        elif (x,y) in frame:color=INK
        elif (x,y) in hair:color=PLUM
        else:color=PAPER
        d.rectangle((p[0],p[1],p[0]+psize-1,p[1]+psize-1),fill=color)
    statuses=['●' if all(grid[y-TOP,x-LEFT] for x,y in lamp_target(l)) else '○' for l in LAMPS]
    txt='   '.join(f'{name} {v}' for (name,v) in zip((lamp.word for lamp in LAMPS),statuses))
    d.rectangle((18,height-58,width-18,height-17),fill=(23,33,50))
    d.text((29,height-52),txt,font=label,fill=CORAL)
    d.text((width-250,61),'TIMING ONLY · NO AUDIO',font=small,fill=INK)
    return canvas

saves={}
frames=[]
for g in range(350):
    if g in (264,268,276,284,288,326,342):
        saves[g]=draw_state(world,g,closeup=True)
    if 250<=g<=344 and g%2==0:
        frames.append(draw_state(world,g).resize((1056,652),Image.Resampling.NEAREST))
    world=step(world)

frames[0].save(OUT/'first_lyric_native_cues.gif',save_all=True,
               append_images=frames[1:],duration=83,loop=0,optimize=True)
labels=[264,268,276,288,326,342]
contact=Image.new('RGB',(3*960,2*670),BACKGROUND)
for i,g in enumerate(labels):contact.paste(saves[g],((i%3)*960,(i//3)*670))
contact.save(OUT/'first_lyric_progress_contact_sheet.png',optimize=True)
saves[288].save(OUT/'first_lyric_progress_all_four.png',optimize=True)
print('Rendered one continuous Life universe through g349; GIF, contact sheet, RLE.')
