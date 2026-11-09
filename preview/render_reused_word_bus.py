"""Inspection only: two sung WE onsets occupy one REAL Conway glyph location.

The clean portrait camera shows real stable art and fully occupied lip tiles,
not the clutter of passing glider tracks. A second camera, BELOW the optical
lyric speech bubble, shows the same simulated controller's 84 real catalysts.
The cameras are presentation only; the unchanged native-Life source still
contains all transit gliders at their actual coordinates. The remaining full lettering
is NOT reconstructed by this narrow two-line hardware pilot.
"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from PIL import Image,ImageDraw,ImageFont
from life.core import evolve,place
from life.first_line_singing_character import safe_art
from life.physical_lip_splitter_bridge import SINGER_TRANSLATION,WORD_PIXEL,LIP_TARGET,splitter_catalysts
from life.reusable_word_cue import character_world_with_second_lip,line_times,SECOND_LIP_GLOBAL,SECOND_LIP_LOCAL
from life.glider_controlled_mouth import BLOCK
from life.symmetric_full_mouth import target_blocks
from life.expressive_mouth import START_LINE
from preview.make_character_round2 import PALETTE

ROOT=Path(__file__).resolve().parents[1]
W,H=1360,980
BG=(7,11,23)
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
def font(size,bold=False):
    path='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf' if bold else FONT
    return ImageFont.truetype(path,size)


# Fixed within-card optical regions. The physically separate cameras do not
# change the source universe or assert that controller catalyst cells moved.
CARD_FACE=(16,76,321,389)
CARD_BUBBLE=(340,77,624,235)
CARD_CONTROL=(340,250,624,391)
assert CARD_FACE[2]<CARD_BUBBLE[0] and CARD_FACE[2]<CARD_CONTROL[0]
assert CARD_CONTROL[1]>CARD_BUBBLE[3]


def _mouth_tile_origins():
    """Candidate 2x2 sites from the EXISTING character's real mouth wiring."""
    cells=target_blocks('medium')|target_blocks('open')
    sites={(x,y) for x,y in cells
           if (x-1,y) not in cells and (x,y-1) not in cells}
    sites.update(START_LINE)
    sites.add(tuple(LIP_TARGET))
    sites.add(tuple(SECOND_LIP_LOCAL))
    return tuple(sorted(sites))


MOUTH_TILE_ORIGINS=_mouth_tile_origins()


def observed_lip_cells(world):
    """Select only whole B3/S23 Life lip tiles; never synthesize screen poses."""
    ax,ay=SINGER_TRANSLATION
    return {(x,y) for origin in MOUTH_TILE_ORIGINS
            for x,y in place(BLOCK,origin[0]+ax,origin[1]+ay)
            if place(BLOCK,origin[0]+ax,origin[1]+ay)<=world}


def _panel_boxes(left,top):
    face=tuple(v+(left if i%2==0 else top) for i,v in enumerate(CARD_FACE))
    bubble=tuple(v+(left if i%2==0 else top) for i,v in enumerate(CARD_BUBBLE))
    ctrl=tuple(v+(left if i%2==0 else top) for i,v in enumerate(CARD_CONTROL))
    return face,bubble,ctrl


