"""Three *stable*, recognizable B3/S23 mouth silhouette targets.

These are alternate initial patterns: not yet a signal-controlled 3-state Life
machine. Each is entirely made from true disjoint 2x2 Life still-life blocks.
One shared face remains unchanged, with a mouth which is a thin band, shallow
oval, or tall oval. All cell positions use the same coordinates.

The intentional two-cell buffer between logical pixels allows arbitrary
silhouettes to be built as stable Life block mosaics without accidental
births. Existing signal circuits may be routed to change pixels later, but
such a transition is NOT established by this asset.
"""
from __future__ import annotations

import math
from .core import place

BLOCK = {(0,0), (0,1), (1,0), (1,1)}
PITCH = 4
STATES = ('closed', 'medium', 'open')
HALF_WIDTH = 11
APERTURE = {'closed': 1, 'medium': 4, 'open': 8}
MOUTH_Y = 9


def mosaic(points: set[tuple[int,int]]) -> set[tuple[int,int]]:
    return set().union(*(place(BLOCK, PITCH*x, PITCH*y)
                         for x,y in points)) if points else set()


def mouth_pixels(state: str) -> set[tuple[int,int]]:
    """Anchored lip edges with identical corners across all three poses."""
    if state not in APERTURE:
        raise ValueError(f'Unknown mouth state: {state!r}')
    depth = APERTURE[state]
    pts=set()
    for x in range(-HALF_WIDTH, HALF_WIDTH+1):
        t = max(0.0, 1.0 - (x/HALF_WIDTH)**2)
        radius = int(round(depth * math.sqrt(t)))
        pts.add((x, MOUTH_Y-radius))
        pts.add((x, MOUTH_Y+radius))
        if state=='closed' and abs(x)<=9:
            pts.add((x,MOUTH_Y))
    return pts


def mouth(state: str) -> set[tuple[int,int]]:
    return mosaic(mouth_pixels(state))


def face_pixels() -> set[tuple[int,int]]:
    """Schematic but legible fixed face designed around mouth bounds."""
    out=set()
    for y in range(-25, 29):
        normalized = (y+1)/28.0
        if abs(normalized)>=1:
            continue
        extent = int(round(26.5*math.sqrt(1.0-normalized*normalized)))
        out.add((-extent,y));out.add((extent,y))
    for x in range(-12, 13):
        t = max(0,1-(x/26.0)**2)
        out.add((x, -25-int(round(1.2*t))))
        out.add((x, 29+int(round(1.2*t))))
    for x in range(-18,19):
        out.add((x,-23-int(round(2*(1-(x/20)**2)))))
    for cx in (-11,11):
        for dx in range(-4,5):
            out.add((cx+dx,-13 - (1 if abs(dx)<3 else 0)))
        out.update({(cx-4,-8),(cx-3,-7),(cx-2,-6),(cx+2,-6),
                    (cx+3,-7),(cx+4,-8),(cx,-7),(cx,-6)})
    out.update({(-1,-3),(0,-3),(0,-2),(0,-1),(-1,0)})
    out.update({(-8,32),(-8,33),(-8,34),(8,32),(8,33),(8,34)})
    return out

FACE = mosaic(face_pixels())


def scene(state: str) -> set[tuple[int,int]]:
    return FACE | mouth(state)


def shifted_scene(state: str, dx: int, dy: int) -> set[tuple[int,int]]:
    return place(scene(state),dx,dy)
