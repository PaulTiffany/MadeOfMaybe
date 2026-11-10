# Recovered and qualified native first-20-second two-source music film

This sprint was interrupted after a 20-second video was generated but
before source/qualification was committed. Recovery inspected the local
native frame stream and found that the old 8,866-cell result and newer
8,926-cell preflight came from **different finite vocal cue schedules**.
The newest schedule has four physical mouth states; it includes an
intro MEDIUM-to-OPEN switch at g824 and closes near the end of the
measured first vocal episode (g1682 ~8.76s), avoiding the earlier
~1.2-second overhold. We re-evolved the 8,926-cell g0 world through
g3840, separately evolved five initial native components at **every
generation**, and verified their union equals the full-world state
throughout. No collisions or per-frame interventions.

The 130 static 2x2 Life tiles omitted from the generation-zero
portrait and rounded bubble are explicitly enumerated in
data/native_first20_removed_tiles.json: 80 portrait tiles and 50 rim
tiles were omitted for measured physical route clearance. This is
ordinary initial geometric staging. No still-life cells are erased
by the renderer or during playback.

Actual components in the **one** B3/S23 world:
1. Preserved static singer and native upper lip: **6,500 cells**.
2. Rounded stable Life bubble with real entry/exit clearance: **652**.
3. **35 unchanged original right-angle LWSS turners**, matching
   the real first word WE from above at g2156, including original
   debris eaters and seven shared text eaters: **1,519**.
4. Finite preloaded V-driven 4-pose glider synthesis/erase trains,
   using the first three independently measured Suno vocal episodes:
   **240**.
5. Independent lyric-W and vocal-V gliders physically colliding
   to make/erase a small mouth-accent block near g2156: **15**.

Native checkpoints: at g752 medium 4/4 physical lip blocks; g904
open 4/4; g1800 and g2000 closed; g2200 and g2400 open 4/4;
g3008 and g3840 medium 4/4. True 35-LWSS word WE (420 real Life
cells) is present at exact first lyric g2156=11.2292s and moves 12
cells left by g2180. All movie frames sample actual complete-world
snapshots every eighth generation: **481 frames, 24 fps, 20.0417s**.
Original recording is added afterward without visual compositing.
One globally continuous camera, no subtitle glyphs, fake jaw states,
HUD labels, borders, masks, camera hard cuts, or second universe.

**Causal limits**: The V triggers are precompiled from measured
isolated-Suno stem activity, retaining the known reverb observation
uncertainty. This is not an online or feedback driven audio detector.
The word accent's W lane uses the same first-word timestamp but is
NOT physically forked from the actual moving LWSS word stream.
The physically conditioned two-glider AND is genuine; the full
independent W+V priority controller and reusable oscillating jaw
remain unqualified. The rest of the 403 lyrics and 4-minute video
have not been built. The symbolics and zero-cell finale are deferred.

The source replay is intentionally deterministic from a documented
g0 layout. Its five-component comparison does not assert interactions
between the five components; their intentionally independent evolution
makes a valid one-world film, but it does not by itself establish that
all the source signals are wired into one causal gate graph.
