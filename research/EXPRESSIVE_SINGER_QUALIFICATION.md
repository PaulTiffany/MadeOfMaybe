# Expressive singer — B3/S23 mouth, no permanent teeth

## Why this iteration exists

The symmetric 40-signal singer had a **permanent 9-block central line**. That line was useful as a closed-mouth cue, but it remained visible *inside* the MEDIUM and OPEN apertures and read like stiff teeth. This iteration gives the central line **real glider-driven on/off behavior**, adds two naturally oscillating iris glints, and renders the active Life lip cells with a more readable horizontal camera aspect.

## Physical apparatus

- **Mouth contours:** exactly the symmetric upper/lower glider banks from `life/symmetric_full_mouth.py`, unchanged: 7 MEDIUM and 13 OPEN independent targets, each reflected top-to-bottom (40 controlled output blocks overall).
- **Closed lip:** 5 2×2 still-life blocks at x = -16,-8,0,8,16; y=49. Each starts present, is destroyed by a real glider collision at generation 98, and reconstructed by 2 incoming gliders at generation 800,800,812,932,908, respectively. The reactions are genuine B3/S23, not frame edits.
- **Eye glints:** two independent period-2 blinkers, deliberately placed in opposite phases at (-44,-122) and (+44,-122). They coexist with the original facial still lifes and all signal traffic.
- **Other scenery:** the existing speech bubble, words and pulsar, unchanged and still inside the SAME Life world.

## Correct sequence for THIS actual initial universe

| Generation | Visible mouth state | Central line |
| ---: | --- | --- |
| 60 | CLOSED (pursed band) | present |
| 180 | MEDIUM | absent |
| 288 | OPEN | absent |
| 420 | MEDIUM | absent |
| 540 | BREATH (neutral, not closed) | absent |
| 680 | OPEN, direct return | absent |
| 778 | BREATH (neutral, not closed) | absent |
| 960 | CLOSED, mechanically rebuilt | present |

**Limitation:** this is NOT yet a full seven-event CLOSED/MEDIUM/OPEN/CLOSED sequencer. In particular, the short middle close at g540 is a neutral absence, because safe glider restoration at that interval was not found. We must qualify earlier restoration/re-erasure routes or adjust the music's breathing choreography before saying arbitrary 3-state commands are supported. This is genuine physical progress rather than a simulated substitution.

## Visual presentation caveat

The preview employs a 1.52:1 horizontal pixel aspect, optical blur/glow derived only from *actual live lip cells*, and dim color for in-transit signal gliders. Camera styling does **not** alter the B3/S23 rules, introduce synthetic mouth cells, or remove moving machinery from the actual universe. The RLE preserves exact lattice coordinates and square cells when opened in Golly.

## Verification

`tests/test_expressive_mouth.py` checks all 980 generations of the complete union and independently evolving components, including protected fixed face/bubble and both period-2 eyes. Checkpoints assert that the five lip blocks are absent in active states and physically restored by generation 960. It also checks that the eye glints are true period-2 Life oscillators.

Run:

```sh
python -m unittest tests.test_expressive_mouth -v
python preview/make_expressive_mouth.py
```

Outputs:
- `patterns/expressive_singer_glider_performance.rle` — **complete** initially seeded, one-world Life performance.
- `preview/expressive_glider_singer.gif` — accelerated observation of genuine computed generations.
- `preview/expressive_mouth_contact_sheet.png` — six genuine checkpoints, colorized for presentation.
- `preview/expressive_singer_bubble.png` — one actual open-state universe with the unmodified bubble.

## Next engineering requirements

1. A reliable g540 close **and** subsequent re-open with no signal-route interference, or a musically acceptable score that avoids such a reversal.
2. Refit the visible mouth geometry/controls to a shallower, wider natural oval in the actual cell coordinates, not only by camera projection.
3. Map audio to legal control-event generations, then requalify the complete, audio-specific starting world.
