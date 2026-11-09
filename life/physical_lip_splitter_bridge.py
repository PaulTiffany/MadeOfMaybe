"""A real lyric-glider branch controls an EXISTING lip block of the singer.

Physical B3/S23 bridge, not a synchronized playback overlay:
* One initial incoming glider traverses an 84-cell stable duplicator.
* The duplicator's SW output replaces the original make glider for the
  existing WE glyph's first 2x2 Life pixel, at its native onset g=2156.
* Its NE output replaces the original erase glider for the lower-left
  MEDIUM-lip pixel, removing that actual singer lip tile at g~2312.
* The latter tile's final erase glider is rerouted by D4 orientation to
  preserve its subsequent rebuild/reset, avoiding the splitter's other path.

This is ONE physical mouth tile / ONE lyric pixel, NOT a 403-word fanout
network or a replacement for the entire lip bank. All other existing lip
circuits, facial art and 360 lyric pixels are retained unchanged.

The single source input is present at g0, all glyph gliders are preloaded,
and the simulation advances at the same 192 generations/audio-second.
"""
from __future__ import annotations

from functools import lru_cache
from .core import evolve,place
from .first_line_singing_character import (retimed_dynamic_components,
    _connected,_glider_velocity,anchor_delay,art_seed,safe_art)
from .first_line_karaoke import (components as lyric_components, score as lyric_score,
    max_envelope_radius, ERASE_GENERATION, GPS)
from .glider_controlled_mouth import BLOCK,rotate,block_erase_at
from .lyric_mouth_fanout import (CATALYSTS,PRIMARY_INPUT,NORTHWEST_GLIDER,
    SOUTHEAST_GLIDER)

LIP_NAME='lower_medium_0'
LIP_TARGET=(-80,54)
WORD_PIXEL=(0,0)
WORD_COMPONENT='WE_0_pixel_000'
SPLITTER_ORIENTATION=2
SPLITTER_LOCAL_ORIGIN=(-563,489)
# Exact translation forced by identifying both glider outputs at generation 340.
# This moves the portrait near (but NOT into) the word's certified footprint.
SINGER_TRANSLATION=(1071,-1019)
FINAL_ERASER_D4=6
SELECTED_ERASE_LOCAL_G=458
REFERENCE_SPLIT_OUTPUT_G=340
CAUSAL_WORD_G=lyric_score()[0].make_g # 2156
CAUSAL_LIP_G=2312
ABLATED_VALID_THROUGH_G=2350
FULL_CHECK_G=anchor_delay()+980


def split_input():
    return place(rotate(PRIMARY_INPUT,SPLITTER_ORIENTATION),*SPLITTER_LOCAL_ORIGIN)


def splitter_catalysts():
    return place(rotate(CATALYSTS,SPLITTER_ORIENTATION),*SPLITTER_LOCAL_ORIGIN)


def split_seed(include_input=True):
    return splitter_catalysts() | (split_input() if include_input else set())


def _sort_gliders(cells):
    return sorted((set(x) for x in _connected(cells)),
                  key=lambda p:(min(x for x,y in p),min(y for x,y in p)))


@lru_cache(maxsize=1)
def replaced_lip_glider():
    pieces=_sort_gliders(retimed_dynamic_components()[LIP_NAME])
    assert len(pieces)==6 and all(len(x)==5 for x in pieces)
    return frozenset(pieces[2])


@lru_cache(maxsize=1)
def replaced_word_glider():
    pieces=_sort_gliders(lyric_components()[WORD_COMPONENT])
    matches=[p for p in pieces if len(p)==5 and _glider_velocity(p)==(-1,1)]
    assert len(matches)==1
    return frozenset(matches[0])


@lru_cache(maxsize=1)
def replacement_final_eraser():
    glider=place(rotate(block_erase_at(SELECTED_ERASE_LOCAL_G),FINAL_ERASER_D4),
                 *LIP_TARGET)
    v=_glider_velocity(glider)
    assert v==(1,-1)
    delta=anchor_delay()//4
    return frozenset(place(glider,-v[0]*delta,-v[1]*delta))


@lru_cache(maxsize=1)
def character_dynamic_parts():
    old=retimed_dynamic_components()
    pieces=_sort_gliders(old[LIP_NAME])
    out={name:frozenset(cells) for name,cells in old.items() if name!=LIP_NAME}
    # Index 2 is supplied by splitter output; index 0 would intersect the
    # other branch and is replaced by an independently routed erase glider.
    for i in (1,3,4,5):out[f'{LIP_NAME}_retained_{i}']=frozenset(pieces[i])
    out[f'{LIP_NAME}_repaired_final_erase']=replacement_final_eraser()
    out['shared_84cell_catalysts']=frozenset(splitter_catalysts())
    out['shared_only_input_glider']=frozenset(split_input())
    return out


def character_dynamic_seed(*,source_enabled=True):
    parts=character_dynamic_parts()
    return set().union(*(v for k,v in parts.items()
                         if source_enabled or k!='shared_only_input_glider'))


def lyric_seed_without_replaced_glider():
    """The REAL complete 7-word lyric stage, missing only one native glider."""
    all_lyrics=set().union(*lyric_components().values())
    original=replaced_word_glider()
    assert original<=all_lyrics
    return all_lyrics-set(original)


