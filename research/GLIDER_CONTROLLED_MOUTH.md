# First **operational** three-state glider-driven Life mouth

This is not a still-image pose comparison. The mouth actually changes as the
**same** Conway B3/S23 universe evolves, with every control glider supplied in
the initial RLE. The original speech bubble, block-letter title, and pulsar
remain present in that universe and stay independent of the new control
corridors for the entire qualified score.

## What runs

Three visually distinct HOLD conditions are represented by stable block-based
lips. The upper lip is a 18-block horizontal band. Four selected output blocks
form either a shallow lower lip (MEDIUM) or a deep lower lip (OPEN). In the
CLOSED state, both banks are empty; only the upper band remains.

| Generation | State | Notes |
| ---: | --- | --- |
| 60 | CLOSED | Stable before first actuation |
| 180 | MEDIUM | Four shallow lower-lip blocks present |
| 288 | OPEN | Medium bank erased; four deep-lip blocks present |
| 420 | MEDIUM | Deep bank erased; shallow lip rebuilt |
| 540 | CLOSED | Both lower-lip banks erased |
| 680 | OPEN | **Direct skip** from CLOSED to OPEN; medium is never built |
| 778 | CLOSED | Open bank erased; all control gliders consumed |

The output is a **native three-state Life animation**, including reversals and
a skip. It is a deliberately sparse first working mouth, *not* the previously
presented dense oval geometry and not yet final-quality character art.

The cells are genuinely stable during each hold, but the world continues to
contain other incoming gliders between events. The schedule's geometry
has been compiled for this exact 785-generation demo. We do not assert arbitrary
new MIDI/Suno timings will work with unchanged routing. Subsequent audio
compilation should reuse these verified reactions and reroute each new score,
then rerun the complete-world independence test.

## Mechanism

- **MAKE:** two carefully phased gliders collide to produce one 2×2 block
  exactly at their target, leaving no debris. The canonical collision comes
  from [GameOfLifeText](https://github.com/MartinSA04/GameOfLifeText),
  which itself uses native Life block synthesis.
- **ERASE:** a southeast glider on a selected line collides with a 2×2
  block and removes *both*, leaving nothing. We verified the exact reaction
  independently at different launch distances. Rotation and reflection
  preserve both reactions.
- **HOLD:** block is a B3/S23 still life. Absence is also stable.
- **TIMING:** a glider travels one diagonal cell per four generations. We
  algebraically backstep its starting coordinates to reach a target
  generation, then choose input angles and small timing offsets to avoid
  cross-signal reactions. All signals are part of the *initial* configuration.
- **COMPONENT INDEPENDENCE:** each actual generation of the combined world
  equals the union of the independent simulations of all components.
  This is verified for all **785 consecutive generations**, not sampled
  frames alone. Clearance checking includes births caused by cells two
  squares apart, not merely direct touching.

The fixed head portrait is a Life still-life block mosaic. A few head blocks
were omitted at initial-layout time where they would interfere with glider
lanes; this is **not** renderer masking, deletion, or video compositing.
Likewise the existing bubble and pulsar are translated outside the control
footprint; their underlying constructions are unchanged.

## Reproduce

Requires Python 3.10+ and no packages for exact simulation:

```shell
python -m unittest discover -s tests -v
python -m life.export_operational > patterns/operational_three_state_mouth.rle
```

Open the RLE in **Golly** to watch the real B3/S23 world. View the head in
its normal coordinates near (0,0) and advance to the generations in the table.
The existing bubble is translated to the right, outside all routed signals;
zoom out or pan right to locate it.

To generate preview GIF/PNGs (Pillow is the only additional dependency):

```shell
python -m pip install Pillow
python preview/make_operational_mouth.py
```

Check `preview/operational_mouth_three_states.png`,
`preview/operational_mouth_closeup.png`, and
`preview/operational_mouth_glider_control.gif`.
These previews display real Life cells. Captions/colors and camera crops
are presentational, not input into the simulation.

## Acceptance & next work

**Qualified:** one-world control, reversible three-state progression,
CLOSED→OPEN skip, full-scene noninteraction, compact RLE export.

**Not yet qualified:** arbitrary user-supplied cue compilation, audio sync,
rapid-fire changes, denser and more visually continuous lip outlines,
or an independently triggerable reusable gate/logic controller. This demo
is a *preloaded glider score*, not an interactive signal interface.

The first next artistic task is densifying the two controlled lower-lip arcs
while keeping the signal lanes independent. After that, compile the vocal
activity/Suno timestamps into a longer preloaded glider score and requalify
against the complete scene.
