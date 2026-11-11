# Physically actuated dual-input mouth bank — finite pilot

This sprint extends the earlier physical two-glider word/vocal AND
truth table into **real medium/open lip block states**, not simulated
mouth poses. The existing `glider_controlled_mouth.py` has a stable upper
lip, four source-controlled lower-lip blocks for MEDIUM and four different
ones for OPEN, with real native 2-glider block synthesis and glider block
erasure. We preserve those existing precise trajectories.

The pilot splits each 2-glider MAKE into an independently present
clock glider and a gated VOICE glider. No VOICE input means no moving
medium/open lip pixels. A separate WORD command produces a real,
single-block lip-accent using another native 2-glider synthesis, then
erases the block at a native generation (no renderer masking). There is
no per-frame injection of Life cells. All source gliders and erasers
exist at generation zero. Physical input ablation runs four native
B3/S23 source cases, verifying actual medium/open/word-accent cells.

At original native checkpoints for VOCAL=true:

  g60 CLOSED
  g180 MEDIUM (4/4 real native medium lip blocks)
  g288 OPEN (4/4 real native open lip blocks)
  g420 MEDIUM (4/4)
  g540 CLOSED (**KNOWN SUSTAIN GAP: not yet corrected**)
  g680 OPEN (4/4)
  g778 CLOSED

A WORD event independently creates and erases a physical accent block
at g180, including when there is no vocal signal. With BOTH input
sources, all original lip block banks and accent clear by g784: the
world returns to exactly the original 72 stable upper-lip cells. For
other source combinations, unmatched clock and erase gliders may still
travel through the world, and must receive real eaters before
integration. This is physical source conditioning, **not a complete
priority selector**. It demonstrates that no new large mouth shape is
necessary for coarse three-pose movement.

**Crucial limitations:**
- W and V in this fixture are synthetic Boolean source ablations.
- The actual real Suno isolated-vocals stem has been generated in the
  user's Suno library, but its audio bytes have not entered the local
  waveform analysis. No false "song-aligned" claims.
- This is a short fixed choreography, not a reusable live vocal
  oscillator with arbitrary note lengths, no correction of the g540
  silent gap, and no full 403-word scheduling.
- The original rounded-bubble singer and real word redirectors are
  **separate native universes**. Physical routing/fanout and
  collision audit of their union remain undone.
- No graphics program is authorized to choose singing mouth poses
  from the prototype score.

The next engineering objective is a repeatable and collision-cleared
vocal-gated cycling jaw with native word-accent priority; then rerun
actual isolated-vocal amplitude activity through it.

Sources: `life/dual_source_mouth_pixel.py`,
`tests/test_dual_source_mouth_pixel.py`.
