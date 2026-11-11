# Reusable G-to-LWSS bank: native source/sink proof and song-slot feasibility

Status: **bounded native hardware test; full 3:58.88 movie NOT built.**

The user requested genuine B3/S23 hardware, smaller native letters, and
independent Suno-aligned word/vocal sources; not renderer-selected animation.

We reuse the published Luke Kiernan (2023) 105-cell G-to-LWSS catalyst
and its already qualified westbound reflection (see
`research/REUSABLE_LWSS_2023_QUALIFICATION.md`). We position our existing
seven-cell fishhook `EATER_TEXT` at translation (+32,+24) so each westbound
LWSS is consumed. Per lane the **105 catalyst + 7 eater = 112 stable cells**
are left intact. This is not a new converter invention.

## Bounded actual Life proof

A single g0 B3/S23 world includes **3 lanes at 200-cell pitch, 8
188-generation-separated gliders per lane** (24 actual incoming gliders).
It starts with **456 cells**, is compared to the union of independently
evolved physical lanes at **every generation g0 through g1700**, and
ends with **exactly 336 stable cells**: the original three 112-cell
catalyst/eater assemblies and nothing else. Exact westbound 12-cell
LWSS readouts appear in all three lanes at g200. In the counterfactual
where the *first glider in lane 1* is omitted at g0, that lane's g200
output disappears, the others remain, and the full world still resets
exactly to the same 336 stationary cells. No per-frame injection, glyph
sprites, or lip animation is used.

A four-input bank was additionally checked offline; the checked-in
reproducible test uses the longer eight-input stress case. No claim is
made that 188 generations is a mathematically minimal safe spacing.

## Full song timing compiler (NOT full native routing proof)

`life.reusable_lwss_bank.full_song_schedule()` reads the original 403
Suno-aligned sung words and converts each 3×4 glyph lit cell to one
native converter activation request. Every requested onset is already
phase-locked to **192 Life generations/second**. A deterministic
earliest-available interval scheduler assigns each request to a
converter lane with **at least 188 generations between that lane's
successive incoming gliders**. It can materialize all original gliders
as disjoint **generation-zero** five-cell source patterns and checks
g0 cardinality (5 source cells per request + 112 station cells per lane).
Exact source counts and required lane count are machine-produced by
the CI JSON artifact rather than handwaved from average throughput.

**Crucial boundary:** in this stage the known reliable output fishhooks
*eat* the converted LWSSes. The source/sink array is intentionally
physically separate from the singer and words. The full-song slot
allocator guarantees only g0 source non-overlap, valid phase and
per-lane recovery scheduling; it does **not** establish all-generation
cross-talk freedom for the much larger constructed bank, letter-row
packing, word shaping, 403 words visibly moving inside one bubble,
feeding a native mouth with independent Suno V, or cleaning up the
singer/world to zero cells. The bounded 3×8 proof may not be promoted
to an unbounded 10,366-pixel result.

## Next constrained engineering steps

1. Qualify a physically routed alternative to the sink eater that
   preserves converter reuse **and** places westbound LWSSes in a compact
   visible 3×4 word, with collision checks through actual disappearance.
2. Connect a *real* W branch and independently measured V on/off
   source to the actual three-position mouth; verify holds, gaps, reset,
   and source ablations against one-world B3/S23 evolution.
3. Only then compile the full 403-word song and its shared continuous
   camera; original audio may be muxed without retiming, not rendered
   as simulated mouth or textual overlays.

Original converter citation: https://conwaylife.com/wiki/G-to-LWSS_(2023).
