"""Compile the original 403-word Suno score into one physical B3/S23 g0.

Reuses the existing original singer (WE/MADE W+V mouth mechanisms), two
existing later-V lip controls, the 3x4 LWSS font, original 19-cell
SOUTH->WEST corner and existing fishhook eaters.

One data-driven construction for all later words. The 401 stages are packed
into 47 spatially reusable source/reading lanes (not 401 distant
word stages). This is a PHYSICAL source, not a renderer or a certificate.

This source layout deliberately uses 36-cell glyph pitch for clearance:
it does NOT yet meet the compact 8-cell-pitch seven-lane presentation
target, and its 403-word full evolution is not yet qualified. A short
direct-native replay of the first 20 words matched all 18 new words.

No CI, runtime changes to Life cells, optical glyphs or animated mouth.
"""
from __future__ import annotations
import argparse,gzip,json
from pathlib import Path
from .core import place
from .full_song_lwss_readhead import full_word_plan
from .native_half_font_first20 import lit_pixels
from .integrated_we_made_second_w import universe as original_singer
from .full_song_vocal_extension import native_lip_gliders
from .vertical_lwss_corner import STATION,INPUT
from .staggered_word_mesh import EATER_NORTHEAST,EATER_SOUTHWEST,EATER_TEXT

PITCH=36
BASE_X=2070
BASE_Y=-710
LANE_Y=-1600
HARDWARE_GUARD=135
SHIP_GUARD=14
# Carry forward the two observed and locally repaired station reactions.
# These are NOT special rendering rules or individual word implementations.
PRIOR_OBSERVED_REPAIRS={(17,31):-24,(4,13):-24}

def song_words():
    return tuple({'index':i,'text':w.text,'g':w.make_g}
                 for i,w in enumerate(full_word_plan()))

def recipe(word):
    G=word['g']
    initial=[]
    for i,(col,row) in enumerate(lit_pixels(word['text'])):
        x=152+36*i
        n=1+PITCH*col-x+43+(G-200)//2
        if n%2:raise AssertionError(('unreachable phase',word['index'],i))
        initial.append((i,col,row,x,n//2))
    D=min(p[-1] for p in initial)-20
    if D<0:raise AssertionError(('source begins before g0',word['index']))
    out=[]
    for i,col,row,x,k in initial:
        delta=PRIOR_OBSERVED_REPAIRS.get((word['index'],i),0)
        X=x+BASE_X+2*D+delta
        K=k-D-delta//2
        if K<20 or G<200+4*K:
            raise AssertionError(('unreachable station',word['index'],i))
        if X-43-(G-200-4*K)//2!=BASE_X+1+PITCH*col:
            raise AssertionError(('wrong actual WEST arrival',word['index'],i))
        out.append({'ordinal':i,'col':col,'row':row,'X':X,'K':K})
    return out,D

def conflicts(a,b):
    if max(a['left'],b['left'])<min(a['right'],b['right']):
        return True
    for r in range(4):
        if any(abs(x-y)<SHIP_GUARD for x in a['rays'][r]
                                 for y in b['rays'][r]):
            return True
    return False

def layout(limit=403):
    original=song_words()
    if len(original)!=403 or limit<2 or limit>403:
        raise AssertionError('unexpected original Suno score')
    lanes=[];result=[]
    for word in original[2:limit]:
        routes,D=recipe(word)
        spec={'index':word['index'],'text':word['text'],'g':word['g'],
              'routes':routes,'D':D,
              'left':min(p['X'] for p in routes)-HARDWARE_GUARD,
              'right':max(p['X'] for p in routes)+HARDWARE_GUARD,
              'rays':[[word['g']//2+PITCH*p['col']
                       for p in routes if p['row']==r] for r in range(4)]}
        for lane,already in enumerate(lanes):
            if not any(conflicts(spec,other) for other in already):break
        else:
            lane=len(lanes);lanes.append([])
        spec['lane']=lane
        spec['base_y']=BASE_Y+LANE_Y*lane
        lanes[lane].append(spec)
        result.append(spec)
    return result,len(lanes)

def score(limit=403):
    stages,lanes=layout(limit)
    singer=original_singer()
    if len(singer)!=8734:
        raise AssertionError('original two-W+V converted singer was altered')
    late_v=set(native_lip_gliders('medium_0'))|set(native_lip_gliders('open_1'))
    if len(late_v)!=1290 or singer&late_v:
        raise AssertionError('original independent Suno V input source altered')
    world=set(singer)|late_v
    for lane in range(lanes):
        eaters=set().union(*(place(EATER_TEXT,BASE_X,
                          BASE_Y+LANE_Y*lane+PITCH*r)
                          for r in range(4)))
        if world&eaters:
            raise AssertionError(('shared eater overlaps signal source',lane))
        world|=eaters
    stations=0
    for stage in stages:
        y0=stage['base_y']
        parts=[]
        for p in stage['routes']:
            x=p['X'];y=y0+PITCH*p['row']
            corner=place(STATION|EATER_NORTHEAST|EATER_SOUTHWEST,x,y)
            incoming=place(INPUT,x,y-2*p['K'])
            if len(corner|incoming)!=42:
                raise AssertionError(('invalid true converter',stage['index'],p['ordinal']))
            parts.append(corner|incoming)
        added=set().union(*parts)
        if len(added)!=sum(map(len,parts)):
            raise AssertionError(('same-word g0 collision',stage['index']))
        if added&world:
            raise AssertionError(('different-word source overlap',stage['index']))
        stations+=len(added)
        world|=added
    report={
       'rule':'B3/S23','Suno_song_id':'53610991-7381-4749-96e1-79b8e3b1c28b',
       'aligned_words_in_initial_state':limit,
       'original_singer_and_first_2_converted_WV_words_preserved':True,
       'original_43_later_V_events_2_lip_tiles_preloaded':True,
       'later_real_19_cell_SOUTH_to_WEST_word_stages':len(stages),
       'later_actual_9_cell_incoming_LWSS_count':sum(len(s['routes']) for s in stages),
       'distinct_reusable_spatial_lanes':lanes,
       'base_readhead_x':BASE_X,'top_readhead_y':BASE_Y,
       'lane_spacing':LANE_Y,'glyph_pitch':PITCH,
       'generation_zero_cells':len(world),
       'native_source_additional_station_cells':stations,
       'score_not_yet_original_8cell_readout_geometry':True,
       'full_403_one_world_forward_replay_verified':False,
       'word_control_full_403_connected_to_mouth':False,
       'full_8_tile_three_state_mouth_connected':False,
       'bubble_staged':False,'finished_music_video':False,
       'stages':[{'index':s['index'],'text':s['text'],'onset_g':s['g'],
                  'lane':s['lane'],'readout_x':BASE_X,
                  'readout_y':s['base_y'],'moving_pixel_count':len(s['routes']),
                  'uniform_Gondry_offset_periods':s['D']}
                 for s in stages]}
    return world,report

def export(directory,limit=403):
    directory=Path(directory);directory.mkdir(parents=True,exist_ok=True)
    cells,report=score(limit)
    path=directory/f'complete_{limit}_physical_SOUTH_to_WEST_g0.tsv.gz'
    with gzip.open(path,'wt',encoding='utf8',compresslevel=6) as f:
        for x,y in sorted(cells):f.write(f'{x} {y}\n')
    (directory/f'complete_{limit}_physical_score.json').write_text(
        json.dumps(report,indent=2)+'\n',encoding='utf8')
    return report

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--out',type=Path,required=True)
    p.add_argument('--words',type=int,default=403)
    args=p.parse_args()
    print(json.dumps(export(args.out,args.words),indent=2))
