# Native moving karaoke glyphs — first physical experiment

Each **illuminated pixel** of our existing 5x7 alphabet has been replaced with a genuine native B3/S23 **lightweight spaceship (LWSS)**. Each nine-cell spacecraft translates **two Life cells left per four generations**. At pitch eight, the entire glyph composition `WE MADE` (107 LWSS objects / 963 initial live cells) was evolved for **128 exact native generations** and remained precisely the union of its original separated ships, shifted left at c/2. No runtime insertion or position interpolation is involved. `tests.test_moving_lyric_train` has four focused tests.

This establishes a feasible **moving-letter primitive** and radically changes the possibility of a scrolling/crawling speech-bubble display. It does *not* establish a full 403-word conveyor or timing-fit, which must be analyzed separately.

## Concrete timing/packing constraint

The first WE and MADE word onsets occur **48 generations** apart. At LWSS speed c/2, this corresponds to only **24 Life cells** of longitudinal separation. A two-letter word **WE** at 8-cell glyph pitch occupies **93 Life cells** along the rail (before an additional guard). So one nonoverlapping linear word train cannot make both words pass the *same fixed read head* exactly at their word onsets at this physical scale. A lone giant 403-word line with gaps for silence cannot bypass the width-versus-speed constraint.

Options worth testing: keep an **independently timed highlighting read-head** over a scroll that can span multiple simultaneously displayed words; allow separate parallel lanes; use smaller/denser independently qualified ships; or change display design so a word is not required to fit entirely between consecutive onset marks. Phrase gaps can be encoded as larger track spacing without difficulty.

## One physical control switch vs video colors

Standard B3/S23 is binary: there are no innate RGB cells. A physically controlled **switch** can route an incoming spaceship stream between two lanes, replace a ship with a different coded pattern, or block it. The camera can then **color by lane/pattern**, but these are observational colors, not physical Life state. A single switch can control every ship that subsequently *passes through it*; it cannot instantaneously recolor every spaceship already distributed across the universe. Note that the technical Life term *glider color* means checkerboard parity, not rendered RGB.

**Open gate to qualify:** one reusable word-cued switch affecting the passing ship stream, clean non-destructive signal reset, source ablation, phrase-level blank spacing, and a single camera over the singer + moving typography. The finale must destroy/consume all outbound movers, not leave them escaping to infinity.

Reproduce: `python -m unittest tests.test_moving_lyric_train -v`.
