# One-world Conway film: strict no-cheat production contract

The user rejected the editorial full-song v1 because it contains
hard cuts, camera-designed borders, labels, synthetic word highlighting,
and renderer-selected lip poses. This was a **valid correction**.
The full-length editorial v1 may be retained as a staging reference but
**must never be described as the finished Conway music video**.

The new short film is **19.04 seconds** at **24fps** and original
**192 native B3/S23 generations per audio second**. Its first 11 seconds
show one continuous glider→apparatus→singer camera movement; from 11s
onward the camera is fixed. There are no frames from a second universe,
no scene cuts, no hand-painted borders, no titles/HUD, and no subtitles
or word/pose changes added by a video renderer. All actual Life cells
are produced from **one 9,046-cell generation-zero universe** by running
the WHOLE B3/S23 world from g0 through g3648, saving every eighth
complete state. The artist may tint real occupied cells by fixed world
coordinates, but this visual tint is not a claimed Life color switch.
The original Suno audio may be muxed afterward WITHOUT modifying the
native visual frames. Audio is not stored in this repository.

**Actual native world used:** the already qualified
`life.relocated_singer_anchor.universe()`, containing our singer,
real original two-word glider controller, and native speech bubble.
This earlier face still has **independently choreographed** lip circuits;
it is not the complete later phrase-gated singer. The small lyric
device makes/erases an actual one-pixel WE cue at g2156/2578 and
g2976/3402; it is NOT the 403-word moving text mechanism. No symbolics
or all-zero finale are included.

For the full 238.88s film to satisfy this contract, require:
1. **One generation-zero Life pattern** containing singer, integrated
   moving lyric streams for every original word and necessary routing,
   all actual gates, and any staging decorations that are physically alive.
2. **Full B3/S23 evolution** or a mathematically justified
   decomposition with collision-free proofs spanning the film.
3. One **continuous global affine camera** over that entire same universe.
4. Lip motions, lyric colors, phrase changes and symbolic animations must
   arise from native B3/S23 states. A renderer may color states/lanes,
   but never substitute actors or glyphs, translate letters independently,
   or add scripted visual states.
5. Real audio muxed without retiming the Life clock; no hard edits.
6. User-requested future nuke must end with genuinely zero live Life
   cells (not a fade-to-black).

The existing 35-turner WE and 107-turner WE MADE devices are qualified
as **separate patterns**, not yet merged into the singer or the entire
403-word song. Therefore we must not label the 19-second native opener
a finished full-song karaoke. No arbitrarily prolonged mouth poses should
be imposed to conceal missing held-note physiology.

**Build native silent reference:**

```sh
python - <<'PY'
from pathlib import Path
from life.relocated_singer_anchor import universe
cells=universe()
assert len(cells)==9046
Path('output/native').mkdir(parents=True,exist_ok=True)
with open('output/native/seed.tsv','w') as f:
 for x,y in sorted(cells):f.write(f'{x} {y}\n')
PY
g++ -O3 -std=c++17 research/one_world_native_frames.cpp -o /tmp/nativefilm
/tmp/nativefilm output/native/seed.tsv output/native/world_frames.bin 3648 8
python preview/render_one_world_native_no_cuts.py \
 --frames output/native/world_frames.bin \
 --out output/native/one_world_opening_silent.mp4
```

Physically co-located full-song engineering is an independent follow-on,
not something an optical renderer can certify.
