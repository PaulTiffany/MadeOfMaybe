"""Gondry-style BACKWARD staging of the Suno karaoke as real southbound LWSSes.

A B3/S23 movie is not generally reversible. An isolated period-four LWSS *is*
kinematically reversible: prescribe its desired position at word-onset g,
then place the unchanged ship exactly g/2 Life cells NORTH at generation zero.
All 403 word targets are compiled first, then the one immutable g0 pattern.

Every pixel is a real 9/12-phase spaceship. Words fall DOWN from above;
no converter array, runtime glyph insertion, text overlay or backwards Life
rule is used. The reusable seven-cell south-facing fishhooks eat the ships
after they pass the physical reading line.

This is a lyric-only native universe. The existing singer/rounded rim and
independent Suno vocal-to-mouth hardware are NOT integrated or qualified.
"""
from __future__ import annotations
from bisect import bisect_left, bisect_right
from dataclasses import dataclass, asdict
from functools import lru_cache
from pathlib import Path
import json
from .core import evolve, place
from .phrase_crawler_eater import LWSS, EATER_LEFT
from .native_half_font_first20 import lit_pixels
from .full_song_karaoke import ALIGNMENT_FILE, compile_plan, GPS
from .lyric_cues import read_alignment
from .export_operational import compact_rle

PITCH_X = 10
PITCH_Y = 8
SAME_LANE_GAP = 64
READ_Y = 0
EATER_Y = 160
SONG_END_G = 45864
FPS = 24


def turn_down(cells):
    """Clockwise D4 turn: the existing westbound c/2 LWSS heads south."""
    return {(y, -x) for x, y in cells}


SHIP = frozenset(turn_down(LWSS))
EATER = frozenset(turn_down(EATER_LEFT))


@lru_cache(maxsize=1)
def ship_phases():
    phases = [frozenset(SHIP)]
    for _ in range(3):
        phases.append(frozenset(evolve(phases[-1])))
    if evolve(phases[3]) != place(SHIP, 0, 2):
        raise AssertionError('source is not a southbound c/2 spaceship')
    for p in phases:
        if max(x for x, _ in p) - min(x for x, _ in p) >= 7:
            raise AssertionError('ship extends beyond column isolation envelope')
        if max(y for _, y in p) - min(y for _, y in p) >= 7:
            raise AssertionError('ship extends beyond row isolation envelope')
    return tuple(phases)


@lru_cache(maxsize=1)
def eater_reaction():
    if len(EATER) != 7 or evolve(EATER) != set(EATER):
        raise AssertionError('receiver not a stable fishhook')
    alive = set(EATER | SHIP)
    isolated = set(SHIP)
    trace = [frozenset(alive)]
    first_interaction = None
    for g in range(1, 41):
        alive = evolve(alive)
        isolated = evolve(isolated)
        trace.append(frozenset(alive))
        if alive != set(EATER) | isolated and first_interaction is None:
            first_interaction = g
    if first_interaction != 37 or trace[-1] != EATER:
        raise AssertionError('native receiver reaction changed')
    # A column at x+10 is guaranteed independent for this entire reaction.
    if any(not (-3 <= x <= 4) for state in trace for x, _ in state):
        raise AssertionError('reaction escapes the 8-column isolation envelope')
    return tuple(trace)


@dataclass(frozen=True)
class FallingWord:
    index: int
    text: str
    onset_g: int
    lane: int
    source_line: int
    pixel_count: int
    max_column: int

    @property
    def x0(self):
        return self.lane * lane_stride()

    @property
    def arrival_seconds(self):
        return self.onset_g / GPS


@lru_cache(maxsize=1)
def lane_stride():
    words = [w for line in compile_plan(read_alignment(ALIGNMENT_FILE))
             for w in line.words]
    # 10 cells per column; the furthermost ship/eater reaches +/- 4/3.
    cols = [max(c for c, _ in lit_pixels(w.text)) for w in words]
    return PITCH_X * (max(cols) + 3) + 16


