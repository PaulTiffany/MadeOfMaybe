"""Bounded native B3/S23 proof of a reusable G-to-LWSS + eater bank.

The known Luke Kiernan 2023 converter emits an actual westbound LWSS.
A previously qualified fishhook catches the output, restoring 112 stable
cells per lane. The isolated sink is NOT yet a routed lyric display.

Separately, compile all real Suno 3x4 glyph pixel deadlines into
188-generation-separated converter slots. That is a scheduling result,
NOT evidence that a large native station bank forms visible typography.
"""
from __future__ import annotations
from dataclasses import asdict, dataclass
from functools import lru_cache
from heapq import heappop, heappush
from .core import evolve, place
from .reusable_glider_to_lwss_2023 import hardware, INPUT, west, train
from .staggered_word_mesh import EATER_TEXT

MIN_GAP_G = 188  # qualified 2023-converter input spacing, not a minimum bound
LANE_PITCH = 200  # real Life-cell separation for bounded native array test
REF_OUTPUT_G = 200
EATER = frozenset(place(EATER_TEXT, 32, 24))  # translated real fishhook
FIXED = frozenset(set(hardware()) | set(EATER))


@dataclass(frozen=True)
class PixelRequest:
    generation: int
    word_index: int
    pixel_index: int
    column: int
    row: int
    word: str
    lane: int


def fixed_lanes(count: int):
    if count < 1:
        raise ValueError('need at least one converter')
    return set().union(*(place(FIXED, 0, lane * LANE_PITCH)
                         for lane in range(count)))


def delayed_glider(generation: int, lane: int):
    """Preloaded southeast source producing native westbound LWSS at generation."""
    if generation < REF_OUTPUT_G or generation % 4 or lane < 0:
        raise ValueError('invalid native launch phase')
    delay = (generation - REF_OUTPUT_G) // 4
    return place(west(place(INPUT, 47-delay, 47-delay)),
                 0, lane * LANE_PITCH)


def sample_parts(lanes=3, shots=8, omit=None):
    """Three independently staged, repeated converter+fishhook assemblies.

    Samples BEGIN at g200 and are spaced 188g. An ablated input is
    omitted at g0; no cell changes are performed during Life evolution.
    """
    if not 1 <= lanes <= 8 or not 1 <= shots <= 8:
        raise ValueError('bounded native sample only')
    if omit is not None and not (0 <= omit[0] < lanes and
                                 0 <= omit[1] < shots):
        raise ValueError('bad source ablation')
    parts = []
    for lane in range(lanes):
        cells = place(FIXED, 0, lane * LANE_PITCH)
        for shot in range(shots):
            if omit != (lane, shot):
                cells |= delayed_glider(REF_OUTPUT_G + MIN_GAP_G * shot, lane)
        if len(cells) != len(FIXED) + 5 * (shots-(omit is not None and omit[0] == lane)):
            raise AssertionError('within-lane source overlap')
        parts.append(cells)
    if len(set().union(*parts)) != sum(map(len, parts)):
        raise AssertionError('cross-lane g0 source overlap')
    return tuple(parts)


def reference_westbound():
    """Exact 12-cell c/2 westbound phase from the published converter."""
    world = train(1)
    for _ in range(REF_OUTPUT_G):
        world = evolve(world)
    output = world - set(hardware())
    if len(output) != 12:
        raise AssertionError('missing real converted LWSS phase')
    flight = set(output)
    for _ in range(4):
        flight = evolve(flight)
    if flight != place(output, -2, 0):
        raise AssertionError('not a real westbound c/2 LWSS')
    return frozenset(output)


