"""Known reusable 2023 G-to-LWSS conduit, reflected to output WEST.

Luke Kiernan's 105-cell stable Life converter, from
https://conwaylife.com/wiki/G-to-LWSS_(2023) . This is not our new
invention or a renderer trick. The original lyric LWSS turner remains
one-shot; this is an independently qualified *reusable* alternative.
"""
from __future__ import annotations
from functools import lru_cache
from .core import parse_rle,evolve,place
from .vertical_lwss_corner import components

RLE='''x = 65, y = 64, rule = B3/S23
bo$2bo$3o32$47b2o$47b2o2$56b2o$56bobob2o$58bobo$57b2obo$57bo2b2o$58b2o2bo$59bobo$59bob2o$30b2o26b2obo2bo$30b2o29bob2o$48bo12bo$26bo22bo10b2o$26b3o18b3o$29bo$28b2o31b2o$48b2o6b2obo2bo$47bobo5bobob3o$34b2o12bo6bobo$34bobo16b3ob5o$35bo16bo3bo4bo$52b2o2bobo$43bo13b2o$42bobo2b2o$31b2o10bo3bobo$32bo16bo$29b3o17b2o$29bo!'''
INPUT=frozenset({(1,0),(2,1),(0,2),(1,2),(2,2)})

def west(cells):
    return {(y,x) for x,y in cells}

@lru_cache(maxsize=1)
def hardware():
    initial=parse_rle(RLE)
    h=initial-set(INPUT)-place(INPUT,47,47)
    if len(h)!=105 or evolve(h)!=h:
        raise AssertionError('failed to isolate original 105-cell catalyst')
    return frozenset(west(h))

def train(n=4,gap_g=188):
    if n<0 or gap_g<4 or gap_g%4:raise ValueError('bad input train')
    gliders=[west(place(INPUT,47-gap_g*i//4,47-gap_g*i//4))
             for i in range(n)]
    world=set(hardware())|set().union(*gliders)
    if len(world)!=105+5*n:raise AssertionError('source overlap')
    return world

def output_ships(world):
    ships=[]
    for c in components(set(world)-set(hardware())):
        if len(c)!=12:continue
        after=set(c)
        for _ in range(4):after=evolve(after)
        if after==place(c,-2,0):ships.append(frozenset(c))
    return ships

def qualify(n=4,gap_g=188,until=1000):
    w=train(n,gap_g)
    for _ in range(until):w=evolve(w)
    ship=output_ships(w)
    if not set(hardware())<=w or len(ship)!=n or len(w)!=105+12*n:
        raise AssertionError('station not restored or outputs not clean')
    return {'rule':'B3/S23',
      'known_2023_source':'https://conwaylife.com/wiki/G-to-LWSS_(2023)',
      'stable_hardware_cells':105,
      'input_gliders':n,'qualified_recovery_interval':gap_g,
      'output_LWSS_direction':'west',
      'output_LWSS_count':len(ship),'tested_generation':until,
      'terminal_population':len(w),'hardware_restored':True,
      'extraneous_ash':0,'whole_song_converter_array_built':False}
