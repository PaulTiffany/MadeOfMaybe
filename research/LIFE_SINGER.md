# Singer feasibility: signal-controlled mouth in B3/S23

## Target

One initial Conway Game of Life universe. Constant generation rate. Every mouth change is caused by Life's own interactions, with gliders placed to arrive on specific generations. No external changes to living cells, no variable playback clock, and no swapping animation frames.

## Verified preexisting mechanisms

- **Smiley**: Achim Flammenkamp's 1994 oscillator has 17 live cells and period 8, but oscillates continuously. There is **no verified pause/restart mechanism for Smiley** here. https://conwaylife.com/wiki/Smiley
- **Stop and restart**: glider/Herschel signals can become stationary memory until a second signal releases them. This is a technique for *signals*, not a proof of controlling Smiley. https://conwaylife.com/wiki/Stop_and_restart
- **High-clearance glider-to-block converter** (Luke Kiernan, October 2023): A glider produces a stable block; another appropriately separated glider on the same input lane removes it cleanly. The mechanism can toggle repeatedly. https://conwaylife.com/wiki/Glider_to_block
- **Bistable switch**: named SET and RESET inputs with robust state semantics can support a more sophisticated controller if required. https://conwaylife.com/wiki/Bistable_switch
- **Glider**: moves diagonally c/4, so moving a starting glider d cells farther along its incoming lane delays arrival by exactly 4d generations. https://conwaylife.com/wiki/Glider

## What is now tested, not merely proposed

The source RLE in life/singer_pilot.py contains the 2023 high-clearance glider-to-block converter. The pilot takes its initial glider out of the stationary apparatus and pre-places three gliders on one trajectory, spaced 48 cells along the northwest direction (192 generations apart). It adds eight harmless still-life blocks to mark two eyes, eyebrows, nose and face accents.

The entire universe runs as a **single** B3/S23 simulation; tests check:

| Generation | 2x2 mouth block at (11..12,14..15) |
|---|---|
| 170 | PRESENT |
| 362 | ABSENT |
| 554 | PRESENT |

By generation 575, everything has settled back to the exact original stationary apparatus plus **only** the mouth block. The two-glider test returns precisely to the original apparatus.

**No claim of photorealistic or even clearly readable mouth motion is made.** This is a true 1-bit actuator that can wait arbitrarily long for the next signal, not an 8-phase mouth oscillator.

## Musical clock and compute

For a fixed simulation rate R generations/second, a trailing glider offset d yields an event separation of 4d / R seconds, subject to device recovery. For the verified d=48 example at R=100, this is 1.92 s per toggle. A constant R is selected **once**; we do not modulate simulation speed to mimic singing.

The current source reaction settles approximately 150 generations after a glider at the demonstrated starting point. Calibrate the exact appearance/disappearance generation, then place all song-control gliders in the initial universe so that their arrivals match target lyric phrase boundaries. Faster syllabic articulation may require a faster *constant* rate, a smaller independently qualified switch, or multiple interacting circuits.

A sparse Python reference simulator suffices for this tiny test; Golly/HashLife are appropriate for larger sequences. The harder problem is geometric design of readable lips and routing signals clear of the portrait, not raw computation.

## Next build sequence

1. Design clear **open / closed** mouth still lifes using one or several safe toggle bits. Show actual Life evolution, not rendered geometry changes.
2. Route control lanes into the portrait without destroying eyes, hair, or facial still lifes. Validate exact reaction outcomes and recovery times. Do not assume independent parts can overlap.
3. Use Suno's *Made of Maybe* word timestamps to derive simple phrase-level ON/OFF events, not phonemes. Compile a glider launch constellation and verify the event generations.
4. Render ~8 seconds of the first chorus and compare mouth changes against actual audio.
5. Optionally explore an 8-phase signal-driven mouth. Directly pausing the existing Smiley is still unproved.

Source credit: Luke Kiernan (2023), documented on LifeWiki.
