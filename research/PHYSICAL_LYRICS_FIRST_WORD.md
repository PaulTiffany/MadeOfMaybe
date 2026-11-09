# A real glider-written lyric — first physical word

**Evidence:** The **35 lit glyph pixels of `WE`** are all genuine 2×2 B3/S23
still lifes, each synthesized by two pre-positioned gliders and later
**completely erased by a third glider**. The word is not a caption overlay,
a bitmap inserted by the renderer, or a single progress lamp.

This is a proof of the *text actuator*, **not yet production karaoke**.

## What happens in the actual Life universe

| Event | Generation | 24-generation/s clock | Reality |
|---|---:|---:|---|
| Glider traffic already present | 0 | 0.000s | 105 input gliders, 525 live cells |
| First 2×2 letter block complete | 220 | 9.167s | first visible physical pixel |
| All 35 glyph blocks present | **268** | **11.167s** | `WE` completely legible |
| Suno-aligned start of `We` | — | **11.224s** | alignment source, 57ms after completion |
| Suno-aligned end of `We` | — | **11.479s** | **not** physically met by eraser |
| First letter block erased | 374 | 15.583s | gradual deconstruction starts |
| Entire word cleanly erased | **442** | **18.417s** | zero remaining cells, all gliders consumed |

**Key limitation:** The word writes on during a 48-generation (~2-second)
pre-roll, and removal lags the vocal end by **6.94 seconds**. This is **not**
word-level timed karaoke yet; it demonstrates safe activation and erasure of
an actual entire word with no renderer intervention. Our prior seven-word
pilot still provides more accurate timing for **lamps**, not the letters.

## Geometry, source and composition

- Source letters: existing project's `life/lyric_font.py`, full **5×7** font.
- A glyph pixel is 4 live Life cells, arranged as a **2×2 block**. `WE`
  has **35** such pixels, or **140** visible Life cells when complete.
- Pixel pitch **20** actual Life cells is deliberately spacious to keep
  glider approaches independent; appearance is visibly sparse at raw scale.
- MAKE: two phased gliders synthesize each block; method comes from
  [GameOfLifeText](https://github.com/MartinSA04/GameOfLifeText).
- ERASE: one phased glider consumes the block leaving no debris.
- 35 independently routed components / **105 real control gliders**.
- Inputs are **all in the initial condition**, not injected at the event time.
- At every single tick **0..480**, actual full-word evolution equals the union
  of each individual pixel's independent evolution; no crosstalk.
- The existing singer, bubble and pulsar are retained unchanged in the
  exported combined universe, with WE spatially separated as its **own
  lyric stage**, not yet written inside the original speech bubble. Two
  groups' spatial separation is checked every tick **0..480**. This stage
  isolation is intentional: existing bubble outlines intercept incoming
  gliders if the signal grid is simply moved inside them.
- `data/we_physical_glider_routes.json` records every launch schedule and
  orientation. `life/native_lyric_word.py` interprets the data without a
  procedural animation or event-time world edits.

The preview contains two views of the **same native Life simulation**:
**raw** shows every live cell including control gliders; **display-enlarged**
expands a detected stable 2×2 Life block into one larger on-screen square.
The second view is cosmetic magnification of actual observed Life cells,
not a physical pixel-dense Life lettering layout.

## Reproduce

From repo root, Python 3.12+:

```sh
python -m unittest tests.test_native_lyric_word -v
python -m life.export_native_lyric_word > patterns/native_we_glider_written_world.rle
python -m life.export_native_lyric_word --word-only > patterns/native_we_glider_only.rle
python -m pip install Pillow
python preview/make_native_word.py
```

The full-world `.rle` contains the complete g0 singer + static bubble + symbolic stage,
including all of the distant incoming text-control gliders, and can be loaded
in **Golly**. Nothing in the renderer touches the Life universe.

## Next engineering problems — evidence-driven

1. **Throughput:** optimize two-glider construction/erasure packing so a
   readable word can be made and removed at the actual start/end timestamps,
   not over several seconds. Many dense gliders collide, so a single toggle
   doesn't magically switch a whole word. Consider a native high-clearance
   glider synthesis planner, fewer-pixel typefaces, or block-to-letter
   multiplexing; measure performance rather than assume capacity.
2. **Bubble ingress:** route signals around/through controlled apertures in
   the original speech bubble; maintain noninteraction of the face/border.
3. **Full lyric sequence:** score several real words in one initial universe,
   then do page reuse. Only after this is qualified should we map the song's
   articulation to the existing three-state mouth.
4. **Art direction:** close the pitch-20 visual spacing through better Life
   geometry or a clearly disclosed optical magnification pass.

A deterministic but **greedy** clearance-search tool for new words lives in
`research/route_native_word.py`. It was used to reproduce all 35 selected
WE construction routes from the source manifest, with explicit recovery
checkpoints for the slower eraser stage. It makes no guarantee that arbitrary
phrases or pixel pitches can be packed.
