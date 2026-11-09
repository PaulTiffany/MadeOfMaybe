"""Stylized female-coded singer portrait entirely from Life still-life blocks.

Refines the original prototype's near-circular head to a tapered oval/heart-
shaped face with sweeping hair, almond eyes, winged eyeliner, gently arched
brows, a nose bridge and tip, and cheekbone marks. This changes ONLY the
initial placement of inert art; the *qualified* mouth and independent glider
components are unchanged. Dynamic signal cells are never culled during play.

Every art tile is a 2x2 Life block on a pitch-8 base grid, interpolated
into some additional pitch-four tiles for smoother yet stable strokes. A *conservative*
space-time exclusion volume over the exact 980-generation performance keeps
all new decoration outside the mouth-control and eye-glint trajectories.
Art is inspected after an exact whole-board superposition test, not assumed
safe merely because it was screened geometrically.
"""
from __future__ import annotations
from functools import lru_cache
from math import sqrt, cos, pi
from .core import evolve, place
from .glider_controlled_mouth import BLOCK
from .lyric_font import bubble_lyric_cells
from .expressive_mouth import (
    components as base_components, QUALIFICATION_END, EXPRESSIVE_CHECKPOINTS,
)

PITCH=8
ART_TYPES=('contour','hair','brows','eye_liner','iris','nose','cheekbones')
# Tiny two-phase Life glints moved *inside* the new raised almond eyes.
LEFT_GLINT={(x,-160) for x in (-53,-52,-51)}
RIGHT_GLINT={(52,y) for y in (-161,-160,-159)}


def _interp(v:float, anchors:list[tuple[float,float]])->float:
    if v<=anchors[0][0]:return anchors[0][1]
    for (x0,y0),(x1,y1) in zip(anchors,anchors[1:]):
        if v<=x1:
            t=(v-x0)/(x1-x0)
            return y0+t*(y1-y0)
    return anchors[-1][1]


def _oval_profile()->set[tuple[int,int]]:
    # Logical-pixel coordinate. Almost vertical at temples, then tapered jaw.
    anchors=[(-31,2),(-30,7),(-29,10),(-27,14),(-25,17),
             (-22,19),(-18,20),(-14,21),(-9,22),(-3,22),
             (3,21),(8,20),(12,19),(17,17),(21,14),
             (25,11),(28,7),(30,4),(31,1)]
    pts=set()
    for y in range(-31,32):
        x=round(_interp(y,anchors))
        pts|={(x,y),(-x,y)}
    # top and chin closure, no hard corner or cartoon round ears
    for x in range(-4,5):
        pts.add((x,-31+round(abs(x)*.15)))
    for x in range(-5,6):
        pts.add((x,31-round(abs(x)*.16)))
    return pts


def _hair()->set[tuple[int,int]]:
    pts=set()
    # Asymmetric front fringe: diagonal side-part framing the forehead.
    for x in range(-19,14):
        y=round(-28+3.5*sin_sweep((x+19)/32))
        pts.add((x,y))
    # Side part traveling down toward the left temple, out of the brow area.
    for i,y in enumerate(range(-28,-9)):
        x=-17 - round(2*sin_sweep(i/19))
        pts.add((x,y))
    # A shorter swept lock over the right temple.
    for x in range(12,19):
        pts.add((x,round(-26+0.8*(x-12))))
    # Hair crown, narrow above the head oval; disconnected deliberate lights.
    for x in range(-11,13):
        if x%2==0:
            pts.add((x,round(-33+2.5*(x/12)**2)))
    return pts


def sin_sweep(t:float)->float:
    return (1-cos(pi*min(1,max(0,t))))*.5


def _brows()->set[tuple[int,int]]:
    pts=set()
    for c,tilt in ((-7,1),(7,-1)):
        # lifted, gently curved eyebrow (end arches differ subtly).
        for dx in range(-5,6):
            arch=-27+round((dx/5)**2*2)+round(tilt*dx/5)
            pts.add((c+dx,arch))
        # a two-pixel-wide emphasis near the inner brow
        pts.add((c+(-2 if c<0 else 2),-26))
    return pts


def _eyes()->tuple[set[tuple[int,int]],set[tuple[int,int]]]:
    ink=set();iris=set()
    for c,wing in ((-7,-1),(7,1)):
        # Eyelids as tapered almond, a bolder upper arc, softer lower arc.
        for dx in range(-5,6):
            normalized=abs(dx)/5
            upper=-21-round(1.3*(1-normalized**1.6))
            lower=-19+round(0.65*(1-normalized))
            ink.add((c+dx,upper))
            if abs(dx)<=3 or abs(dx)==5:
                ink.add((c+dx,lower))
        # slight upturned outer wing, rather than a round dot-eye
        for offset in (1,2):
            ink.add((c+wing*(5+offset),-22-offset))
        # iris and lash marks, centered inside the almond
        iris|={(c,-20),(c+1,-20),(c,-19)}
        ink.add((c+wing*3,-19))
    return ink,iris


