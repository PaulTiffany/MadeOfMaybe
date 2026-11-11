"""One physical glider input → karaoke pixel AND three-state mouth port.

This is a *four-word causal integration pilot*, not yet the 403-word physical
mouth harness or a replacement for the character's existing lip artwork.
One stable 84-cell glider duplicator is supplied per word event. Its NW and
SE output gliders operate a 2-bit three-state mouth register and physically
construct one independently measurable lyric pixel. Every other glider used
as a partner in a two-glider block synthesis is preloaded at generation zero.

Source of the splitter topology: LifeWiki's stable (74/75/78+) glider
  duplicator: https://conwaylife.com/wiki/Glider_duplicator
The displayed 76x53 RLE contains two example input gliders and a transient
six-cell object. Remove both examples and transient to obtain 84 stable
catalyst cells. Reintroduce exactly ONE input glider for each event.

Causal test: remove any one input glider and BOTH its lyric block and the
corresponding mouth transition fail. All 4 events are driven by the exact
word-onset generations already compiled by life.full_song_karaoke.
"""
from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from .core import evolve, parse_rle, place
from .full_song_karaoke import ALIGNMENT_FILE, GPS, compile_plan
from .lyric_cues import read_alignment
from .glider_controlled_mouth import (BLOCK, SYNTH_GLIDER_SW, rotate)

# Original RLE is included as provenance, rather than an unexplained array
# of cells. The shape is from LifeWiki's stable duplicator example.
REFERENCE_RLE = '''x = 76, y = 53, rule = B3/S23
obo$b2o$bo17$20bo$21b2o$20b2o5$51b2o$52bo$52bobo$42bo10b2o$40b3o$39bo$39b2o$24b2o48b2o$25bo48b2o$25bob2o$26bo2bo23bo$27b2o24bo$42b2o9b3o$42b2o11bo4$51bo3b2o$50bobo3bo$49bobo3bo$45b2obobo3bo$45b2obo2b4obo5b2o$49bobo3bobo5bo$45b2ob2o2bo2bobo2b3o$46bobo2b2o3bo3bo$34b2o10bobo$34b2o11bo!'''
PRIMARY_INPUT = frozenset({(0,0),(2,0),(1,1),(2,1),(1,2)})
SECOND_REFERENCE_INPUT = frozenset({(20,19),(20,21),(21,20),(21,21),(22,20)})
TRANSIENT = frozenset({(53,36),(53,37),(53,38),(54,38),(55,38),(55,39)})
CATALYSTS = frozenset(parse_rle(REFERENCE_RLE)-PRIMARY_INPUT-SECOND_REFERENCE_INPUT-TRANSIENT)
SPLIT_G = 340
# These are exact B3/S23 glider states at generation 340 of the primitive.
NORTHWEST_GLIDER = frozenset({(57,9),(57,10),(57,11),(58,9),(59,10)})
SOUTHEAST_GLIDER = frozenset({(76,55),(77,53),(77,55),(78,54),(78,55)})

# Three named states are encoded by TWO independent stable 2x2 Life blocks:
# CLOSED = C present, O absent; MEDIUM = neither; OPEN = O present, C absent.
# Only one mouth bit changes per word onset. Coordinates are an intentionally
# separated route-qualification register, *not* the final rendered lip geometry.
CLOSED_PORT = (0,0)
OPEN_PORT = (100,20)
WORD_START_STATES = ('medium','open','medium','closed')
# Explicitly spaced nonintersecting preloaded splitter routes. These values
# were obtained by native B3/S23 testing, NOT a decorative animation choice.
RELATIVE_FLIGHT_STEPS = (0,90,200,340)
ACTION_SCRIPT = (('erase','closed'),('make','open'),('erase','open'),('make','closed'))
CHECKPOINTS = {0:'closed',2156:'medium',2204:'open',2272:'medium',2296:'closed'}
FINAL_QUALIFICATION_G = 2320


@dataclass(frozen=True)
class SharedWordEvent:
    index: int
    word: str
    make_g: int
    action: str
    mouth_port: str
    flight_steps: int
    trigger_generation: int
    splitter_translation: tuple[int,int]
    word_pixel: tuple[int,int]
    mouth_pixel: tuple[int,int]


def song_score():
    # The two-line fixture is for local pilot tests only. GitHub CI contains
    # the full Suno alignment and qualifies all word-onset intent entries.
    source = ALIGNMENT_FILE if ALIGNMENT_FILE.exists() else (
        Path(__file__).resolve().parents[1] / 'data' / 'first_verse_alignment_fixture.json')
    return compile_plan(read_alignment(source))


