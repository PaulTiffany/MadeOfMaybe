"""Timebase planning for *physical* Life karaoke, without the speech bubble.

Audio always runs at its recorded speed. One global B3/S23 universe advances at
``gps`` Life generations per AUDIO second. Changing ``gps`` is a composition
constant, NOT a variable rate during playback, and NOT frame interpolation.

Physical gliders must be rescheduled at generation zero for the new clock;
merely playing an existing RLE faster accelerates *all* existing scenes.

All word-block MAKE completions are g=0 mod 4; clean ERASE completions are
g=2 mod 4. We preserve these glider reaction phases when re-timing.
"""
from __future__ import annotations
from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP
from .lyric_cues import generation
from .native_lyric_word import (PixelRoute, routes, COMPLETE_GENERATION,
                               ERASED_GENERATION, AUDIO_START)
from .glider_controlled_mouth import BLOCK,block_make_at,block_erase_at,rotate
from .core import place


def nearest_phase(seconds:float, gps:int, residue:int)->int:
    """Nearest nonnegative g with g%4 == residue, using exact decimal math."""
    if not 0 <= residue < 4 or gps <= 0 or seconds < 0:
        raise ValueError('Invalid rate, time or 4-phase residue')
    raw=(Decimal(str(seconds))*gps-Decimal(residue))/4
    n=int(raw.quantize(Decimal('1'),rounding=ROUND_HALF_UP))
    return residue+4*max(0,n)


@dataclass(frozen=True)
class ClockPlan:
    gps:int
    start_s:float
    line_clear_s:float
    make_at:int
    erase_by:int
    make_shift:int
    erase_shift:int
    first_make:int
    first_erase:int

    @property
    def preroll_s(self)->float:
        return (self.make_at-self.first_make)/self.gps

    @property
    def erase_tail_s(self)->float:
        return (self.erase_by-self.first_erase)/self.gps

    @property
    def onset_error_s(self)->float:
        return self.make_at/self.gps-self.start_s

    @property
    def clear_error_s(self)->float:
        return self.erase_by/self.gps-self.line_clear_s

    def as_dict(self)->dict:
        return {key:getattr(self,key) for key in (
          'gps','start_s','line_clear_s','make_at','erase_by',
          'make_shift','erase_shift','first_make','first_erase',
          'preroll_s','erase_tail_s','onset_error_s','clear_error_s')}


def plan_we(gps:int, line_clear_s:float=13.42, start_s:float=AUDIO_START)->ClockPlan:
    """Reuse verified glider lanes, retiming construction and line-wide clear.

    Initial-condition routes remain unqualified until a full B3/S23 run
    verifies crosstalk and final erasure at the new rate. Allowing a word to
    **remain visible through the line** avoids demanding clean erase at the
    end of every 0.25-second sung token.
    """
    if line_clear_s <= start_s:
        raise ValueError('Line clear must follow word onset')
    if gps <= 0:
        raise ValueError('Life clock must be positive')
    new_make=nearest_phase(start_s,gps,0)
    new_clear=nearest_phase(line_clear_s,gps,2)
    make_shift=new_make-COMPLETE_GENERATION
    erase_shift=new_clear-ERASED_GENERATION
    old=routes()
    if min(r.make_tick+make_shift for r in old)<4:
        raise ValueError('Not enough lead-in for glider construction')
    if min(r.erase_tick+erase_shift for r in old)<22:
        raise ValueError('Not enough lead-in for glider erasure')
    # Basic temporal collision guard, NOT a substitute for sim qualification.
    if min((r.erase_tick+erase_shift)-(r.make_tick+make_shift) for r in old) < 26:
        raise ValueError('Erase arrives too close to construction; reroute')
    return ClockPlan(gps,start_s,line_clear_s,new_make,new_clear,
       make_shift,erase_shift,
       min(r.make_tick+make_shift for r in old),
       min(r.erase_tick+erase_shift for r in old))


def retimed_routes(plan:ClockPlan)->tuple[PixelRoute,...]:
    return tuple(PixelRoute(r.x,r.y,r.make_tick+plan.make_shift,
                   r.make_orientation,r.erase_tick+plan.erase_shift,
                   r.erase_orientation) for r in routes())


def pixel_seed(route:PixelRoute)->set[tuple[int,int]]:
    return place(rotate(block_make_at(route.make_tick),route.make_orientation)
               |rotate(block_erase_at(route.erase_tick),route.erase_orientation),
                 route.x,route.y)


def _respace(route:PixelRoute,pitch:int)->tuple[int,int]:
    if pitch<20 or pitch%4:
        raise ValueError('Testing only positive pixel pitches >=20 divisible by 4')
    if route.x%20 or route.y%20:
        raise ValueError('Original physical word is not on the pitch-20 grid')
    return (route.x//20*(pitch-20),route.y//20*(pitch-20))


def physical_components(plan:ClockPlan,pitch:int=20)->dict[str,set[tuple[int,int]]]:
    """Shift reaction corridors while keeping the original text pixel topology.

    Spreading target pixels may be necessary: extending glider approaches
    introduces *new collisions*, even when retiming math is phase-perfect.
    Source glyph art is unchanged; larger pitch only increases physical space.
    """
    return {f'WE_{i:02}':place(pixel_seed(route),*_respace(route,pitch))
            for i,route in enumerate(retimed_routes(plan))}


def physical_targets(plan:ClockPlan,pitch:int=20)->tuple[set[tuple[int,int]],...]:
    return tuple(place(BLOCK,route.x+dx,route.y+dy)
       for route in retimed_routes(plan)
       for dx,dy in [_respace(route,pitch)])


def physical_initial(plan:ClockPlan,pitch:int=20)->set[tuple[int,int]]:
    return set().union(*physical_components(plan,pitch).values())



def mouth_timing_targets(old_gps:int,new_gps:int)->dict:
    """Reference audio positions; input gliders STILL need to be re-routed.

    Port-specific arrival phases should be imposed when compiling the actual
    mouth controller; this list is a timebase contract, not a qualified RLE.
    """
    if old_gps<=0 or new_gps<=0:raise ValueError('positive clock rates only')
    from .glider_controlled_mouth import BANK_SCHEDULES
    return {bank:[{'action':act,'audio_s':tick/old_gps,
                   'target_generation':generation(tick/old_gps,new_gps)}
                  for act,tick in changes]
            for bank,changes in BANK_SCHEDULES.items()}
