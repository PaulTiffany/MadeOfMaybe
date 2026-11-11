"""Full Suno W and V event tape as preloaded, true B3/S23 gliders.

503? No: EXACTLY 403 word-onset events and 106 isolated-vocal
on/off events. Each is one real 5-cell glider at g0, traveling on
phase-aligned noninterfering c/4 rails. All tracks are physically
unwired to the singing face in this stage; do NOT mistake this
for the full native karaoke/video. No runtime insertion or edits.
"""
from __future__ import annotations
from dataclasses import dataclass,asdict
from pathlib import Path
import json
from .core import evolve,place
from .singer_pilot import INPUT_GLIDER
from .full_song_karaoke import compile_plan,ALIGNMENT_FILE
from .lyric_cues import read_alignment
from .dual_channel_mouth_logic import time_to_g
from .native_half_font_first20 import universe as first_world
from .export_operational import compact_rle

ROOT=Path(__file__).resolve().parents[1]
SOURCE_FILE=ROOT/'data/made_of_maybe_vocal_gate_take1_v0.json'
SONG_END_G=45864
SPACING=24
MIN_GAP=64
W_START=(600000,-600000)
V_START=(610000,-600000)

@dataclass(frozen=True)
class Packet:
    source:str
    index:int
    generation:int
    lane:int
    target_x:int
    target_y:int
    label:str

def source_events():
    words=[word for line in compile_plan(read_alignment(ALIGNMENT_FILE))
                  for word in line.words]
    v=json.loads(SOURCE_FILE.read_text(encoding='utf8'))
    assert len(words)==403 and len(v['intervals_seconds'])==53
    assert v['vocal_stem_id']=='bee52d16-b01b-4224-bd4c-5c51081d813b'
    ev=[('W',i,w.make_g,w.text) for i,w in enumerate(words)]
    for i,(a,b) in enumerate(v['intervals_seconds']):
        ev.extend((('V+',i,time_to_g(a),'on'),
                   ('V-',i,time_to_g(b),'off')))
    assert len(ev)==509 and all(g>0 and g%4==0 for _,_,g,_ in ev)
    return ev

def packets():
    ev=source_events();out=[]
    for name,base in (('W',W_START),('V',V_START)):
        subset=sorted((q for q in ev if (q[0]=='W')==(name=='W')),
                       key=lambda e:(e[2],e[1],e[0]))
        last=[]
        for src,i,g,label in subset:
            lane=next((j for j,old in enumerate(last) if g-old>=MIN_GAP),None)
            if lane is None:lane=len(last);last.append(-1000000)
            last[lane]=g
            out.append(Packet(src,i,g,lane,base[0]+SPACING*lane,
                                         base[1]-SPACING*lane,label))
    return tuple(out)

def packet_cells(packet):
    if packet.generation%4:raise ValueError('phase mismatch')
    k=packet.generation//4
    return place(INPUT_GLIDER,packet.target_x-k,packet.target_y-k)

def tape_cells():
    return set().union(*(packet_cells(p) for p in packets()))

def certify():
    pk=packets()
    tracks={}
    for p in pk:tracks.setdefault((p.source[0],p.lane),[]).append(p)
    for line in tracks.values():
        line.sort(key=lambda e:e.generation)
        if any(b.generation-a.generation<MIN_GAP for a,b in zip(line,line[1:])):
            raise AssertionError('two gliders too close on one lane')
    intercepts={p.target_x-p.target_y for p in pk}
    if len(intercepts)!=len(tracks):
        raise AssertionError('cross-source glider rail overlap')
    shape=set(INPUT_GLIDER)
    for _ in range(4):shape=evolve(shape)
    if shape!=place(INPUT_GLIDER,1,1):
        raise AssertionError('glider velocity incorrectly assumed')
    scene=first_world()
    low=min(abs(x-y) for x,y in tape_cells())
    high=max(abs(x-y) for x,y in scene)
    if low-high<4*SONG_END_G+30:
        raise AssertionError('glider tape could reach portrait under finite-speed bound')
    return {
       'rule':'B3/S23','end_generation':SONG_END_G,
       'duration_seconds':238.875,
       'word_lyric_source':'53610991-7381-4749-96e1-79b8e3b1c28b',
       'isolated_vocal_stem':'bee52d16-b01b-4224-bd4c-5c51081d813b',
       'word_onset_gliders':403,'vocal_on_and_off_gliders':106,
       'initial_source_live_cells':len(tape_cells()),
       'word_lanes':max(p.lane for p in pk if p.source=='W')+1,
       'vocal_lanes':max(p.lane for p in pk if p.source!='W')+1,
       'minimum_same_lane_generation_gap':MIN_GAP,
       'source_rails_disjoint_from_singer_at_all_song_ticks_by_finite_speed':True,
       'all_sources_connected_to_physical_singer_controller':False,
       'all_403_words_visible_in_native_video':False,
       'four_minute_film_complete':False}

def export(folder):
    folder=Path(folder);folder.mkdir(parents=True,exist_ok=True)
    groups=tape_cells();combined=first_world()|groups
    assert len(combined)==8090+len(groups)
    (folder/'full_song_unwired_source_tape.rle').write_text(compact_rle(combined,(
       'Genuine B3/S23 glider tape with Suno 403 W + 106 V events.',
       'Gliders preloaded at g0; timing 192 generations per audio second.',
       'TAPE UNWIRED: NOT the finished four-minute singer/karaoke.'
    )),encoding='utf8')
    (folder/'tape_manifest.json').write_text(
         json.dumps([asdict(p) for p in packets()],indent=2)+'\n')
    result=certify()
    (folder/'tape_qualification.json').write_text(json.dumps(result,indent=2)+'\n')
    return result

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser()
    p.add_argument('--out',required=True)
    args=p.parse_args()
    print(json.dumps(export(args.out),indent=2))
