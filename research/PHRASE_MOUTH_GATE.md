# Simplest mouth control: a phrase-gated three-pose cycle

Do not independently program lip motions for 403 words. Use one reusable
physical mouth mechanism with three states:

1. Karaoke first word MAKE starts singing in **MEDIUM**.
2. During a sung phrase, successive eligible native word MAKE events
   alternate **MEDIUM ↔ OPEN**. Faster words hold the current state.
3. Karaoke line CLEAR closes to **CLOSED** on genuine breaks. When the next
   line starts too soon (or overlaps the previous), treat them as *one*
   continuously sung phrase: no fake short closed-mouth interval.

One Life rate = **192 generations per second**, derived from the existing
Suno karaoke. No phonemization, runtime cell edits, second motor clock,
or new timestamps. The 96-generation minimum (.5s) is a conservative
state-selection requirement and must **not** be confused with the stronger
whole-universe collision/clearance qualification.

The full score selects **35 phrases**, **35 starts**, **148 sparsely selected
medium/open alternations**, and **35 closes** = **218 state requests**,
rather than 403 bespoke lip cycles. The **minimal external phrase-gate interface is exactly 70 source events**
(35 start / 35 stop). The optional 148 intermediate word-onset requests
are only for a word-driven cycle if a self-repeating actuator is not used. A future autonomous, *physically gated* repeat
mechanism could reduce the number of external alternate triggers still further,
but that is not implemented or being claimed.

Example for the first sung line: g2156 MEDIUM (WE), g2272 OPEN (A),
g2416 MEDIUM (OUT), g2578 CLOSED (line clear). Second line follows:
g2976 MEDIUM, g3084 OPEN, g3208 MEDIUM, g3402 CLOSED.

`life.phrase_mouth_gate` is a **source-linked intent compiler only**.
It does not act on the existing singer's Life cells. The relocated 84-cell
splitter is still NOT connected to the complete narrow/lower lip bank; physical
gate wiring, counterfactual source ablation, spatial clearance and signal
reset remain necessary before claiming a finished native-Life performance.

Reproduce: `python -m unittest tests.test_phrase_mouth_gate -v` and
`python -m life.export_phrase_mouth_gate`.
