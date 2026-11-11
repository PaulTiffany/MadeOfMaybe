"""Render REAL B3/S23 glider-controlled mouth with three persistent poses.

Run from repo root: python preview/make_operational_mouth.py
Pillow is optional; cell simulation/tests require stdlib only.
Every changing shape comes from Life evolution, not frame injection.
"""
from __future__ import annotations
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))

from PIL import Image,ImageDraw,ImageFont
from life.core import evolve
from life.glider_controlled_mouth import (
    universe, components, MEDIUM_TARGETS, OPEN_TARGETS, UPPER_LIP,
    prepared_face, FULL_DURATION, POSE_SAMPLES, active_pixels,
)

ROOT=Path(__file__).resolve().parent
W,H=680,870
ZOOM=1.42
OX,OY=W//2,470
C_BG=(11,19,30);C_FACE=(190,224,215);C_LIP=(255,159,155)
C_GLIDER=(45,74,96);C_TEXT=(214,225,231);C_SUB=(131,159,172)
try:
    FONT=ImageFont.truetype('DejaVuSans.ttf',22)
    BOLD=ImageFont.truetype('DejaVuSans-Bold.ttf',27)
    SMALL=ImageFont.truetype('DejaVuSans.ttf',17)
except OSError:
    FONT=BOLD=SMALL=ImageFont.load_default()

FACE=set(prepared_face())
FRACTION=1

def img(state: set[tuple[int,int]], g:int, label:bool=True):
    canvas=Image.new('RGB',(W,H),C_BG)
    draw=ImageDraw.Draw(canvas)
    # Entire crop contains only actual B3/S23 cells; the simulation also
    # contains more distant routing gliders and the unchanged speech bubble.
    for x,y in state:
        screenx=int(OX+x*ZOOM);screeny=int(OY+y*ZOOM)
        if 0<=screenx<W-4 and 0<=screeny<H-4:
            tile=(screenx,screeny,screenx+max(1,int(ZOOM*2))-1,screeny+max(1,int(ZOOM*2))-1)
            if (x,y) in FACE:
                color=C_FACE
            elif (x,y) in UPPER_LIP:
                color=C_LIP
            elif any(tx<=x<=tx+1 and ty<=y<=ty+1
                     for tx,ty in MEDIUM_TARGETS+OPEN_TARGETS):
                color=C_LIP
            else:
                color=C_GLIDER
            draw.rectangle(tile,fill=color)
    if label:
        phase=POSE_SAMPLES.get(g)
        if phase:
            title=phase.upper()
        else:
            a=active_pixels('medium')<=state
            b=active_pixels('open')<=state
            title='SIGNALS IN FLIGHT'
            if a:title='MEDIUM HOLD'
            if b:title='OPEN HOLD'
        draw.text((28,18),title,font=BOLD,fill=C_TEXT)
        draw.text((28,55),f'G{g:03d} · unedited B3/S23 cells',font=SMALL,fill=C_SUB)
    return canvas


def main():
    cells=universe()
    frames=[]
    snapshots={}
    snapshots_cells={}
    for gen in range(FULL_DURATION):
        if gen in POSE_SAMPLES:
            snapshots_cells[gen]=set(cells)
            snapshots[gen]=img(cells,gen)
        if gen%8==0:
            frames.append(img(cells,gen).resize((510,650),Image.Resampling.NEAREST))
        cells=evolve(cells)
    # Stable reference positions to show state differences side by side.
    markers=[(60,'CLOSED'),(180,'MEDIUM'),(288,'OPEN')]
    mini_w,mini_h=510,650
    sheet=Image.new('RGB',(3*mini_w,mini_h),(11,19,30))
    for i,(g,title) in enumerate(markers):
        picture=snapshots[g].resize((mini_w,mini_h),Image.Resampling.NEAREST)
        sheet.paste(picture,(i*mini_w,0))
    sheet.save(ROOT/'operational_mouth_three_states.png',optimize=True)
    # Higher-magnification, completely authentic-cell mouth crop.
    # Static upper lip and switched lower lip can be inspected side by side.
    zw,zh=810,565
    zp=3.55
    zox,zoy=zw//2,175
    zoomsheet=Image.new('RGB',(3*zw,zh),C_BG)
    for i,(g,title) in enumerate(markers):
        panel=Image.new('RGB',(zw,zh),C_BG)
        d=ImageDraw.Draw(panel)
        for x,y in snapshots_cells[g]:
            X=int(zox+x*zp);Y=int(zoy+y*zp)
            if 0<=X<zw-8 and 0<=Y<zh-8:
                if (x,y) in UPPER_LIP or any(tx<=x<=tx+1 and ty<=y<=ty+1
                      for tx,ty in MEDIUM_TARGETS+OPEN_TARGETS):
                    color=C_LIP
                else:
                    color=(30,48,63)
                d.rectangle((X,Y,X+6,Y+6),fill=color)
        d.text((24,15),title,font=BOLD,fill=C_TEXT)
        d.text((24,50),f'Generation {g}: actual B3/S23 cells',font=SMALL,fill=C_SUB)
        zoomsheet.paste(panel,(i*zw,0))
    zoomsheet.save(ROOT/'operational_mouth_closeup.png',optimize=True)
    # More explicit transitions: one playback, no image frames substituted.
    frames[0].save(ROOT/'operational_mouth_glider_control.gif',save_all=True,
                   append_images=frames[1:],duration=86,loop=0,optimize=True)
    for g in (60,180,288,420,540,680,778):
        snapshots[g].save(ROOT/f'operational_mouth_g{g}.png',optimize=True)
    print('Made three-state contact sheet + native-Life GIF + 7 actual checkpoints')

if __name__=='__main__':
    main()
