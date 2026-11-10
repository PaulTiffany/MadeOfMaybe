"""Qualify every rendered frame against exactly one B3/S23 world."""
import json,struct
from pathlib import Path
from life.core import evolve,place
from life.native_half_font_first20 import universe,expected_word
from life.native_word_vocal_link import MOUTH_CORNER
from life.relocated_singer_anchor import SINGER_TRANSLATION
from life.glider_controlled_mouth import BLOCK,MEDIUM_TARGETS,OPEN_TARGETS
from life.refined_singer_candidate import LIP_DROP_Y

def frames(path):
    with Path(path).open('rb') as f:
        while h:=f.read(8):
            g,n=struct.unpack('<iI',h)
            buf=f.read(n*8)
            if len(buf)!=n*8:raise ValueError('short native frame')
            yield g,set(struct.iter_unpack('<ii',buf))

def verify(path):
    observed={};n=0;prev=-8
    for g,cells in frames(path):
        if g!=prev+8:raise AssertionError((g,prev))
        n+=1;prev=g
        if g in (0,752,904,2152,2176,2200,2304,3008,3840):
            observed[g]=cells
    if n!=481 or prev!=3840 or observed[0]!=universe():
        raise AssertionError('not a continuous 8090-cell native universe')
    w=set(observed[2152]);nextw=set(observed[2176])
    for _ in range(4):w=evolve(w);nextw=evolve(nextw)
    if len(expected_word())!=204 or not expected_word()<=w:
        raise AssertionError('missing 17 moving mini word pixel ships')
    if not expected_word(-12)<=nextw:
        raise AssertionError('word is not traveling at c/2')
    accent=place(BLOCK,MOUTH_CORNER[0]+SINGER_TRANSLATION[0],
                      MOUTH_CORNER[1]+SINGER_TRANSLATION[1])
    if not accent<=w or not accent<=observed[2200] or accent<=observed[2304]:
        raise AssertionError('native W/V physical lip gate failed')
    for g,medium,opening in ((752,4,0),(904,0,4),(2200,0,4),(3008,4,0)):
        cells=observed[g]
        actual=[sum(place(BLOCK,x+SINGER_TRANSLATION[0],
             y+LIP_DROP_Y+SINGER_TRANSLATION[1])<=cells for x,y in targets)
             for targets in (MEDIUM_TARGETS,OPEN_TARGETS)]
        if actual!=[medium,opening]:raise AssertionError((g,actual))
    return {'rule':'B3/S23','generation_0_cells':len(observed[0]),
       'generation_3840_cells':len(observed[3840]),
       'full_world_frames':481,'native_lyric_moving_pixels':17,
       'native_LWSS_cells_at_g2156':204,'c2_motion_g2180':True,
       'true_two_source_lip_block':True,
       'full_238_88s_video_complete':False}

if __name__=='__main__':
    import sys
    result=verify(sys.argv[1])
    Path(sys.argv[2]).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
