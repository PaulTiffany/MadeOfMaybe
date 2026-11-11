"""First FULL-LIP / karaoke integration at a shared, constant Life clock.

One unchanged B3/S23 initial condition contains all 361 physical lyric blocks
and the existing genuinely moving multi-tile singer. The character performance
is backstepped in four-generation glider phases to align its MEDIUM checkpoint
with the line-clear event, preserving singing articulation through SAND. This qualifies music-timed real lips, *not* physical
fanout from the text's individual glider signals: that gate remains an explicit
routing task. No phoneme score, runtime edits, camera overlays or audio stretch.

The character and lyric are separated spatially by a proven clearance band;
a split-screen camera can show both regions simultaneously.
"""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from .core import evolve, place
from .character_round2 import components as original_components, prepared_character_art
from .glider_controlled_mouth import BLOCK
from .first_line_karaoke import score as lyric_score, universe as lyric_universe, max_envelope_radius, ERASE_GENERATION, GPS

CHARACTER_X = -5000
ORIGINAL_MEDIUM_CHECKPOINT = 180
LAST_ORIGINAL_GENERATION = 980
STABLE_POSES = {
    60: 'closed',180: 'medium',288: 'open',420: 'medium',
    540: 'breath',680: 'open',960: 'closed',
}
EXCLUDED_FACE_MOTION = ('right_brow_lift_', 'left_wink_')


def anchor_delay() -> int:
    """No separately authored mouth clock: anchor to the native lyric line clear."""
    delta = ERASE_GENERATION - 490
    if delta < 0 or delta % 4:
        raise ValueError('source lyric does not permit 4-phase physical retiming')
    return delta


def _connected(cells):
    remain = set(cells)
    while remain:
        first = remain.pop(); component = {first}; queue=[first]
        while queue:
            x,y = queue.pop()
            for dx in (-1,0,1):
                for dy in (-1,0,1):
                    point=(x+dx,y+dy)
                    if point in remain:
                        remain.remove(point); component.add(point); queue.append(point)
        yield component


def _glider_velocity(cells):
    at4=set(cells)
    for _ in range(4):
        at4=evolve(at4)
    directions=[(dx,dy) for dx in (-1,1) for dy in (-1,1)
                if at4 == place(cells,dx,dy)]
    if len(cells)!=5 or len(directions)!=1:
        raise ValueError('the retiming compiler only accepts exact c/4 gliders')
    return directions[0]


@lru_cache(maxsize=1)
def original_dynamic_components():
    parts=original_components(with_bubble=False)
    return {k:frozenset(v) for k,v in parts.items()
            if not k.startswith('art_') and not k.startswith(EXCLUDED_FACE_MOTION)}


@lru_cache(maxsize=1)
def retimed_dynamic_components():
    delay=anchor_delay()
    packets={}
    for name,cells in original_dynamic_components().items():
        pieces=set()
        for component in _connected(cells):
            if len(component)==5:
                vx,vy=_glider_velocity(component)
                # Exactly undo (delay/4) native Life periods at g0.
                component=place(component,-vx*(delay//4),-vy*(delay//4))
            elif len(component) not in (3,4):
                raise ValueError(f'unsupported dynamic seed in {name}: {len(component)} cells')
            pieces.update(component)
        packets[name]=frozenset(pieces)
    return packets


@lru_cache(maxsize=1)
def dynamic_seed():
    return frozenset().union(*retimed_dynamic_components().values())


@lru_cache(maxsize=1)
def safe_art():
    """Remove static tiles *before initialization* if retimed gliders traverse them.

    This is not a playback mask; it rebuilds one fixed character initial world.
    The 2-cell guard means a static source and moving source cannot jointly
    affect a birth or survival, and the retained static art is itself stable.
    """
    world=set(dynamic_seed()); forbidden=set()
    for _ in range(anchor_delay()+LAST_ORIGINAL_GENERATION+1):
        for x,y in world:
            if -350<x<350 and -440<y<350:
                for dx in (-2,-1,0,1,2):
                    for dy in (-2,-1,0,1,2):
                        forbidden.add((x+dx,y+dy))
        world=evolve(world)
    accepted={}
    for name,cells in prepared_character_art().items():
        valid=set()
        for x,y in cells:
            if (x-1,y) in cells or (x,y-1) in cells:
                continue
            block=place(BLOCK,x,y)
            if block <= cells and block.isdisjoint(forbidden):
                valid.update(block)
        accepted[name]=frozenset(valid)
    art=frozenset().union(*accepted.values())
    if evolve(set(art))!=set(art):
        raise AssertionError('retimed portrait contains unstable static art')
    if len(art)<4500:
        raise AssertionError('retiming stripped away too much of the character artwork')
    return accepted


def art_seed():
    return frozenset().union(*safe_art().values())


def character_seed():
    return set(dynamic_seed()) | set(art_seed())


def combined_seed():
    """A single initial condition; disjoint singer stage + 7-word glyph stage."""
    lyric=lyric_universe()
    portrait=place(character_seed(),CHARACTER_X,0)
    if portrait & lyric:
        raise AssertionError('singer and physical lettering overlap')
    return lyric | portrait


def timed_checkpoints():
    delay=anchor_delay()
    return {g+delay:name for g,name in STABLE_POSES.items()}


def singer_coordinates_at(generation, *, include_art=True):
    """Native Life evolution in singer's LOCAL coordinates (not video glyphs)."""
    if generation<0:raise ValueError(generation)
    live=set(dynamic_seed())
    for _ in range(generation):live=evolve(live)
    if include_art:live|=set(art_seed())
    return live


def spatial_certificate():
    lyric=lyric_universe()
    singer=character_seed()
    lyric_minx=min(x for x,y in lyric)
    singer_maxx=max(x for x,y in singer)+CHARACTER_X
    # Life's one-cell/generation propagation cone conservatively bounds the
    # moving singer. The 7-word packet envelope is independently verified.
    horizon=anchor_delay()+LAST_ORIGINAL_GENERATION
    singer_light_cone_maxx=singer_maxx+horizon
    lyric_trajectory_minx=-max_envelope_radius()
    if singer_light_cone_maxx+2>=lyric_trajectory_minx:
        raise AssertionError('singer/lyrics may interact within qualified horizon')
    return {'lyric_min_seed_x':lyric_minx,
            'singer_max_seed_x':singer_maxx,
            'initial_x_separation':lyric_minx-singer_maxx,
            'worst_case_trajectory_gap_x':lyric_trajectory_minx-singer_light_cone_maxx,
            'light_cone_horizon_generation':horizon,
            'singer_cell_count':len(singer),'lyric_seed_cells':len(lyric),
            'combined_initial_cells':len(singer)+len(lyric),
            'delay_g':anchor_delay(),'constant_gps':GPS,
            'last_qualified_singer_g':anchor_delay()+LAST_ORIGINAL_GENERATION,
            'physical_shared_duplicator_connected':False}
