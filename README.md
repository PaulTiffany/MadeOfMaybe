# Made of Maybe — cellular-automaton music video

A music video assembled from native Conway's Game of Life (B3/S23) behaviors. The target is **one initial universe at one constant generation rate**: live pattern interactions, independent objects, and signals pre-placed to meet the musical score. No AI video generation or intermediate frame substitution.


## Full song — genuine glider-written karaoke (text-first)

The full-song compiler now treats **every sung line** in the 468-token Suno
alignment as a separately qualified Life stage, building **every word** with
preloaded two-glider block synthesis, then erasing the whole line with a third
glider per pixel. One fixed **192-generation/audio-second** clock, no
runtime insertion or variable simulation rate. The original recorded song
continues at its original tempo. The singer and speech bubble are deliberately
**not** in this full-song text-first RLE.

```bash
python -m unittest tests.test_full_song_karaoke -v
python -m life.verify_full_song_karaoke
python -m life.export_full_song_karaoke
python -m life.export_full_song_cues
```

GitHub Actions publishes the one full-song RLE, all word and line timings,
SRT, per-stage camera schedule, and reaction certificate in its artifacts.
The world is intentionally enormous and sparse; the presentation renderer
will magnify verified Live Life block outputs as glyph pixels. This is a
**qualified native-Life score**, not a finished 24fps karaoke video.
See [FULL_SONG_NATIVE_LIFE_KARAOKE.md](research/FULL_SONG_NATIVE_LIFE_KARAOKE.md).

## CURRENT — karaoke-first fast Life clock (speech bubble deferred)

The soundtrack stays at **normal speed**, but the *single constant* Conway
clock can be increased from **24 to 48 / 96 / 192 generations per audio second**.
At **192 generations/s**, the first genuine 35-block lyric word **WE** is
physically constructed over just **0.250 seconds**, finishing at **11.229s**,
within **5.2 ms** of Suno's **11.224s** word onset. We let the word **stay
visible until the line finishes**, then gliders completely erase it by
**13.427s** (target 13.420s). There are no renderer cell edits or overlays
inside the Life universe. The first 48/96/192-rate worlds pass real full
B3/S23 per-generation independence and completion/clearance tests.

**Important:** Retiming the original gliders at the same pitch produces new
cross-lane collisions. The verified first-word solutions use *more physical
space* between letter pixels (pitch 80 at 48/96, pitch 160 at 192).
This is not a minimum pitch and not yet a complete karaoke line. The new
fast-clock world deliberately contains **only lyrics**; the speech bubble is
postponed. The mouth will need a separate glider rescore (multiplying desired
musical times by the new constant rate) before reunion.

```sh
python -m unittest tests.test_lyric_clock -v
python -m life.export_clocked_text --gps 192 --pitch 160 > patterns/clocked_we_192.rle
python preview/make_clocked_word.py
```

See [rate experiment and limitations](research/KARAOKE_CLOCK_RATE_EXPERIMENT.md).
The old 24-gens/sec pilot is retained below as historical evidence.

---

## NEW — physical 5×7 lyric word made and erased entirely by gliders

We have gone beyond the seven correctly timed *lamps*. The first actual
5×7 Life word, **WE**, is now constructed and erased by **105 preloaded
B3/S23 gliders** (three per 2×2 glyph pixel). All **35 physical glyph blocks**
finish assembling by generation **268** (11.167s versus Suno's 11.224s
word onset). They persist as still lifes and are completely erased by
generation **442** (18.417s). The 35 routing subsystems pass an exact
**481-checkpoint** independent-evolution comparison, and the word remains
spatially independent of the existing character and speech bubble through
all 481 generations. The combined initial universe is Golly-exportable.

This is an **engineering pilot, not finished karaoke**: letter creation
begins ~2 seconds early; erasure is almost 7 seconds late relative to
Suno's end of “We.” The text is on a separate isolated Life stage so the
control gliders don't destroy the previously qualified bubble. The 5×7
render-preview optically enlarges only truly present 2×2 Life blocks;
a raw-cell view simultaneously shows all glider traffic. The next tasks
are to increase circuit packing throughput and route through the bubble.

```sh
python -m unittest tests.test_native_lyric_word -v
python -m life.export_native_lyric_word > patterns/native_we_glider_written_world.rle
python -m life.export_native_lyric_word --word-only > patterns/native_we_glider_only.rle
python -m pip install Pillow
python preview/make_native_word.py
```

See [physical-word qualification](research/PHYSICAL_LYRICS_FIRST_WORD.md).

