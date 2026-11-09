"""Exact block-occupancy sampling of the preloaded, isolated B3/S23 text circuits.

For normal flight and holding intervals, use proven c/4 glider motion and
stable 2x2-block rules. For *both reaction windows*, calculate the actual
Life generations. We do not infer occupancy from subtitle or caption time.

Under the full_song_karaoke isolation certificate, every text pixel is a
translated copy of this verified three-glider packet. Consequently a query
for one physical 2x2 target has the same result as a full-universe Life step.
This is a sparse-state solver, not a post-hoc glyph/frame replacement.
"""
from __future__ import annotations
from functools import lru_cache
from .core import evolve
from .full_song_karaoke import isolated_triple
from .glider_controlled_mouth import BLOCK

# Both reactions are calculated from 40 *actual* B3/S23 generations. A target
# lies far from the approaching gliders until these windows. The primitive
# checker separately certifies their entire noninteracting flight prefixes.
REACTION_WINDOW = 40


@lru_cache(maxsize=1)
def make_trace() -> tuple[bool, ...]:
    make, erase = 200, 602
    start = make - REACTION_WINDOW
    a, b, _ = isolated_triple(make, erase, start)
    world = a | b
    trace = []
    for g in range(start, make + 1):
        trace.append(BLOCK.issubset(world))
        if g < make:
            world = evolve(world)
    if trace[-1] is not True or any(trace[:-1]):
        raise AssertionError('MAKE precursor is not a clean block transition')
    if world != BLOCK:
        raise AssertionError('MAKE reaction leaves unexpected debris')
    return tuple(trace)


@lru_cache(maxsize=1)
def erase_trace() -> tuple[bool, ...]:
    make, erase = 200, 602
    start = erase - REACTION_WINDOW
    # At this distance, the single eraser glider is separated from the
    # (already manufactured and now stable) 2x2 target block.
    _, _, incoming = isolated_triple(make, erase, start)
    world = set(BLOCK) | incoming
    trace = []
    for g in range(start, erase + 1):
        trace.append(BLOCK.issubset(world))
        if g < erase:
            world = evolve(world)
    if not trace[0] or trace[-1] or world:
        raise AssertionError('ERASE reaction failed or left debris')
    return tuple(trace)


def block_alive_at(make_g: int, erase_g: int, generation: int) -> bool:
    """Return whether all four cells of target block exist in the native world.

    This predicate is valid for isolated 2-glider MAKES and 1-glider ERASES
    with phases make_g = 0 mod 4, erase_g = 2 mod 4, and hold >=42 ticks.
    It does not claim that flying gliders disappear from the actual universe;
    the optical projector simply crops to the target block sites.
    """
    if make_g <= 0 or make_g % 4 or erase_g % 4 != 2 or erase_g - make_g < 42:
        raise ValueError('unqualified glider packet schedule')
    if generation < 0 or generation >= erase_g:
        return False
    if generation < make_g - REACTION_WINDOW:
        return False
    if generation <= make_g:
        return make_trace()[generation - (make_g - REACTION_WINDOW)]
    if generation < erase_g - REACTION_WINDOW:
        return True
    return erase_trace()[generation - (erase_g - REACTION_WINDOW)]