@lru_cache(maxsize=1)
def word_plan():
    words = [w for line in compile_plan(read_alignment(ALIGNMENT_FILE))
             for w in line.words]
    if len(words) != 403 or GPS != 192:
        raise AssertionError('wrong Suno score or clock')
    lane_last = []
    out = []
    previous_g = -1
    for w in words:
        g = w.make_g
        if g < 4 or g % 4 or g < previous_g:
            raise AssertionError('invalid or unsorted source onset')
        previous_g = g
        pixel_coords = lit_pixels(w.text)
        if not pixel_coords:
            raise AssertionError(('word has no physical glyph pixels', w.text))
        lane = next((n for n, old in enumerate(lane_last)
                     if g - old >= SAME_LANE_GAP), None)
        if lane is None:
            lane = len(lane_last)
            lane_last.append(-1000000)
        lane_last[lane] = g
        out.append(FallingWord(w.word_index, w.text, g, lane,
                               w.word_index, len(pixel_coords),
                               max(x for x, _ in pixel_coords)))
    if {w.index for w in out} != set(range(403)):
        raise AssertionError('missing or duplicated source word')
    return tuple(out)


def select_words(count=None, omit=None):
    words = word_plan() if count is None else word_plan()[:count]
    if omit is None:
        return words
    return tuple(w for w in words if w.index != omit)


