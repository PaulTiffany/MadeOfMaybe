# Reusable Conway source: two lyric events, two real lip actions

**Verified sprint, 2026-11-09.** One native B3/S23 84-cell glider
splitter now accepts two separately timed, preloaded input gliders. It drives
**the same lyric-pixel location twice** and the same singer's **two real lip
tiles** without a separate mouth clock. All 3,403 generations of the
portrait-protected two-line fixture are qualified. This is not yet a completed
three-state, 40-element mouth or a 403-word integrated film.

## Actual song events and reuse

The first two lines of the real Suno word alignment both begin with **WE**.
Their word onsets correspond to g2156 and g2976 at the global fixed rate
**192 generations/audio-second**. Each word's first pixel is the exact same
2×2 cell block at world `(0,0)`; it is physically created and erased in the
same Life universe on this schedule:

| Generation | Source and observed physical result |
|---:|---|
| 2156 | First `WE` lyric anchor formed |
| 2312 | Source 1's branch erases singer's **existing** `lower_medium_0` lip tile |
| 2578 | First lyric anchor erased |
| 2976 | Source 2's branch forms the **same** lyric anchor again |
| 3148 | Nearby second lip tile remains a native 2×2 block |
| **3152** | Source 2's branch **erases** that nearby lip tile |
| 3402 | Second lyric anchor erased |

The two incoming gliders are separated by 820 generations, with their
preloaded positions 205 cells apart along the same input trajectory. They
reuse one unchanged **84-cell** catalyst. No gliders, blocks or text are
inserted at playback time. Two clean outbound gliders remain when the
small anchor-only system finishes (84+10 = **94** live cells); the complete
source world has no unexplained debris in the measured horizon.

### Why the second lip tile works

A first attempt to construct an additional mouth tile from a second glider
partner FAILED because that partner crossed existing mouth machinery. That
proposal is excluded from the qualified pattern.

Instead, the second tile is **preloaded from generation zero**, eight Life
cells farther along the existing north-east erase-glider route: local singer
coordinate **(-72,46)**, eight cells northeast of the existing tile at
(-80,54). Source 1 is consumed when it erases the old tile, so it cannot
hit the second tile. When source 2 passes through the now-empty old tile
position, it continues and consumes the second tile at **g3152**. Thus the
second cue's *same physical glider* now causes both lyric construction and
one lip change. It is not a renderer opacity switch.

**Causal ablation:** removing input 2 prevents **both** the second lyric
pixel's construction at g2976 and the second lip tile's erasure at g3152.
Removing input 1 prevents the first lyric construction and first existing-lip
erasure. The source-1-absent counterfactual can leave an uncancelled partner
glider that interferes with later erasure; it is **not** a clean operational
fallback and is not misrepresented as such.

The new second tile is an *added, initially present* nearby real Life block;
it is not one of the original 40 independent lip routes. This still does NOT
actuate the entire Closed/Medium/Open contour.

## Protecting her face

`protected_character_certificate` runs actual B3/S23 updates from generation
0 through **3402** with the second physical mouth tile, second trigger, the
existing singer's dynamic mouth machinery, the actual glyph anchor, and
unchanged character art. A strict two-cell spacetime guard excludes all
collisions with the original **5,796 static singer art cells** (hair, eyes,
brows, face and jewelry). The first original causal lip's on/off/rebuild
checkpoints remain unchanged.

`two_lip_causal_certificate` separately evolves the source-present and
second-source-ablated universes to g3156, checking both lyric and lip
outcomes directly rather than inferring them from scheduled labels.

## Reproducibility

```sh
python -m unittest tests.test_reusable_word_cue -v
python -m life.export_reusable_word_cue --with-portrait --skip-long-replay \
  --out patterns/two_line_reused_word_and_singer.rle \
  --report output/two_line_reused_word_and_singer.json
python preview/render_reused_word_bus.py
```

GitHub Actions workflow `.github/workflows/reused-word-cue.yml` uploads the
portrait-inclusive Golly RLE and JSON certificate. All source pulses are
present at generation 0, at a constant GPS=192.

## Outstanding requirements for the full film

1. Reuse the **entire lyric font**, not just one physically anchored pixel of
   WE. The legacy full-song karaoke already builds all 403 words, but its
   per-line physical pitches remain huge and are optically projected. Lowering
   their pitch without re-routing causes real B3/S23 glider collisions.
2. Expand to an actual **three-state whole-lip fanout**, not two individual
   event-controlled tiles. The other original lip components remain separately
   preloaded and follow their previous verified fixed performance.
3. Qualify all 403 events in a single complete B3/S23 layout, render with the
   original recorded audio, and add the speech bubble only after the video
   works without it.

**Net result:** two sequential, causally shared word/lip actions in the real
character, through one reusable physical duplicator. It is a concrete
hardware integration advance with explicitly limited scope.
