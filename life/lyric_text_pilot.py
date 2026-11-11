"""First real Life lyric-control pilot for Made of Maybe (first four words).

The existing speech bubble's two 5x7 caption lines are native Life STILL
LIFES, present from generation zero. Four *new* physical word-progress lamps
are glider-synthesized and erased at Suno-aligned generations while the
entire existing singer and bubble run in the SAME uninterrupted universe.

This is an intentional intermediate milestone, not full karaoke: the words
are not yet built/erased at cue times, and their physical lamps sit just
outside the right bubble border to avoid disturbing the glyphs and frame.
Only the first four aligned words are physically routed. The full-song cue
sheet is compiled separately by life.lyric_cues.
"""
from __future__ import annotations

from dataclasses import dataclass
from .character_round2 import components as character_parts
from .core import place
from .glider_controlled_mouth import BLOCK,block_make_at,block_erase_at,rotate
from .lyric_font import line_cells
from .lyric_cues import AUDIO_ID, GENERATIONS_PER_SECOND, make_generation

CAPTION_LINES = ('WE MADE', 'A WINDOW')
CAPTION_ORIGINS = ((295,-149),(291,-91))
END_GENERATION = 326   # 13.583s, shortly after 'sand' finishes at 13.420s
SAMPLE_START = 240
SAMPLE_END = 350

@dataclass(frozen=True)
class WordLamp:
    word: str
    lyric_start_s: float
    target: tuple[int,int]
    make_direction: int
    erase_direction: int

    @property
    def activation_generation(self) -> int:
        return make_generation(self.lyric_start_s)

# D4 input orientations were selected by clearance search and verified
# over all 350 generations in a single composed B3/S23 universe. Coordinates
# deliberately sit OUTSIDE the bubble to preserve all existing bodywork.
LAMPS = (
    WordLamp('WE',11.224,(540,-140),3,0),
    WordLamp('MADE',11.479,(540,-90),0,1),
    WordLamp('A',11.824,(540,-40),2,1),
    WordLamp('WINDOW',11.964,(540,10),2,1),
)


def caption_cells():
    return set().union(*(line_cells(line,origin)
                         for line,origin in zip(CAPTION_LINES,CAPTION_ORIGINS)))


def lamp_target(lamp: WordLamp):
    return place(BLOCK,*lamp.target)


def lamp_seed(lamp: WordLamp):
    """Generation-zero gliders; block turns on, holds, then disappears."""
    make = rotate(block_make_at(lamp.activation_generation),lamp.make_direction)
    erase = rotate(block_erase_at(END_GENERATION),lamp.erase_direction)
    return place(make|erase,*lamp.target)


def components():
    pieces=character_parts(with_bubble=True)
    pieces.pop('bubble_lyrics')  # deliberately remove old static title at g=0
    pieces['caption_stable_5x7']=caption_cells()
    pieces.update({f'lyric_progress_{lamp.word.lower()}':lamp_seed(lamp)
                   for lamp in LAMPS})
    return pieces


def universe():
    return set().union(*components().values())


def actual_lamp_states(world):
    """Observe actual cells; never tell Life what a word state *should* be."""
    return {lamp.word:lamp_target(lamp)<=world for lamp in LAMPS}
