# Controller relocation and narrower-mouth qualification (2026-11-09)

The latest user request is a **physical reroute**, not another camera relocation,
and a narrower, lower, cheek-preserving real-Life mouth. We did not silently
reinterpret this as a camera-only change.

## Physical transmission component

`life/physical_glider_relay.py` isolates a **49-cell stable Snark glider
reflector** (Mike Playle, 2013). One physical input glider produces one
90-degree reflected glider; it is not a gun that produces independent pulses.
Two preloaded inputs 820 generations apart reuse the same still-life hardware.
The exact B3/S23 replays through generation 920 have two clean outgoing
gliders, unchanged catalysts, and input-ablation controls. Three regression
tests cover this. **This is a qualified relay primitive, not complete wiring
to the singer.**

## Why moving the current splitter directly below the bubble is not enough

The established first sung `WE` has a native 2×2 pixel at **world (0,0)**
at generation **2156**. Its original splitter is near world **(508,-530)**,
and the exact output glider is at x≈454 by generation **340**. The
below-bubble proposal `SPLITTER_LOCAL_ORIGIN=(380,120)` would place the
corresponding output at x≈1397 at generation 340. An unassisted c/4 glider,
even after passive reflectors, can advance at most **454 cells per coordinate**
between g340 and g2156; x≈1397 to x=0 is impossible by this word deadline.
A reflector/extension cannot increase signal propagation speed. A glider
*gun* is also not a source-causal substitute.

Thus a real below-bubble controller requires **moving the physical lyric
pixel sink near the singer as well**, re-synthesizing its partner gliders,
and re-routing both split outputs into the lip bank. The bubble cannot merely
be another view of the old distant (0,0) sink if full physical co-location
is required. The current PR does **not** certify this end-to-end relocation.

## New actual-Life singer pose candidate

`life/refined_singer_candidate.py` preserves the original facial geometry,
brows, iris circuitry, and **nine of ten original cheek blocks**. Rather
than squeezing glider lanes closer together (which caused immediate native
B3/S23 collisions in exploratory tests), it:
- omits outer medium/open lip lanes, reducing the medium/open half-width to
  53/49 Life units (from up to 80);
- shifts the remaining lip/closed-line *physical circuits* down 32 Life cells,
  preserving their internal packet timings;
- removes only 33 pre-existing static art blocks whose two-cell spacetime
  exclusion zones would be violated; this includes one cheek block;
- checks independent moving channels for **980 exact generations**, checks
  real medium/open/closed-line occupancy, and verifies remaining static Life
  art and a two-cell guard against all moving routes.

**Scope limit:** the original connected `lower_medium_0` lip channel is
among the discarded outer channels. The earlier WE→lip physical bridge is
still preserved separately; it cannot be claimed for this alternative mouth
until a new word-sourced branch is physically wired and ablated. The g540
rest remains a BREATH, not a falsely certified CLOSED state.

## Next qualified integration gate

Place the reusable splitter beneath the bubble, move the first physical
lyric-pixel sink into that compact region, route both glider branches using
reusable Snarks/reflectors with phase-accurate flight times, and replace an
actual retained lip route in the refined face. Verify same-source ablation,
whole-body separation, signal reset, and Golly RLE replay before replacing
the legacy seven-word singer. Then extend to 403 word sources.
