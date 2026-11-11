# Compact complete WE: physically staggered 35-turner native-Life verification

The original full moving WE proof used 35 one-shot vertical-to-left
LWSS turning stations with horizontal pitch 80 and glyph row pitch 64.
The earlier seven-row compact test showed that a very close two-column
checkerboard collided. It did NOT establish that a 35-turner word could
use those exact tight clearances.

We actually tested 35 complete turning fixtures, not just the station
bounding boxes, and checked their independent native B3/S23 evolution.

- With 36-cell negative x progression, output traffic struck neighboring
  still-untriggered stations at generation 2091.
- With 36-cell positive x progression, row pitches 18, 24 and 32 still
  produced interactions at generations 3386, 3521 and 3682.
- With 36-cell positive x progression AND 36-cell glyph row pitch,
  the combined native universe evolved with NO unintended cross-component
  interactions at every generation through g6000.

35 initial vertically arriving LWSS patterns are paired with 35 real
one-shot turners. Each has two real glider-debris eaters. Seven shared
left-side eaters receive the resulting moving seven-row lettering.
No source spaceships are injected after g0. The camera is not involved in
assembly. Station x-origin span drops from 2720 to 1224 Life cells, and
the 7 glyph-row origin span shrinks from 384 to 216 cells.

# Phase arithmetic

For each illuminated 5x7 glyph pixel (column,row), assigned ordinal i:

    station_x = 300 + 36*i
    station_y = 36*row
    target_x = 1 + 36*column
    target_y = 12 + 36*row

Our physically qualified corner produces a 12-cell LWSS phase with
minimum output x coordinate -43 at generation 200. Delay its incoming
down-moving LWSS by shifting it 2k cells farther upstream, where

    k = (target_x - station_x + 43 + (6000-200)/2) / 2

All 35 k values are nonnegative integers. The output formation at g6000
contains 35 separate live LWSSes (420 moving Life cells) arranged as WE.
Since LWSSes all move left at c/2, the assembled text remains moving
rather than becoming static dots.

# Exact qualification

The existing independent C++ native-Life checker simulates the g0
union and each of 36 independently seeded physical components through
g6000, comparing the two representations at EVERY generation. It then
continues the single native world through g7600.

Clean main world:
- g0: 1,519 native live cells.
- g6000: 959 cells, EXACTLY the expected 420 moving word cells plus 539
  stable eater cells.
- g7600: EXACTLY 539 cells = original 77 seven-cell eaters. No moving
  spaceships, debris, or additional still lifes.

The single-source-ablation run physically removes one nine-cell initial
input and no other hardware:
- g0: 1,510 cells.
- g6000: 966 = 34 outgoing LWSSes, eaters, plus untriggered 19-cell corner.
- g7600: 558 = same 539 eaters plus that untouched 19-cell station.

Both simulations verify full-world noninteraction until g6000; the final
worlds are exact stationary Life patterns. Source code and Golly RLEs,
route manifests and certificates are produced by the focused CI workflow.

# Scope and next work

This is the complete 35-pixel first word WE, physically compacted and
qualified. It is NOT YET the complete 403-word song or a repeatable
one-shot corner: all 35 stations are consumed in the reaction. The row
eaters are reusable. Continuing requires word/phrase signal scheduling,
turner recycling or spare stations, and clearance checks for successive
passing words and shared highlight/mouth signals. An all-zero finale
also needs deliberate dismantling of the 77 remaining eater structures.

The 14s preview is accelerated native Life observation, not music timing.


## Extension: the same geometric compiler assembles WE MADE

The identical station x-pitch 36 and glyph row pitch 36 also assemble
both words WE MADE, as one physically moving 107-pixel seven-row text train.
No separate per-word stage or optical text rendering is introduced.
The word spacing is inherited from the same 5x7 Life glyph vocabulary.
For this longer phrase, 107 real turning stations are preloaded and fired
at staggered native generations to coincide at g6000. An exact whole-world
native Life audit compares all 108 independently evolved components at
EVERY tick from g0 through g6000 without interaction.

The WE MADE populations in a separate certified native run are:
g0 = 4,543; g6000 = 2,831 (1,284 moving LWSS-phase cells + 1,547 eater
cells); g10000 = exactly 1,547 stable eater cells. A single source-ablated
word-pixel run likewise passed g0 through g10000: 4,534 -> 2,838 -> 1,566,
the latter including the unchanged 19-cell unactivated turner.
The word must travel farther to its left eaters, hence g10000 cleanup
rather than g7600. The fixed horizontal pitch is already sufficient
for a physically spaced phrase, but its two words do not yet have
separately qualified song onset / highlight timings. Reuse of each
individual turner remains unimplemented.
