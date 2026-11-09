# Made of Maybe — character round 2 (glider-controlled facial expression)

The previous [styled singer](STYLED_FACE_QUALIFICATION.md) looked like a
thinly outlined face with sparse hair. This revision strengthens the portrait
without touching the already qualified upper/lower lip controller, bubble,
static title text, or pulsar.

## Actual new Life geometry

- **Wavy hair:** asymmetrical, side-swept bangs, expanded crown, multiple
  shoulder-length curls on both sides, highlight strands, and a few curls in
  the foreground. These are hundreds of real, stable B3/S23 2×2-block tiles,
  *not painted hair or a non-Life background*. Hair is independently stable.
- **Expression:** arched asymmetric brow artwork, stronger outer lashes,
  two little drop earrings, and eye glints (right eye retained).
- **Right eyebrow accent:** three separately routed glider packets synthesize
  an elevated three-block eyebrow accent by g288, hold it through g420, and
  erase it before g540. Gliders are in the initial universe. This is a
  **modest accent movement**, not a wholesale translation of the eyebrow.
- **Left eye iris wink:** three original permanent iris blocks were replaced
  with three native reversible block switches. The iris is present through
  g420, disappears by g540, and is reconstructed by g680. The eye outline
  **does not physically close**; this is a quick *iris-dimming / squint cue*,
  not a full blinking eyelid. The former periodic left glint is omitted.
- **Original glider mouth:** unchanged, including the limitation that the
  middle g540/g778 breath isn't a fully restored closed line. Only g60/g960
  are fully CLOSED with the current centerline apparatus.

## Native Life qualifications

The six new dynamic elements use the `block_make_at` (two-glider synthesis),
`block_erase_at` (clean one-glider deletion), and D4 orientation primitives
already independently tested in this repository. A routing search checked
full *980-generation signal trajectories*, not merely a cropped eyebrow or
face region. Static portrait blocks are fitted only where there is clearance
from every old and new glider trajectory. Whole-frame cell evolution is
then compared against the union of independent components across all 980
successive generations; the filter alone is not treated as proof.

All decorative features are native stable Life still lifes, the glints are
native oscillators, and mouth/brow/iris are changed only through preloaded
collisions. Cosmetic colors and camera framing do not modify Conway cells.

### Measured checkpoints

| Generation | Mouth | Elevated eyebrow accent | Left iris |
|---:|---|---|---|
| 60 | Closed | Off | Present |
| 180 | Medium | Off | Present |
| 288 | Open | On | Present |
| 420 | Medium | On | Present |
| 540 | Breath/neutral | Off | Absent (squint cue) |
| 680 | Open | Off | Present |
| 960 | Closed | Off | Present |

## Reproduce

```sh
python -m unittest tests.test_character_round2 -v
python -m unittest discover -s tests -v
python preview/make_character_round2.py
```

`patterns/character_round2_native_life.rle` contains the *entire* initial
Conway universe with all gliders and the existing static caption. The
preview contact sheet, GIF, and checkpoints are computed from actual Life
steps: `preview/character_round2_four_expressions.png`,
`preview/character_round2_real_life.gif`, and checkpoint PNG files.

## Still pending

- More natural flexible cheek/eyelid geometry and a **true eyelid closure**.
- Genuine full closed/medium/open state restoration at all musical rests.
- Full glider-synthesized karaoke rather than initial static `MADE OF MAYBE`.
- Compile Suno's word alignment into future glider trajectories and audio
  rendering; this isn't synchronized to the song yet.

This exact layout and timeline is qualified; **arbitrary new compositions
are not automatically independent**. Re-run tests after any geometry or
cue change.
