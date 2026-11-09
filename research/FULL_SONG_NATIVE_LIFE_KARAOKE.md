# Made of Maybe — full-song glider-written lyrics

**Design:** encode the **complete song**, not just the first seven words, into
one genuine Conway's Game of Life B3/S23 starting universe. This is the
**karaoke layer only**: no singer or bubble, by request. They will be
integrated after the text is qualified.

## Inputs and outputs

- Original source: `data/made_of_maybe_suno_alignment.json` (468 Suno alignment tokens,
  with original token indices retained). The connected Suno song is
  `53610991-7381-4749-96e1-79b8e3b1c28b`, duration 238.88 s.
- `life/full_song_karaoke.py`: every sung line becomes an independent
  physical **text stage**, each word's 5×7 glyph pixels attached to its real
  Suno-aligned onset. Lines remain visible until their sung end.
- `life/export_full_song_karaoke.py`: outputs **ONE sparse RLE** containing
  *all* gliders from song generation zero, plus machine-readable score JSON.
  No runtime cells are inserted, moved, or swapped.
- `life/export_full_song_cues.py`: one SRT file covering the whole song,
  word cue CSV and camera/stage schedule CSV (a camera may move; Life cells
  must not be changed).
- `life/verify_full_song_karaoke.py`: independently validates every unique
  word's preloaded three-glider packet by proving glider c/4 phase flight
  is collision-free, simulating actual B3/S23 near the MAKE and ERASE events,
  and checking that the resulting block holds and is consumed.
- GitHub Actions publishes the completed RLE, score JSON, SRT, camera map,
  and verification report as an artifact.

## Fixed song/simulation clocks

One constant **192 B3/S23 generations per audio second**. The song is not
accelerated. A two-glider 2×2-block synthesis lands on a 4-generation phase;
clean deletion lands on a 2-mod-4 phase. Quantizing either endpoint thus
introduces at most approximately 10.42 ms error. Extremely short final
words may force a somewhat later **line clear** so a make/delete packet
has at least 42 generations of physical separation. We report those delays.

## Timing and spatial safety contract

At the start of the universe, each textual pixel contains precisely THREE
prepositioned GLIDERS (15 cells): two converge to write a Life block and the
third later removes it. Each word has its own make generation; all words on
one sung line share a clear generation. Existing blocks remain still lifes
until clearance. The actual Life **simulation** determines all state changes.

There are two separate, complementary checks:

1. **Native packet physics:** compare the four exact phases of each isolated
   glider against the c/4 translation identity. Before the reaction window,
   prove the three gliders remain Moore-neighborhood separated at every single
   generation. Simulate the remaining generations in the *real B3/S23 engine*.
   Assert block birth at the intended tick, subsequent hold, and no debris
   after deletion.
2. **Full-world composition:** each packet is given a deliberately conservative
   rectangular space-time envelope; neighboring pixel origins are separated
   by >2× this radius. Sung lines occupy separate stages with vertical
   envelopes also separated. This implies the Life evolution of the union
   equals the union of separately evolving packets, by local rule locality.

This is a compositional argument, NOT a full 45,000-generation step-by-step
simulation of every cell of the whole song. Primitive trajectories are
actually checked; isolation is qualified for the entire schedule by explicit
geometry. Every added singer/bubble component must satisfy the same checks.

## Deliberate limitations

- **Enormous sparse coordinates:** a robust feasibility proof is more useful
  than compact glider engineering at this stage. Later we can optimize space
  or use delay lines and better routing. Never use a dense array for this RLE.
- **Camera projection needed:** each 2×2 live block sits on a giant physical
  lattice to keep its glider trails independent. A display should convert
  target coordinates to logical glyph pixels by sampling **real 2×2 Life
  blocks**; the scene RLE remains the full initial universe. Simply zooming
  Golly out to fit the full stage makes individual cells invisible.
- **Unfinished video:** this exports a world and a matching event score, not
  a 24fps final muxed music video or hardware-accelerated full-length renderer.
  The timed camera/SRT are reference instruments, not image substitution.
- **Alignment defects:** the Suno data has three zero-duration raw tokens.
  They are retained and flagged when merged rather than silently corrected.
- **No mouth phonemization yet.** The singer, face, and bubble are intentionally
  excluded as requested.

## Reproduce locally or through GitHub Actions

```sh
python -m unittest tests.test_full_song_karaoke -v
python -m life.verify_full_song_karaoke --out output/full_song_physics.json
python -m life.export_full_song_karaoke \
  --out patterns/made_of_maybe_full_song_native_life.rle \
  --score output/made_of_maybe_full_karaoke_score.json
python -m life.export_full_song_cues --out output/full_song_native_life
```

Run these from the repository root with Python ≥3.10. All commands except
video previewing need no third-party Python dependencies.
