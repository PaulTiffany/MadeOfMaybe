# V-01: vocal isolation includes spatially diffuse release energy

**Status: observed and quantified from the actual user-uploaded Suno
vocal take 1 on 2026-11-10.** This is a qualification about the
**measurement operator**, not evidence of perfect dry/wet source
separation, and not a new programmable mouth drive.

## Provenance

- Original song: `53610991-7381-4749-96e1-79b8e3b1c28b`
- Actual uploaded isolated vocals: `bee52d16-b01b-4224-bd4c-5c51081d813b`.
  MP3 embedded Suno clip ID verified.
- Stem SHA-256: `1df830717e8d17f8fede34136d5188f87750bc3d8dd08f503f7c204b8951e011`
- Original mix SHA-256: `4b4ff4887bd85dbf9e95dd5febc04aa1d725b5fb8d2557ef4224bd02e7442f5f`
- Source music nominal: 238.88s; MP3 container 238.92s; decoded
  sample stream approx 238.894s. Do not silently equate these values.
- Actual measured machine-readable gate: `data/made_of_maybe_vocal_gate_take1_v0.json`.
  **The MP3 itself is not committed.**

## Stereo evidence for a wet vocal tail

Measured 20ms stereo RMS windows, using M=(L+R)/2 and S=(L−R)/2:

| Location | Direct-like phrase | Subsequent diffuse release |
|---|---|---|
| 13 seconds | 12.90–13.40: −23.54 dBFS, S/M 0.008 | 13.85–14.35: −64.89 dBFS, S/M 1.017 |
| 26 seconds | 26.00–26.40: −24.78 dBFS, S/M 0.028 | 26.65–27.40: −52.43 dBFS, S/M 1.574 |
| 233 seconds | 232.70–233.30: −20.49 dBFS, S/M 0.092 | 233.75–234.50: −46.64 dBFS, S/M 1.362 |

The lower-level release becomes much more spatially diffuse. This is
consistent with reverb, echo or doubled/processed vocals **but it does
NOT uniquely identify reverb**. Nor does the energy floor reveal the
actual time phonation ceased. Do not interpret every audible sample
of the isolated stem as continued singing.

A conservative screening heuristic identified **nine** reverb-like
diffuse release intervals totaling **7.66s**. All nine are
**already excluded** by the present **mono** RMS voice-activity gate
at 0.14×P90 threshold. This demonstrates that aggressive destructive
de-reverberation is **not necessary** to exclude these obvious tails
from the current jaw candidate score. Other embedded effects and
quiet genuine phonation remain unresolved.

## Qualification of the observer's choice

The same stem with the same lyrics produces the following when the
mono vocal detector's relative RMS threshold is varied:

| Relative threshold | Vocal episodes | Active seconds | Voice-on / no aligned word | Mouth requests |
|---:|---:|---:|---:|---:|
| 0.08 | 23 | 219.56 | 99.12 s | 335 |
| 0.10 | 31 | 216.64 | 96.60 s | 334 |
| **0.14** | **53** | **211.76** | **93.04 s** | **332** |
| 0.18 | 65 | 207.66 | 90.12 s | 331 |
| 0.22 | 79 | 205.04 | 88.69 s | 330 |
| 0.30 | 98 | 198.84 | 85.08 s | 327 |

A **20.72s** change in detected activity is an observation-policy
effect, not a change in the recorded song. The 93.04s apparent
voice-only activity includes nonlexical vocals, word alignment
gaps, held notes, processing and detector error; it is **not
93s of certified held notes**.

### Mix clock vs isolated-vocal stem clock

First-difference FFT cross-correlation of original mix vs isolated
stem, at 16kHz mono, ±300ms search, peaks at **exactly 0 samples lag**
in the tested windows 11–14, 28–30, 58–62, 198–202 and 230–234s
(normalized coefficients 0.510, 0.416, 0.701, 0.400, 0.259).
This is positive spot-check evidence that the original 192g/s
Life-song clock need not be shifted for this Suno stem. It does not
certify every word boundary or a whole-song sample-perfect offset.

## Engineering implication

Use **W** for original aligned word attacks and **V** for a qualified,
threshold-sensitive vocal-activity candidate. Record a separate
**uncertain wet-tail** observation class for QA, not a new causal
drive; never let mere wet energy keep the mouth articulating. The
current B3/S23 two-input glider/three-pose mouth PILOT can be
fed such a score only **after** all source gates, repeated oscillator,
physical routing, actual singer connection and collision clearance
are independently qualified.

No optical mouth overrides, invented phonemes, cell injection or
renderer trick is licensed by this finding. The machine-readable
manifest explicitly marks `native_B3S23_full_song_mouth_qualified=false`.