def full_song_mouth_intent():
    """Whole-song *intent* score; 403 shared word onsets, not wired hardware.

    This has no separate clock or phoneme source. Subsequent hardware routing
    must still add line-clear closes, avoid repeated-lane interference, and
    fan out from one mouth port to the singer's real multi-tile lip banks.
    """
    return tuple({'word_index':w.word_index,'word':w.text,'generation':w.make_g,
                  'seconds':w.make_g/GPS,
                  'target_state':WORD_START_STATES[w.word_index%4],
                  'source_line':line.line_index}
                 for line in song_score() for w in line.words)


@lru_cache(maxsize=1)
def events() -> tuple[SharedWordEvent,...]:
    first = song_score()[0]
    result=[]
    for i,(word,(action,port),k) in enumerate(zip(first.words,ACTION_SCRIPT,RELATIVE_FLIGHT_STEPS)):
        when=word.make_g
        rel_time=600+4*k
        trigger=when-rel_time
        if trigger<0 or trigger%4:
            raise ValueError('splitter input must have nonnegative 4-phase preflight')
        mouth=CLOSED_PORT if port=='closed' else OPEN_PORT
        if action=='erase':
            relative_mouth=(144+k,121+k)
            relative_word=(-11-k,-57-k)
        else:
            relative_mouth=(-11-k,-57-k)
            relative_word=(143+k,122+k)
        translation=(mouth[0]-relative_mouth[0],mouth[1]-relative_mouth[1])
        result.append(SharedWordEvent(i,word.text,when,action,port,k,trigger,
                    translation,tuple(relative_word[j]+translation[j] for j in (0,1)),mouth))
    return tuple(result)


def event_parts(event: SharedWordEvent) -> dict[str,set[tuple[int,int]]]:
    """All native Life seed cells for one reusable splitter and two sinks.

    The two output gliders are created by the duplicator under actual Life,
    never inserted directly. At g=trigger+340 they have exact known shape.
    """
    i=event.index
    when=event.make_g
    k=event.flight_steps
    translation=event.splitter_translation
    n=(when-4)//4
    mouth=event.mouth_pixel
    word=event.word_pixel
    if event.action=='erase':
        # Output NW will be glider 1 in a real two-glider lyric block synthesis.
        partner_word=place(SYNTH_GLIDER_SW,word[0]+4+n,word[1]+2-n)
        partner_mouth=set()
    else:
        # NW splitter output makes the mouth bit; partner is a second glider.
        partner_mouth=place(SYNTH_GLIDER_SW,mouth[0]+4+n,mouth[1]+2-n)
        # SE splitter output becomes a lyric MAKE glider after D4 orientation 3.
        # Transform the second, independent precursor glider in the full
        # two-glider synthesis at the word output target.
        partner_word=place(rotate(place(SYNTH_GLIDER_SW,4+n,2-n),3),*word)
    return {
        f'device_{i}':place(set(CATALYSTS),*translation),
        f'trigger_{i}':place(set(PRIMARY_INPUT),translation[0]-event.trigger_generation//4,
                          translation[1]-event.trigger_generation//4),
        f'word_partner_{i}':partner_word,
        f'mouth_partner_{i}':partner_mouth,
    }


def components(missing_inputs=frozenset()):
    """Initial conditions only; missing_inputs used for causal ablation tests."""
    parts={'closed_port_initial':place(BLOCK,*CLOSED_PORT)}
    for event in events():
        pieces=event_parts(event)
        if event.index in missing_inputs:
            pieces.pop(f'trigger_{event.index}')
        parts.update(pieces)
    return parts


def universe(missing_inputs=frozenset()):
    return set().union(*components(missing_inputs).values())


def mouth_state(world):
    closed=place(BLOCK,*CLOSED_PORT)<=world
    opened=place(BLOCK,*OPEN_PORT)<=world
    if closed and not opened:return 'closed'
    if opened and not closed:return 'open'
    if not closed and not opened:return 'medium'
    return 'INVALID:both_ports_active'


def formed_word_pixels(world):
    return {event.word: place(BLOCK,*event.word_pixel)<=world for event in events()}


def checkpoints(*, missing_inputs=frozenset(), samples=None):
    """Direct B3/S23 evolution; advances one unchanged initial world."""
    samples=set(CHECKPOINTS if samples is None else samples)
    world=universe(missing_inputs)
    for g in range(max(samples)+1):
        if g in samples:
            yield g,set(world)
        if g<max(samples):world=evolve(world)
