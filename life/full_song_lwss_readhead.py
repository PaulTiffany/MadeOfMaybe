"""TRUE native B3/S23 401-word westbound LWSS destination score, NO BUBBLE.

This is the Gondry *OUTPUT FIRST* layout: prescribe exactly where every
original Suno word appears as REAL 3x4 moving lightweight spaceships,
backtrace each ship in free flight to its actual generation-zero cells,
and physically catch the ships with the already proven eater-1.

The first two words WE/MADE use the EXISTING proven, visible, southbound
->90-degree-converter->westbound native Life hardware and singer W/V lip.
Remaining 401 words are currently preloaded as WESTBOUND LWSS in the
output rail -- NOT yet proven to originate from physical corner converters.
That input-backtrace gate is explicit. No rendered/subtitle glyph insertion.

Physically compact layout, aligned at 192 native generations per song
second. A real eight-cell LWSS row pitch is verified with native B3/S23
24-ship eater trains; the same fishhook clears these rows. Do not confuse
the promised completed converter ancestry with a mere output score.
"""
from __future__ import annotations
from dataclasses import dataclass,asdict
from pathlib import Path
import heapq,json
from functools import lru_cache
from .core import evolve,place
from .native_half_font_first20 import components as original_components,lit_pixels
from .two_line_native_singer import made_parts,SHIFT,ROW_Y
from .full_song_karaoke import ALIGNMENT_FILE,compile_plan,GPS
from .lyric_cues import read_alignment
from .phrase_crawler_eater import LWSS,EATER_LEFT
from .export_operational import compact_rle

PITCH=8
ROW_PITCH=48
X_ANCHOR=2500
Y_ANCHOR=-530
HORIZONTAL_GUARD=8
SONG_DURATION=238.88
END_G=45864

@dataclass(frozen=True)
class MovingWord:
    index:int
    text:str
    make_g:int
    lane:int
    glyph_pixel_count:int
    source_left:int
    source_right:int
    physical_lyric_x:int
    physical_lyric_y:int

@lru_cache(maxsize=1)
def full_word_plan():
    lines=compile_plan(read_alignment(ALIGNMENT_FILE))
    words=tuple(w for l in lines for w in l.words)
    if len(words)!=403 or GPS!=192:
        raise AssertionError('original Suno song score was replaced')
    return words

