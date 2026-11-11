"""Qualified three-state, glider-driven Life mouth: REAL reversible animation.

A set of two-glider block syntheses and clean one-glider block deletions
change the visible mouth outline. All gliders are present at generation zero,
all transitions are native B3/S23, and there are no scripted cell edits.

The choreography is compiled to individual launch lanes, whose rotations and
start offsets are chosen to avoid mutual interaction. This is a verified
*fixed score*, not yet a general audio-to-glider optimizer. The inactive lip
banks are genuinely empty. Direct Closed->Open skip at the end is implemented.

Two-glider construction source:
 https://github.com/MartinSA04/GameOfLifeText/blob/main/src/game_of_life_text/construction.py
Clean block deletion is validated in our own B3/S23 simulator; see tests.
"""
from __future__ import annotations

from functools import lru_cache
from .core import evolve, place
from .singer_pilot import INPUT_GLIDER
from .three_state_mouth import face_pixels, BLOCK as PIXEL_BLOCK, PITCH

BLOCK={(0,0),(1,0),(0,1),(1,1)}
# Clean two-glider collision -> one block at (-4,-2), after four ticks.
# Both inputs can be backstepped arbitrarily many four-tick periods.
SYNTH_GLIDER_NW={(0,0),(0,1),(0,2),(1,0),(2,1)}
SYNTH_GLIDER_SW={(-3,-3),(-3,-2),(-3,-1),(-2,-1),(-1,-2)}

# A southeast-moving glider placed at (-8,-8) erases a block at (0,0)
# in 22 ticks, producing *nothing*. Both actions are pure glider physics.
DELETE_BASE=(-8,-8)

# State transitions: C->M->O->M->C->O->C, including a direct C->O jump.
# Times here are target completion generations, not renderer instructions.
BANK_SCHEDULES={
    'medium': (('make',124),('erase',246),('make',368),('erase',490)),
    'open':   (('make',248),('erase',366),('make',612),('erase',734)),
}
POSE_SAMPLES={60:'closed',180:'medium',288:'open',420:'medium',540:'closed',680:'open',778:'closed'}
FULL_DURATION=785

# Physical output blocks (upper lip is fixed). These are actual B3/S23
# coordinates, not post-render or pseudo-cell overlays.
MEDIUM_TARGETS=((-80,54),(-25,77),(25,77),(80,54))
OPEN_TARGETS=((-80,77),(-25,125),(25,125),(80,77))
UPPER_LIP_ORIGINS=tuple(range(-105,106,12))
UPPER_LIP=set().union(*(place(BLOCK,x,30) for x in UPPER_LIP_ORIGINS))

# (launch shift in ticks, synthesis orientation, deletion orientation).
# Different orientations are intentional. They keep incoming gliders below
# the fixed upper lip while avoiding cross-lane collisions.
# A greedy clearance search produced these assignments, followed by full
# real-universe simulation and checks on every tick.
ROUTING={
    ('medium',0):(-32,2,5),
    ('medium',1):(16,7,6),
    ('medium',2):(-16,2,3),
    ('medium',3):(16,2,3),
    ('open',0):(-32,7,6),
    ('open',1):(0,2,5),
    ('open',2):(-24,7,4),
    ('open',3):(24,7,4),
}


def rotate(cells: set[tuple[int,int]], direction: int) -> set[tuple[int,int]]:
    """D4 transformation preserving the output block at {(0,0)..(1,1)}."""
    if not 0<=direction<8:
        raise ValueError('direction must be 0..7')
    out=cells
    if direction%2:out={(1-x,y) for x,y in out}
    for _ in range(direction//2):out={(1-y,x) for x,y in out}
    return out


def block_make_at(t: int) -> set[tuple[int,int]]:
    """Two input gliders, making one output block exactly at generation t."""
    if t<4 or (t-4)%4:
        raise ValueError('make arrival generation must be 4 mod 4')
    n=(t-4)//4
    return place(SYNTH_GLIDER_NW,4+n,2+n) | place(SYNTH_GLIDER_SW,4+n,2-n)


def block_erase_at(t: int) -> set[tuple[int,int]]:
    """One glider cleanly erases a block by generation t (22 mod 4)."""
    if t<22 or (t-22)%4:
        raise ValueError('erase arrival generation must be 2 mod 4')
    n=(t-22)//4
    return place(INPUT_GLIDER,DELETE_BASE[0]-n,DELETE_BASE[1]-n)


def routed_pixel(bank: str, index: int) -> set[tuple[int,int]]:
    """Entire preloaded glider schedule for one dynamic mouth output pixel."""
    target=(MEDIUM_TARGETS if bank=='medium' else OPEN_TARGETS)[index]
    timing_shift,make_direction,erase_direction=ROUTING[bank,index]
    seed=set()
    for action,t in BANK_SCHEDULES[bank]:
        if action=='make':
            packet=rotate(block_make_at(t+timing_shift),make_direction)
        else:
            packet=rotate(block_erase_at(t+timing_shift),erase_direction)
        seed |= place(packet,*target)
    return seed


def signal_components() -> dict[str,set[tuple[int,int]]]:
    return {
        f'{bank}_{i}':routed_pixel(bank,i)
        for bank in ('medium','open')
        for i in range(len(MEDIUM_TARGETS if bank=='medium' else OPEN_TARGETS))
    }


def signal_seed() -> set[tuple[int,int]]:
    return set().union(*signal_components().values())


def active_pixels(state: str) -> set[tuple[int,int]]:
    """Expected lip cells at stable checkpoints, not used to drive evolution."""
    if state not in ('closed','medium','open'):raise ValueError(state)
    if state=='closed':return set()
    targets=MEDIUM_TARGETS if state=='medium' else OPEN_TARGETS
    return set().union(*(place(BLOCK,*target) for target in targets))


def moore(cells: set[tuple[int,int]]) -> set[tuple[int,int]]:
    return {(x+dx,y+dy) for x,y in cells
            for dx in range(-2,3) for dy in range(-2,3)}


@lru_cache(maxsize=1)
def prepared_face() -> frozenset[tuple[int,int]]:
    """Keep existing face block art wherever actual signal paths are clear.

    This is an *initial-condition layout* operation, not a runtime mask.
    Full glider trajectories, including future gliders, are checked at every
    generation. Entire 2x2 face blocks are omitted near wires, so none are
    removed or drawn by the renderer at playback time.
    """
    interference=moore(UPPER_LIP)
    bodies=signal_components()
    # Collect exact spacetime clearance for each moving glider bank.
    for g in range(FULL_DURATION):
        for key,cells in bodies.items():
            interference.update(moore(cells))
            bodies[key]=evolve(cells)
    face=set()
    for x,y in face_pixels():
        tile=place(BLOCK,8*x,8*y)
        if not tile & interference:
            face |= tile
    return frozenset(face)


def components(with_face: bool=True, with_bubble: bool=True):
    parts={'upper_lip':set(UPPER_LIP),**signal_components()}
    if with_face:
        parts['fixed_face']=set(prepared_face())
    if with_bubble:
        from .composition import bubble_parts, symbol
        frame,text=bubble_parts()
        # Same previously qualified bubble/text/symbol patterns, translated
        # well outside the singer's lifetime control corridors.
        parts['bubble_outline']=place(frame,1000,-60)
        parts['bubble_lyrics']=place(text,1000,-60)
        parts['pulsar']=place(symbol(),1400,-90)
    return parts


def universe(with_face=True,with_bubble=True):
    return set().union(*components(with_face,with_bubble).values())
