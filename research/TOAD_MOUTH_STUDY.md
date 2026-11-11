# A much simpler mouth shape: native Toad

The requested visual is an oval (open) that collapses into a horizontal
band (closed). The **Toad** is a real 6-cell, period-2 Conway Life oscillator
discovered by Simon Norton in 1970. Its two exact phases look like:

```
Band / closed        Oval / open (one generation later)

 .###                  ..#.
 ###.                  #..#
                       #..#
                       .#..
```

The face in `life/toad_mouth_study.py` contains *stable* block-built features
with one Toad in its mouth region. It does not interact with those features;
a test checks this for 100 consecutive generations. Visual previews come
from actual Life evolution and contain no mouth replacement or time edits.

**Crucial limitation:** a Toad oscillates every generation. This is not yet a
singer, because it cannot hold the open or closed phase until a control glider
arrives. Use the two phases as a **geometry target** for a glider-controlled,
holdable shape or investigate an interruptible oscillator. Do not slow the
simulation or swap rendered mouth frames.

The speech bubble and existing singer composition are *unchanged*.

Source: https://conwaylife.com/wiki/Toad
