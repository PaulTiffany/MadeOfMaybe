"""One actual B3/S23 singer, two converted words and TWO causal W/V mouth events.

Incremental integration of the previously qualified 8814-cell WE+MADE singer.
The original face, word glyph converters, lip motion and first WE-associated
W/V marker remain intact. A second, original 19-cell converter-borne W marker
and an independent Suno-stem V glider physically make a previously inactive
MEDIUM lip tile at original MADE onset g2204. The block is erased at g2326.

This uses precisely the existing native_word_vocal_link marker architecture,
not a new lip renderer or an invented word signal. The marker is the same
original supplementary W lane used for WE, not a tapped glyph-pixel branch.

Only 33 original fixed 2x2 facial-art tiles are omitted at g0 to clear this
extra signal path, following the original actor's clearance approach.
No runtime interventions. Source and one-world B3/S23 short movie qualified
locally. This is a two-word, two-W/V-event sprint, NOT all-song wiring.
"""
from __future__ import annotations
import json
from pathlib import Path
from functools import lru_cache
from .core import evolve, place
from .vertical_lwss_corner import STATION, INPUT
from .staggered_word_mesh import EATER_NORTHEAST, EATER_TEXT
from .glider_controlled_mouth import SYNTH_GLIDER_NW, block_erase_at, rotate, BLOCK
from .relocated_singer_anchor import SINGER_TRANSLATION
from .native_word_vocal_link import marker_to_mouth, MARKER_STATION, MOUTH_CORNER
from .two_line_native_singer import components as original_components

WORD_MADE_G = 2204
SOURCE_WE_G = 2156
SOURCE_MADE_ERASE_G = 2326
MEDIUM_LIP_TARGET = (1046, -910)
CLEARANCE_END_G = 2400
EXPECTED_ORIGINAL_PART_SIZES = (6408, 742, 240, 52, 1372)
EXPECTED_REMOVED_FACE_TILES = 33

def made_word_marker_sources(*,word=True,vocal=True):
    """Second real 19-cell corner and two-source W/V lip synthesis at MADE."""
    dx = MEDIUM_LIP_TARGET[0] - (MOUTH_CORNER[0] + SINGER_TRANSLATION[0])
    dy = MEDIUM_LIP_TARGET[1] - (MOUTH_CORNER[1] + SINGER_TRANSLATION[1])
    sx = MARKER_STATION[0] + SINGER_TRANSLATION[0] + dx
    sy = MARKER_STATION[1] + SINGER_TRANSLATION[1] + dy
    source = (place(STATION | EATER_NORTHEAST, sx, sy)
              | place(EATER_TEXT, sx-232, sy)
              | place(block_erase_at(SOURCE_MADE_ERASE_G), *MEDIUM_LIP_TARGET))
    if word:
        # Same original W-marker converter; twelve additional input periods
        # place the downstream W byproduct at the MADE Suno time.
        periods = 130 + (WORD_MADE_G-SOURCE_WE_G)//4
        source |= place(INPUT, sx, sy-2*periods)
    if vocal:
        # Independent V input from the already recorded isolated-Suno activity
        # interval 10.96...13.50, containing MADE at g2204.
        n = (WORD_MADE_G-4)//4
        source |= place(rotate(place(SYNTH_GLIDER_NW, 4+n, 2+n), 3),
                        *MEDIUM_LIP_TARGET)
    if len(source) != 38+9*bool(word)+5*bool(vocal):
        raise AssertionError('MADE W/V source accidentally overlaps at g0')
    return source

def _tile_containing(face, x, y):
    for dx in (0,-1):
        for dy in (0,-1):
            tile = frozenset((x+dx+i,y+dy+j) for i in (0,1) for j in (0,1))
            if tile <= face:
                return tile
    raise AssertionError(('facial 2x2 tile not located', x, y))

@lru_cache(maxsize=1)
def scene_components():
    previous = tuple(map(set, original_components(900,144)))
    if tuple(map(len,previous)) != EXPECTED_ORIGINAL_PART_SIZES:
        raise AssertionError('existing first-two-word singer has changed')
    if place(marker_to_mouth(), *SINGER_TRANSLATION) != previous[3]:
        raise AssertionError('existing qualified original W/V marker has changed')
    face = previous[0]
    extra = made_word_marker_sources()
    shadowed = set()
    live = set(extra)
    # Exact per-generation physical sweep, not a hypothetical track.
    # Only ORIGINAL STATIONARY facial blocks are cleared at g0.
    for g in range(CLEARANCE_END_G+1):
        for x,y in live:
            for dx in range(-2,3):
                for dy in range(-2,3):
                    if (x+dx,y+dy) in face:
                        shadowed.add(_tile_containing(face,x+dx,y+dy))
        if g<CLEARANCE_END_G:
            live = evolve(live)
    removed = set().union(*shadowed)
    if len(shadowed)!=EXPECTED_REMOVED_FACE_TILES or len(removed)!=4*len(shadowed):
        raise AssertionError(('unexpected face clearance',len(shadowed)))
    retained = face - removed
    if evolve(retained) != retained:
        raise AssertionError('original facial blocks cease to be stable')
    parts = (retained, previous[1], previous[2], previous[3], previous[4],extra)
    if len(set().union(*parts))!=8734 or sum(map(len,parts))!=8734:
        raise AssertionError('original 8814 singer and 52-cell second marker overlap')
    return tuple(frozenset(p) for p in parts)

def universe():
    return set().union(*scene_components())

def export(folder):
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)
    parts = scene_components()
    with (folder/'we_made_two_WV_g0.tsv').open('w') as f:
        for x,y in sorted(universe()):
            f.write(f'{x} {y}\n')
    with (folder/'we_made_two_WV_parts.tsv').open('w') as f:
        f.write(f'{len(parts)}\n')
        for i,part in enumerate(parts):
            for x,y in sorted(part):
                f.write(f'{i} {x} {y}\n')
    scope = {
        'rule':'B3/S23', 'original_suno_song':'53610991-7381-4749-96e1-79b8e3b1c28b',
        'original_V_stem':'bee52d16-b01b-4224-bd4c-5c51081d813b',
        'g0_population':8734, 'original_face_singer_lyrics_unmodified_except_33_clearance_tiles':True,
        'original_Suno_WE_W_V_onset_g':SOURCE_WE_G,
        'new_Suno_MADE_W_V_onset_g':WORD_MADE_G,
        'original_WE_MADE_19_cell_down_to_west_converters_preserved':True,
        'new_MADE_marker_19_cell_converter':True,
        'original_WV_lip_target':[1191,-947],
        'new_WV_existing_medium_lip_target':list(MEDIUM_LIP_TARGET),
        'new_MADE_lip_erased_at_g':SOURCE_MADE_ERASE_G,
        'removed_stable_face_tiles_at_g0':EXPECTED_REMOVED_FACE_TILES,
        'original_three_state_mouth_hardware_preserved':True,
        'extra_W_marker_is_companion_word_lane_not_tapped_LWSS_glyph':True,
        'full_song_WV_wired':False,
        'all_403_words_converted_in_actor_space':False,
        'complete_song_video':False,
    }
    (folder/'we_made_two_WV_scope.json').write_text(json.dumps(scope,indent=2)+'\n')
    return scope

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser()
    p.add_argument('--out',type=Path,required=True)
    print(json.dumps(export(p.parse_args().out),indent=2))
