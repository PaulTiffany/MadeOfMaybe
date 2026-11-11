# Made of Maybe: causal lyric-to-mouth glider fanout

## Goal and scope

The user requested **no phonemization, no separate mouth timing mechanism**:
the existing karaoke word-onset triggers must also drive the singer's
**CLOSED / MEDIUM / OPEN** states. The music remains at its fixed original
speed; the single Life clock is **192 generations per audio second**.

This commit qualifies a **physical four-word controller demonstration**
using the existing Suno-to-Life onset generations. It does *not* claim the
full 403-word Life karaoke has been merged with all 40 lip control tiles.

## Actual Life splitter, not duplicated Python scheduling

Topology: the stable glider duplicator documented at
https://conwaylife.com/wiki/Glider_duplicator (76×53 RLE, stable 74/75/78+
example). The published demonstration contains two input gliders, plus a
six-cell transient. Isolating the relevant 84 **stationary catalyst** cells
makes a clean, unchanged, idle splitter. We then place one **input glider**
per chosen word event.

- With no input, the 84-cell apparatus is an exact still life (`F(A)=A`).
- With one input, after 340 generations, the entire native Life state is
  **exactly** the original 84 catalysts plus **two outgoing gliders**;
  their coordinates and phases are asserted in `tests/test_lyric_mouth_fanout.py`.
- After 400 generations a second input glider produces another two outputs
  with the catalyst hardware unchanged. This is a reusable circuit.
- For each word, one branch participates in **real two-glider block synthesis
  for one lyric pixel** (second glider preloaded). The other branch either
  constructs a mouth control block (second glider preloaded) or cleanly erases
  a mouth control block. No cells are drawn, pasted, or inserted at runtime.
- The four events are on separated prepositioned routes; their final combined
  B3/S23 world is checked *per generation*, not assembled from snapshots.

## Physical event schedule — no new musical clock

The four onsets are taken **directly** from the full-song karaoke compiler's
first four `WordPlan.make_g` values. There is no independent mouth score.

| Song word | Appearance g | Audio position | Mouth action | State after action |
|---|---:|---:|---|---|
| WE | 2156 | 11.229 s | erase C bit | MEDIUM |
| MADE | 2204 | 11.479 s | construct O bit | OPEN |
| A | 2272 | 11.833 s | erase O bit | MEDIUM |
| WINDOW | 2296 | 11.958 s | reconstruct C bit | CLOSED |

Initial state: **CLOSED**. The register uses exactly two stable Life blocks:
`C` present means closed; neither present means medium; `O` present means
open. This is a *genuine 3-state physical port register*, not a pictorially
complete facial mouth. The C and O port origins are deliberately separated
by `(100,20)` cells to allow four independent signal paths.

One source glider per event is first positioned far upstream of an unchanged
splitter. At generation `trigger_g` it reaches the splitter's standard input.
Both branches then fly to their assigned word/mouth target, arriving on the
same actual audio onset (mouth erasure completes +2 Life generations, i.e.
10.4 ms after its paired word). The splitter's different preflight offsets
are *physical flight distances*, not a second clock.

## Strong causal controls

The complete world starts with **390 live cells** (4×84 catalysts, 4 input
gliders, 6 other preloaded synthesis partner gliders, and one mouth C block).
After generation 2296 the exact world holds **356 live cells**, comprising
4×84 preserved catalysts, the reconstructed C block, and four word pixels;
there is **no signal debris**.

The critical ablation tests each remove **only one source input glider from
the initial condition**. In all four cases *both* the corresponding lyric
block and mouth transition fail, without deleting any preloaded synthesis
partner. This is evidence of **physical causal splitting**, not two unrelated
timed reactions.

## Inspection and reproducibility

```sh
python -m unittest tests.test_lyric_mouth_fanout -v
python -m life.export_lyric_mouth_fanout \
  --out patterns/lyric_mouth_shared_splitter.rle \
  --manifest output/lyric_mouth_shared_splitter.json
pip install Pillow
python preview/make_lyric_mouth_fanout.py
```

- `patterns/lyric_mouth_shared_splitter.rle`: generation-zero universe to
  evolve directly in Golly, using B3/S23.
- `output/lyric_mouth_shared_splitter.json`: exact four physical route designs
  **plus full-alignment shared word-onset intent** on GitHub; local fixture
  fallback produces only 14 intent events if the full Suno file is absent.
- `preview/lyric_mouth_shared_fanout.gif`: diagrammatically arranged native
  Life-cell **port observations** from one uninterrupted simulation. The
  typography, layout, time labels, and lamps are presentation, not extra Life
  cells. The four lyric ports are **one pixel per word, not full letterforms**.

## Next integration steps, honestly delimited

1. Use the source word gliders that already construct karaoke glyphs; replace
   at least one glyph input per word with a splitter output, then route the
   other output to the singer. This pilot deliberately uses four independent
   lyric pixels instead of rewriting the very large full-song RLE.
2. Repeatedly fan out from event signals into **all real lip contour pixels**
   of the existing styled singer; don't substitute the two-port register for
   a visually expressive mouth. Physically certify clearances and reaction
   order in the combined singer + lyrics universe.
3. Derive gap/line-end closures from **karaoke line-clear events** (rather
   than authoring independent rest timestamps) and handle potential C→O
   two-bit jumps. Current full-song intent list simply repeats M→O→M→C at
   each word onset and is **not yet a qualified full-song Life circuit**.
4. Keep the speech bubble deferred until the unified lyrics/singer controller
   is qualified, as requested.

This is a working **causal splitter / shared timing primitive** and an
end-to-end four-event state cycle. It is not yet a full-song singing face.