---

## Lyrics-first alignment pilot (current active work)

The connected Suno source for *Made of Maybe* has **468 raw timing tokens**;
all are saved verbatim in `data/made_of_maybe_suno_alignment.json` on this
research branch, including three zero-duration anomalies. **We are doing text
before phonemes**: `life/lyric_cues.py` converts token/syllable fragments
into timed words, two-row (eight-character) caption pages, generation scores,
CSV, JSON and diagnostic SRT. `life/caption_library.py` exports each caption
page as native, stable B3/S23 blocks inside the **existing** speech bubble.
The GitHub lyric CI job exports the complete song's page library as Golly RLE.

The first physical synchronization proof is a real, constant-clock Life
universe (`life/lyric_text_pilot.py`): the singer, 5×7 caption
`WE MADE / A WINDOW`, unchanged bubble, and four separate glider-created
progress blocks for `WE`, `MADE`, `A`, `WINDOW`. The blocks turn on at
generations 268, 276, 284, 288 and are erased at 326 by real Life reactions.
The combined universe was checked against independent subsystems for **350**
consecutive generations. `life/lyric_text_scene.py` also places the remaining
**three** words OUT, OF, SAND in a *second physical caption page* within the
same Life universe; all seven progress blocks are native glider-controlled.
An actual double-rounding bug was corrected: OF now switches at generation
308 rather than 312. It does not replace subtitle letters yet, and the
blocks currently sit **right of the bubble**, to avoid invalidating routes.
No phoneme mapping has begun.

```sh
python -m pip install numpy scipy Pillow
python -m unittest tests.test_lyric_cues tests.test_caption_library tests.test_lyric_text_pilot -v
python -m life.lyric_cues --alignment data/made_of_maybe_suno_alignment.json --out output/lyric_cues/made_of_maybe
python -m life.caption_library --alignment data/made_of_maybe_suno_alignment.json --out output/lyric_cues/native_page_rles
python -m life.export_lyric_text_pilot > output/lyric_cues/first_lyric_glider_progress.rle
python preview/make_lyric_text_pilot.py
python preview/make_caption_library_preview.py
```

See [lyrics-first qualification](research/LYRICS_FIRST_QUALIFICATION.md).

---

## Character round 2 — wavy hair + glider-controlled eyebrow and iris

The new `life/character_round2.py` builds a much more deliberate singer:
shoulder-length asymmetric violet hair with separate curls, side-swept
bangs, highlight strands, fuller eyeliner/lashes, drop earrings, and a
high, mischievously arched right eyebrow. **Every visible cell is real Life.**

Six new glider-controlled elements give her actual expression without
replacing pictures: three blocks appear on the right eyebrow for the open
vowel, while three blocks in the left iris disappear and later reconstruct
for a brief squint/wink-like cue. The rest of the face, existing mouth
control circuits and original speech bubble remain independently arranged.
The eye *outline* does not physically shut, so the new iris wink is not
full eyelid animation. Lyrics still don't change during the simulation.

See `preview/character_round2_four_expressions.png` and
`preview/character_round2_real_life.gif`; inspect the complete generation-zero
universe in `patterns/character_round2_native_life.rle`.

```sh
python -m unittest tests.test_character_round2 -v
python -m unittest discover -s tests -v
python preview/make_character_round2.py
```

Full qualification and limitations: [CHARACTER_ROUND2_QUALIFICATION.md](research/CHARACTER_ROUND2_QUALIFICATION.md).

---

## Previous: oval face + expressive eyes + readable native-Life captions

A user-directed aesthetic update is implemented in `life/styled_singer.py`
and `life/lyric_font.py`. The old circle/Pac-Man silhouette is now a tapered
oval with a smaller ear/temple profile and chin; arched brows, almond eyes,
winged eyeliner, real period-2 iris glints, swept hair and nose/cheek marks
are **actual stable 2x2 Life blocks**, laid out to avoid every control glider
flight path across the exact 980-generation performance. The same moving
three-state mouth and centerline restoration hardware remain in operation.
The text in the existing bubble uses a fuller 5x7 Life bitmap font instead
of the earlier 3x5 stub, and the generator accepts alternate short captions.
**The caption is still static and the video is NOT synchronized to audio.**

Preview: `preview/styled_singer_four_states.png`,
`preview/styled_singer_native_life.gif` and
`patterns/styled_singer_glider_world.rle`. For repro:

```shell
python -m unittest discover -s tests -v
python preview/make_styled_singer.py
```

