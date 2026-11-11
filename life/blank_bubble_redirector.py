"""Reuse the EXISTING LWSS right-angle turner inside a blank native speech bubble.

The earlier 19-cell vertical-to-horizontal B3/S23 reaction and its three
qualified eater-1 fishhooks are unchanged. A small real aperture lets an
incoming vertical LWSS enter the bubble, turn left at g2156, traverse the
empty display region and be eaten without ash. One g0 Life universe.
This proves a single routed pixel, NOT the whole 403-word karaoke.
"""
from functools import lru_cache
from .core import evolve,place
from .composition import bubble_parts
from .relocated_singer_anchor import relocated_anchor,portrait,SINGER_TRANSLATION
from .vertical_lwss_corner import STATION,INPUT,outgoing_lwss
from .staggered_word_mesh import EATER_NORTHEAST,EATER_SOUTHWEST,EATER_TEXT

STATION_LOCAL=(460,-122)
CATCHER_LOCAL_X=285
TOP_APERTURE_X=(428,459)
OUTPUT_G=2156
FLIGHT_DELAY=(OUTPUT_G-200)//4
NATIVE_END_G=3648

@lru_cache(maxsize=1)
def bubble_outline():
    border,_obsolete_static_text=bubble_parts()
    border=place(border,160,-90)
    # Remove complete native 2x2 still-life border tiles, never overpaint.
    border={p for p in border if not(p[1] in (-174,-173)
            and TOP_APERTURE_X[0]<=p[0]<=TOP_APERTURE_X[1])}
    if evolve(border)!=border:
        raise AssertionError('bubble entry aperture is not stable Life')
    return frozenset(border)

@lru_cache(maxsize=1)
def existing_redirector():
    x,y=STATION_LOCAL
    station=place(STATION,x,y)
    incoming=place(INPUT,x,y-2*FLIGHT_DELAY)
    cleanup=place(EATER_NORTHEAST,x,y)|place(EATER_SOUTHWEST,x,y)|place(
        EATER_TEXT,CATCHER_LOCAL_X+57,y)
    if len(station|incoming|cleanup)!=19+9+3*7:
        raise AssertionError('existing turner hardware overlaps')
    return frozenset(station|incoming|cleanup)

@lru_cache(maxsize=1)
def persistent_hardware():
    x,y=STATION_LOCAL
    return frozenset(place(EATER_NORTHEAST,x,y)
        |place(EATER_SOUTHWEST,x,y)
        |place(EATER_TEXT,CATCHER_LOCAL_X+57,y))

def components():
    base=relocated_anchor()|portrait()|place(bubble_outline(),*SINGER_TRANSLATION)
    device=place(existing_redirector(),*SINGER_TRANSLATION)
    if base&device:raise AssertionError('existing turner overlaps singer/controller/bubble')
    return frozenset(base),frozenset(device)

def universe():
    base,turner=components()
    return set(base|turner)

def source_report():
    """Direct exact native test of the *unchanged*, established reaction."""
    moving=set(existing_redirector())
    for g in range(NATIVE_END_G+1):
        if g in (OUTPUT_G,OUTPUT_G+24):
            output=outgoing_lwss(moving)
            if output is None or len(output)!=12:
                raise AssertionError(f'no outgoing LWSS at g{g}')
            expected=(417,-110) if g==OUTPUT_G else (405,-110)
            if (min(x for x,y in output),min(y for x,y in output))!=expected:
                raise AssertionError(f'LWSS phase/path wrong at g{g}')
        if g<NATIVE_END_G:moving=evolve(moving)
    if moving!=set(persistent_hardware()):
        raise AssertionError('redirector emitted unconsumed debris')
    return {'rule':'B3/S23','initial_population':len(universe()),
            'blank_bubble':True,'entry_aperture_native_still_life':True,
            'same_19_cell_turner':True,'source_turn_generation':OUTPUT_G,
            'output_position':(417,-110),'output_c2_verified':True,
            'native_cleanup_generation':NATIVE_END_G,
            'remaining_original_eater_cells':21,
            'turner_reusable':False,'full_song_integrated':False}
