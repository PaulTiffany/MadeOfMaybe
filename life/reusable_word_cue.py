"""Two LINE-start events through ONE physical B3/S23 splitter and lyric pixel.

A fixed 84-cell glider duplicator is reused by two incoming, preloaded
SE/NW-phase compatible gliders. The same letter pixel is constructed, erased,
constructed again, and erased again at the Suno-aligned first-word times for
lines 1 and 2. No independent clock or runtime cell insertion is used.

This proves a *time-multiplexed lyric-source anchor* with stable reusable
catalysts. Source 1 erases an original lip tile, and source 2 erases a small,
initially-present nearby lip tile farther down the same glider corridor,
after source 1 was consumed at the first lip. The remaining glyph pixels
still use the sparse score; this is two tiles, not the complete mouth.
"""
from __future__ import annotations
from functools import lru_cache
from pathlib import Path

from .core import evolve, place
from .full_song_karaoke import compile_plan,pixel_seed
from .lyric_cues import read_alignment
from .first_line_singing_character import _glider_velocity
from .physical_lip_splitter_bridge import (SINGER_TRANSLATION,
    splitter_catalysts, split_input, replaced_word_glider,
    coupled_pixel_remainder, WORD_PIXEL)
from .glider_controlled_mouth import BLOCK

FIXTURE = Path(__file__).resolve().parents[1]/'data'/'first_verse_alignment_fixture.json'


def line_times(path=FIXTURE):
    lines=compile_plan(read_alignment(path))
    if len(lines)<2:
        raise ValueError('two source lines required')
    a,b=lines[:2]
    if a.words[0].make_g>=a.clear_g or a.clear_g>=b.words[0].make_g or b.words[0].make_g>=b.clear_g:
        raise ValueError('sequential lyric lifetimes must not overlap')
    if (b.words[0].make_g-a.words[0].make_g)%4:
        raise ValueError('two cue phases incompatible with splitter reuse')
    return ((a.words[0].make_g,a.clear_g),(b.words[0].make_g,b.clear_g))


def next_input():
    first=split_input();velocity=_glider_velocity(first)
    g1,g2=line_times()[0][0],line_times()[1][0]
    dt=(g2-g1)//4
    return place(first,-velocity[0]*dt,-velocity[1]*dt)


def second_replaced_word_glider():
    source=set(replaced_word_glider())
    velocity=_glider_velocity(source)
    g1,g2=line_times()[0][0],line_times()[1][0]
    dt=(g2-g1)//4
    return place(source,-velocity[0]*dt,-velocity[1]*dt)


def second_word_remainder():
    gmake,gerase=line_times()[1]
    all_gliders=set(pixel_seed(gmake,gerase))
    glider=second_replaced_word_glider()
    if not glider<=all_gliders:
        raise AssertionError('phase-shifted splitter output does not match next word source')
    return all_gliders-glider


def seed(source_one=True,source_two=True):
    catalysts=place(splitter_catalysts(),*SINGER_TRANSLATION)
    signals=set(catalysts)
    if source_one: signals|=place(split_input(),*SINGER_TRANSLATION)
    if source_two: signals|=place(next_input(),*SINGER_TRANSLATION)
    signals|=coupled_pixel_remainder()
    signals|=second_word_remainder()
    if len(signals)!=len(catalysts)+5*int(source_one)+5*int(source_two)+10+len(second_word_remainder()):
        raise AssertionError('source packets overlap at native g0')
    return signals


def checkpoints(source_one=True,source_two=True):
    times=line_times();samp={0,times[0][0],times[0][1],times[1][0],times[1][1]}
    live=seed(source_one,source_two);out={}
    for g in range(max(samp)+1):
        if g in samp:
            out[g]={'block':place(BLOCK,*WORD_PIXEL)<=live,'population':len(live),
                    'catalysts':place(splitter_catalysts(),*SINGER_TRANSLATION)<=live}
        if g<max(samp):live=evolve(live)
    return out


def qualification():
    g1,e1=line_times()[0];g2,e2=line_times()[1]
    both=checkpoints();missing_1=checkpoints(False,True);missing_2=checkpoints(True,False)
    if not (both[g1]['block'] and not both[e1]['block'] and
            both[g2]['block'] and not both[e2]['block']):
        raise AssertionError('the two complete lyric lives did not switch correctly')
    if not (not missing_1[g1]['block'] and missing_1[g2]['block'] and
            missing_2[g1]['block'] and not missing_2[g2]['block']):
        raise AssertionError('input ablation did not isolate the two word events')
    if not all(state['catalysts'] for r in (both,missing_1,missing_2) for state in r.values()):
        raise AssertionError('splitter catalyst corrupted')
    return {'rule':'B3/S23','constant_gps':192,'input_gliders':2,
            'shared_physical_splitter_catalysts':len(splitter_catalysts()),
            'word_pixel_origin':WORD_PIXEL,'generation_window':[0,e2],
            'first_line_make_erase':[g1,e1],'second_line_make_erase':[g2,e2],
            'first_source_ablation_prevents_first_make':True,
            'second_source_ablation_prevents_second_make':True,
            'same_physical_word_pixel_reused':True,
            'no_runtime_cell_edits':True,'source_is_original_suno_word_onset':True,
            'actual_full_lip_coupling_for_second_event':False,
            'full_song_layout_compacted':False}