Qualification and known limitations: [STYLED_FACE_QUALIFICATION.md](research/STYLED_FACE_QUALIFICATION.md).

---

## Expressive singer — real moving centerline and twinkling eyes (latest candidate)

The **tooth-like permanent interior line is gone from active mouth poses**. Five actual Life blocks form a pursed CLOSED band; incoming gliders cleanly erase them by generation 98 and later reconstruct them (generation 800–932). The original symmetric MEDIUM/OPEN upper-and-lower glider contours remain independently controlled. Two small native period-2 eye oscillators add subtle autonomous motion without crossing any controls. The existing bubble/text and pulsar are unchanged.

The preview uses a **horizontal camera stretch and optical glow** to make the Life-cell shapes more legible. These are cosmetic presentation choices; the RLE has exact B3/S23 cells at their real coordinates.

**Important limitation:** the middle rests at generations 540 and 778 are currently **BREATH/NEUTRAL**, not a mechanically reconstructed CLOSED state. We genuinely close at generation 60 and reconstruct CLOSED by generation 960, with MEDIUM and OPEN transitions in between. The seven-event fully reversible controller is still the earlier symmetric version with its permanent central line; we have *not* yet combined both properties. The expressive prototype is not synchronized to audio.

```sh
python -m unittest tests.test_expressive_mouth -v
python preview/make_expressive_mouth.py
```

Inspect `preview/expressive_mouth_contact_sheet.png`,
`preview/expressive_glider_singer.gif`,
`preview/expressive_singer_bubble.png`, and
`patterns/expressive_singer_glider_performance.rle`. Full qualification and
limitations: [expressive singer research](research/EXPRESSIVE_SINGER_QUALIFICATION.md).

---

## Symmetric full-mouth study (previous)

`life/symmetric_full_mouth.py` makes **both the upper and lower lips move**:
the already qualified glider-controlled lower-bank circuitry is reflected
across the mouth's horizontal midline, giving symmetric MEDIUM/OPEN outlines
under one constant-rate B3/S23 simulation. Both eyebrows/eyes were moved into
verified clear flight corridors; the existing speech bubble, lettering and
pulsar are unchanged. The scene executes CLOSED → MEDIUM → OPEN → MEDIUM →
CLOSED → OPEN (direct skip) → CLOSED from preloaded gliders.

```sh
python -m unittest discover -s tests -v
python preview/make_symmetric_mouth.py
```

Inspect `preview/symmetric_mouth_three_states.png`,
`preview/symmetric_mouth_gliders.gif`,
`preview/symmetric_singer_bubble.png` and Golly-compatible
`patterns/symmetric_moving_lips.rle`. The 785-generation independence and
face-stability checks pass for this exact choreography.

**Honest limitation:** The short central CLOSED lip line is still permanent
and reads as teeth when the lips open. This stage is more symmetrical and
removes the stiff upper-lip contour but is **not a fully animated three-pose
silhouette**. It has not yet been timed to the audio; contours remain dotted.
See `research/SYMMETRIC_MOUTH_QUALIFICATION.md`.

---

## Denser stage composition (latest experiment)

`life/dense_glider_mouth.py` composes **23 independent glider-driven lower-lip
outputs** (10 for MEDIUM, 13 for OPEN) with a denser 53-block fixed upper lip,
the same stable face, existing bubble/lettering and pulsar. The bubble is
translated closer to the performer, but the design itself is unchanged.

One complete initial Life universe performs CLOSED → MEDIUM → OPEN → MEDIUM →
CLOSED → OPEN → CLOSED with direct skip. The combined stage and its individually
evolving components agree across all 785 generations. No cells are injected
during playback. The lip remains *dotted*; the presentation is not yet aligned
to the music.

```sh
python -m unittest discover -s tests -v
python preview/make_dense_mouth.py
```

See `preview/dense_singer_bubble_stage.gif`,
`preview/dense_mouth_three_states.png`, and the fully preloaded Golly pattern
`patterns/dense_three_state_singer.rle`. Qualification details in
`research/DENSE_GILDER_MOUTH_QUALIFICATION.md`.

---

## Operational mouth — glider-controlled three-state animation (new)

The working performer is now available as a **single initial B3/S23 pattern**
with genuine reversible transitions. This is not a sheet of three static
mouth pictures, and none of its changing cells are video overlays.

