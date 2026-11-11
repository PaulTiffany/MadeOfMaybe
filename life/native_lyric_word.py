"""First ACTUAL glider-written and erased 5x7 lyric, as native B3/S23.

All 35 glyph pixels of WE are built with two incoming gliders, held as
real 2x2 still lifes, and erased with one glider each. All packets exist at
initial generation zero. A score was selected by conservative 2-cell
spacetime-clearance search (see research/PHYSICAL_LYRICS_FIRST_WORD.md).

This pilot demonstrates physical lettering, NOT word-by-word full-song
karaoke. WE finishes by generation 268 (near 11.224s); text starts writing
at g220 and is completely erased at g442 (~18.42s), well after its vocal
end. The separate singer/bubble is unchanged, and the physical word is in
an isolated symbolic stage to avoid crossing the existing bubble border.
"""
from __future__ import annotations
from dataclasses import dataclass
from functools import lru_cache
import json
from pathlib import Path
from .core import evolve,place
from .glider_controlled_mouth import BLOCK,rotate,block_make_at,block_erase_at
from .lyric_font import line_cells

WORD='WE'
AUDIO_START=11.224
AUDIO_END=11.479
CLOCK=24
PITCH=20
COMPLETE_GENERATION=268
ERASED_GENERATION=442
VERIFY_THROUGH=480
WORD_STAGE_ORIGIN=(2400,-100)

@dataclass(frozen=True)
class PixelRoute:
    x:int
    y:int
    make_tick:int
    make_orientation:int
    erase_tick:int
    erase_orientation:int

@lru_cache(maxsize=1)
def routes()->tuple[PixelRoute,...]:
    path=Path(__file__).resolve().parent.parent/'data'/'we_physical_glider_routes.json'
    return tuple(PixelRoute(*row) for row in json.loads(path.read_text(encoding='utf-8')))


def target_cells()->set[tuple[int,int]]:
    return line_cells(WORD,(0,0),pitch=PITCH)


def pixel_target(route:PixelRoute)->set[tuple[int,int]]:
    return place(BLOCK,route.x,route.y)


def pixel_seed(route:PixelRoute)->set[tuple[int,int]]:
    make=place(rotate(block_make_at(route.make_tick),route.make_orientation),route.x,route.y)
    erase=place(rotate(block_erase_at(route.erase_tick),route.erase_orientation),route.x,route.y)
    return make|erase


def signal_components()->dict[str,set[tuple[int,int]]]:
    return {f'WE_pixel_{i:02}':pixel_seed(route) for i,route in enumerate(routes())}


def local_universe()->set[tuple[int,int]]:
    return set().union(*signal_components().values())


def composed_components(with_character=True)->dict[str,set[tuple[int,int]]]:
    # Physically one board with distant native Life components, no render-time layers.
    parts={f'lyric_{k}':place(v,*WORD_STAGE_ORIGIN)
           for k,v in signal_components().items()}
    if with_character:
        from .character_round2 import components as character_parts
        parts.update(character_parts(with_bubble=True))
    return parts


def composed_universe(with_character=True)->set[tuple[int,int]]:
    return set().union(*composed_components(with_character).values())


def observed_glyph(live:set[tuple[int,int]],origin=(0,0))->set[tuple[int,int]]:
    """Actual live cells in glyph's target rectangles; never a renderer swap."""
    tgt=place(target_cells(),*origin)
    return live&tgt


def simulate(samples=(0,200,220,240,260,268,312,366,398,420,442,480)):
    """Evolve local native universe and yield exact requested sample states."""
    samples=set(samples)
    live=local_universe()
    for t in range(max(samples)+1):
        if t in samples:
            yield t,live
        if t<max(samples):live=evolve(live)
