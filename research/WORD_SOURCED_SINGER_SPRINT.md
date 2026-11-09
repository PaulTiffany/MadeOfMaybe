# Singer integration: source-linked three-state score and causal first-line film

**Qualification scope (2026-11-09):** The first-line renderer reads the
actual physical glider duplicator that jointly controls a real WE letter pixel
and one previously existing lower-lip tile; the complete 403-word **intent**
score is sourced only from already verified karaoke word construction and
line-clearing generations. This is an incremental integration, not a claim that
every lyric event already controls every lip contour.

## A single control-score source

`life.word_driven_expression` compiles every lyric onset and line clear to
`closed`, `medium`, `open`, without phonemization, new pitch detection, or any
second clock. It uses the already compiled `make_g` and `clear_g` fields from
`life.full_song_karaoke`; no timeline independent of those karaoke events is
introduced. Each line starts medium, alternates open/medium for subsequent
words, and closes on the same native Life line-clear event. Repeated target
states are dropped in the concise intent; raw word events remain available.

**This is a target score, not hardware.** Some successive word cues are only
8 native generations apart in the local first-two-line fixture. Even a clean
block erasure takes 22 generations, so the visible full-lip contours cannot
simply be commanded at every word event without rate-adaptation and a new
collision-qualified routing design. The audit exposes sub-22/sub-48 gaps and additionally exports an
**uncertified 48-generation rate-limited candidate**. That candidate drops
changes it cannot satisfy without inventing any replacement event times;
its routes still require native B3/S23 qualification.

## The real first-line coupling video

`preview/render_causal_firstline_singer.py` evolves
`life.physical_lip_splitter_bridge.bridge_unit_seed` at **192 generations per
second** and observes its actual Life-cell state. It is **not** the prior
independently retimed `life.first_line_singing_character.dynamic_seed`.
The video makes the original single WE glyph pixel conditional on its physical
block occupancy. The singer's mouth tile is read from the same causal world;
the other real mouth tiles evolve under their previously qualified gliders.
The rest of the 360 native first-line glyph pixels use the existing certified
optical camera sampler (those pixels are not inserted by the renderer).

One glider input supplies **one lyric pixel + one lip element**. Deleting that
input removes both physical outcomes at checkpoints, as tested by
`tests.test_physical_lip_splitter_bridge`. The proof does not establish
phonetic articulation, all lip tile fanout, or 403-word physical coupling.

The video is **silent** unless `--audio /path/to/MadeOfMaybe.wav` is supplied.
Audio is not resampled or time-stretched. The output clip shows 10.93–15.43s
of the original song's timeline; it is not a finished four-minute film.

## Reproduce

```shell
python -m unittest tests.test_causal_firstline_camera tests.test_word_driven_expression -v
python -m unittest tests.test_physical_lip_splitter_bridge -v
python -m life.export_word_driven_expression --alignment data/made_of_maybe_suno_alignment.json
python preview/render_causal_firstline_singer.py --out preview/causal_firstline_singer.mp4
```

GitHub Actions runs full-alignment assertions and uploads the 4.5-second
physical-causal proof video as an artifact. The full word alignment file is
tracked by the GitHub branch; local fixture-only checkouts may not have it.

## Two-level REAL glider fanout: one input → four outputs

A second, separate B3/S23 hardware experiment now proves that the stable
84-cell duplicator can be cascaded. Place two additional duplicators directly
on the two *physically produced* first-stage outputs, with phase-matched
orientations. One initial glider and **252 stationary catalyst cells**
produce **four independent five-cell output gliders by generation 683**.
No runtime signal is ever inserted. Actual B3/S23 simulation validates
three stable catalyst banks, four moving gliders, and no extra debris.
Source ablation leaves only the stable catalysts. The exact exported Golly
pattern is `patterns/one_to_four_word_glider_splitter.rle`.

**Scope:** these four outlet gliders are not yet routed to the complete
character's lips; this is the missing fanout *capacity* primitive rather than
a claim of four causally actuated lip tiles. Additional phases, reflected
branches and protected routes need clearance tests before using the outputs.

## Next gate (not bypassed)

Increase the number of native lyric glider branches connected to the existing
40 lip elements, and establish reversible Closed / Medium / Open switching at
word-driven cue times. Require source-ablation and complete 2-cell-halo
spacetime independence, not only an optically synchronized composite. Then
connect these links across all karaoke lines, render and only afterward add
the speech bubble.
