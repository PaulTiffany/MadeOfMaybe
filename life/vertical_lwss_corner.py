"""One real B3/S23 corner: LWSS arrives vertically from above, leaves left.

Based on knightlife's July 2009 LWSS 90-degree-turning reaction:
https://conwaylife.com/forums/viewtopic.php?p=633

This is a consumable one-shot reaction, not a reusable lyric-row relay.
It emits additional gliders/debris. Source ablation and actual four-step
spaceship velocities are checked in native B3/S23.
"""
from collections import Counter

# The 19 original stable cells are a beehive, boat, and pond.
BEEHIVE=frozenset({(1,0),(0,1),(2,1),(0,2),(2,2),(1,3)})
BOAT=frozenset({(8,6),(7,7),(9,7),(7,8),(8,8)})
POND=frozenset({(14,20),(15,20),(13,21),(16,21),(13,22),(16,22),(14,23),(15,23)})
# Nine-cell c/2 LWSS traveling right in the input-oriented version.
LWSS_RIGHT=frozenset({(1,16),(4,16),(5,17),(1,18),(5,18),
                      (2,19),(3,19),(4,19),(5,19)})

def orient(p):
    """Rotate the whole reaction: right-moving input becomes down-moving."""
    x,y=p
    return (-y,x)

def shifted(cells,x=0,y=0):
    return {(a+x,b+y) for a,b in cells}

STATION=frozenset(map(orient,BEEHIVE|BOAT|POND))
INPUT=frozenset(map(orient,LWSS_RIGHT))

def evolve(cells):
    neighbors=Counter((x+dx,y+dy) for x,y in cells
                      for dx in (-1,0,1) for dy in (-1,0,1) if dx or dy)
    return {p for p,n in neighbors.items() if n==3 or n==2 and p in cells}

def components(cells):
    remain=set(cells);parts=[]
    while remain:
        component={remain.pop()};stack=list(component)
        while stack:
            x,y=stack.pop()
            for dx in (-1,0,1):
                for dy in (-1,0,1):
                    p=(x+dx,y+dy)
                    if p in remain:
                        remain.remove(p);component.add(p);stack.append(p)
        parts.append(component)
    return parts

def drift(cells,steps):
    world=set(cells)
    for _ in range(steps):world=evolve(world)
    return world

def outgoing_lwss(world):
    """Locate a separately traveling leftbound LWSS by exact c/2 motion."""
    for group in components(world):
        if len(group) in (9,12) and drift(group,4)==shifted(group,-2,0):
            return group
    return None

def qualify():
    assert len(STATION)==19 and evolve(STATION)==set(STATION)
    assert len(INPUT)==9 and drift(INPUT,4)==shifted(INPUT,0,2)
    live=STATION|INPUT
    at200=drift(live,200)
    outgoing=outgoing_lwss(at200)
    if outgoing is None or len(outgoing)!=12:
        raise AssertionError('no clean 90-degree LWSS output at generation 200')
    if drift(outgoing,40)!=shifted(outgoing,-20,0):
        raise AssertionError('output LWSS fails continued c/2 left travel')
    if outgoing_lwss(drift(STATION,200)) is not None:
        raise AssertionError('an uncaused output appears without the incoming ship')
    if STATION<=at200:
        raise AssertionError('unexpected recovery: this recipe is supposed to be one-shot')
    return {'rule':'B3/S23','input':'LWSS from above, traveling down at c/2',
            'output':'LWSS traveling left at c/2','at_generation':200,
            'additional_output_solo_lwss_travel_verified_through_g':240,
            'one_shot':True,'station_reusable':False,
            'persistent_infrastructure_initial_cells':19,
            'input_cells':9,'source_ablation_prevents_output':True,
            'full_phrase_or_7_row_corner_qualified':False,
            'spurious_glider_cleanup_qualified':False}
