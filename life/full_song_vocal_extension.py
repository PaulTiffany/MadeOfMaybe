"""Preserve the ORIGINAL singer and its three-state 20-second mouth circuits.

Rearm TWO existing real physical lip tiles for the 43 later observed V-stem
episodes (26.00–233.60 s), from only generation-zero glider sources.
This is a direct extension of the qualified original word/vocal singer:
the existing facial art, three-state opening V lanes, W->lip glider,
and real 90-degree-converted WE and MADE glyphs are preserved intact.

Both later lip tiles use the previously qualified two-glider block synthesis
and clean one-glider deletion (D4 phase matched). The separate 43-episode
glider trains do not interfere with each other or the original singer;
a native C++ all-generation separation proof is bundled in
research/verify_full_song_vocal_extension.cpp (44,862 generations).

Scope deliberately limited: 43 later vocal episodes at TWO lip tiles.
The original first 26 seconds remain the previously qualified finite
V timing, not a new 53-event reinterpretation. Six other lip outputs
and 403 lyric-word source controls remain to be connected and certified.
"""
from __future__ import annotations

from dataclasses import asdict,dataclass
from functools import lru_cache
from pathlib import Path
import json

from .core import place
from .full_song_karaoke import GPS
from .glider_controlled_mouth import (
    MEDIUM_TARGETS,OPEN_TARGETS,ROUTING,rotate,
    block_make_at,block_erase_at)
from .refined_singer_candidate import LIP_DROP_Y
from .relocated_singer_anchor import SINGER_TRANSLATION
from .two_line_native_singer import components as original_singer_components

ROOT=Path(__file__).resolve().parents[1]
SCORE_FILE=ROOT/'data'/'made_of_maybe_vocal_gate_take1_v0.json'
SONG_ID='53610991-7381-4749-96e1-79b8e3b1c28b'
VOCAL_STEM_ID='bee52d16-b01b-4224-bd4c-5c51081d813b'
POST_OPENING_FROM_S=26.0
LAST_NATIVE_G=44862
TARGETS={
 'medium_0':(MEDIUM_TARGETS[0][0]+SINGER_TRANSLATION[0],
             MEDIUM_TARGETS[0][1]+LIP_DROP_Y+SINGER_TRANSLATION[1]),
 'open_1':(OPEN_TARGETS[1][0]+SINGER_TRANSLATION[0],
           OPEN_TARGETS[1][1]+LIP_DROP_Y+SINGER_TRANSLATION[1])
}
TARGET_MODES={'medium_0':('medium',0),'open_1':('open',1)}

@dataclass(frozen=True)
class VocalEpisode:
    source_index:int
    original_onset_seconds:float
    original_release_seconds:float
    physical_make_g:int
    physical_erase_g:int

def quantize_make(t):
    return max(4,4+4*round((float(t)*GPS-4)/4))

def quantize_erase(t):
    return max(22,22+4*round((float(t)*GPS-22)/4))

@lru_cache(maxsize=1)
def later_vocal_episodes():
    record=json.loads(SCORE_FILE.read_text(encoding='utf8'))
    if (record['song_id']!=SONG_ID or record['vocal_stem_id']!=VOCAL_STEM_ID
        or len(record['intervals_seconds'])!=53):
        raise AssertionError('wrong original Suno vocal source score')
    out=[]
    for i,(a,b) in enumerate(record['intervals_seconds']):
        if a<POST_OPENING_FROM_S:
            continue
        make_g=quantize_make(a)
        erase_g=quantize_erase(b)
        if make_g>=erase_g or make_g%4 or erase_g%4!=2:
            raise AssertionError(('unreachable native mouth timing',i))
        out.append(VocalEpisode(i,a,b,make_g,erase_g))
    if len(out)!=43 or out[0].physical_make_g!=4992 or out[-1].physical_erase_g!=44850:
        raise AssertionError('original 43 later voice events changed')
    return tuple(out)

@lru_cache(maxsize=2)
def native_lip_gliders(name):
    if name not in TARGETS:
        raise KeyError(name)
    bank,index=TARGET_MODES[name]
    _,make_dir,erase_dir=ROUTING[bank,index]
    target=TARGETS[name]
    out=set()
    for episode in later_vocal_episodes():
        making=place(rotate(block_make_at(episode.physical_make_g),make_dir),
                     *target)
        erasing=place(rotate(block_erase_at(episode.physical_erase_g),erase_dir),
                      *target)
        if len(making)!=10 or len(erasing)!=5 or out&(making|erasing):
            raise AssertionError(('source gliders overlap at g0',name,episode.source_index))
        out|=making|erasing
    if len(out)!=645:
        raise AssertionError(('missing native pulse',name,len(out)))
    return frozenset(out)

def components():
    original=original_singer_components(900,144)
    if tuple(map(len,original))!=(6408,742,240,52,1372):
        raise AssertionError('original 20-second actor/WE/MADE source changed')
    parts=tuple(original)+(native_lip_gliders('medium_0'),
                           native_lip_gliders('open_1'))
    if tuple(map(len,parts))!=(6408,742,240,52,1372,645,645):
        raise AssertionError('incorrect preserved original components')
    if len(set().union(*parts))!=10104:
        raise AssertionError('new original-Suno vocal glider overlaps existing actor')
    return parts

def universe():
    return set().union(*components())

def export(destination):
    destination=Path(destination)
    destination.mkdir(parents=True,exist_ok=True)
    parts=components()
    with (destination/'original_singer_plus_43_two_lip_g0.tsv').open('w') as f:
        for x,y in sorted(universe()):
            f.write(f'{x} {y}\n')
    with (destination/'original_singer_plus_43_two_lip_components.tsv').open('w') as f:
        f.write(f'{len(parts)}\n')
        for i,p in enumerate(parts):
            for x,y in sorted(p):f.write(f'{i} {x} {y}\n')
    with (destination/'original_stem_later_43_episodes.tsv').open('w') as f:
        for ep in later_vocal_episodes():
            f.write(f'{ep.source_index} {ep.physical_make_g} {ep.physical_erase_g}\n')
    report={
      'rule':'B3/S23','original_song_id':SONG_ID,'original_vocal_stem_id':VOCAL_STEM_ID,
      'original_singer_g0_cells_preserved':8814,
      'original_first20_full_three_state_v_gliders_preserved':240,
      'original_WE_and_MADE_real_90_degree_conversion_preserved':True,
      'original_W_to_mouth_glider_preserved':True,
      'new_late_vocal_episodes':43,
      'new_full_length_lip_tiles':['medium_0','open_1'],
      'new_V_source_gliders':258,
      'new_V_g0_cells':1290,
      'one_world_initial_population':10104,
      'additional_mouth_lip_cell_targets':{k:list(v) for k,v in TARGETS.items()},
      'proof_generations_through':LAST_NATIVE_G,
      'proof':'research/verify_full_song_vocal_extension.cpp',
      'native_proof_does_not_rely_on_video_overlays':True,
      'all_53_vocal_episodes_identically_wired':False,
      'remaining_six_full_song_mouth_lip_targets_connected':False,
      '403_word_to_full_song_mouth_connected':False,
      'all_403_words_actual_upstream_converters_in_one_readhead':False,
      'finished_four_minute_video':False,
      'physical_bubble_in_this_seed':False}
    (destination/'physical_43_V_two_lip_qualification_scope.json').write_text(
         json.dumps(report,indent=2)+'\n')
    return report

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser()
    p.add_argument('--out',type=Path,required=True)
    args=p.parse_args()
    print(json.dumps(export(args.out),indent=2))
