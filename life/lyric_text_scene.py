"""First lyric line, native Life cues for ALL SEVEN aligned words.

This is the next step after lyric_text_pilot: two independent still-life
caption pages occupy the same initial B3/S23 universe and seven native
make/erase glider cue-lamps are scheduled against Suno word onset times.

IMPORTANT: neither caption page is dynamically manufactured or replaced;
text is present from generation zero. Camera can pan/cut between regions in
previews, but the Life universe remains one uninterrupted fixed-rate run.
"""
from __future__ import annotations
from dataclasses import dataclass
from .core import place
from .lyric_font import line_cells
from .lyric_cues import GENERATIONS_PER_SECOND
from .lyric_text_pilot import (
    LAMPS as FIRST_LAMPS, WordLamp, END_GENERATION,
    components as first_components, lamp_seed, lamp_target,
)

# Retain original character, fully qualified first bubble and four cues.
# The second independent bubble is simply translated from the first and
# holds the remaining words of the *same* lyric line.
SECOND_BUBBLE_OFFSET = (600, 0)
SECOND_CAPTION_LINES = ('OUT OF', 'SAND')
SECOND_CAPTION_ORIGINS = ((895, -149), (891, -91))
SECOND_LAMPS = (
    WordLamp('OUT',12.593,(1140,-140),3,0),
    WordLamp('OF',12.909,(1140,-90),0,1),
    WordLamp('SAND',12.968,(1140,-40),2,3),
)
ALL_LAMPS = FIRST_LAMPS + SECOND_LAMPS
QUALIFICATION_GENERATIONS = 350


def second_caption_cells():
    return set().union(*(line_cells(line,origin)
                         for line,origin in zip(SECOND_CAPTION_LINES,SECOND_CAPTION_ORIGINS)))


def components():
    parts = first_components()
    parts['bubble_2_outline'] = place(parts['bubble_outline'], *SECOND_BUBBLE_OFFSET)
    parts['bubble_2_caption_5x7'] = second_caption_cells()
    for lamp in SECOND_LAMPS:
        parts[f'lyric_progress_{lamp.word.lower()}'] = lamp_seed(lamp)
    return parts


def universe():
    return set().union(*components().values())


def status(cells: set[tuple[int,int]]):
    """Actual Life-cell make/erase state for each word, not a rendering trick."""
    return {lamp.word:lamp_target(lamp) <= cells for lamp in ALL_LAMPS}


def caption_by_page(page: int):
    if page == 0: return ('WE MADE','A WINDOW')
    if page == 1: return SECOND_CAPTION_LINES
    raise ValueError('First lyric-line pilot has exactly two pages')


def selected_page(generation: int):
    """Camera decision only; not a Life state update."""
    return 0 if generation < round(12.593*GENERATIONS_PER_SECOND) else 1
