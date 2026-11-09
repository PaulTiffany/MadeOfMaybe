# One continuous Life singer and physically written lyrics — first-line integration

## What has been built and directly verified

The existing visual character (long, layered hair, oval face, eyeliner and earrings)
is backstepped **in actual 4-generation glider phases** so its previously
qualified **multi-tile** lip animation falls over the first sung line of
*Made of Maybe*. We use the native lyric line-clear generation (2578 at the
fixed 192 generations/audio-second) as the **only score anchor**; the retiming
delay is `2578 - 490 = 2088` generations. The song is *not* sped up. We do not
separately generate phonemes or author an independent clock. The motion is one
fixed native Life choreography shifted to the lyric line, **not per-word mouth
selection**.

The first line's seven fully written and cleared words remain the **same 361
native 2×2 still lifes constructed/erased by 1,083 initially present gliders**.
The singer lives at X=-5000 and the lyrics at their original independent,
wide-pitch stage. Both coexist in **one seed RLE and one constant B3/S23
universe**. A **split-screen camera** displays them simultaneously, without
moving cells or modifying the Life state. Hair and features consist only of
initially seeded, stable 2×2 Life still lifes; static tiles whose 2-cell
Moore halo crosses retimed gliders are discarded **at construction time**.
This discards some facial detail but preserves the hairstyle.

The retimed dynamic seed has 255 valid c/4 gliders and static mouth elements.
Evolving this new world for 2088 generations recovers the *exact* original
unretimed performance seed. The subsequent 980-generation mouth sequence
therefore follows the previous qualified full-lip choreography. The safe
art is checked against every generated step through generation 3068.
We also calculate a conservative signal-propagation light cone against the
text's certified 647-cell target-route bound to establish **finite-horizon
spatial independence** of the two stages.

## What is not yet built

**The glider splitter has NOT been connected to the full lip banks.** The
four-word independent duplicator proof remains valid, but its output devices
and approaches interfere with the existing dense-mouth routes when placed
near the singer. In a direct retiming trial, the 390-cell bus and retimed
multi-block mouth diverged from independent evolution at **generation 435**;
even rotating one event's fanout hit portrait gliders at later generations.
This is a measured routing failure, not a reason to claim the apparatus works.
The current shared **score anchor** does not establish a shared **physical
signal**. The full song contains 403 compiled word cues, but only this first
line is qualified as a physically coexisting singer-and-lyrics performance.
No complete four-minute physically driven character has yet been built.

The next routing work should: (1) keep the hair/lip seed, (2) reserve glider
corridors for both dense lip banks and word-to-mouth fanout, (3) route and
ablate the first shared input at a real lip tile while preserving the rest
of the contour, (4) then compile line-by-line mouth transitions from the
song's **existing** word and line-clear events. Each combined full-universe
seed must be requalified under B3/S23; a renderer may never fake switching
by replacing mouth cells or selecting alternate initial worlds.

## Reproduction

```sh
python -m unittest tests.test_first_line_singing_character -v
python -m life.export_first_line_singer
python preview/render_first_line_singer.py
# Add --audio /path/to/song.wav to mux unchanged original recording (optional)
```

- `patterns/first_line_singing_character.rle` is the combined Golly world.
- `preview/first_line_singing_character.mp4` is a silent **4.5s** first-line
  film at 24fps; original song audio is not bundled.
- `preview/first_line_singing_character_contact.png` shows actual sampled
  Life cells, and `output/first_line_singing_character_report.json` records
  generation timing, initial size and spatial qualification.
