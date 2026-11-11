"""Original Suno V stem -> REAL repeated B3/S23 lip-tile actuation through song.

This is a precise continuation of the established native_half_font_first20
singer, not a new face, a rendered mouth sprite, or a new karaoke mechanism.

The known two-glider block synthesis and one-glider erase recipes are used
at one of the *existing* singer's medium-mouth tiles for all 53 observed
vocal intervals. All 159 input gliders exist at generation zero.

Qualification scope: original singer and native WE+MADE first two words
remain; the 240-cell old finite four-event vocal source is EXCLUDED from
this variant so it cannot collide with the 53-event signal, which replaces
one target only. Original W->lip marker remains intact. The other seven
three-state lip actuators are NOT yet rebuilt and connected for full song.

The tiny C++ verifier in research/verify_full_song_vocal_extension.cpp
checks all 44862 B3/S23 generations through a rigorous component-separation
certificate, i.e. it does NOT rely on frame overlays or source injection.
"""
from __future__ import annotations

import json
from dataclasses import asdict,dataclass
from pathlib import Path
from functools import lru_cache

from .core import place
from .full_song_karaoke import GPS
from .glider_controlled_mouth import (
    MEDIUM_TARGETS,ROUTING,BLOCK,rotate,block_make_at,block_erase_at)
from .refined_singer_candidate import LIP_DROP_Y
from .relocated_singer_anchor import SINGER_TRANSLATION
from .two_line_native_singer import components as two_word_components

ROOT=Path(__file__).resolve().parents[1]
VOCAL_FILE=ROOT/'data'/'made_of_maybe_vocal_gate_take1_v0.json'
TARGET=(MEDIUM_TARGETS[0][0]+SINGER_TRANSLATION[0],
        MEDIUM_TARGETS[0][1]+LIP_DROP_Y+SINGER_TRANSLATION[1])
MAKE_DIR=ROUTING['medium',0][1]
ERASE_DIR=ROUTING['medium',0][2]
EXPECTED_V_EPISODES=53
FIRST_SAMPLE_G=0
LAST_VERIFY_G=44862

@dataclass(frozen=True)
class VocalEpisode:
    index:int
    original_onset_seconds:float
    original_release_seconds:float
    physical_make_g:int
    physical_erase_g:int

def quantize_make(t):
    # Native synthesis phase: exactly 4 (mod 4).
    return max(4,4+4*round((float(t)*GPS-4)/4))

def quantize_erase(t):
    # Native clean erasure phase: exactly 22 (mod 4).
    return max(22,22+4*round((float(t)*GPS-22)/4))

@lru_cache(maxsize=1)
def episodes():
    record=json.loads(VOCAL_FILE.read_text(encoding='utf8'))
    if (record['song_id']!='53610991-7381-4749-96e1-79b8e3b1c28b'
        or record['vocal_stem_id']!='bee52d16-b01b-4224-bd4c-5c51081d813b'):
        raise AssertionError('wrong source song / isolated vocal')
    intervals=record['intervals_seconds']
    if len(intervals)!=EXPECTED_V_EPISODES:
        raise AssertionError('unexpected Suno isolated-vocal activity score')
    result=[]
    for i,(a,b) in enumerate(intervals):
        onset=quantize_make(a);release=quantize_erase(b)
        if onset>=release or onset%4 or release%4!=2:
            raise AssertionError(('invalid physical mouth episode',i,onset,release))
        result.append(VocalEpisode(i,a,b,onset,release))
    return tuple(result)

@lru_cache(maxsize=1)
def native_pulse_cells():
    out=set()
    for p in episodes():
        make=place(rotate(block_make_at(p.physical_make_g),MAKE_DIR),*TARGET)
        erase=place(rotate(block_erase_at(p.physical_erase_g),ERASE_DIR),*TARGET)
        if len(make)!=10 or len(erase)!=5 or out & (make|erase):
            raise AssertionError(('pulse packets collide at generation zero',p.index))
        out|=make|erase
    if len(out)!=EXPECTED_V_EPISODES*15:
        raise AssertionError('missing source glider')
    return frozenset(out)

def parts():
    previous=two_word_components(900,144)
    if tuple(map(len,previous))!=(6408,742,240,52,1372):
        raise AssertionError('the existing real singer or WE/MADE changed')
    # The prior four-event V packets were time-limited independent sources.
    # The full V stem replaces them in THIS qualification variant only.
    preserved=(previous[0],previous[1],frozenset(),previous[3],
               previous[4],native_pulse_cells())
    all_cells=set().union(*preserved)
    if sum(map(len,preserved))!=len(all_cells) or len(all_cells)!=9369:
        raise AssertionError('new source or preserved original singer overlap')
    return tuple(preserved)

def universe():
    return set().union(*parts())

def export(destination):
    destination=Path(destination)
    destination.mkdir(parents=True,exist_ok=True)
    segments=parts()
    seed=set().union(*segments)
    with (destination/'native_singer_53_vocal_g0.tsv').open('w') as f:
        for x,y in sorted(seed):f.write(f'{x} {y}\n')
    with (destination/'native_singer_53_vocal_components.tsv').open('w') as f:
        f.write(f'{len(segments)}\n')
        for i,part in enumerate(segments):
            for x,y in sorted(part):f.write(f'{i} {x} {y}\n')
    with (destination/'native_53_vocal_events.tsv').open('w') as f:
        for p in episodes():
            f.write(f'{p.index} {p.physical_make_g} {p.physical_erase_g}\n')
    report={
      'rule':'B3/S23',
      'original_suno_vocal_stem_id':'bee52d16-b01b-4224-bd4c-5c51081d813b',
      'suno_vocal_episodes':len(episodes()),
      'source_gliders_at_g0':len(native_pulse_cells())//5,
      'source_vocal_cells_at_g0':len(native_pulse_cells()),
      'all_parts_g0_population':len(seed),
      'actual_singer_plus_90_degree_WE_and_MADE_preserved':True,
      'actual_W_to_lip_original_marker_preserved':True,
      'full_song_vocal_score_controls_one_existing_lip_tile':True,
      'actual_lip_tile_global_coordinate':list(TARGET),
      'legacy_four_event_V_input_bank_removed_in_this_variant':True,
      'other_seven_lip_tiles_are_not_full_song_rewired':True,
      'word_source_403_events_to_mouth_not_full_song_wired':True,
      'whole_song_403_word_converter_readhead_not_finished':True,
      'native_53_episode_full_duration_C_plus_plus_proof_required':True,
      'this_is_not_finished_music_video':True,
    }
    (destination/'native_53_vocal_extension_scope.json').write_text(
         json.dumps(report,indent=2)+'\n')
    return report

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser()
    p.add_argument('--out',type=Path,required=True)
    a=p.parse_args()
    print(json.dumps(export(a.out),indent=2))
