"""Expressive, genuinely glider-controlled singer audition.

The earlier symmetric singer's permanent nine-block mid-mouth line looked
like teeth when the lips opened. Here the line is an actual Life object:
five initial blocks are erased by incoming gliders at g98, and recreated
by independently routed two-glider syntheses by g932.

Upper and lower lips retain their qualified preloaded symmetric control.
The scene is one uninterrupted B3/S23 universe. It does *not* yet support
reclosing the central line at the middle g540 rest: that checkpoint is
labelled BREATH, not falsely claimed to be CLOSED. Five final blocks are
restored by g960. The prior controller remains available separately.
"""
from __future__ import annotations
from .restored_centerline import (
    components as _base_components, universe as _base_universe, START_LINE, RESTORE_ROUTES, ERASE_TIME,
    QUALIFICATION_END
)
from .symmetric_full_mouth import target_blocks, POSE_SAMPLES, MIDLINE
from .glider_controlled_mouth import BLOCK
from .core import place

# These are inspection checkpoints, NEVER renderer-driven state changes.
# The band at 540 genuinely remains absent. We intentionally preserve the
# validity of these observations rather than substituting pixels.
EXPRESSIVE_CHECKPOINTS = {
    60: 'closed',
    180: 'medium',
    288: 'open',
    420: 'medium',
    540: 'breath',
    680: 'open',
    778: 'breath',
    960: 'closed',
}

LINE_CELLS = frozenset().union(*(place(BLOCK, *position) for position in START_LINE))

# A pair of independently evolving *real* Life blinkers, in opposite phase.
# Each is 3 live cells and switches orientation every generation. Both
# locations passed exact 980-generation noninteraction qualification with
# the singer/glider circuits and existing bubble.
LEFT_EYE_GLINT = {(-45,-122),(-44,-122),(-43,-122)}
RIGHT_EYE_GLINT = {(44,-123),(44,-122),(44,-121)}


def components(with_bubble=True):
    p = _base_components(with_bubble=with_bubble)
    p['left_eye_glint'] = set(LEFT_EYE_GLINT)
    p['right_eye_glint'] = set(RIGHT_EYE_GLINT)
    return p


def universe(with_bubble=True):
    return set().union(*components(with_bubble=with_bubble).values())


def stable_mouth_at(world: set[tuple[int, int]]):
    """Read actual completed mouth cells from the full simulated universe.

    This function is for presentation / measurement only. It never edits Life.
    """
    active = set()
    for state in ('medium', 'open'):
        candidates = target_blocks(state)
        # A complete 2x2 tile is counted only if all four cells exist.
        for x,y in candidates:
            if (x-1,y) not in candidates and (x,y-1) not in candidates:
                tile=place(BLOCK,x,y)
                if tile <= world:
                    active.update(tile)
    line = set()
    for xy in START_LINE:
        tile=place(BLOCK,*xy)
        if tile<=world:
            line.update(tile)
    return active,line
