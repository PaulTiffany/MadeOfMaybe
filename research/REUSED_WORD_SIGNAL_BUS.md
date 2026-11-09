# Two sequential lyric cues through one physical Conway splitter

**Sprint scope:** a time-multiplexed native-Life cue *anchor* for two successive
song lines. This is a positive compact-control result, **not** compaction of
all 23,057 song glyph tiles, and not completion of 403 word-to-mouth routes.

## Problem with the old layout

The full-song text-only world uses widely separated physical line stages.
The second line's first pixel was over 10,000 cells from the fixed singer,
beyond even Life's generation-zero causal cone at its scheduled generation
2976 (`life.causal_layout_limit`). We cannot attach a single shared physical
source to the singer without changing that arrangement.

## What is now physically qualified

The first two sung lyric lines both start with **WE**, aligned at 11.224 s
and 15.499 s. At 192 native generations/audio-second, their first word
completes at generations **2156** and **2976**. Their line-clear events
are **2578** and **3402**.

`life.reusable_word_cue` reuses the *exact same physical location (0,0)* for
the first 2×2 pixel of both words. It also uses the *same* stable 84-cell
Conway glider duplicator, excited by **two** preloaded gliders 820 ticks
apart. The second input is placed 205 cells upstream along the same glider
track, so its travel phase reproduces the already-qualified first output
geometry. This is a physically reusable catalyst, not an injected signal or
an independent mouth clock.

The two outputs of each duplication feed one source-glider path to the same
word-pixel sink, while the other path remains available for expression
wiring. The first one is already causally coupled to an original lower-lip
tile. The second expression branch is **not** connected to an actual lip tile
in this milestone; a trial of constructing a second lip pixel failed when
its partner glider collided with the existing character motion. This failed
routing is **not** included as qualified code.

A single unchanged B3/S23 initial condition constructs and erases the pixel
**twice**:

| Generation | Real native Life observation |
|---:|---|
| 2156 | First lyric pixel physically ON |
| 2578 | First line erase; pixel OFF |
| 2976 | Second line physically ON at the **same location** |
| 3402 | Second line erase; pixel OFF |

The target is never repositioned, and there are no runtime cell edits.
Source ablation is causal: removing input 1 blocks the first construction;
removing input 2 blocks the second construction. **Important:** removing the
first source leaves an uncancelled partner glider which can disturb the later
erase. The complete-source universe is clean, but the ablated universes are
not independently qualified for cleanup. The first event's *existing* real
lip ablation result remains separately certified by the prior sprint.

After the second clear, the 114-cell input pattern has exactly **94** live
cells: the original **84** stable duplicator cells and **two moving 5-cell
gliders**. This is not silent debris—those unconsumed fanout branches remain
live and should be terminated or used before integrating a complete film.

## Protecting the existing singer

`protected_character_certificate()` performs actual per-generation B3/S23
simulation, **3,403** sampled generations from g0 through g3402, containing:

- the existing multi-element singer's original control gliders;
- the original causal WE word pixel and lip tile;
- a second preloaded glider through the **same** splitter;
- the second WE pixel's independent partner and eraser gliders.

The **5,796 native still-life cells** of the character's hair, eyes, face,
and jewelry are unchanged. A two-cell Moore-distance guard is verified
against the entire dynamic world for every generation; the original lower
lip still appears, erases, rebuilds and resets at its original checkpoints.
This is a finite-horizon property of this fixture, not a general unlimited
reusable-bus safety theorem.

## Reproduce

```sh
python -m unittest tests.test_reusable_word_cue -v
python -m life.export_reusable_word_cue
python -m life.export_reusable_word_cue --with-portrait \
  --out patterns/two_line_reused_word_and_singer.rle \
  --report output/two_line_reused_word_and_singer.json
```

The two-line source fixture is `data/first_verse_alignment_fixture.json`,
corresponding exactly to the first two sung lines of the full Suno
alignment. GitHub CI exports the portrait-inclusive pattern and report.

## Next physical design gates

1. **Multiple lyric anchor tiles** at a common reused stage, screened with
   actual 2-cell spacetime clearance. Merely reducing the legacy pixel pitch
   from 1,600 to 8 fails native B3/S23 collision tests; visual camera scaling
   is not a substitute for physical routing.
2. Route the reusable splitter's *second* expression branch into an existing
   mouth element without collisions (and ultimately a three-state fanout).
3. Repeat the bus over all timed lyric events and prove clean downstream
   word erasure, expression transitions and shared-cause ablation across
   the song. Finally render with the original song and add the speech bubble.

**Current guarantee: two sequential real lyric anchors plus the intact
single original causal lip tile, not a finished synchronized singer.**
