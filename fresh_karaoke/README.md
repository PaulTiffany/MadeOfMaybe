# Made of Maybe — START FRESH / one-line LWSS karaoke

This is an **independent implementation**, not the earlier WE/MADE singer pilot or lane-switching full-song video. It meets **Phase 1** of the new directive: the entire **403-word, 238.875-second** Suno song as **one continuous horizontal strip** of real westbound Conway lightweight spaceships.

### Watch

- `output/MadeOfMaybe_ONE_LINE_403_LWSS_FULL_SONG.mp4` — 960 × 540, 48 fps, original Suno audio.
- `output/MadeOfMaybe_ONE_LINE_403_LWSS_FULL_SONG_SMALL.mp4` — 640 × 360, 30 fps, original Suno audio, mobile-friendly.

### Physical construction

- 403 words, original order; 10,366 actual LWSS glyph pixels.
- 93,294 live cells **all preloaded at generation zero**.
- Exactly **four shared physical rows** at y = 0, 8, 16, 24. No separate lanes, page changes, caption stages, or word substitutions.
- Uniform native Conway B3/S23 LWSS velocity: (−2, 0) cells per 4 native generations.
- One clock: **1,920 native generations per audio second**. Full song runs for 458,640 native generations (238.875 seconds). The 48 fps video samples one frame every 40 generations.
- Each ship's four exact native B3/S23 phases were derived by actual Game of Life evolution. Ship neighborhoods are disjoint in **all four phases** across the entire score; therefore the union of independently translated native trajectories is mathematically the exact evolution of the one starting universe, with no runtime cell injection. An additional short direct evolution of six consecutive words matched the predicted world at native checkpoints.
- Camera is fixed. Only the original ship cells are plotted. There is no text overlay, no singer, no mouth, no bubble, no converter and no eater **yet**. Those are later phases.

### Timing limitation (measured)

A single westbound belt has a strict spatial packing constraint: two successive words cannot occupy the same location, even when the upstream Suno onset timestamps are nearly identical. The 3×4 glyphs are separated by 8 cells per pixel, and consecutive words have at least 24 cells between their last and first lit pixels. The compiler delays the next word **only where physical clearance requires it**.

The previous 403-word compiler had already phase-quantized the original 468-token Suno alignment at 192 native generations/s. For **386 of the 403 words** the new physical readhead arrival is identical to that established quantized onset. The other **17 words** are delayed by 2.08–100 ms; the worst is “I'M” (same source timestamp as the previous “NOW”). The *original quantization* also carries up to ~10.4 ms time resolution, separate from the reported packing delays. Exact per-word arrival/delay is in `output/all_403_words_physical_arrivals.json`.

No word is independently triggered by the renderer. Every arrival comes solely from initial x-coordinate and fixed LWSS velocity.

### Reproduce

```bash
python compile_karaoke.py --out output
python narrow_physical_probe.py
python render_karaoke.py \
  --original-audio /path/to/your/authorized_original_Made_of_Maybe.mp4 \
  --out output/MadeOfMaybe_ONE_LINE_403_LWSS_FULL_SONG.mp4
```

Requirements: Python 3.10+, NumPy, ffmpeg. Original recording is not bundled into the source ZIP; it is preserved in the delivered video files. `--silent` is supported if source music is not present.

### Next phase / not done

This is **karaoke only**. The next operation is to fit the previously qualified **real Conway eaters to these unchanged four tracks**. Then solve southbound converter ancestry backward from this accepted output, derive W word attacks from the physical stream, connect independent Suno V, finally attach the singer/three-state mouth and speech bubble. The working karaoke is the fixed reference and must not be redesigned to accommodate decoration.

No CI was created or run for this independent implementation.