@lru_cache(maxsize=1)
def layout():
    plans=[]
    for w in full_word_plan()[2:]:
        xy=lit_pixels(w.text)
        if not xy:raise AssertionError(('empty native moving word',w.word_index))
        xs=[w.make_g//2+PITCH*x for x,y in xy]
        plans.append((min(xs),max(xs)+4,w,xy))
    plans.sort(key=lambda v:(v[0],v[2].word_index))
    heap=[];next_lane=0;staged=[]
    for left,right,w,xy in plans:
        if heap and heap[0][0]+HORIZONTAL_GUARD<=left:
            previous_end,lane=heapq.heappop(heap)
        else:
            lane=next_lane;next_lane+=1
        heapq.heappush(heap,(right,lane))
        staged.append(MovingWord(w.word_index,w.text,w.make_g,lane,
            len(xy),left,right,X_ANCHOR,Y_ANCHOR+ROW_PITCH*lane))
    return tuple(sorted(staged,key=lambda m:m.index)),next_lane

def singer_parts():
    parts=original_components()
    # omit old bubble (index1); it is constructed only after the complete
    # physical film tells us the unoccupied corridors.
    first=tuple(parts[k] for k in (0,2,3,4))
    second=place(set().union(*made_parts(0,ROW_Y)),SHIFT[0]+900,SHIFT[1])
    return first+(second,)

def source_seeds():
    placed,lanes=layout()
    sources=set()
    for p in placed:
        for col,row in lit_pixels(p.text):
            x=p.physical_lyric_x+p.make_g//2+PITCH*col
            y=p.physical_lyric_y+PITCH*row
            segment=place(LWSS,x,y)
            if segment & sources:
                raise AssertionError(('overlapping real spaceship at g0',p.index,col,row))
            sources|=segment
    return sources

def eaters():
    _,lanes=layout()
    cells=set()
    for lane in range(lanes):
        for row in range(4):
            part=place(EATER_LEFT,X_ANCHOR,Y_ANCHOR+ROW_PITCH*lane+PITCH*row)
            if part&cells:raise AssertionError('native fishhook lanes overlap')
            cells|=part
    if evolve(cells)!=cells:
        raise AssertionError('receiver bank not a native B3/S23 still life')
    return cells

@lru_cache(maxsize=1)
def motion_phases():
    p=[frozenset(LWSS)]
    for i in range(3):p.append(frozenset(evolve(p[-1])))
    if evolve(p[3])!=place(LWSS,-2,0):
        raise AssertionError('not a true westbound LWSS c/2 orbit')
    return tuple(p)

def row_events():
    """All physical arrivals at the actual seven-cell catcher (not render cues)."""
    out={}
    for p in layout()[0]:
        for col,row in lit_pixels(p.text):
            y=p.physical_lyric_y+PITCH*row
            arrival=p.make_g+2*PITCH*col
            out.setdefault(y,[]).append((arrival,p.index,col,row))
    return {y:tuple(sorted(records)) for y,records in out.items()}

def verify_train_geometry():
    staged,lanes=layout()
    rows=row_events()
    total=sum(p.glyph_pixel_count for p in staged)
    if len(staged)!=401 or total!=10366-17-32:
        raise AssertionError(('missing original Suno word or LWSS pixel',len(staged),total))
    for y,events in rows.items():
        if any(b[0]-a[0]<2*PITCH for a,b in zip(events,events[1:])):
            raise AssertionError(('same-row LWSSs physically collide',y))
    original=list(singer_parts())
    sources=source_seeds()
    receiver=eaters()
    parts=original+[sources,receiver]
    if len(set().union(*parts))!=sum(map(len,parts)):
        raise AssertionError('first-singer vs complete native LWSS train g0 overlap')
    if max(x for x,y in receiver)>min(x for x,y in sources):
        raise AssertionError('receiver lies in front of source rail')
    return {'rule':'B3/S23','Suno_sung_words_total':403,
            'native_converted_WE_MADE_in_original_singer':True,
            'prepositioned_output_WEST_LWSS_words':len(staged),
            'prepositioned_output_WEST_LWSS_pixels':total,
            'prepositioned_output_WEST_LWSS_cells':len(sources),
            'source_is_one_immutable_generation_zero_universe':True,
            'original_WV_mouth_retained':True,
            'physical_rounded_bubble_cells':0,
            'moving_WEST_velocity':'(-2,0)/4 generations',
            'native_3x4_pixel_pitch':PITCH,
            'native_row_pitch':ROW_PITCH,'physical_readhead_x':X_ANCHOR,
            'physical_readhead_y':Y_ANCHOR,
            'physical_parallel_lanes':lanes,
            'distinct_eater_rows':len(rows),
            'fishhook_cells':len(receiver),
            'native_eaters_are_B3S23_still_life':True,
            'all_same_lane_ships_spaced_at_least_eight_cells':True,
            'true_source_g0_population':sum(map(len,parts)),
            'song_end_g':END_G,'nominal_song_duration_s':SONG_DURATION,
            'actual_90_degree_converters_for_all_403_words':False,
            'full_song_WV_lips_physically_wired':False,
            'complete_native_movie_rendered':False,
            'optical_2x2_block_karaoke_substitute_used':False,
            'final_nuke_or_symbolics':False}

def export(out):
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    report=verify_train_geometry()
    original=singer_parts();ships=source_seeds();fixed=eaters()
    cells=set().union(*original,ships,fixed)
    (out/'all_403_words_native_westbound_output_g0.rle').write_text(
        compact_rle(cells,(
           'One actual B3/S23 universe, native singer, 401 preloaded LWSS words.',
           'Original Suno WE/MADE arrive via original 90-degree converters.',
           'Native compact W-moving 3x4 word pixels, 8-cell pitch.',
           'No bubble, no lyric overlay, no final nuke.',
           '401 later converter BACKTRACE and full native lip gate remain open.'
        )),encoding='utf8')
    (out/'native_lyric_rail.json').write_text(
        json.dumps([asdict(x) for x in layout()[0]],indent=2)+'\n')
    (out/'native_eater_arrival_events.json').write_text(
        json.dumps({str(y):v for y,v in row_events().items()},indent=2)+'\n')
    (out/'physical_native_workprint_contract.json').write_text(
        json.dumps(report,indent=2)+'\n')
    return report

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser()
    p.add_argument('--out',required=True)
    a=p.parse_args()
    print(json.dumps(export(a.out),indent=2))
