"""Moving LWSS karaoke: phrase trains, blank timing gaps, reusable eater bank.

Seven font rows plus a separate START/STOP cue row each end in an actual
7-cell Life eater-1. No runtime cell insertion, no camera-defined motion.
The cue ships are physical markers, NOT a qualified color switch.
"""
from __future__ import annotations
from dataclasses import dataclass,asdict
from .core import evolve,place,parse_rle
from .lyric_font import GLYPHS

LWSS=frozenset(parse_rle('x = 5, y = 4, rule = B3/S23\nbo2bo$o$o3bo$4o!'))
PITCH=8
CUE_ROW=-16
EATER_1=frozenset(parse_rle('x = 4, y = 4, rule = B3/S23\n2o$obo$2bo$2b2o!'))
# An exact D4 rotation of eater-1: consumes a leftward LWSS at (0,0)
# and returns to precisely the same seven cells by generation 40.
EATER_LEFT=frozenset({(-23,-3),(-22,-3),(-22,-2),(-22,-1),
                      (-21,0),(-20,-1),(-20,0)})
ROWS=(CUE_ROW,0,8,16,24,32,40,48)
EATERS=frozenset().union(*(place(EATER_LEFT,0,y) for y in ROWS))

@dataclass(frozen=True)
class PhrasePlacement:
    phrase:str
    left_x:int
    right_x:int
    blank_space_cells:int
    gap_g:int
    glyph_ship_count:int

def glyph_origins(text,*,x=0):
    out=[]
    for i,ch in enumerate(text.upper()):
        if ch not in GLYPHS:raise ValueError(f'unsupported character: {ch!r}')
        for row,bits in enumerate(GLYPHS[ch]):
            for col,bit in enumerate(bits):
                if bit=='1':out.append((x+PITCH*(6*i+col),PITCH*row))
    return tuple(out)

def initial_world(phrases=('WE MADE','A WINDOW'),*,gap_g=192,with_markers=True):
    """Return one preloaded B3/S23 universe and exact phrase placements."""
    if gap_g<0 or gap_g%4:raise ValueError('gap_g must be a multiple of 4')
    if not phrases:raise ValueError('at least one phrase required')
    world=set(EATERS);placements=[];last_right=None
    for phrase in phrases:
        local=glyph_origins(phrase)
        if not local:raise ValueError('empty glyph phrase')
        left=0 if last_right is None else last_right+6+gap_g//2
        positions=glyph_origins(phrase,x=left)
        right=max(x+4 for x,y in positions)
        if with_markers:positions=positions+((left,CUE_ROW),(right+8,CUE_ROW))
        ships=set().union(*(place(LWSS,*xy) for xy in positions))
        if ships&world:raise AssertionError('overlap in initial Life seed')
        world|=ships
        blank=0 if last_right is None else left-last_right-1
        placements.append(PhrasePlacement(phrase,left,right,blank,gap_g,len(local)))
        last_right=right
    return world,tuple(placements)

def expected_clearance_g(placements):
    return max(p.right_x for p in placements)*2+96

def qualify(phrases=('WE MADE','A WINDOW'),*,gap_g=192):
    """Check the whole B3/S23 universe against eight separate row evolutions."""
    whole,placements=initial_world(phrases,gap_g=gap_g)
    lanes=[]
    for y in ROWS:
        sites=[]
        for p in placements:
            if y==CUE_ROW:sites.extend([(p.left_x,y),(p.right_x+8,y)])
            else:
                sites.extend((x,by) for x,by in glyph_origins(p.phrase,x=p.left_x) if by==y)
        lanes.append(place(EATER_LEFT,0,y) |
                     set().union(*(place(LWSS,*point) for point in sites)))
    if set().union(*lanes)!=whole:raise AssertionError('incorrect initial decomposition')
    init_population=len(whole)
    end=expected_clearance_g(placements)
    for g in range(end+1):
        if whole!=set().union(*lanes):
            raise AssertionError(f'inter-row interference at native generation {g}')
        if g<end:
            whole=evolve(whole);lanes=[evolve(l) for l in lanes]
    if whole!=set(EATERS):raise AssertionError('uncleared ships or reaction debris')
    if evolve(set(EATERS))!=set(EATERS):raise AssertionError('eater not stable')
    return {'rule':'B3/S23','phrases':list(phrases),
            'glyph_ships':sum(p.glyph_ship_count for p in placements),
            'native_start_stop_marker_ships':2*len(placements),
            'eater_rows':len(ROWS),'eater_cells':len(EATERS),
            'initial_population':init_population,'generations_replayed':end,
            'final_population':len(whole),'reusable_eaters_restored':True,
            'exact_native_row_independence':True,
            'placements':[asdict(p) for p in placements],
            'cue_markers_operate_color_switch':False,
            'song_timing_qualified':False,
            'whole_universe_extinguished':False}