def final_world(source_one=True,source_two=True):
    """Advance the exact anchor hardware to second line clear, for debris audit."""
    last=line_times()[1][1]
    live=seed(source_one,source_two)
    for _ in range(last):live=evolve(live)
    return live


def splitter_reuse_certificate():
    """After two real signals, exactly the 84-cell device and clean outputs."""
    from .first_line_singing_character import _connected,_glider_velocity
    device=place(splitter_catalysts(),*SINGER_TRANSLATION)
    after=final_world()
    if not device<=after:raise AssertionError('shared splitter failed to reset')
    extras=after-device
    groups=list(_connected(extras))
    if len(groups)!=2 or any(len(g)!=5 for g in groups):
        raise AssertionError(f'uncleared debris after two pulses: {sorted(map(len,groups))}')
    velocities=sorted(_glider_velocity(g) for g in groups)
    if velocities!=[(1,-1),(1,-1)]:
        raise AssertionError(f'unexpected output directions {velocities}')
    return {'physical_catalysts':len(device),'surviving_clean_gliders':len(groups),
            'final_life_cell_population':len(after),'at_generation':line_times()[1][1]}


def character_world_seed():
    """Existing actual multi-element singer plus TWO local word-cue events.

    Does not alter any facial art, preexisting real-mouth glider, or any other
    pixel of the seven-word first line. It is a restricted *anchor + singer*
    qualification, not the finished two-line lyric-stage universe.
    """
    from .physical_lip_splitter_bridge import bridge_unit_seed
    world=bridge_unit_seed(with_art=False)
    world|=place(next_input(),*SINGER_TRANSLATION)
    world|=second_word_remainder()
    return world


# Position of the real, already connected mouth tile. We do not overwrite
# the singer's existing lip bank with a presentation artifact.
from .physical_lip_splitter_bridge import LIP_TARGET,SINGER_TRANSLATION as _ST
LIP_TARGET_GLOBAL=(LIP_TARGET[0]+_ST[0],LIP_TARGET[1]+_ST[1])

# An independent initially-present 2x2 tile eight cells farther along the
# existing NORTH-EAST lip-erase glider track. Source 1 is CONSUMED at the
# first lip before reaching this block; source 2 travels through the now-empty
# original site and erases this nearby actual lip tile at g3152.
# This positioning was screened against the original face and moving signals.
SECOND_LIP_OFFSET=8
SECOND_LIP_LOCAL=(LIP_TARGET_GLOBAL[0]-_ST[0]+SECOND_LIP_OFFSET,
                  LIP_TARGET_GLOBAL[1]-_ST[1]-SECOND_LIP_OFFSET)
SECOND_LIP_GLOBAL=(LIP_TARGET_GLOBAL[0]+SECOND_LIP_OFFSET,
                   LIP_TARGET_GLOBAL[1]-SECOND_LIP_OFFSET)
SECOND_LIP_ERASE_G=3152


def character_world_with_second_lip(*,second_source_enabled=True):
    """ONE Life initial state, two shared-cause word pixels and TWO lip actions.

    The first lip is an existing dynamic character contour element. The second
    2x2 lip element is added at generation zero and erased only by the delayed
    sibling output from the same reusable splitter. No runtime insertion.
    """
    dynamic=character_world_seed()
    if not second_source_enabled:
        dynamic-=place(next_input(),*SINGER_TRANSLATION)
    tile=place(BLOCK,*SECOND_LIP_GLOBAL)
    if tile & dynamic:
        raise AssertionError('second initial lip tile overlaps a signal')
    return dynamic|tile


