"""Character round 2: voluminous Life hair, expressive asymmetric brow/eyes.

Every hair strand, accessory, and eyebrow tile is a genuine stable B3/S23
block. Decorative geometry is fit to 980-tick spacetime exclusion footprints;
no pixels are added or removed by the renderer during playback.

A separately addressed glider-controlled eyebrow accent is optional until
its full-universe qualification passes. The base mouth/bubble are untouched.
"""
from __future__ import annotations
from math import sin,cos,pi,sqrt
from functools import lru_cache
from .core import evolve,place
from .styled_singer import components as base_components, PITCH, _stroke_tiles, _protected_tile_origins,QUALIFICATION_END
from .glider_controlled_mouth import BLOCK,rotate,block_make_at,block_erase_at


def smoothstep(t):
    t=max(0.,min(1.,t))
    return t*t*(3-2*t)


def bezier(points,steps=80):
    """Return a rasterized long curve in 8-cell logical pixels."""
    a,b,c,d=points
    out=set()
    for i in range(steps+1):
        t=i/steps;s=1-t
        x=(s**3*a[0]+3*s*s*t*b[0]+3*s*t*t*c[0]+t**3*d[0])
        y=(s**3*a[1]+3*s*s*t*b[1]+3*s*t*t*c[1]+t**3*d[1])
        out.add((round(x),round(y)))
    return out


def hair_illustration():
    """Side-swept, layered wavy shoulder-length hair, not a helmet halo."""
    silhouette=set();strands=set();shine=set()
    strokes=[
        # full crown above the head, with a real side part
        ((-25,-21),(-29,-43),(-4,-44),(9,-39)),
        ((9,-39),(27,-40),(30,-29),(27,-17)),
        # thick asymmetric left hair body, behind ear and along cheek
        ((-24,-24),(-31,-15),(-27,3),(-30,15)),
        ((-30,15),(-28,23),(-37,28),(-37,34)),
        ((-37,34),(-39,37),(-33,40),(-29,38)),
        ((-29,38),(-25,35),(-27,29),(-25,24)),
        # second long dark left ribbon towards shoulder
        ((-27,-16),(-30,-5),(-29,13),(-34,23)),
        ((-34,23),(-37,27),(-32,34),(-28,32)),
        # right-sided volume with a curled lower tip
        ((26,-22),(33,-9),(27,9),(32,21)),
        ((32,21),(36,27),(37,31),(34,35)),
        ((34,35),(29,39),(25,32),(27,27)),
        ((27,27),(30,15),(25,5),(25,-7)),
        # shorter hanging curl over one shoulder
        ((31,10),(34,21),(28,30),(31,34)),
    ]
    for curve in strokes: silhouette.update(bezier(curve))
    # broad crown, a few separated internal hair-layer lines, swooping over forehead
    wisps=[
        ((-21,-31),(-10,-36),(9,-36),(23,-27)),
        ((-19,-34),(-5,-34),(6,-31),(17,-26)),
        ((-22,-27),(-11,-27),(-3,-22),(6,-24)),
        ((-18,-25),(-4,-24),(11,-21),(17,-22)),
        ((-27,-13),(-23,-5),(-26,8),(-26,15)),
        ((-32,6),(-29,13),(-35,22),(-33,30)),
        ((27,-17),(24,-5),(31,4),(27,13)),
        ((32,19),(29,28),(34,32),(30,35)),
    ]
    for curve in wisps: strands.update(bezier(curve))
    highlights=[
        ((-21,-35),(-6,-41),(10,-41),(21,-34)),
        ((-24,-17),(-28,-4),(-24,10),(-31,20)),
        ((24,-29),(32,-15),(28,-4),(29,5)),
        ((-32,27),(-36,32),(-33,36),(-31,35)),
    ]
    for curve in highlights:shine.update(bezier(curve))
    return {'hair_mass':silhouette,'hair_waves':strands,'hair_gloss':shine}


def brow_illustration():
    pts=set()
    for center,inner_lift in ((-7,0),(7,2)):
        for dx in range(-6,7):
            # Contrasting expression: lifted right brow, mischievously arched.
            t=dx/6
            arch=round(-27 - inner_lift - (2 if abs(t)<.45 else 0)+2.4*t*t)
            if center<0:arch+=round(-.4*t)
            else:arch+=round(.7*t)
            pts.add((center+dx,arch))
            if -3<=dx<=0:
                pts.add((center+dx,arch+1))
    return pts


def jewelry_illustration():
    # Two miniature open drop-earrings, placed outside the head outline.
    pts=set()
    for c in (-24,24):
        pts.update({(c,-2),(c,-1),(c-1,0),(c+1,0),
                    (c-1,1),(c+1,1),(c,2)})
    return pts


def lash_illustration():
    pts=set()
    # Small swept lash flourishes at outer eye corners.
    for c,side in ((-7,-1),(7,1)):
        pts|={(c+side*6,-21),(c+side*7,-23),(c+side*7,-24),
              (c+side*5,-21)}
    return pts