**Control sequence:** `CLOSED → MEDIUM → OPEN → MEDIUM → CLOSED → OPEN → CLOSED`.
The second `CLOSED → OPEN` is a **direct skip**; no medium frame is required.
Two-glider syntheses make stable lower-lip blocks, while single gliders erase
them cleanly. Incoming signals are all preloaded into the initial universe.
The singer face, original speech bubble/lyrics, and pulsar evolve together
without cross-component interference for 785 exact generations.

```shell
python -m unittest discover -s tests -v
python -m life.export_operational > patterns/operational_three_state_mouth.rle
python -m pip install Pillow
python preview/make_operational_mouth.py
```

Look for `preview/operational_mouth_glider_control.gif` and the
`operational_mouth_three_states.png`/`operational_mouth_closeup.png` previews.
The 6.7-KB compact RLE opens in Golly; the state snapshots occur at generations
60, 180, 288, 420, 540, 680 and 778. The face is near the RLE's original
coordinates, and the bubble is translated out of the control lanes.

**Scope:** This is a successful *preloaded glider choreography*, not yet a
polished full oval mouth or a general-purpose arbitrary-timing switch. Each
lower-lip state currently consists of four independently actuated blocks.
New score timings require routing and requalification; Suno timing is not yet
integrated. See [research/GLIDER_CONTROLLED_MOUTH.md](research/GLIDER_CONTROLLED_MOUTH.md).

---

## Initial composition pilot (historical)

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

## Earlier three-state static pose study (historical)

`preview/three_state_mouth_contact_sheet.png` compares **CLOSED, MEDIUM and
OPEN** mouths in the same stable face. All three are valid, persistent B3/S23
configurations built from 2×2 blocks, exported as individual RLE files under
`patterns/singer_mouth_*_stable.rle`. The current speech bubble/text compound
still composes independently with all three poses.

**Important:** This is a contact sheet of *three different initial universes*,
NOT a three-state signal-switched Life animation yet. Reversible and skipped
transitions were unimplemented in this earlier static prototype. The operational
glider-controlled states are now implemented above. Details: [three-state mouth research](research/THREE_STATE_MOUTH_CANDIDATE.md).

## Next refinements

The glider-scheduled seven-event demo now works; improve visual mouth density so MEDIUM and OPEN form continuous, legible arcs rather than four distinct dots per state. Then compile Suno phrase/activity timing into new glider placements. Each new score must requalify the full universe, including the speech bubble and lyric counterpoint.

See [research/LIFE_SINGER.md](research/LIFE_SINGER.md) and [research/COMPOSITION_PILOT.md](research/COMPOSITION_PILOT.md).

### Improved mouth candidate (still under visual review)

The original 2x2 block did not resemble a mouth. We added a genuine six-cell
**beehive** produced and removed by Mitchell Riley's glider-controlled
beehive factory, plus a tighter provisional emoji-like face. This produces
an open/closed/open aperture instead of merely blinking a block.

    python -m unittest discover -s tests -v
    python preview/make_beehive_face.py

View `preview/beehive_face_compare.png` (closed vs open with no debug labels),
`preview/beehive_face.gif` (real simulated generations), or open
`patterns/beehive_singer_with_bubble.rle` in Golly.

**The speech bubble is unchanged.** The new face and existing bubble/pulsar
have been independently qualified together for 610 generations. This
remains **draft artwork**, not yet an accepted singer or lip-sync.

---

## Lyrics-first milestone — 7 physically controlled word cues

Before mapping mouth articulation, the repo now captures the **complete Suno alignment** (`data/made_of_maybe_suno_alignment.json`, 468 raw tokens) and compiles a fixed-24-gens/sec *word timeline* and line-wrapped 5×7 Life-bubble text. The first 7 lyric words from **WE MADE A WINDOW OUT OF SAND** have glider-made progress lamps in one continuous, verified Life universe, spread across two independent still-life caption pages. A camera cut in the preview changes which page is shown; it does not add or remove Life cells. **The caption letters remain static** — progress lights, not the glyphs, are controlled. No phoneme inference has been attempted.

```bash
python -m life.lyric_cues --alignment data/made_of_maybe_suno_alignment.json --out output/lyric_cues
python -m unittest tests.test_lyric_cues tests.test_lyric_text_pilot tests.test_lyric_text_scene -v
python -m life.export_first_line > patterns/seven_word_glider_timed_captions.rle
python preview/make_lyric_text_scene.py
```

Inspect `preview/seven_word_native_life_cues.gif`,
`preview/seven_word_cue_contact_sheet.png`, the RLE, and
[lyric alignment qualification](research/LYRIC_ALIGNMENT_FIRST_PASS.md).
