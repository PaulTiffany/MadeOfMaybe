# Denser glider-controlled Life mouth — qualified composition

This extends the working but sparse four-pixel-per-state prototype by 15 more
independently routed glider channels. Native B3/S23 lower lips are now
**10 MEDIUM** and **13 OPEN** 2x2-block pixels, with 53 permanent upper-lip
blocks. The fixed Life-cell face, unchanged speech bubble and text, and
period-3 pulsar are part of the same initial universe.

## Verified

- Seven actual mouth checkpoints in one continuous simulation: G60 CLOSED,
  G180 MEDIUM (10 switched blocks), G288 OPEN (13), G420 MEDIUM (10),
  G540 CLOSED, G680 OPEN (13, direct skip), G778 CLOSED.
- All gliders are included at generation zero. Each block is synthesized by
  two colliding gliders or erased by one; no playback cell insertion or deletion.
- Every one of 785 actual composed generations is compared against the union
  of all 28 independently evolved components (23 actuated bank pixels and five
  non-actuated art components). Exact equality is required.
- The unchanged bubble and letters are merely repositioned closer to the
  singer; composition is requalified after that placement change.
- Candidate route selection checks state *at each cue checkpoint*, not merely
  that all injected gliders eventually disappear.

## Limits

The outlines are denser but still dotted, not a smooth aperture. Some signal
gliders remain visible inside the lower half of the face. This is a verified
fixed-score glider choreography, not yet a reusable interactive switch or
an audio-timed performance. New timings require solving routes again and
replaying the whole composition. The existing contact sheet/GIF is **not**
synchronized with Suno's audio.

## Reproduce

```sh
python -m unittest discover -s tests -v
python -m pip install Pillow
python preview/make_dense_mouth.py
```

The preview script writes `patterns/dense_three_state_singer.rle` for
Golly plus `preview/dense_mouth_three_states.png` (G60/G180/G288),
`preview/dense_mouth_glider_control.gif`, and
`preview/dense_singer_bubble_stage.gif` showing the **same** live board.

References:
- https://github.com/MartinSA04/GameOfLifeText
- https://conwaylife.com/wiki/Glider_to_block
- https://conwaylife.com/wiki/Bistable_switch
