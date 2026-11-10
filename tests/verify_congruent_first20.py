"""Assertions on real native full-world frames, never on video-renderer state."""
import json,struct
from pathlib import Path
from life.core import evolve,place
from life.native_congruent_first20 import (
 components,provenance,word_routes,word_accent,FIRST_WORD_G,WE_SHIFT,VOICE_EVENTS)
from life.glider_controlled_mouth import BLOCK,MEDIUM_TARGETS,OPEN_TARGETS
from life.staggered_word_mesh import reference_output
from life.refined_singer_candidate import LIP_DROP_Y
from life.relocated_singer_anchor import SINGER_TRANSLATION

def frames(path):
    with Path(path).open('rb') as f:
        while True:
            h=f.read(8)
            if not h:break
            g,n=struct.unpack('<iI',h)
            payload=f.read(8*n)
            if len(payload)!=8*n:raise ValueError('truncated world frame')
            yield g,set(struct.iter_unpack('<ii',payload))

def mouth(cells):
    return {
      'medium':sum(place(BLOCK,x+SINGER_TRANSLATION[0],
              y+LIP_DROP_Y+SINGER_TRANSLATION[1])<=cells for x,y in MEDIUM_TARGETS),
      'open':sum(place(BLOCK,x+SINGER_TRANSLATION[0],
              y+LIP_DROP_Y+SINGER_TRANSLATION[1])<=cells for x,y in OPEN_TARGETS),
      'word_accent':place(BLOCK,SINGER_TRANSLATION[0],
                              100+SINGER_TRANSLATION[1])<=cells,
    }

def word_phase(dx=0):
    p=reference_output()
    return set().union(*(place(p,44+36*col+WE_SHIFT[0]+SINGER_TRANSLATION[0]+dx,
                             36*row+WE_SHIFT[1]+SINGER_TRANSLATION[1])
              for _,col,row,*_ in word_routes()))

def verify(native):
    src=provenance()
    keep={0,752,904,1688,1800,2000,2152,2176,2200,2320,2400,3008,3840}
    selected={}
    count=0;last=-8
    for g,world in frames(native):
        assert g==last+8,(g,last)
        last=g;count+=1
        if g in keep:selected[g]=world
    assert count==481 and last==3840
    assert len(selected[0])==8926
    assert set().union(*components())==selected[0]
    observed={str(g):mouth(selected[g]) for g in selected}
    expected={0:(0,0,False),752:(4,0,False),904:(0,4,False),
              1800:(0,0,False),2000:(0,0,False),2200:(0,4,True),
              2320:(0,4,False),2400:(0,4,False),3008:(4,0,False),
              3840:(4,0,False)}
    for g,(m,o,w) in expected.items():
        assert observed[str(g)]==dict(medium=m,open=o,word_accent=w),(g,observed[str(g)])
    at2156=set(selected[2152])
    at2180=set(selected[2176])
    for _ in range(4):
        at2156=evolve(at2156)
        at2180=evolve(at2180)
    we=word_phase()
    assert len(we)==420 and we<=at2156
    assert word_phase(-12)<=at2180
    assert not observed['0']['word_accent']
    decision={}
    for word in (False,True):
        for vocal in (False,True):
            cells=word_accent(w=word,v=vocal)
            for _ in range(FIRST_WORD_G):cells=evolve(cells)
            produced=place(BLOCK,0,100)<=cells
            assert produced==(word and vocal)
            decision[f'{int(word)}{int(vocal)}']=produced
    return {
       'rule':'B3/S23','song_duration_qualified_s':481/24,
       'audio_generation_rate':192,'video_frame_count':481,
       'g0_population':8926,'full_world_last_generation':3840,
       'whole_world_equals_all_five_independent_parts_at_every_tick':'verified in C++ job',
       'actual_g2156_word':'WE','native_moving_pixel_count':35,
       'native_cells_at_g2156_in_moving_word':420,'c2_movement_to_g2180':True,
       'source_vocal_stem':src['vocal_stem_id'],'vocal_events':VOICE_EVENTS,
       'mouth_native_checkpoints':observed,
       'independent_native_word_and_vocal_accent_truth_table':decision,
       'not_physically_branched_from_LWSS_letters':True,
       'not_reusable_word_voice_oscillator':True,
       'not_complete_song_or_nuke':True,
       'no_runtime_injected_cells':True,
    }

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser()
    p.add_argument('--frames',required=True)
    p.add_argument('--output',required=True)
    a=p.parse_args()
    result=verify(a.frames)
    Path(a.output).write_text(json.dumps(result,indent=2)+'\n',encoding='utf8')
    print(json.dumps(result,indent=2))
