# Physical glider fanout reaches an existing lip tile

**Status:** finite-horizon B3/S23 qualification of one causal connection,
not end-to-end musical lip synchronization. This experiment deliberately
retains the existing character and full seven-word first-line physical karaoke.

## Hypothesis and alteration

The existing 84-cell catalyst duplicates **one preloaded input glider**.
The output paths are placed so that, at native generation 340, they coincide
exactly with two previously independent five-cell gliders: a construction
glider belonging to the *first original WE glyph pixel*, and an erasure glider
belonging to `lower_medium_0`, one of the actual singer's lower lip tiles.
Those two original gliders are removed, replaced by the split output. One
additional final eraser is rerouted to avoid the new pathway and restore the
original later lip sequence. All other original glider mechanisms are retained.

The portrait is translated `(1071, -1019)` Life cells so that the branch
reaches the glyph without crossing protected portrait artwork. The shared
controller and seven lyric words are in one initial B3/S23 world at a
constant **192 generations per music second**.

## Direct causal test

Run exactly the same Life seed **with** and **without** that single input
glider (all other cells, including catalysts, remain identical):

| Native generation | With input | Without input |
| --- | --- | --- |
| 2156 (~11.229s) | Original WE letter pixel alive | Letter pixel absent |
| 2312 (~12.042s) | Existing lower-medium lip tile erased | Lip tile remains alive |
| 2456 | Original lip tile reconstructed | Independent baseline only |
| 2554 | Lip tile erased as original schedule demands | Independent baseline only |
| 2578 and 3068 | Original dynamic portrait restored plus catalyst | Not asserted beyond ablation window |

The observation is taken from live 2×2 Life block occupancy, not a
presentation label or an inferred score. The control signal's two observed
outputs show real causal dependence on the one source glider. There is a
**156-generation (~0.81s) lag** from the first glyph onset to this lip
response; this is *not* yet accurate word-by-word mouth timing.

## Collision and preservation qualification

- Verified exact two-output glider equality at generation 340.
- Native Life source-on evolution checked through generation **3068**, and
  source-off evolution through **2350** (plus checkpoints at 2156/2312).
- Stationary portrait art has **5,796 original live cells**, unchanged, and a
  two-cell forbidden collision halo around all art is checked against the
  complete dynamic singer evolution through g3068.
- Bridge's measured native Life bounding box plus a four-cell reserve is
  disjoint from the certified paths of the other **360** seven-word glyph
  pixels by a conservative minimum clearance of **405** cells.
- The exported RLE's **12,588** initial live cells parse back to exactly the
  same original relative coordinates and have no overlapping seed roles.
- Source-on at g2578/2700/3068 exactly equals the former original singer
  dynamic state plus the stable catalyst (no glider debris).

These are finite-horizon tests and component-clearance arguments, **not** a
45,000-generation exhaustive replay of the full song.

## Reproduction

```bash
python -m unittest tests.test_physical_lip_splitter_bridge -v
python -m life.export_physical_lip_splitter_bridge \
  --out patterns/first_line_physical_lip_bridge.rle \
  --report output/first_line_physical_lip_bridge.json
python -m pip install 'Pillow>=10,<13'
python preview/render_physical_lip_bridge.py
```

The optional preview `preview/real_lip_shared_signal_ablation.png` provides
*camera enlargement only* around the original lip tile, showing the source-on
and source-off native Life results. The RLE is authoritative, not the image.

## What is **not** claimed

1. Not a fanout to all lip tiles or the complete singer's three lip contours.
2. Not yet a 403-word physical coupling for the full song.
3. Not a substitution of the already-rendered independently timed first-line
   singer footage with this new causal controller.
4. Not exact musical synchronization of all three mouth modes.
5. Not a compact full-song lyric layout; only this **one connection** has been
   routed with collision-free physical Life gliders.

The next engineering gate is to multiplex more independent original lip
gliders, while preserving causal ablation, portrait clearance and the
three-state mouth recovery sequence. Only then should a combined causal
singer video replace the independent-stage demonstration.
