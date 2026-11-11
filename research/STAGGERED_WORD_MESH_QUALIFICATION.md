# Geometric staging: real native moving WE from above

This experiment is a **complete, physically validated moving word** in one B3/S23 universe, not an animated font or optical lettering.

We use the existing 5x7 alphabet for *geometry only*. Each of its 35 illuminated pixels in **WE** is a real nine-cell LWSS approaching vertically from above. Each hits a separately placed one-shot 90-degree converter (knightlife's 2009 beehive/boat/pond reaction), which emits a **left-moving LWSS**. The 35 converters are spread laterally by 80 Life cells, and their input ships are offset vertically to arrive at deliberately different times.

For font column c, row r, turner index i, pixel pitch 64, desired formation generation T=6000, station coordinates X=300+80i, Y=64r, and input vertical shift -2k, the exact four-generation phase equation is:

x(T) = X - 43 - (T - 200 - 4k)/2
y(T) = Y + 12
k = [1 + 64c - X + 43 + (T - 200)/2]/2.

All 35 k values are nonnegative integers. Therefore the more distant turns occur earlier and their emitted ships arrive in their proper **complete moving-word geometry at exactly g6000**. These are real spaceship cells, not printed glyphs. At generation 6000 all 35 outputs are the same 12-cell LWSS phase, leftbound at c/2.

### Important failed geometry and remedy

Our first unprotected WE mesh suffered a **real cross-signal collision at g5541**: a diagonal glider emitted from one turner collided with a legitimate pixel emitted from another. Distributing stations alone was insufficient.

Each one-shot converter emits **two unwanted diagonal gliders**. We qualified two additional stable eater-1 fishhooks per converter; these intercept both gliders before they threaten another lane. Seven further eater-1 fishhooks, **shared per lyric row**, consume the entire assembled moving word after it passes. Total long-lived hardware: 70 local diagonal eaters + 7 row eaters.

### Whole-universe native qualification

- 35 turners, 35 incoming vertically moving LWSSes, 70 glider eaters and seven row eaters; **1519 living cells at g0**.
- A separate compiled C++ B3/S23 implementation compares the whole world at **every single generation g0–g6000** with independently evolved physical components, checking for unplanned cross-component interference.
- At **g6000**, exact cell-set equality establishes **35 real 12-phase left-moving LWSSes spelling WE**, plus 539 stable eater cells. Total **959** live cells.
- The ships subsequently travel toward and are consumed by the **same seven row eaters**.
- At **g7600**, the entire world is **exactly 539 stationary eater cells** (77 original fishhooks, all recovered); no escaped spaceship or debris.
- Counterfactual: remove the final source LWSS (pixel ordinal 34). At g6000, exactly that pixel is absent; at g7600, the unused 19-cell converter survives alongside the same recovered 539 eater cells. Independent full-world checks and exact snapshot equality pass. This specific ablation is certified; not every arbitrary removed source is guaranteed collision-free.
- A 14-second **accelerated hardware-proof** MP4 uses actual positions from one native Life simulation; it is **not** synchronized with the original 192-generation-per-second song.

### Limits

The 35 right-angle converters are **one-shot** and consumed, not repaired/reused. The 77 eater structures survive and would require intentional clean removal for the requested whole-world nuke. This prototype certifies **one complete word** and its destruction into reusable row eaters—not a complete timed phrase conveyor, physical color/highlighting switch, singer mouth linkage, or the full 403-word musical production.

Next qualification gate: multiple words through staggered lanes with true source-aligned timing, sufficient new/reconstructed corner apparatus, and repeatably recovered shared row eaters. The geometry no longer requires placing a separate stationary glyph in each faraway space.

### Reproduce

Use:

python -m unittest tests.test_vertical_lwss_corner tests.test_staggered_word_mesh -v

python -m life.staggered_word_mesh

g++ -O3 -std=c++17 research/staggered_mesh_native.cpp -o mesh_native

mesh_native output/staggered_word_mesh/we_components.tsv 7600 output/staggered_word_mesh/we_final.tsv 6000 output/staggered_word_mesh/we_formation.tsv output/staggered_word_mesh/we_frames.bin

python preview/render_staggered_word_mesh.py --frames output/staggered_word_mesh/we_frames.bin

Full end-to-end, including one-source ablation and exact final world, is in .github/workflows/staggered-word-mesh.yml.

Original converter concept: https://conwaylife.com/forums/viewtopic.php?p=633
