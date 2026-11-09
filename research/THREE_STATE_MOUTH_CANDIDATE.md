# Three-state mouth geometry (visual candidate, not a circuit)

Three concrete, native B3/S23 still-life target poses which the singer can
hold indefinitely:

| Pose | Lip geometry | Centerline half-aperture (logical pixels) |
|---|---|---|
| CLOSED | Narrow horizontal band | 1 |
| MEDIUM | Shallow oval | 4 |
| OPEN | Tall oval | 8 |

The mouth corners and entire face are invariant across states. The mouth
is 23 logical pixels wide. Every logical pixel is a stable 2x2 block at
pitch 4, so **all live cells are genuine Life**.

The poses are **three different initial conditions**, not successive
frames of a single signal-controlled Life universe. Each is verified
stable and each coexists with the existing stable speech bubble/lyrics
and independently oscillating pulsar. No runtime cell updates or frame
swapping are allowed for the final animation.

Still UNSOLVED: glider-driven transitions between these three target
patterns (including reversibility and direct skips). A Callahan
bistable SET/RESET switch by itself does not automatically turn the
many mosaic pixels on and off. Need a certified actuation network, or
a smaller switchable set of mouth shapes.

Prior art:
- https://conwaylife.com/wiki/Bistable_switch
- https://conwaylife.com/wiki/Glider_to_block
- https://conwaylife.com/wiki/Toad
- https://conwaylife.com/wiki/Block

Reproduce:

    python -m unittest discover -s tests -v
    python preview/make_three_state_mouth.py

The preview script produces three individual Golly-compatible RLEs:
patterns/singer_mouth_{closed,medium,open}_stable.rle.
