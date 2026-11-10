# Suno isolated vocals → physically testable Life input lanes

## Data obtained in Suno

Original song **MADE OF MAYBE**, id
`53610991-7381-4749-96e1-79b8e3b1c28b`.

A user-authorized **two-stem** Suno split was created and is **complete**:
group `stemgrp_6a64aec3-a369-4d16-9ac8-af0afd068691`.
Both 238.88s vocal clips are in the owner's Suno library:

- Take 1 vocals: `bee52d16-b01b-4224-bd4c-5c51081d813b`.
- Take 2 vocals: `8375d878-79aa-4460-9b68-897281642ca2`.

Two instrumental counterparts were also created by Suno automatically.
Suno specifies this action consumes 10 credits total when both takes
complete. **Do not call the splitting operation a second time.**

The signed download URL from the Suno integration is available to the
account owner. This repository **does not embed, proxy, log or commit**
the time-limited signed download URL. The isolated audio bytes have
**not** been ingested into this local build environment, so no
production waveform onset/hold durations are claimed yet.

Run this offline once the authorized vocal stem MP3 is available:

```sh
python -m tools.compile_suno_vocal_controller \
  --vocals 'MADE OF MAYBE - Vocals.mp3' \
  --output output/made_of_maybe_dual_source_requests.json
```

The compiler decodes the actual isolated vocals to mono 16kHz PCM16
via ffmpeg, measures RMS in 20ms windows with a 90th-percentile-derived
threshold, merges short gaps and rejects very short pulses. This is
**vocal activity**, NOT phoneme recognition. It combines the measured
vocal envelope with the preexisting 403 exact Suno word cues at
192 native Life generations/audio-second, preserving a SHA256 of
the input and separate source IDs. Held notes can keep issuing
OPEN/MEDIUM request events after the word alignment ends.

## New physically qualified native Life logic

`life/dual_source_native_gate.py` establishes an elementary **real
B3/S23 two-input AND gate**, not a Python Boolean substitute.
Each source is a five-cell moving Life glider. If two independent
inputs arrive, their physical collision creates a four-cell
stable block at generation 124; if either glider is absent, there
is no block. Three separated readout sites demonstrate clocked W
(word), clocked V (voice), and actual W∧V simultaneously. All four
0/1 input combinations are simulated and verified in the same
physical-rule implementation; stable results persist beyond the
gate decision. Source ablation changes the actual native output.

## Explicit boundary of this sprint

The three output blocks are **physical indicators** only. They are not
yet physically wired to a repeatable priority gate and oscillator,
nor to the large singer's existing three lip stances.
The source signals for these indicators are independently preloaded:
native fanout/oscillator gating is NOT verified.
The real audio envelope is unavailable in the sandbox until its
download is supplied here; synthetic test tones are marked as fixtures.

To finish the user's specification, the following must be qualified
under one Life universe: actual W and V glider delivery, physical
priority arbitration, gated OPEN/MEDIUM repeated oscillation while
V remains active, real CLOSED reset when W=V=0, collisions with
rounded speech-bubble rim and existing LWSS redirectors, physical
connection to the three-stanced actual singer, and all 403 words.
None of these are replaced by renderer edits.
