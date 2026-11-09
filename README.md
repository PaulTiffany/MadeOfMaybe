# Made of Maybe

A music video experiment using **actual Conway's Game of Life (B3/S23)** and glider-controlled animation synchronized to the song.

## First tested result

An initially present train of gliders alternately creates, erases, and recreates a stable two-by-two block, using Luke Kiernan's 2023 high-clearance toggle. A rudimentary face built of stationary Life blocks is in the **same simulation**; everything advances at the same constant rate. There are no imposed edits, reseedings, or animation frame swaps.

**This is a mouth-control proof, not yet a convincing singing face or a controllable Smiley oscillator.**

Read [research/LIFE_SINGER.md](research/LIFE_SINGER.md) for research and limitations.

Run with Python 3.10+ and no dependencies:

    python -m unittest discover -s tests -v
    python -m life.export_pattern > singer_three_pulses.rle

Open the RLE in [Golly](https://golly.sourceforge.io/).

Source attribution: [Luke Kiernan's glider-to-block safe toggle (2023)](https://conwaylife.com/wiki/Glider_to_block).
