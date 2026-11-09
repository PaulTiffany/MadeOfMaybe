# A complete seven-word native-Life karaoke line (no speech bubble)

**Actual B3/S23 integration proof, 9 Nov 2026.** The full first sung line,
**WE MADE A WINDOW / OUT OF SAND**, is synthesized word-by-word as **361
independent native 2×2 stable blocks**. Two gliders build each block and a
third erases it: **1,083 input gliders**, all present at generation zero.
No live cell insertion, font overlays inside the Life substrate, runtime
pause, or time-varying universe clock.

The soundtrack plays at its normal tempo; this Life universe advances at
**192 generations per *audio second***. Life generation rate is distinct
from the video frame rate. Every word is physical, not a timed signal lamp.

| Lyric | True Suno onset (s) | Life completion (g) | Physical appearance (s) | Error (ms) | 2×2 pixel blocks |
|---|---:|---:|---:|---:|---:|
| WE | 11.224 | 2156 | 11.229 | +5.167 | 35 |
| MADE | 11.479 | 2204 | 11.479 | +0.167 | 72 |
| A | 11.824 | 2272 | 11.833 | +9.333 | 18 |
| WINDOW | 11.964 | 2296 | 11.958 | −5.667 | 96 |
| OUT | 12.593 | 2416 | 12.583 | −9.667 | 42 |
| OF | 12.909 | 2480 | 12.917 | +7.667 | 30 |
| SAND | 12.968 | 2488 | 12.958 | −9.667 | 68 |

The complete first line is still present after generation 2488 and fully
erased by generation **2578 = 13.427s** (seven milliseconds after its
13.420s final word end). Earlier words stay on the screen as subsequent
words arrive: **accumulating karaoke**, rather than erasing each word at
its tiny 0.1–0.5s aligned token end. Glider erasure begins shortly before
its *completion* generation and may nibble at blocks before 13.427s.

## Certifying independence: conservative space-first approach

The earlier 35-pixel WE router had trouble extending its glider travel paths
for a faster global clock: the same pitch-20 lanes physically collide. We
therefore proved a deliberately spacious alternative for all seven words:

- Choose a single phase-compatible 2-glider MAKE pattern and a clean
  1-glider ERASE pattern for each pixel, at the appropriate fixed generation.
- Prove all seven unique word reaction templates independently using exact
  B3/S23 evolution across 2578 generations and verify no debris remains.
- Over the same finite interval, each individual signal circuit remains
  within **647 Life cells** (L∞ norm) of its output pixel.
- Keep physical pixel origins at **pitch 1600**. Any two origins differ by
  at least 1600 in x or y. Thus their occupied component boxes are separated
  by at least **306 empty-cell coordinates** in one dimension across this
  entire sequence — far outside Life's one-cell interaction radius.
- This is a finite-run mathematical *noninteraction certificate*; arbitrary
  reprogrammed routes require requalification.
- Finally, the **whole 5,415-cell initial universe** was actually advanced
  from generation zero through 2578. Every word's entire 5x7 block mask
  appeared exactly at its recorded cue. There were **zero living cells** at
  g2578. A test reproduces this full-world run.

The word stage has **two native Life rows** (not a renderer-only line break).
Output-camera pixels are *optically magnified projections* of physically
present 2×2 stable blocks. This is explicitly a visual presentation step,
not an attempt to claim the display has the same spatial scale as the huge
physical Life world. It does **not** add the missing letters or switch any
Life cell at render time.

## Crucial boundaries and next research steps

This is a **whole lyric line**, not yet the full 238.88-second song.
The pitch1600 world is extremely spatially extravagant; making the text
small enough for a practical shared stage, minimizing glider travel lanes,
and scaling to many lyric pages is still work. The speech bubble is not part
of this experiment, by design. The singer, eyes, and mouth are also omitted:
their glider events must be rescored to this new global rate before
qualification in a shared universe. We have deliberately **not** made
any phoneme claims.

The next engineering target is to repeat the same on-beat physical lettering
for the *second* sung line and then build a reusable lyric-line scheduler that
reuses/clears caption stages without crosstalk. Once full text is qualified,
rescore the singer and finally position the bubble.

## Reproduce

```bash
python -m unittest tests.test_first_line_karaoke -v
python -m life.export_first_line_karaoke \
 --manifest output/first_line_karaoke_192_manifest.json \
 > patterns/first_line_karaoke_192.rle
python preview/make_first_line_karaoke.py
```

The `.rle` can be opened directly in Golly; all gliders are seeded at g0.
