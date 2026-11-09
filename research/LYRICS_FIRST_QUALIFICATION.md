# Made of Maybe — lyrics first, before phonemization

## Exact musical source

Connected Suno clip ID: `53610991-7381-4749-96e1-79b8e3b1c28b`, duration
238.88 seconds. `data/made_of_maybe_suno_alignment.json` contains all **468**
alignment tokens as returned by Suno, including `success`, original offsets,
`p_align`, punctuation, syllable fragments, section headers, and three tokens
with zero-duration spans. These anomalies are tracked, never secretly corrected.
We **do not** regard word alignment as phoneme timing or a vocal-dynamics map.

The Life clock is currently **24 B3/S23 generations per second**. The
scheduler distinguishes nearest-generation word onset from physically
permitted 2-glider block construction (at multiples of four generations).
A MAKE event can differ from Suno onset by about 83 milliseconds, even before
actual circuit flight clearance is considered. This is acceptable for the
first coarse word-cue test, not proof of exact lip synchronization.

## What is complete

- `life/lyric_cues.py`: deterministic, provenance-preserving token merge,
  word-event CSV, page-event CSV, JSON page manifest and SRT reference.
- `life/caption_library.py`: constructs each caption page (up to two lines,
  maximum eight characters per line) as **genuine stable Life blocks** within
  the unchanged bubble geometry. Every generated page is an independently
  valid Golly RLE asset; none is just video text.
- `life/lyric_text_pilot.py`: first-verse LIVE **four-word progress cue**:
  `WE` at generation 268 (11.167 s), `MADE` at 276 (11.500 s), `A` at 284
  (11.833 s), `WINDOW` at 288 (12.000 s). Native preloaded glider pairs
  create one actual still-life block per word, those blocks remain ON through
  generation 320, and four glider collisions erase them by generation 326.
  Suno onsets are respectively 11.224, 11.479, 11.824 and 11.964 seconds.
- The four physical progress blocks are currently **to the right of the
  bubble**, NOT over the lyrics. A corridor search for unmodified direct
  glider routes inside the unchanged bubble failed; rerouting via reflectors
  or qualifying channels through the bubble will be required to place markers
  beside each word. The static title words are present in the universe from
  generation zero. They do **not** appear/disappear with their timestamps.
- A second, prior experiment in `life/lyric_text_scene.py` composes **seven**
word lamps across two **separate** independent Life bubble pages for the
complete first line (WE MADE A WINDOW OUT OF SAND); an external camera can
choose which page to frame, but no Life text is swapped or injected.
This seven-lamp performance has an additional 350-generation composition test.
We fixed a real scheduler defect: double-rounding 12.909 seconds selected
generation **312**, giving a 91 ms timing error for OF. Direct rounding
to the four-generation MAKE phase chooses **308**, within 76 ms. The target
SAND is separately scheduled for generation 312.

The first four words' fixed Life text, physical progress blocks, singer,
  existing bubble, hair, eye/brow controls and pulsar all evolve on **one
  constant-clock universe**. A full exact B3/S23 replay for 350 generations
  compares the composite to its independently evolved major subsystems at
  EVERY generation, and checks all four activation/erasure states.

## Reproduction

Requires Python >=3.12. Sparse Life renderer and timing compiler use Python
standard library; install `numpy scipy Pillow` for the accelerated full-board
qualification and previews.

```sh
python -m unittest tests.test_lyric_cues tests.test_caption_library tests.test_lyric_text_pilot tests.test_lyric_text_scene -v
python -m life.lyric_cues --alignment data/made_of_maybe_suno_alignment.json --out output/lyric_cues/made_of_maybe
python -m life.caption_library --alignment data/made_of_maybe_suno_alignment.json --out output/lyric_cues/native_page_rles
python -m life.export_lyric_text_pilot > output/lyric_cues/first_lyric_glider_progress.rle
python -m life.export_first_line > output/lyric_cues/seven_word_glider_timed_captions.rle
python preview/make_lyric_text_pilot.py
python preview/make_caption_library_preview.py
```

The GitHub Action `Native Life lyric cue qualification` runs the full 468-token
build, full native page validation and the actual 350-generation independent
Life replay, then uploads its CSV/SRT/JSON/RLE and rendered preview files.
No web requests, audio credits or AI inference are needed at test time.

## Next engineering milestone, explicitly NOT accomplished here

Enable **physical lyric replacement inside the same visible bubble** from
prepositioned gliders: qualified per-letter synthesis/erasure and signal
routing, scheduled to each page without colliding with the unchanged face or
other components. We already have the text shapes, event score and reusable
MAKE/ERASE primitive; the remaining work is compositional routing at scale.

Do not solve this by inserting Life cells when subtitles change, overlaying
karaoke text and calling it native Life, swapping RLE worlds at runtime, or
changing the global Life generation rate. The SRT is a diagnostic reference,
not the animation mechanism. **No phonemization is undertaken here.**
