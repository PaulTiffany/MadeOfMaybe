# Made of Maybe — cellular-automaton music video

A music video assembled from native Conway's Game of Life (B3/S23) behaviors. The target is **one initial universe at one constant generation rate**: live pattern interactions, independent objects, and signals pre-placed to meet the musical score. No AI video generation or intermediate frame substitution.

## Working composition pilot

The first **singer + speech bubble + lyric text + pulsar** scene is available. It contains:

- **Singer:** stable Life-block portrait scaffold (very rough, not a final character).
- **Mouth bit:** Luke Kiernan's 2023 glider-to-block toggle, with three preloaded control gliders that produce ON → OFF → ON.
- **Speech bubble:** stable block-built outline.
- **Lyric text:** stable Life-block bitmap text, currently “MADE OF / MAYBE”, not yet dynamically synthesized or karaoke-synchronized.
- **Symbolic counterpoint:** a native period-3 pulsar, spatially isolated from the others.

Each component advances under the same global B3/S23 clock. The tests compare the union of individually evolved components to the **actual composite universe at every generation for 610 generations** and verify that the actuator reaches a stable state after the final signal. This qualifies this particular scene and schedule, not arbitrary future compositions.

This is an **integration and feasibility proof**, not yet a convincing singer or an audio-synchronized video.

## Run

Requires Python 3.10+; the Life engine and tests need **no packages**.

```bash
python -m unittest discover -s tests -v
python -m life.export_pattern > singer_three_pulses.rle
python -m life.export_scene > singer_bubble_pulsar.rle
```

Open the `.rle` in [Golly](https://golly.sourceforge.io/). For presentation previews only, install Pillow:

```bash
python -m pip install Pillow
python preview/make_compound_preview.py
```

This produces a GIF, keyframes, a static contact sheet of four researched symbols, and the RLE under `patterns/`. The GIF is a visualization of genuine computed generations, **not timed to the audio**. Presentation colors and explanatory labels are overlays; Life cells and their evolution are real.

## Auditioned pattern sources

- [Glider-to-block safe toggle](https://conwaylife.com/wiki/Glider_to_block) — Luke Kiernan (2023).
- [Pulsar](https://conwaylife.com/wiki/Pulsar) — period 3.
- [Heart](https://conwaylife.com/wiki/Heart) — period 5.
- [Smiley](https://conwaylife.com/wiki/Smiley) — period 8; **no verified ability to pause it**.
- [Gosper glider gun](https://conwaylife.com/wiki/Gosper_glider_gun) — periodic emitter with unbounded output; **not yet qualified for composite placement**.

## Next step

Choose an aesthetically readable mouth geometry and map short lyric activity intervals from Suno to pre-positioned signal gliders. Then verify the resulting *combined* simulation before recording a chorus video. Every independently scheduled composition must declare an active spatial footprint, incoming/outgoing signal corridors, and time window.

See [research/LIFE_SINGER.md](research/LIFE_SINGER.md) and [research/COMPOSITION_PILOT.md](research/COMPOSITION_PILOT.md).