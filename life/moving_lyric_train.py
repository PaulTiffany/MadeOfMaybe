"""Experimental moving lyric glyphs using native independent Conway spaceships.

Each lit 5x7 font position becomes one real 9-cell lightweight spaceship,
moving left at c/2 rather than remaining a static 2x2 block. This is a
motion/packing proof, NOT a connected karaoke or colored global switch.
"""
from __future__ import annotations
from .core import evolve, parse_rle, place
from .lyric_font import GLYPHS

LWSS_RLE = 'x = 5, y = 4, rule = B3/S23\nbo2bo$o$o3bo$4o!'
LWSS = frozenset(parse_rle(LWSS_RLE))
GLYPH_PITCH = 8
GENERATIONS_PER_SECOND = 192

def lit_ship_origins(text, *, pitch=GLYPH_PITCH):
    if pitch < GLYPH_PITCH:
        raise ValueError('unverified LWSS pixel pitch')
    origins = []
    for i, char in enumerate(text.upper()):
        try:
            glyph = GLYPHS[char]
        except KeyError as exc:
            raise ValueError(f'unsupported character: {char!r}') from exc
        for row, bits in enumerate(glyph):
            for col, lit in enumerate(bits):
                if lit == '1':
                    origins.append((pitch * (6 * i + col), pitch * row))
    return tuple(origins)

def moving_word_components(text, *, pitch=GLYPH_PITCH, origin=(0, 0)):
    ox, oy = origin
    return tuple(frozenset(place(LWSS, ox + x, oy + y))
                 for x, y in lit_ship_origins(text, pitch=pitch))

def seed(text, *, pitch=GLYPH_PITCH, origin=(0, 0)):
    parts = moving_word_components(text, pitch=pitch, origin=origin)
    result = set().union(*parts)
    if len(result) != 9 * len(parts):
        raise AssertionError('moving glyph ships overlap at generation zero')
    return result

def native_motion_certificate(text='WE MADE', *, steps=128, pitch=GLYPH_PITCH):
    """Every tick is real B3/S23: whole phrase translates without crosstalk."""
    if steps < 0 or steps > 1024:
        raise ValueError('unsupported finite test horizon')
    pieces = tuple(map(set, moving_word_components(text, pitch=pitch)))
    world = set().union(*pieces)
    initial = set(world)
    for g in range(steps + 1):
        if world != set().union(*pieces):
            raise AssertionError(f'spaceship glyphs interact at generation {g}')
        if g % 4 == 0 and world != place(initial, -g // 2, 0):
            raise AssertionError(f'glyph not translated at generation {g}')
        if g < steps:
            world = evolve(world)
            pieces = tuple(evolve(part) for part in pieces)
    return {'rule': 'B3/S23', 'text': text, 'initial_cells': len(initial),
            'ships': len(pieces), 'generation_horizon': steps,
            'exactly_translates_c2_orthogonal': True,
            'all_ships_independent': True, 'color_is_native_life_state': False,
            'word_highlight_switch_implemented': False,
            'phrase_gate_connected': False, 'whole_song_physical_lane_fit': False}

def minimum_linear_word_extent(word, *, pitch=GLYPH_PITCH):
    if not word:
        return 0
    return (6 * len(word) - 1) * pitch + 5

def onset_gap_vs_word_extent(first_word, second_word, *, pitch=GLYPH_PITCH):
    """Necessary (not sufficient) single-rail fit for successive word onsets."""
    g0, g1 = first_word.make_g, second_word.make_g
    if g1 < g0:
        raise ValueError('word events not ordered')
    shift = (g1 - g0) // 2
    extent = minimum_linear_word_extent(first_word.text, pitch=pitch)
    return {'first_word': first_word.text, 'second_word': second_word.text,
            'generations_between_word_onsets': g1 - g0,
            'linear_cells_available_at_c2': shift,
            'first_word_lwss_extent_cells': extent,
            'minimum_guard_cells': 2,
            'one_rail_nonoverlap_possible': shift >= extent + 2}