def coupled_pixel_remainder():
    return set(lyric_components()[WORD_COMPONENT])-set(replaced_word_glider())


def bridge_unit_seed(*,source_enabled=True,with_art=False):
    """Exact joint real singer + ONE real word pixel, in GLOBAL coordinates."""
    seed=place(character_dynamic_seed(source_enabled=source_enabled),*SINGER_TRANSLATION)
    seed|=coupled_pixel_remainder()
    if with_art:seed|=place(art_seed(),*SINGER_TRANSLATION)
    return seed


def complete_world_seed(*,source_enabled=True):
    """Seven real lyric words + the full character, ONE static initial world."""
    singer=place(character_dynamic_seed(source_enabled=source_enabled),*SINGER_TRANSLATION)
    static=place(art_seed(),*SINGER_TRANSLATION)
    lyric=lyric_seed_without_replaced_glider()
    if len(singer|static|lyric)!=len(singer)+len(static)+len(lyric):
        raise AssertionError('initial singer, portrait art and lyrics overlap')
    return singer|static|lyric


def assert_exact_signal_match():
    """Prove the duplicator branches REPLACE (not accompany) original gliders."""
    mouth=set(replaced_lip_glider())
    word=set(replaced_word_glider())
    for _ in range(REFERENCE_SPLIT_OUTPUT_G):
        mouth=evolve(mouth)
        word=evolve(word)
    output_mouth=place(rotate(NORTHWEST_GLIDER,SPLITTER_ORIENTATION),
                       *SPLITTER_LOCAL_ORIGIN)
    output_word=place(rotate(SOUTHEAST_GLIDER,SPLITTER_ORIENTATION),
                      SPLITTER_LOCAL_ORIGIN[0]+SINGER_TRANSLATION[0],
                      SPLITTER_LOCAL_ORIGIN[1]+SINGER_TRANSLATION[1])
    assert mouth==output_mouth
    assert word==output_word
    return {'native_g':REFERENCE_SPLIT_OUTPUT_G,
            'replaced_existing_lip_signal':True,
            'replaced_existing_lyric_signal':True,
            'shared_initial_input_gliders':1,
            'splitter_stationary_catalyst_cells':len(CATALYSTS)}


def word_and_lip_at(world):
    """Read actual Life-cell occupancy, never a renderer-derived score."""
    word=place(BLOCK,*WORD_PIXEL)<=world
    x=LIP_TARGET[0]+SINGER_TRANSLATION[0]
    y=LIP_TARGET[1]+SINGER_TRANSLATION[1]
    lip=place(BLOCK,x,y)<=world
    return (word,lip)


@lru_cache(maxsize=1)
def spatial_certificate():
    """Screen word-pixel envelope vs every OTHER native karaoke pixel.

    The other 360 glyph routes have already been individually qualified by
    their exact <=R footprint from the pixel target until line clear, and
    are EMPTY afterward. This bridge unit's bounding box is measured from
    exact native Life states, expanded by 4 cells to cover clock phases.
    The bound also includes all original static character art, unchanged.
    """
    radius=max_envelope_radius()
    static=place(art_seed(),*SINGER_TRANSLATION)
    core=bridge_unit_seed()
    xs=[x for x,y in static];ys=[y for x,y in static]
    xmin,xmax,ymin,ymax=min(xs),max(xs),min(ys),max(ys)
    for g in range(ERASE_GENERATION+1):
        if g%4==0:
            left=min(x for x,y in core); right=max(x for x,y in core)
            top=min(y for x,y in core); bottom=max(y for x,y in core)
            xmin=min(xmin,left);xmax=max(xmax,right)
            ymin=min(ymin,top);ymax=max(ymax,bottom)
        if g<ERASE_GENERATION:core=evolve(core)
    xmin-=4;xmax+=4;ymin-=4;ymax+=4
    distances=[]
    for wi,w in enumerate(lyric_score()):
        for j,(x,y) in enumerate(w.targets):
            if wi==0 and j==0:continue
            dx=max(xmin-x,x-xmax,0)
            dy=max(ymin-y,y-ymax,0)
            distances.append(max(dx,dy)-radius-2)
    least=min(distances)
    if least<=0:
        raise AssertionError('a separate karaoke pixel may collide with the bridge')
    return {'measured_bridge_life_bbox':[xmin,xmax,ymin,ymax],
            'other_lyric_pixel_count':len(distances),
            'lyric_individual_radius':radius,
            'minimum_guaranteed_life_cell_clearance':least,
            'native_clock_gps':GPS,'source_glider_controls_real_word_and_lip':True,
            'completed_full_song_lip_wiring':False}


def assert_portrait_protected(*,end=FULL_CHECK_G):
    """Exact B3/S23 2-cell-halo check against UNMODIFIED hair, eyes, etc."""
    art=art_seed()
    forbidden={(x+dx,y+dy) for x,y in art
               for dx in (-2,-1,0,1,2) for dy in (-2,-1,0,1,2)}
    dynamic=character_dynamic_seed()
    for g in range(end+1):
        if any(c in forbidden for c in dynamic):
            raise AssertionError(f'portrait collision at native generation {g}')
        if g<end: dynamic=evolve(dynamic)
    return {'verified_native_generations':end,
            'unchanged_art_cells':len(art),
            'full_art_replacement_or_masking':False}