def render(path=ROOT/'preview/reused_word_bus_two_lines.png'):
    times=line_times();wanted=[times[0][0],times[0][1],times[1][0],times[1][1]]
    still={};live=character_world_with_second_lip()
    for g in range(wanted[-1]+1):
        if g in wanted:still[g]=set(live)
        if g<wanted[-1]:live=evolve(live)
    # art_seed() contains these same stable Life cells in the portrait-inclusive
    # Golly RLE. The dynamic-only optical sampler omits static art for speed.
    art=safe_art()
    catalysts=place(splitter_catalysts(),*SINGER_TRANSLATION)
    assert len(catalysts)==84
    canvas=Image.new('RGB',(W,H),BG);d=ImageDraw.Draw(canvas)
    d.text((27,16),'ONE SPLITTER. TWO SONG LINES. TWO REAL LIP ACTIONS.',font=font(23,True),fill=(240,222,248))
    d.text((28,48),'Clear portrait camera | native glyph bubble | controller BELOW bubble',font=font(15),fill=(167,191,219))
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
        face,bubble,ctrl=_panel_boxes(left,top)
        d.rounded_rectangle(face,radius=10,fill=(10,17,34),outline=(52,71,95),width=1)
        d.text((face[0]+12,face[1]+8),'SINGER / ART + TRUE LIP SITES',
               font=font(11,True),fill=(168,208,231))
        ax,ay=SINGER_TRANSLATION
        xoff=face[0]+151;yoff=face[1]+153
        sx=.50;sy=.50
        def mark_face(x,y,col,size=2):
            u=xoff+int(x*sx);v=yoff+int(y*sy)
            if face[0]+4<u<face[2]-size-4 and face[1]+28<v<face[3]-size-5:
                d.rectangle((u,v,u+size,v+size),fill=col)
        # Unlike the former raw whole-world plot, flying control packets
        # are viewed in the separate controller camera, NOT through her face.
        for name,cells in art.items():
            color=PALETTE.get(name,(210,212,239))
            for x,y in cells:mark_face(x,y,color,2)
        lip=observed_lip_cells(pixels)
        assert lip<=pixels
        for x,y in lip:mark_face(x-ax,y-ay,(252,119,167),3)
        # The bubble is an optical frame around the REAL 2x2 glyph port. It
        # is NOT claimed to be a new Life still-life bubble added to this seed.
        d.rounded_rectangle(bubble,radius=12,fill=(21,32,57),outline=(112,108,165),width=2)
        d.polygon([(bubble[0]+12,bubble[3]-1),(bubble[0]-9,bubble[3]+18),
                   (bubble[0]+45,bubble[3]-1)],fill=(21,32,57))
        d.text((bubble[0]+16,bubble[1]+9),'LYRIC BUBBLE  /  NATIVE GLYPH',
               font=font(11,True),fill=(211,216,245))
        d.text((bubble[0]+16,bubble[1]+30),'WE starts here  ·  cell (0,0)',
               font=font(11),fill=(166,184,211))
        block=place(BLOCK,*WORD_PIXEL)
        on=block<=pixels
        pitch=10;bx=bubble[0]+24;by=bubble[1]+62
        for y in range(-4,5):
            for x in range(-4,5):
                active=(x,y) in pixels
                color=(110,244,211) if active else (34,50,77)
                d.rectangle((bx+(x+4)*pitch,by+(y+4)*pitch,
                             bx+(x+4)*pitch+pitch-3,by+(y+4)*pitch+pitch-3),
                            fill=color)
        d.text((bubble[0]+152,bubble[1]+76),'ON' if on else 'OFF',
               font=font(19,True),fill=(110,244,211) if on else (247,162,183))
        if on!=expected:
            raise AssertionError(f'wrong native anchor occupancy at g{g}: {on} != {expected}')
        # Actual same-world catalyst cell sample shown below the bubble.
        # No controller cells are translated within the B3/S23 simulation.
        d.rounded_rectangle(ctrl,radius=10,fill=(12,26,41),outline=(61,93,105),width=1)
        d.text((ctrl[0]+13,ctrl[1]+8),'CONTROL HARDWARE  /  84 REAL LIFE CELLS',
               font=font(11,True),fill=(127,223,200))
        seen=catalysts & pixels
        if len(seen)!=84:raise AssertionError(f'catalyst damaged at g{g}')
        minx=min(x for x,y in catalysts);miny=min(y for x,y in catalysts)
        for x,y in seen:
            u=ctrl[0]+15+int((x-minx)*1.1)
            v=ctrl[1]+34+int((y-miny)*1.1)
            if u<ctrl[0]+115 and v<ctrl[3]-6:
                d.rectangle((u,v,u+1,v+1),fill=(119,225,202))
        # All three indicator values come from the exact checkpoint universe.
        original=place(BLOCK,ax+LIP_TARGET[0],ay+LIP_TARGET[1])<=pixels
        added=place(BLOCK,*SECOND_LIP_GLOBAL)<=pixels
        labels=(('WE PIXEL',on),('ORIGINAL LIP',original),('SECOND LIP',added))
        for j,(key,active) in enumerate(labels):
            px=ctrl[0]+130;py=ctrl[1]+35+j*27
            d.text((px,py),key,font=font(10,True),fill=(161,184,206))
            d.text((ctrl[2]-12,py),'LIVE' if active else 'OFF',
                   font=font(10,True),anchor='ra',
                   fill=(116,241,200) if active else (246,164,186))
    d.text((28,H-29),'OPTICAL LAYOUT ONLY  |  Portrait and controller are separately cropped from the same native Life world',
           font=font(13),fill=(163,182,202))
    path.parent.mkdir(parents=True,exist_ok=True);canvas.save(path,optimize=True)
    print('Wrote',path,'bytes',path.stat().st_size)
    return path

if __name__=='__main__':render()
