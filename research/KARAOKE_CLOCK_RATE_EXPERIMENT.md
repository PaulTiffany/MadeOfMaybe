# Faster Life universe, original-speed music — lyrics first

## Correction to project plan

The speech bubble is **not** part of the karaoke engineering gate. We will
finish the actual, physically switched lyric words first, and only then route
around a bubble. Similarly, the existing singer/mouth geometry is not running
in these high-rate isolated lyric experiments until its signals are rescored.

Music playback remains at 1×. Each final Life universe must still run at **one
constant rate** throughout; the global constant is now configurable, in
**Life generations per audio second**, independent of encoded video fps.

Increasing the rate by k compresses an unchanged N-generation collision
sequence from N/24 seconds to N/(24k) seconds. To put its output at the
*same musical time* its initial glider launch locations must be backstepped
by the correct phase-compatible number of generations. **Simply playing the
existing RLE faster would also make the mouth sing early.** Mouth signals
must likewise be scheduled at `round(k*g_old)` before being qualified again.

## Native text signal test: the genuine 35-pixel word WE

- Source: actual connected Suno word alignment: WE starts at **11.224 s**.
- WE completes at generation **2156** at **192 Life gens/audio-second**,
  physical time **11.229 s** (onset error +5.17ms).
- First glyph pixel appears at g2108, **10.979 s**, giving a **250ms**
  instead of 2000ms construction window, with **no renderer cell insertion**.
- We hold the complete word on screen until the **line ends (13.420 s)**,
  instead of erasing at the word's 11.479 s end. This is a reasonable
  progressive karaoke style and avoids implausibly fast repeated erasures.
- Whole word is erased by **g2578 = 13.427 s** (+7.1ms after line end).
- A glider erasure already begins slightly before its nominal *completion*
  generation, so no claim is made that all 35 blocks remain until g2510.
- The verified preloaded glider construction remains a real 35-component,
  105-glider B3/S23 performance, and all signals vanish cleanly after erasure.

| Life rate | Physical pixel pitch | Construction spread | Erasure spread | Complete WE | Clear line | Verification |
|---:|---:|---:|---:|---:|---:|---|
| 24 | 20 | 2.000 s | 2.833 s | g268 | original erase g442 (18.417s) | historical source only |
| 48 | 80 | 1.000 s | 1.417 s | g540 (11.250s) | g646 (13.458s) | **B3/S23 PASS** |
| 96 | 80 | 0.500 s | 0.708 s | g1076 (11.208s) | g1290 (13.438s) | **B3/S23 PASS** |
| 192 | 160 | **0.250 s** | **0.354 s** | g2156 (11.229s) | g2578 (13.427s) | **B3/S23 PASS** |

`tests/test_lyric_clock.py` runs every generation through each line clearance
(and 16 generations beyond). It checks `F^g(union components)==union F^g(components)`
for every tick, the output's 35 true Life blocks at the target timestamp,
and *zero* live residue after the clear. It does not merely inspect a planned
schedule or project an overlay.

**Important finding:** Extending a glider's approach path can introduce
collisions that did not occur in the original valid 24-rate world. Reusing
the original pitch-20 positions at 96 causes crosstalk immediately; we
verified it. Respace the text's physical still-life pixels to increase
collision-free routing room, then **requalify** in the full simulator.
This particular proof uses pitch 80 at 48/96 and 160 at 192; these are not
minimum pitches and do not establish arbitrary word/caption scaling.

## Next actual deliverable

Compile all **seven words in the first sung line** (WE MADE A WINDOW OUT OF
SAND) at one chosen Life rate, using independent physical text regions and
no speech bubble. Keep words visible as each next word arrives, then clear
the line. Verify glider crosstalk and complete glyph state at every onset.
Only then generate the rest of the karaoke score; later independently rescore
the singer's mouth, eye and brow ports. The audio never changes speed.

At the end, introduce a stable bubble border *after* finding certified
signal corridors. The bubble is a presentation element, not a timing gate.

## Reproduce

```bash
python -m unittest tests.test_lyric_clock -v
python -m life.export_clocked_text --gps 192 --pitch 160 \
  --manifest output/clocked_we_192.json > patterns/clocked_we_192.rle
python preview/make_clocked_word.py
```