def pixel_origins(words):
    """Explicit all-at-g0 preimages of the displayed moving ship pixels."""
    for word in words:
        for col, row in lit_pixels(word.text):
            yield (word.x0 + PITCH_X * col,
                   READ_Y + PITCH_Y * row - word.onset_g // 2)


def receiver_sites(words):
    return frozenset((w.x0 + PITCH_X*c, EATER_Y)
        for w in words for c, _ in lit_pixels(w.text))


def receiver_cells(words):
    return set().union(*(place(EATER, x, y) for x, y in receiver_sites(words)))


def seed_cells(words, *, omit=None):
    all_words = tuple(words)
    active = all_words if omit is None else tuple(w for w in all_words if w.index != omit)
    fixed = receiver_cells(all_words)
    points = tuple(pixel_origins(active))
    moving = set().union(*(place(SHIP, *xy) for xy in points))
    if len(moving) != 9*len(points) or moving & fixed:
        raise AssertionError('native input ships overlap each other or the receivers')
    return fixed | moving


def word_at_readout(word):
    return set().union(*(place(SHIP, word.x0 + PITCH_X*c, READ_Y + PITCH_Y*r)
                          for c, r in lit_pixels(word.text)))


def verify_pulse_lanes(words):
    """A finite geometric separation certificate for any time in free flight.

    All ships have the same four-phase clock and move together at c/2.
    Different columns are 10 cells apart and their entire receiver
    reactions stay within an 8-cell horizontal envelope [-3,4].
    Ships sharing one column have >=8-cell north/south origin spacing.
    The single-spaceship native receiver is restored at local generation 40;
    its interaction occupies only 37..39, while the next pulse is at most
    at local generation 23, so a receiver is never claimed twice.
    """
    phases = ship_phases()
    eater_reaction()
    buses = {}
    points = tuple(pixel_origins(words))
    for x, y in points:
        buses.setdefault(x, []).append(y)
    spacing = None
    for col, ys in buses.items():
        ys.sort(reverse=True)   # southernmost ship arrives first
        for ahead, behind in zip(ys, ys[1:]):
            sep = ahead - behind
            if sep < PITCH_Y or sep % 2:
                raise AssertionError(('same-column source collision', col, sep))
            spacing = sep if spacing is None else min(spacing, sep)
    xvalues = sorted(buses)
    if any((b-a) < PITCH_X for a, b in zip(xvalues, xvalues[1:])):
        raise AssertionError('receiver columns too close for native reaction envelope')
    if any(y > READ_Y + PITCH_Y*3 for _, y in points):
        raise AssertionError('a source did not originate above its reading position')
    if max(w.onset_g for w in words) + 2*EATER_Y + 40 > SONG_END_G:
        raise AssertionError('late words cannot clear before audio ends')
    return {'rule':'B3/S23','words':len(words),'pixel_ships':len(points),
       'distinct_receiver_columns':len(buses),'lanes':1+max(w.lane for w in words),
       'horizontal_glyph_pitch_cells':PITCH_X,
       'vertical_glyph_pitch_cells':PITCH_Y,
       'minimum_same_column_source_separation_cells':spacing,
       'period_four_native_south_velocity_cells':2,
       'native_receiver_first_interaction_at_local_g':37,
       'native_receiver_restored_at_local_g':40,
       'all_g0_ships_are_preloaded':True,
       'backtrace_uses_a_reversible_spaceship_orbit_not_inverse_B3S23':True,
       'conveyor_arrives_physically_from_above':True,
       'full_song_exact_lyrics_backtraced':len(words)==403,
       'physically_inside_original_rounded_bubble':False,
       'independent_vocal_gate_wired':False,
       'native_singing_character_integrated':False,
       'whole_world_zero_at_end':False}


def snapshot(g, words, *, omit=None):
    """EXACT full B3/S23 state from an inductively isolated pulse decomposition.

    This is NOT a graphics overlay. We use the four native spaceship phases
    and the complete 41-state actual fishhook collision kernel. Each bus is
    proven separated in x, while successive ships on a bus are >=8 cells
    apart in y. Check against brute-force global evolution in the tests.
    """
    if g < 0:
        raise ValueError('negative generation')
    words = tuple(words)
    fixed = receiver_sites(words)
    state = receiver_cells(words)
    phases = ship_phases()
    reactions = eater_reaction()
    active = words if omit is None else tuple(w for w in words if w.index != omit)
    for x, y0 in pixel_origins(active):
        contact_origin_g = 2*(EATER_Y-y0)
        relative = g-contact_origin_g
        if relative >= 40:
            continue
        if relative >= 37:
            station = (x, EATER_Y)
            if station not in fixed:
                raise AssertionError('missing reaction receiver')
            state.difference_update(place(EATER, *station))
            state.update(place(reactions[relative], *station))
        else:
            state.update(place(phases[g%4], x, y0 + 2*(g//4)))
    return state


def certificate(words=None):
    words = tuple(word_plan() if words is None else words)
    report = verify_pulse_lanes(words)
    bank = receiver_cells(words)
    sources = seed_cells(words)
    if snapshot(0, words) != sources:
        raise AssertionError('inverse-staging g0 mismatch')
    if snapshot(SONG_END_G, words) != bank:
        raise AssertionError('last real LWSS was not consumed')
    for w in [words[0], words[len(words)//2], words[-1]]:
        if not word_at_readout(w) <= snapshot(w.onset_g, words):
            raise AssertionError(('missing actual on-time native glyph', w.index))
    report.update({
        'song_end_generation':SONG_END_G,
        'source_population_at_g0':len(sources),
        'stable_receiver_cells_at_end':len(bank),
        'song_end_snapshot_exactly_receiver_bank':True,
        'first_word_onset_g':words[0].onset_g,
        'last_word_onset_g':words[-1].onset_g,
        'aligned_word_onset_error_new_generations':0,
        'glyph_raster_overlay_count':0,'frame_cell_injection_count':0,
        'full_native_singing_music_video_finished':False})
    return report


def export(folder):
    folder = Path(folder); folder.mkdir(parents=True, exist_ok=True)
    words = word_plan()
    report = certificate(words)
    full = seed_cells(words)
    (folder/'gondry_full_song_from_above_g0.rle').write_text(
       compact_rle(full, (
           '403 exact Suno timed 3x4 words: southbound LWSS true B3/S23.',
           'Each ship backtraced to g0 by native c/2 drift, never frame-inserted.',
           'One source universe, independent word lanes and stable fishhooks.',
           'LYRIC-ONLY: singer, rounded bubble rim and vocal lip wiring pending.'
       )), encoding='utf8')
    (folder/'gondry_word_schedule.json').write_text(
       json.dumps([asdict(w) | {'x0':w.x0,
                    'arrival_seconds':w.arrival_seconds} for w in words],
                  indent=2)+'\n',encoding='utf8')
    (folder/'gondry_native_qualification.json').write_text(
       json.dumps(report,indent=2)+'\n',encoding='utf8')
    first = words[:2]
    (folder/'first_two_native_seed.rle').write_text(
        compact_rle(seed_cells(first),(
            'Authentic first two Suno words WE and MADE approach from above.',
            'No cuts; check native B3/S23 onset g2156 and g2204.'
        )),encoding='utf8')
    with (folder/'first_two_native_seed.tsv').open('w',encoding='utf8') as f:
        for x,y in sorted(seed_cells(first)):f.write(f'{x} {y}\n')
    return report


if __name__ == '__main__':
    import argparse
    p=argparse.ArgumentParser()
    p.add_argument('--out',required=True)
    a=p.parse_args()
    print(json.dumps(export(a.out),indent=2))
