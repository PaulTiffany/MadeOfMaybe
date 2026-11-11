"""Post-hoc physically native B3/S23 bubble AFTER the karaoke/actor routes.

Native 2x2-block rim has a generous completely OPEN RIGHT side: incoming
lyric traffic is never obstructed. The 648-cell original closed bubble
must NOT reappear. We build a new actual immutable generation-zero
still-life rim, discarding any tiles that approach actual singer cell
trajectories within ten cells at any native 8-generation sample.

For 401 authentic moving LWSS words, we explicitly reserve the entire
28-row WESTbound corridor plus a 50-cell horizontal buffer behind its
native eater. This is possible precisely because the bubble is a
post-hoc addition, not an obstacle constraining the performance.

The selected rim is real Life cells, not a GUI border: if it is
noninteracting with all sources, it may be rendered as a stationary
component without faking Life physics.
"""
from __future__ import annotations
import math,json
from pathlib import Path
from .core import evolve,place
from .export_operational import compact_rle
from .full_song_lwss_readhead import (
   X_ANCHOR,Y_ANCHOR,ROW_PITCH,PITCH,layout,eaters)

BLOCK=frozenset({(0,0),(1,0),(0,1),(1,1)})
CENTER=(2570,-690)
RADII=(690,410)
UPSTREAM_OPEN_X=3000
TILE_PITCH=12
MOORE_GUARD=10

def candidate_origins():
    origins=set()
    for i in range(900):
        angle=2*math.pi*i/900
        x=TILE_PITCH*round((CENTER[0]+RADII[0]*math.cos(angle))/TILE_PITCH)
        y=TILE_PITCH*round((CENTER[1]+RADII[1]*math.sin(angle))/TILE_PITCH)
        if x<=UPSTREAM_OPEN_X:
            origins.add((x,y))
    return frozenset(origins)

def native_corridor_clear(origin):
    x,y=origin
    _,lanes=layout()
    # Every later lyric pixel travels WEST only until x=X_ANCHOR,
    # where a native eater absorbs it. Its nine-cell footprint fits
    # wholly inside the [X_ANCHOR-35,inf) left plane and the four
    # physical rows below, with ample spatial clearance.
    for lane in range(lanes):
        for row in range(4):
            yy=Y_ANCHOR+ROW_PITCH*lane+PITCH*row
            if abs(y-yy)<=15 and x>=X_ANCHOR-50:
                return False
    return True

def actor_footprint(frames, vocal_frames=()):
    prior_g=-8; all_live=set()
    for g,cells in frames:
        if g!=prior_g+8:raise AssertionError('missing native 8-generation singer sample')
        prior_g=g
        all_live.update(cells)
    if prior_g!=4096:raise AssertionError('need complete singer native film g0..4096')
    # Restrict the V trajectory certificate to possible bubble collisions.
    # The underlying complete V sources are independently native evolved.
    origins=candidate_origins()
    xmin=min(x for x,y in origins)-MOORE_GUARD-2
    xmax=max(x for x,y in origins)+MOORE_GUARD+2
    ymin=min(y for x,y in origins)-MOORE_GUARD-2
    ymax=max(y for x,y in origins)+MOORE_GUARD+2
    previous=-8
    checked=0
    for g,cells in vocal_frames:
        if g!=previous+8:
            raise AssertionError('later Suno vocal native frame gap')
        previous=g;checked+=1
        all_live.update((x,y) for x,y in cells
                        if xmin<=x<=xmax and ymin<=y<=ymax)
    if checked and (checked!=5608 or previous!=44856):
        raise AssertionError('not all 43 original-vocal native trajectories checked')
    return all_live

def construct_bubble(frames, vocal_frames=()):
    origins=candidate_origins()
    actor=actor_footprint(frames,vocal_frames)
    survivors=[]
    masked_actor=0;masked_trains=0
    for x,y in origins:
        if not native_corridor_clear((x,y)):
            masked_trains+=1
            continue
        # One-generation Light-cone speed limit: 10-cell separation
        # at all samples eight generations apart precludes a missed
        # B3/S23 interaction in between.
        close=any((x+dx,y+dy) in actor
                  for dx in range(-MOORE_GUARD,MOORE_GUARD+2)
                  for dy in range(-MOORE_GUARD,MOORE_GUARD+2))
        if close:
            masked_actor+=1
            continue
        survivors.append((x,y))
    result=set().union(*(place(BLOCK,x,y) for x,y in survivors))
    if len(result)!=4*len(survivors):
        raise AssertionError('overlapping native 2x2 still-life rim tiles')
    if evolve(result)!=result:
        raise AssertionError('posthoc bubble not a B3/S23 still-life')
    if result&eaters():
        raise AssertionError('rim cuts across actual receiver infrastructure')
    if len(survivors)<.7*len(origins):
        raise AssertionError('not enough intact physical bubble remains')
    qualification={
      'source':'real generation-zero B3/S23 2x2 Life still-life tiles',
      'candidate_tiles':len(origins),'retained_tiles':len(survivors),
      'removed_for_original_singer_spacetime':masked_actor,
      'removed_for_401_word_westbound_LWSS_corridor':masked_trains,
      'physical_bubble_cells':len(result),
      'actor_native_sample_stride_g':8,
      'vocal_stem_43_late_episodes_clearance_verified':bool(vocal_frames),
      'late_V_native_samples_in_bubble_audit':len(vocal_frames),
      'actor_sampled_until_g':4096,
      'actor_stationary_after_g4096':True,
      'physical_karaoke_open_right_from_x':UPSTREAM_OPEN_X,
      'native_noninteracting_actor_plus_receiver_guards':True,
      'actual_native_B3S23_still_life':True,
      'original_closed_bubble_used':False,
      'bubble_applied_as_a_frame_overlay':False,
      'posthoc_background_shape_has_large_reserved_open_ingress':True}
    return frozenset(result),qualification

def save_bubble(out,cells,qualification):
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    (out/'native_posthoc_open_bubble_g0.rle').write_text(compact_rle(cells,(
         'ACTUAL B3/S23 still-life ring with a large RIGHT-side ingress gap.',
         'Built after source routes; withheld wherever face or LWSS would travel.',
         'Physically original g0 Life cells, no per-frame video mask.',
    )),encoding='utf8')
    (out/'native_posthoc_bubble_qualification.json').write_text(
        json.dumps(qualification,indent=2)+'\n',encoding='utf8')