def _nose()->set[tuple[int,int]]:
    # A tapered bridge and two small nostril marks, rather than a four-dot blob.
    return {(-1,-14),(0,-14),(0,-13),(0,-12),(0,-11),(0,-10),
            (0,-2),(-1,-2),(1,-2),(-1,1),(1,1)}


def _cheeks()->set[tuple[int,int]]:
    pts=set()
    for side in (-1,1):
        pts|={(side*14,-5),(side*15,-4),(side*15,-3),
              (side*14,-2),(side*13,-1),(side*12,0),
              (side*15,5),(side*14,6)}
    # A tiny asymmetric beauty mark on left cheek.
    pts.add((-13,2))
    return pts


def design_pixels()->dict[str,set[tuple[int,int]]]:
    eyeliner,iris=_eyes()
    return {
        'contour':_oval_profile(),
        'hair':_hair(),
        'brows':_brows(),
        'eye_liner':eyeliner,
        'iris':iris,
        'nose':_nose(),
        'cheekbones':_cheeks(),
    }


def _stroke_tiles(points:set[tuple[int,int]],kind:str)->set[tuple[int,int]]:
    """Interpolate between adjacent logical pixels onto a pitch-four grid.

    This adds REAL, physically separated 2x2 Life block still lifes, not a
    renderer-drawn stroke. Eye irises retain their finer individual highlights.
    """
    origins={(PITCH*x,PITCH*y) for x,y in points}
    if kind!='iris':
        for x,y in points:
            for dx,dy in ((1,0),(0,1),(1,1),(-1,1)):
                if (x+dx,y+dy) in points:
                    origins.add((PITCH*x+4*dx,PITCH*y+4*dy))
    return origins


def _protected_tile_origins()->set[tuple[int,int]]:
    """Every tile blocked by moving Life trajectories over entire performance.

    Include the eye glints, lip actuation, central-line erasure and return.
    Excludes the original static portrait; the bubble outline remains fixed,
    while its old sparse static lettering is replaced by 5x7 still-life text.
    """
    moving=base_components(with_bubble=False)
    moving.pop('outline');moving.pop('eyes_nose')
    moving.pop('left_eye_glint');moving.pop('right_eye_glint')
    moving['left_eye_glint']=set(LEFT_GLINT)
    moving['right_eye_glint']=set(RIGHT_GLINT)
    forbidden=set()
    # Keep 2-neighborhood around all moving cells; this is conservative.
    for _ in range(QUALIFICATION_END):
        for name,live in moving.items():
            for x,y in live:
                # Only region where the *new* portrait could be drawn.
                if -200<=x<=200 and -300<=y<=270:
                    for dx in (-2,-1,0,1,2):
                        for dy in (-2,-1,0,1,2):
                            forbidden.add((x+dx,y+dy))
            moving[name]=evolve(live)
    return forbidden


@lru_cache(maxsize=1)
def prepared_portrait()->dict[str,frozenset[tuple[int,int]]]:
    safe=_protected_tile_origins()
    result={}
    used=set()
    for typ,pixels in design_pixels().items():
        approved=set()
        for xx,yy in sorted(_stroke_tiles(pixels,typ),key=lambda p:(p[1],p[0])):
            tile=place(BLOCK,xx,yy)
            if tile&safe or tile&used:
                continue
            approved |= tile
            used |= tile
        result[typ]=frozenset(approved)
    return result


def components(with_bubble=True, caption_lines=('MADE OF','MAYBE')):
    parts=base_components(with_bubble=with_bubble)
    parts.pop('outline');parts.pop('eyes_nose')
    if with_bubble:
        # More legible 5x7 native Life font; still static, not yet karaoke.
        parts['bubble_lyrics']=bubble_lyric_cells(caption_lines)
    parts['left_eye_glint']=set(LEFT_GLINT)
    parts['right_eye_glint']=set(RIGHT_GLINT)
    for name,cells in prepared_portrait().items():
        parts['art_'+name]=set(cells)
    return parts


def universe(with_bubble=True, caption_lines=('MADE OF','MAYBE')):
    return set().union(*components(with_bubble=with_bubble,caption_lines=caption_lines).values())