def qualify_sample(lanes=3, shots=8, omit=None, end_g=1700):
    """Whole native world equals independently evolved lanes at every g."""
    if end_g < REF_OUTPUT_G + MIN_GAP_G * (shots - 1) + 100:
        raise ValueError('sample ends before output cleanup window')
    parts = [set(s) for s in sample_parts(lanes, shots, omit)]
    world = set().union(*parts)
    original = len(world)
    fixed = fixed_lanes(lanes)
    output = reference_westbound()
    visible_at_first = None
    for g in range(end_g + 1):
        if world != set().union(*parts):
            raise AssertionError(f'unintended cross-lane collision at g{g}')
        if g == REF_OUTPUT_G:
            visible_at_first = tuple(
                place(output, 0, lane * LANE_PITCH) <= world
                for lane in range(lanes))
        if g == end_g:
            break
        world = evolve(world)
        parts = [evolve(p) for p in parts]
    expected = tuple(omit != (lane, 0) for lane in range(lanes))
    if visible_at_first != expected:
        raise AssertionError('native output readout/source ablation failed')
    if world != fixed or evolve(world) != world:
        raise AssertionError('converter or fishhook did not exactly reset')
    return {'rule': 'B3/S23', 'native_lanes': lanes,
            'shots_per_lane': shots, 'initial_population': original,
            'end_generation': end_g, 'terminal_population': len(world),
            'fixed_cells_per_lane': len(FIXED),
            'first_outputs_present': visible_at_first,
            'source_ablation': omit, 'all_g_independent': True,
            'eater_and_converter_exactly_restored': True,
            'full_song_word_display_built': False,
            'full_song_mouth_controller_built': False}


@lru_cache(maxsize=1)
def full_song_schedule():
    """Greedy minimal-lane interval allocation for exact mini-word deadlines.

    This produces a W source plan for each *glyph pixel*. Output ships
    are still in remote per-lane sinks, NOT assembled at bubble coordinates.
    """
    from .native_half_font_first20 import lit_pixels
    from .full_song_karaoke import ALIGNMENT_FILE, compile_plan
    from .lyric_cues import read_alignment
    lines = compile_plan(read_alignment(ALIGNMENT_FILE))
    requests = []
    for line in lines:
        for word in line.words:
            for pixel_index, (col, row) in enumerate(lit_pixels(word.text)):
                requests.append((word.make_g, word.word_index,
                                 pixel_index, col, row, word.text))
    requests.sort()
    heap = []  # (next_allowed_generation, lane)
    result = []
    count = 0
    for g, wi, pi, col, row, word in requests:
        if g < REF_OUTPUT_G or g % 4:
            raise AssertionError('unlaunchable Suno-aligned deadline')
        if heap and heap[0][0] <= g:
            _, lane = heappop(heap)
        else:
            lane = count
            count += 1
        result.append(PixelRequest(g, wi, pi, col, row, word, lane))
        heappush(heap, (g + MIN_GAP_G, lane))
    if len({r.word_index for r in result}) != 403:
        raise AssertionError('Suno sung word was lost')
    return tuple(result), count


def schedule_audit():
    """Initial-state collision check, NOT a four-minute dynamics proof."""
    plan, count = full_song_schedule()
    per_lane = {}
    for p in plan:
        per_lane.setdefault(p.lane, []).append(p.generation)
    if any(b-a < MIN_GAP_G
           for times in per_lane.values()
           for a, b in zip(times, times[1:])):
        raise AssertionError('converter was oversubscribed')
    seeds = fixed_lanes(count)
    for p in plan:
        seeds |= delayed_glider(p.generation, p.lane)
    expected = len(FIXED) * count + 5 * len(plan)
    if len(seeds) != expected:
        raise AssertionError('all-song preloaded source collision at g0')
    return {
        'rule': 'B3/S23', 'Suno_aligned_word_count': 403,
        'song_pixel_requests': len(plan), 'converter_slots': count,
        'spaced_input_generation_gap': MIN_GAP_G,
        'pixel_requests_with_launch_phase': len(plan),
        'initial_sources_and_stations_population': len(seeds),
        'g0_source_cells_are_all_nonoverlapping': True,
        'native_array_qualified_only_for': 'three lanes x eight shots (and ablation)',
        'converter_outputs_are_currently_eaten': True,
        'outputs_arranged_as_3x4_words': False,
        'voice_signal_causally_connected': False,
        'mouth_actuator_connected': False,
        'full_native_song_film_qualified': False,
    }


if __name__ == '__main__':
    import json
    print(json.dumps(schedule_audit(), indent=2))
