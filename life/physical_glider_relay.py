"""Native B3/S23 single-glider relay, plus an honest relocation reachability gate.

The Snark is a repeatable 90-degree *reflector*, not a glider gun.  Unlike
a gun it never generates an unscheduled pulse; it emits only in response to
an arriving glider.  Its original catalyst RLE is from LifeWiki, Snark
(Mike Playle, 2013).  We remove the example input glider, retain all 49
stationary cells, and preserve that precise signal phase.

This module qualifies the proposed reusable relay as a component.  It does
NOT claim that the existing far-away (0,0) glyph has been rerouted through
a relocated splitter.  That old glyph is outside a c/4 glider's deadline.
"""
from __future__ import annotations

from functools import lru_cache
from .core import evolve,parse_rle,place
from .glider_controlled_mouth import rotate
from .lyric_mouth_fanout import CATALYSTS,PRIMARY_INPUT,SOUTHEAST_GLIDER
from .physical_lip_splitter_bridge import (SINGER_TRANSLATION,
    SPLITTER_LOCAL_ORIGIN,REFERENCE_SPLIT_OUTPUT_G,CAUSAL_WORD_G,WORD_PIXEL)

# LifeWiki's original demonstration contains one five-cell signal at bottom left.
SNARK_RLE = """x = 23, y = 32, rule = B3/S23
14b2o$14bobo$16bo4b2o$12b4ob2o2bo2bo$12bo2bobobobob2o$15bobobobo$16b2obobo$20bo2$6b2o$7bo7b2o$7bobo5b2o$8b2o7$18b2o$18bo$19b3o$21bo7$3o$2bo$bo!"""
SNARK_IN=frozenset({(0,29),(1,29),(2,29),(2,30),(1,31)})
SNARK_CATALYST=frozenset(parse_rle(SNARK_RLE)-SNARK_IN)
SEPARATION_GENERATIONS=820
SNARK_OUT_GENERATION=100

# This is physically below the static bubble in the current singer's LOCAL
# coordinate system.  It is an engineering target, not a qualified move.
PROPOSED_SPLITTER_LOCAL_ORIGIN=(380,120)


def relay_seed(*,one=True,two=True):
    """Two sequential, physically preloaded gliders through ONE stable Snark."""
    cells=set(SNARK_CATALYST)
    if one:cells.update(SNARK_IN)
    if two:cells.update(place(SNARK_IN,-SEPARATION_GENERATIONS//4,
                             SEPARATION_GENERATIONS//4))
    return cells


def _components(cells):
    remain=set(cells)
    groups=[]
    while remain:
        p=remain.pop();group={p};todo=[p]
        while todo:
            x,y=todo.pop()
            for dx in (-1,0,1):
                for dy in (-1,0,1):
                    q=(x+dx,y+dy)
                    if q in remain:
                        remain.remove(q);group.add(q);todo.append(q)
        groups.append(group)
    return groups


def _glider_velocity(cells):
    future=set(cells)
    for _ in range(4):future=evolve(future)
    out=[(dx,dy) for dx in (-1,1) for dy in (-1,1)
         if future==place(cells,dx,dy)]
    if len(cells)!=5 or len(out)!=1:raise AssertionError('not a clean c/4 glider')
    return out[0]


@lru_cache(maxsize=1)
def snark_relay_certificate():
    """Exact native-Life two-pulse, one-pulse and source-ablated replays."""
    catalysts=set(SNARK_CATALYST)
    if len(catalysts)!=49 or evolve(catalysts)!=catalysts:
        raise AssertionError('Snark catalyst geometry is not a 49-cell still life')
    samples=(0,100,820,920)
    checkpoints={}
    results={}
    for key,flags in (('both',(True,True)),('one_only',(True,False)),
                      ('two_only',(False,True)),('off',(False,False))):
        live=relay_seed(one=flags[0],two=flags[1]);seen={}
        for g in range(921):
            if g in samples:
                # At g100 and g920, the 49 stable catalysts MUST have
                # recovered, and all other cells must be clean gliders.
                groups=_components(live-catalysts) if g else []
                seen[g]={'population':len(live),
                         'catalyst_restored':catalysts<=live,
                         'clean_output_gliders':
                          sum(len(p)==5 and _glider_velocity(p)==(1,1)
                              for p in groups) if g in (100,920) else None}
            if g<920:live=evolve(live)
        if key=='both':checkpoints=seen
        results[key]=seen
    if not (results['both'][100]['clean_output_gliders']==1 and
            results['both'][920]['clean_output_gliders']==2 and
            results['one_only'][920]['clean_output_gliders']==1 and
            results['two_only'][920]['clean_output_gliders']==1 and
            results['off'][920]['clean_output_gliders']==0):
        raise AssertionError('Snark is not a clean two-pulse causal repeater')
    if not all(results[k][920]['catalyst_restored'] for k in results):
        raise AssertionError('Snark catalysts failed to recover')
    return {'rule':'B3/S23','stationary_cells':49,
            'input_gliders_preloaded_at_gen_zero':2,
            'source_separation_generations':SEPARATION_GENERATIONS,
            'first_output_generation':SNARK_OUT_GENERATION,
            'output_direction':(1,1),
            'both_outputs_verified_by_native_life':2,
            'source_ablation_prevents_corresponding_output':True,
            'controller_relocation_qualified':False,
            'replays':results}


def proposed_relocation_feasibility():
    """Conservative reachability necessary condition for a GLIDER-ONLY route.

    Reflections, conduits, and delays cannot make an existing c/4 glider
    cover more than one cell per four generations on either coordinate.
    This check must precede any attempt to route the original glyph.
    """
    old=SPLITTER_LOCAL_ORIGIN
    new=PROPOSED_SPLITTER_LOCAL_ORIGIN
    output_at_340=place(rotate(SOUTHEAST_GLIDER,2),
                       new[0]+SINGER_TRANSLATION[0],
                       new[1]+SINGER_TRANSLATION[1])
    # x of all glider cells is significantly to the right of (0,0).
    dx=min(abs(x-WORD_PIXEL[0]) for x,y in output_at_340)
    dy=min(abs(y-WORD_PIXEL[1]) for x,y in output_at_340)
    native_ticks_left=CAUSAL_WORD_G-REFERENCE_SPLIT_OUTPUT_G
    reachable_axis=native_ticks_left//4
    return {'proposed_splitter_local_origin':new,
            'original_splitter_local_origin':old,
            'old_lyric_anchor':WORD_PIXEL,
            'output_generation':REFERENCE_SPLIT_OUTPUT_G,
            'first_word_appearance_generation':CAUSAL_WORD_G,
            'required_min_x_axis_displacement':dx,
            'required_min_y_axis_displacement':dy,
            'max_c4_axis_displacement_before_deadline':reachable_axis,
            'old_lyric_anchor_reachable_by_c4':max(dx,dy)<=reachable_axis,
            'next_required_design_change':'Relocate the native first-word glyph sink closer to the singer and reroute both splitter outlets; then replay both lip/word ablations.',
            'controller_relocation_qualified':False}
