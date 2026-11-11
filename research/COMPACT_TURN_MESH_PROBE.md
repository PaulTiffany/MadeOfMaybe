# Compact stagger test: how little expansion is necessary?

The user proposed replacing dense station packing with a simple checkerboard
stagger (X_X_X / _X_X_X), rather than a complicated timing network.

We tested **actual combined B3/S23 worlds** with seven independent copies
of our previously qualified 19-cell, one-shot vertical-LWSS-to-left-LWSS
corner. Importantly, the existing full **35-turner WE** in
`life/staggered_word_mesh.py` is preserved unmodified; this is a
deliberately smaller packing experiment.

| Candidate | Station row pitch | X layout | First cross-interference |
|---|---:|---|---|
| Dense stack | 8 | all x=0 | generation 1 |
| Alternating checkerboard | 8 | x=(0,-24,0,-24,...) | generation 1 |
| Expanded but aligned | 18 | all x=0 | generation 190 |
| **Small diagonal staircase** | **18** | **x=-36 per next row** | **none through generation 3200** |

The stationary turner occupies **17 rows** in its own y bounding box,
so a station pitch of 18 leaves only **one empty row** between successive
turners (before considering horizontal x separation). Rather than switching
only between two columns, the successful small test uses seven successive
horizontal station positions `0,-36,-72,...,-216`. That avoids
collisions between every pair, not just immediate neighbors.

## Time compensation: geometry itself is the timing

A down-moving LWSS travels c/2; each station 36 cells farther to the left
would otherwise have its output ship 36 cells too far left
at the target moment. Delaying the collision by 72 generations compensates. We therefore place its **initial vertical spaceship 36
cells farther upstream** (and similarly for successive stations). Each
one-shot collision occurs at a different real native generation, but all
seven outgoing ships align horizontally at **generation 800**.

At g800, all seven are genuine **12-cell LWSS phases** with exact x
interval **[-343,-339]** and y intervals starting at 12,30,...,120.
At g900 every ship has traveled exactly **50 cells left**, preserving
all seven rows. Exact whole-world evolution equals the union of seven
separate native B3/S23 worlds at **every generation through g3200**.
A seventh-source ablation leaves exactly six correctly aligned ships.

The horizontal `x=-36` offsets are small relative to the qualified
35-corner WE's previous **80-cell station pitch**. Importantly the
output-row **18-cell** pitch is still wider than the earlier raw
eight-cell LWSS font-row pitch; to preserve readable glyph proportions,
a full-word compact layout should adjust horizontal pixel pitch too.

## Not yet solved

This proves a **seven-row column of simultaneous moving pixels**, not
an entire letter or phrase. The stations are **one-shot**, leave
additional B3/S23 debris, and are not yet reusable. We have neither
the full 35-pixel train compacted at this tight clearance nor the
shared highlight switch and singer/mouth wiring. The user-proposed
simple stagger works in a **diagonal progression** for this seven-row
fixture; the literal two-column alternating checkerboard still collides.

Reproduce: `python -m unittest tests.test_compact_turn_mesh_probe -v`
and `python -m life.export_compact_turn_mesh_probe`.