@lru_cache(maxsize=1)
def two_lip_causal_certificate():
    """Direct ON/OFF ablation of second lyric input and the added lip tile."""
    g1,e1=line_times()[0];g2,e2=line_times()[1]
    a=character_world_with_second_lip(second_source_enabled=True)
    b=character_world_with_second_lip(second_source_enabled=False)
    second_tile=place(BLOCK,*SECOND_LIP_GLOBAL)
    original_tile=place(BLOCK,*LIP_TARGET_GLOBAL)
    lyric_tile=place(BLOCK,*WORD_PIXEL)
    sampled={}
    for g in range(SECOND_LIP_ERASE_G+5):
        if g in (0,g1,2188,2312,2456,2554,e1,g2,3132,
                 SECOND_LIP_ERASE_G-4,SECOND_LIP_ERASE_G,
                 SECOND_LIP_ERASE_G+4):
            sampled[g]={'word_on':lyric_tile<=a,'word_no_second':lyric_tile<=b,
                        'original_lip_on':original_tile<=a,
                        'added_lip_on':second_tile<=a,
                        'added_lip_no_second':second_tile<=b}
        if g<SECOND_LIP_ERASE_G+4:
            a=evolve(a);b=evolve(b)
    if not (sampled[g2]['word_on'] and not sampled[g2]['word_no_second']):
        raise AssertionError('second cue does not causally construct the lyric tile')
    if not (sampled[SECOND_LIP_ERASE_G-4]['added_lip_on'] and
            not sampled[SECOND_LIP_ERASE_G]['added_lip_on'] and
            sampled[SECOND_LIP_ERASE_G]['added_lip_no_second']):
        raise AssertionError('second cue does not causally erase added REAL lip tile')
    if not (sampled[2188]['original_lip_on'] and
            not sampled[2312]['original_lip_on'] and
            sampled[2456]['original_lip_on'] and
            not sampled[2554]['original_lip_on']):
        raise AssertionError('first original real lip tile was disturbed')
    return {'rule':'B3/S23','native_generation_end':SECOND_LIP_ERASE_G+4,
            'shared_stable_duplicators':1,'sequential_word_cues':2,
            'physically_coupled_actual_lip_tiles':2,
            'first_tile_is_existing_singer_contour':True,
            'second_tile_added_at_generation_zero':True,
            'second_tile_local_origin':SECOND_LIP_LOCAL,
            'second_tile_erased_at_generation':SECOND_LIP_ERASE_G,
            'source_two_ablation_prevents_second_glyph_and_second_lip_erase':True,
            'complete_three_state_mouth_coupled':False,
            'all_403_word_gliders_coupled':False,
            'checkpoints':sampled}


@lru_cache(maxsize=1)
def protected_character_certificate():
    """Finite actual-Life check: 2-cell guard against the unchanged portrait.

    Verify BOTH reused word onsets in one singer world and scan every
    generation through second-line erasure for possible art damage. This
    is stricter than looking at the optical video or symbolic cue schedule.
    """
    from .first_line_singing_character import art_seed
    art=place(art_seed(),*SINGER_TRANSLATION)
    if evolve(art)!=art:raise AssertionError('portrait not a stable initial structure')
    guard={(x+dx,y+dy) for x,y in art
            for dx in range(-2,3) for dy in range(-2,3)}
    g1,e1=line_times()[0];g2,e2=line_times()[1]
    word_target=place(BLOCK,*WORD_PIXEL)
    first_lip=(LIP_TARGET_GLOBAL)
    lip_target=place(BLOCK,*first_lip)
    live=character_world_with_second_lip();samp={};
    for g in range(e2+1):
        if live & guard:
            raise AssertionError(f'portrait boundary damaged by lyric bus at generation {g}')
        if g in (g1,2188,2312,2456,2554,e1,g2,e2):
            samp[g]={'lyric_anchor_on':word_target<=live,
                     'original_moving_lip_present':lip_target<=live,
                     'dynamic_population':len(live)}
        if g<e2:live=evolve(live)
    if not (samp[g1]['lyric_anchor_on'] and not samp[e1]['lyric_anchor_on'] and
            samp[g2]['lyric_anchor_on'] and not samp[e2]['lyric_anchor_on']):
        raise AssertionError('the two words did not cycle in the actual singer world')
    if not (samp[2188]['original_moving_lip_present'] and
            not samp[2312]['original_moving_lip_present'] and
            samp[2456]['original_moving_lip_present'] and
            not samp[2554]['original_moving_lip_present']):
        raise AssertionError('the preexisting real mouth was disrupted')
    return {'singer_art_still_life_cells':len(art),
            'unchanged_portrait_spacetime_guarantee':True,
            'native_generations_checked':e2+1,
            'shared_splitter_reused':True,
            'original_one_lip_coupling_preserved':True,
            'second_lip_causally_connected':True,
            'first_two_lyric_anchor_events_physically_coupled':True,
            'second_lip_tile_local_origin':SECOND_LIP_LOCAL,
            'real_life_checkpoints':samp}


