# Stylish oval face and readable caption font — qualification

**Status:** a **working B3/S23 portrait** added to the existing glider-controlled singer, not a finished video or music-synchronized performance. See `preview/styled_singer_four_states.png`, `preview/styled_singer_native_life.gif`, and `patterns/styled_singer_glider_world.rle`.

## User-directed design changes

1. **Oval rather than Pac-Man circle:** the head now has narrower temples, a longer face and a tapering jaw/chin. The static contour is >1.2 times as tall as it is wide in actual Life coordinates, *not a camera trick*. The side/ear region is not exaggerated into giant semicircles.
2. **Eyes and brows:** independent native Life still-life strokes form two almond eyes with a winged outer end, arched (slightly asymmetrical) brows and irises. The little period-two eye glints are placed *inside* the eyes, rather than floating below them.
3. **Nose and cheekbones:** a thin bridge, understated tip, cheekbone contours and a small beauty mark. These details are intentionally stylized because the original glider corridors still cross part of the middle of the face.
4. **Hair framing:** a side-swept fringe and crown rather than a featureless circle.
5. **Caption:** upgraded the previous 3x5 title-card bitmap to a complete 5x7 uppercase-and-digits block font for the static speech bubble. New `bubble_lyric_cells(lines)` accepts arbitrary short text; sample phrases `MADE OF/MAYBE`, `I SEE/YOU` and `NOW/NOW` form valid independent still lifes. This is **not** dynamic karaoke or preloaded glider-written lettering yet.

## Uninterrupted native Life requirements

The active lip actuators, their incoming gliders, and the middle lip erase/reconstruct sequence are reused unchanged. The artistic changes are stable 2x2 Life blocks on a four-cell-or-greater pitch. The motion of both glints is a true Life blinker (period two). There are no video overlays that manufacture facial geometry: only cosmetic cell colors and a faint optical bloom. The camera does not change Life's geometry.

The added art is placed only after enumerating the dynamic signal trajectories for **980 generations**. A two-cell neighborhood excludes decoration near every passing signal, including both glints. `test_styled_singer` then checks the **entire actual universe** against the union of every independently evolved component on every generation, including static bubble and real-letter cells. The spatial exclusion algorithm by itself is never treated as proof.

## Verified states and limits

| Generation | Actual lip pose |
| ---: | --- |
| 60 | CLOSED (five-block resting line exists) |
| 180 | MEDIUM |
| 288 | OPEN |
| 420 | MEDIUM |
| 540 | BREATH / neutral, **not** the resting closed line |
| 680 | OPEN (direct skip) |
| 778 | BREATH / neutral |
| 960 | CLOSED (line reconstructed) |

**Not yet done:** fully reversible middle CLOSE between consecutive vowels, selective eyeliner/blink control, glider-controlled changeable text, Suno lyric cue-to-generation mapping, direct audio/video integration. The new font's two captions are different **alternative initial states**, not live-switchable states of the same running universe.

Run:

```shell
python -m unittest tests.test_styled_singer tests.test_lyric_font -v
python -m unittest discover -s tests -v
python preview/make_styled_singer.py
```

The resulting `.rle` is the **complete** generation-zero world with all control gliders preloaded. Open it in Golly. Any change to the portrait or route is subject to the full 980-generation test again.