# These routes are not generic switches. They are exact preloaded glider
# performances qualified against one character/score and must be rechecked
# if any timing, artwork, or routing changes.
BROW_ROUTES=(
    ((48,-248),-48,0,0),
    ((64,-256),-48,0,0),
    ((80,-248),-48,0,0),
)
# We dim/restore the left iris as a deliberate small wink at g540.
# (target, four-generation time shift, erase D4, remake D4)
WINK_ROUTES=(
    ((-64,-160),-48,0,3),
    ((-56,-160),-16,0,3),
    ((-48,-160),16,0,3),
)
BROW_ON=(288,420)
BROW_OFF=(60,180,540,680,960)
WINK_PRESENT=(60,180,288,420,680,960)
WINK_MISSING=(540,)


def expressivity_signals():
    out={}
    for i,(xy,shift,make_dir,erase_dir) in enumerate(BROW_ROUTES):
        gliders=(place(rotate(block_make_at(256+shift),make_dir),*xy)
                |place(rotate(block_erase_at(478+shift),erase_dir),*xy))
        out[f'right_brow_lift_{i}']=gliders
    for i,(xy,shift,erase_dir,make_dir) in enumerate(WINK_ROUTES):
        # The iris exists from tick zero, goes away for a short wink, and
        # returns through a clean two-glider synthesis (never injected).
        gliders=(place(BLOCK,*xy)
                |place(rotate(block_erase_at(478+shift),erase_dir),*xy)
                |place(rotate(block_make_at(612+shift),make_dir),*xy))
        out[f'left_wink_{i}']=gliders
    return out


def blocks(cells):
    """Recover 2x2 logical-block tiles, required to discard only whole art."""
    origins={(x-x%4,y-y%4) for x,y in cells}
    return {p:place(BLOCK,*p) for p in origins if place(BLOCK,*p)<=cells}


@lru_cache(maxsize=1)
def prepared_character_art():
    """Global spacetime clearance for all art, including new eye/brow gliders.

    The existing controller is unchanged. Static art is fitted *around* the
    glider paths, not removed during playback. Characteristic Life cells can
    never be artificially suppressed or injected by a camera.
    """
    parts=base_components(with_bubble=True)
    parts.pop('art_hair');parts.pop('art_brows');parts.pop('left_eye_glint')
    # Replace three former permanent left iris pixels with three bona fide
    # glider-controlled Life blocks. The right iris remains permanent.
    parts['art_iris']={(x,y) for x,y in parts['art_iris'] if x>=0}
    movements={k:set(v) for k,v in parts.items() if not k.startswith('art_')
               and k not in ('bubble_outline','bubble_lyrics','pulsar')}
    movements.update(expressivity_signals())
    exclusions=set()
    # All motion, including every future mouth, eye and forehead packet.
    for _ in range(QUALIFICATION_END):
        for key,live in movements.items():
            for x,y in live:
                if -400<=x<=400 and -470<=y<=400:
                    exclusions.update((x+dx,y+dy) for dx in range(-2,3) for dy in range(-2,3))
            movements[key]=evolve(live)
    fixed=parts['bubble_outline']|parts['bubble_lyrics']|parts['pulsar']
    for x,y in fixed:
        exclusions.update((x+dx,y+dy) for dx in range(-2,3) for dy in range(-2,3))
    approved={};used=set(fixed)
    # Existing eyes/nose/cheeks/oval remain, except signal lane intrusions.
    for key in ('art_contour','art_eye_liner','art_iris','art_nose','art_cheekbones'):
        cells=set()
        for xy,tile in sorted(blocks(parts[key]).items()):
            if tile&exclusions or tile&used: continue
            cells.update(tile);used.update(tile)
            for x,y in tile:
                exclusions.update((x+dx,y+dy) for dx in range(-2,3) for dy in range(-2,3))
        approved[key]=frozenset(cells)
    designs={**hair_illustration(),'brows':brow_illustration(),
             'lashes':lash_illustration(),'jewelry':jewelry_illustration()}
    for key,logical in designs.items():
        result=set()
        origins=_stroke_tiles(logical,key)
        for ox,oy in sorted(origins,key=lambda p:(p[1],p[0])):
            tile=place(BLOCK,ox,oy)
            if tile&exclusions or tile&used: continue
            result.update(tile);used.update(tile)
            for x,y in tile:
                exclusions.update((x+dx,y+dy) for dx in range(-2,3) for dy in range(-2,3))
        approved['art_'+key]=frozenset(result)
    return approved


# Alias for early visual-prototype callers.
def prepared_details():
    return {k:v for k,v in prepared_character_art().items()
            if k in ('art_hair_mass','art_hair_waves','art_hair_gloss',
                     'art_brows','art_lashes','art_jewelry')}


def components(with_bubble=True):
    parts=base_components(with_bubble=with_bubble)
    for k in list(parts):
        if k.startswith('art_'):parts.pop(k)
    parts.pop('left_eye_glint')
    parts.update({name:set(c) for name,c in prepared_character_art().items()})
    parts.update(expressivity_signals())
    return parts


def universe(with_bubble=True):
    return set().union(*components(with_bubble).values())
