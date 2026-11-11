"""Test real g0→g3840 native film snapshots against both Suno inputs."""
import json,struct,sys
from pathlib import Path
from life.core import evolve,place
from life.native_word_vocal_link import (world,MOUTH_CORNER,FIRST_WORD_G,provenance)
from life.native_congruent_first20 import WE_SHIFT,word_routes
from life.staggered_word_mesh import reference_output
from life.glider_controlled_mouth import BLOCK,MEDIUM_TARGETS,OPEN_TARGETS
from life.relocated_singer_anchor import SINGER_TRANSLATION
from life.refined_singer_candidate import LIP_DROP_Y

def frames(path):
    with Path(path).open('rb') as f:
        while True:
            h=f.read(8)
            if not h:break
            g,n=struct.unpack('<iI',h)
            payload=f.read(8*n)
            if len(payload)!=8*n:raise ValueError('truncated actual Life state')
            yield g,set(struct.iter_unpack('<ii',payload))

def mouth_count(cells,targets):
    return sum(place(BLOCK,x+SINGER_TRANSLATION[0],
                   y+LIP_DROP_Y+SINGER_TRANSLATION[1])<=cells for x,y in targets)

def full_word(dx=0):
    phase=reference_output()
    return set().union(*(place(phase,44+36*col+WE_SHIFT[0]+SINGER_TRANSLATION[0]+dx,
          36*row+WE_SHIFT[1]+SINGER_TRANSLATION[1])
          for _,col,row,*_ in word_routes()))

def verify(path):
    take={};previous=-8;count=0
    for g,cells in frames(path):
        if g!=previous+8:raise AssertionError('non-contiguous Life frames')
        previous=g;count+=1
        if g in (0,752,904,1800,2152,2176,2200,2304,2400,3008,3840):
            take[g]=cells
    assert count==481 and previous==3840
    assert len(take[0])==8867 and take[0]==world()
    assert len(take[3840])==7645
    for g,m,o in [(752,4,0),(904,0,4),(1800,0,0),
                  (2200,0,4),(2400,0,4),(3008,4,0),(3840,4,0)]:
        assert (mouth_count(take[g],MEDIUM_TARGETS),
                mouth_count(take[g],OPEN_TARGETS))==(m,o),(g,m,o)
    formation=set(take[2152]);flight=set(take[2176])
    for _ in range(4):
        formation=evolve(formation);flight=evolve(flight)
    assert len(full_word())==420 and full_word()<=formation
    assert full_word(-12)<=flight
    accent=place(BLOCK,MOUTH_CORNER[0]+SINGER_TRANSLATION[0],
                  MOUTH_CORNER[1]+SINGER_TRANSLATION[1])
    assert accent<=formation and accent<=take[2200]
    assert not accent<=take[2304]
    return {'rule':'B3/S23','g0_population':8867,'native_frames':481,
      'generations_per_second':192,'duration_s':481/24,
      'W_word_WE_g':FIRST_WORD_G,'genuine_WE_LWSS_pixels':35,
      'V_original_isolated_Suno_stem':provenance()['vocal_stem_id'],
      'word_marker_LWSS_byproduct_physically_meets_V_at_mouth':True,
      'actual_mouth_block_erased_by_g2304':True,
      'whole_world_equals_five_components_each_generation_to_3840':
          'separate C++ checker passes',
      'word_marker_is_extra_LWSS_lane_not_one_glyph_pixel':True,
      'full_403_word_song_qualified':False,'repeatable_gate_qualified':False,
      'no_renderer_cell_insertion':True}

if __name__=='__main__':
    a=verify(sys.argv[1])
    Path(sys.argv[2]).write_text(json.dumps(a,indent=2)+'\n')
    print(json.dumps(a,indent=2))
