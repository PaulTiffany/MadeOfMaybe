"""Character round 2: real Life hair, moving eyebrow accent, and wink.

No frames are swapped into the simulation: we render unmodified B3/S23
steps. Camera palette and framing are presentation only.

Run: python preview/make_character_round2.py
"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from PIL import Image,ImageDraw,ImageFont,ImageFilter
from life.core import evolve, place
from life.character_round2 import components,universe,BROW_ROUTES,WINK_ROUTES,QUALIFICATION_END
from life.glider_controlled_mouth import BLOCK
from life.symmetric_full_mouth import target_blocks
from life.expressive_mouth import START_LINE
from life.export_operational import compact_rle

HERE=Path(__file__).resolve().parent
BG=(7,13,28)
PALETTE={
 'art_contour':(224,231,238),
 'art_hair_mass':(141,123,199),
 'art_hair_waves':(197,158,229),
 'art_hair_gloss':(239,213,255),
 'art_brows':(255,175,202),
 'art_eye_liner':(236,232,245),
 'art_iris':(132,231,223),
 'art_nose':(228,181,180),
 'art_cheekbones':(247,144,176),
 'art_lashes':(253,208,223),
 'art_jewelry':(245,203,130),
 'left_eye_glint':(255,245,217),
 'right_eye_glint':(255,245,217),
}
BROW=(255,196,213)
WINK=(115,243,229)
MOUTH=(255,128,169)
CLOSED=(255,201,164)
try:
  FONT=ImageFont.truetype('DejaVuSans-Bold.ttf',24)
  SMALL=ImageFont.truetype('DejaVuSans.ttf',17)
except OSError:
  FONT=SMALL=ImageFont.load_default()

# Set full head and shoulder-length locks inside the camera; both axes use a
# constant proportional relationship throughout the film. No shape warping.
W,H=1000,1020
SX=SY=1.43
OX,OY=486,526


def dotdraw(d,cells,col,rad=0):
    for x,y in cells:
        X,Y=int(OX+x*SX),int(OY+y*SY)
        if -5<X<W+5 and -5<Y<H+5:
            d.rectangle((X,Y,X+max(2,int(SX))+rad,Y+max(2,int(SY))+rad),fill=col)


MOUTH_TILES={state:[place(BLOCK,x,y) for x,y in sorted(target_blocks(state))
           if (x-1,y) not in target_blocks(state) and (x,y-1) not in target_blocks(state)]
             for state in ('medium','open')}
LINE_TILES=[place(BLOCK,*xy) for xy in START_LINE]


def draw_portrait(world,parts,gen,caption=None):
    im=Image.new('RGB',(W,H),BG);d=ImageDraw.Draw(im)
    # Every plotted point corresponds to a live Life cell. The background
    # gliders are intentionally dim but are NOT omitted from the universe.
    dotdraw(d,world,(24,38,55))
    for key,col in PALETTE.items():
        if key in parts:dotdraw(d,parts[key],col,rad=1)
    # Signal endpoints live in the actual world; only complete 2x2 blocks
    # receive their visual highlight. No artificial on/off editing.
    for xy,*_ in BROW_ROUTES:
        tile=place(BLOCK,*xy)
        if tile<=world:dotdraw(d,tile,BROW,rad=2)
    for xy,*_ in WINK_ROUTES:
        tile=place(BLOCK,*xy)
        if tile<=world:dotdraw(d,tile,WINK,rad=1)
    active=set()
    for tiles in MOUTH_TILES.values():
        for tile in tiles:
            if tile<=world:active |=tile
    line=set()
    for tile in LINE_TILES:
        if tile<=world:line |=tile
    dotdraw(d,active,MOUTH,rad=2)
    dotdraw(d,line,CLOSED,rad=2)
    if caption:
        d.rectangle((20,17,400,63),fill=BG)
        d.text((30,23),caption,font=FONT,fill=(222,230,242))
    return im


def main():
    world=universe(False)
    parts=components(False)
    chosen={60:'Rest / closed',180:'Soft vocal',288:'Open + brow lift',
            420:'Medium + brow lift',540:'Wink / breath',
            680:'Open again',960:'Restored closed'}
    snapshots={};gif=[];frame_gens=(0,60,120,180,224,256,288,356,420,480,520,540,580,612,680,778,880,960)
    for gen in range(QUALIFICATION_END):
        if gen in chosen:
            snapshots[gen]=draw_portrait(world,parts,gen,chosen[gen])
        if gen in frame_gens:
            gif.append(draw_portrait(world,parts,gen).resize((600,612),Image.Resampling.NEAREST))
        if gen%240==0:print('Simulating',gen,flush=True)
        parts={k:evolve(v) for k,v in parts.items()}
        world=evolve(world)
    garr=(60,288,540,960)
    cw,ch=640,653
    contact=Image.new('RGB',(2*cw,2*ch),BG)
    for i,g in enumerate(garr):
        # Fit the entire crown, face, earrings and shoulder-length curls.
        frame=snapshots[g].resize((cw,ch),Image.Resampling.NEAREST)
        contact.paste(frame,((i%2)*cw,(i//2)*ch))
    contact.save(HERE/'character_round2_four_expressions.png',optimize=True)
    for g,im in snapshots.items():im.save(HERE/f'character_round2_gen{g:03}.png',optimize=True)
    gif[0].save(HERE/'character_round2_real_life.gif',save_all=True,
                append_images=gif[1:],duration=210,loop=0,optimize=True)
    pats=HERE.parent/'patterns';pats.mkdir(exist_ok=True)
    rle=compact_rle(universe(True),(
       'Conway MadeOfMaybe styled singer with wavy Life hair, eyebrow and wink control.',
       'No runtime insertions or frame swaps, B3/S23 initial-condition performance.',
       'Mouth, brow and one eye use scheduled glider syntheses/deletions.',
       'Speech bubble remains static text, not yet karaoke synchronized.',
    ))
    (pats/'character_round2_native_life.rle').write_text(rle,encoding='utf-8')
    print('Saved four-expression sheet, real Life GIF, seven stills, RLE',flush=True)

if __name__=='__main__':main()
