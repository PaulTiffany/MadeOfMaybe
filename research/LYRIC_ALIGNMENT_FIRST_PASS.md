# Lyric alignment → Life controllers: text FIRST

## Source and provenance

- Suno song ID: `53610991-7381-4749-96e1-79b8e3b1c28b` (*Made of Maybe*, 238.88 s).
- The connected Suno alignment is captured in `data/made_of_maybe_suno_alignment.json`: **468 raw tokens**. No model re-transcription or approximate manual time guesses.
- The raw alignment includes unusual sections embedded in words, fragments such as `don`, `'`, `t`, and **three zero-length tokens** (`on` at 76.384 s, `don` at 143.670 s and `don` at 203.430 s). Preserve this data; do not present it as perfect phonemic truth.
- `life/lyric_cues.py` cleans line/section text, rejoins fragments with token provenance, breaks lyrics into printable two-line Life-bubble pages, and converts timestamps to fixed 24 Life generations/sec. It reports and flags zero-duration source spans. The source-to-generation error is quantization at fixed clock; it is not audio alignment refinement.

## Time model

At **24 Life generations/s**, timestamps become `round_half_up(t*24)`; two-glider block synthesis works only at four-generation phase multiples, so `make_generation` rounds **the source timestamp directly** to the nearest multiple of four (avoid an extra rounding step). Typical onset grid error is ≤2 Life ticks (≤83.4 ms). The exact chosen glider-generation schedule must be checked before playback. **Do not change the global Life tick rate to match syllables.**

## Real B3/S23 pilot, first lyric line

The first lyric line is `WE MADE A WINDOW OUT OF SAND` (11.224–13.420 s). The narrow existing speech bubble requires two spatially independent pages:

- Page 1, stable still-life caption: `WE MADE` / `A WINDOW`
- Page 2, stable still-life caption: `OUT OF` / `SAND`

Seven **physically synthesized** 2×2 progress-lamp blocks appear at their corresponding Suno word onsets. The full seven-lamp schedule runs from generation zero under ordinary B3/S23 with **no runtime cell insertion**, then all seven erase by generation 326 (13.583 s). The second caption, its cue lamps and its gliders occupy a different region of the same universe. The existing hair, face, glider-driven mouth, eyebrows, iris and pulsar continue unchanged.

| Word | Source onset (s) | Glider MAKE generation | Quantized onset (s) |
|---|---:|---:|---:|
| WE | 11.224 | 268 | 11.167 |
| MADE | 11.479 | 276 | 11.500 |
| A | 11.824 | 284 | 11.833 |
| WINDOW | 11.964 | 288 | 12.000 |
| OUT | 12.593 | 304 | 12.667 |
| OF | 12.909 | 308 | 12.833 |
| SAND | 12.968 | 312 | 13.000 |

**Acceptance:** Every single glider packet synthesizes, holds and deletes its target. The **combined singer + both text pages + seven lamps** matches the superposition of independently evolved components for all 350 observed generations. Exported RLE round-trips exactly. These are testable contract claims, not assumptions based on visual appearance.

## Deliberate boundaries

**This is a word-cue pilot, not finished karaoke.** Both caption pages are real, stable Life text that exist from the beginning; the words themselves are **not yet physically constructed/erased at their cue times**. The *progress lamps* are actually driven by preloaded glider collisions. The example GIF changes which physical page the camera crops at 12.593 s; that is a preview camera cut, not a Life-cell transition, and not a license to swap mouth frames. The full 238.88 s performance has not been independently certified as one Life universe. Source alignment is word timing, **not phonemization**.

## Reproduce

```bash
python -m life.lyric_cues --alignment data/made_of_maybe_suno_alignment.json --out output/lyric_cues
python -m unittest tests.test_lyric_cues tests.test_lyric_text_pilot tests.test_lyric_text_scene -v
python -m life.export_first_line > patterns/seven_word_glider_timed_captions.rle
python preview/make_lyric_text_scene.py  # Pillow for image preview only
```

The first command writes `output/lyric_cues_words.csv` and `output/lyric_cues_pages.csv` for the whole song. These are a **scheduling specification**, not yet synthesized B3/S23 glider configurations. Golly can open the RLE file and evolve the seven physical lamps in the correct universe.

## Next gated tasks (text before mouth phonemization)

1. Independently qualify a **true dynamic lyric page**: glider-construct or glider-erase visible letter cells themselves, not just the seven progress lamps. Reuse the 5×7 Life still-life font and the GameOfLifeText two-glider synthesis technique. Routing is potentially hundreds of independently qualified glider lanes per caption; test rather than assume this is trivial.
2. Compile repeated line/page changes for the entire track, preserving existing phrase spacing. Prefer a small scheduled subset, then larger loops, rather than routing 468 tokens without checking an actual composite universe.
3. Map the mouth controller to *vocal activity and broad amplitude states* after the text pipeline is qualified. Suno word times do not constitute phonetic timings.
