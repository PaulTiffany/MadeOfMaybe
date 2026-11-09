# Symmetric paired lips and protected eyes

This is a **native B3/S23** visual experiment on the existing
MadeOfMaybe singer. It does not modify the speech bubble/text or pulsar.

## New mechanism
Two mirrored sets of the previously qualified glider circuits build and
erase both upper and lower contour pixels. The mirror is across y=50, a
symmetry of Conway's rule itself. All control gliders are present at g=0.

Seven MEDIUM targets and thirteen OPEN targets per half are used.
That is 40 independently preloaded control components. Both banks are
physically independent, verified against the real combined Life evolution
at **every one of 785 generations**, including a direct CLOSED to OPEN skip.

The face's eyes and brows were moved to the central corridor. Permanent
face cells are placed only outside a 2-cell margin around *all* moving
glider trajectories over the complete performance window. This is an
initial-layout computation, not a renderer mask.

## Important limitation
The short 9-block resting line is **not** glider-controlled and stays
visible as a teeth-like strip in the open mouth. The moving contour is
still dotted and rounder than the ideal visual. The test proves real
actuated upper/lower lips, not a completed natural mouth or audio lip-sync.

## Reproduction
1. python -m unittest discover -s tests -v
2. python preview/make_symmetric_mouth.py
3. Open patterns/symmetric_moving_lips.rle in Golly.

The script outputs a contact sheet of genuine G60/G180/G288 cells,
a review GIF, and a full stage still with the original speech bubble.
