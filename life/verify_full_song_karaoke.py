"""Check every unique word's native B3/S23 MAKE/HOLD/ERASE packet.

Certified prefix: three phase-indexed c/4 gliders are isolated at every
single generation before construction. The remaining generations evolve
under the ACTUAL sparse Life step, proving block and final destruction.
Spatially isolated copies then compose into the complete song (verified
conservative axis-aligned trajectory envelopes in full_song_karaoke.py).
"""
import argparse
import json
from pathlib import Path
from .lyric_cues import read_alignment
from .full_song_karaoke import (ALIGNMENT_FILE,compile_plan,
              verify_native_packet,stats,physical_targets, pixel_seed)


def check(raw:dict, count:int=0)->dict:
    lines=compile_plan(raw)
    pairs=sorted({(w.make_g,line.clear_g) for line in lines for w in line.words})
    if count>0:pairs=pairs[:count]
    results=[]
    for make,erase in pairs:
        result=verify_native_packet(make,erase)
        radius=erase//4+24
        seed=pixel_seed(make,erase)
        if any(abs(x)>radius or abs(y)>radius for x,y in seed):
            raise AssertionError('initial glider escaped declared static envelope')
        if result['near_collision_max_abs_coordinate']>radius:
            raise AssertionError('one glider reaction escaped declared static envelope')
        results.append(result)
    return {**stats(lines),'unique_word_reactions_verified':len(results),
            'every_selected_reaction_verified':len(pairs)==len(results),
            'max_reaction_near_collisions':max(r['near_collision_max_abs_coordinate'] for r in results),
            'not_a_step_by_step_global_45k_generation_simulation':True,
            'certificate':'Per-glider c/4 phase induction + exact B3/S23 reaction windows + spatial envelope noninteraction'}


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--alignment',type=Path,default=ALIGNMENT_FILE)
    ap.add_argument('--limit',type=int,default=0)
    ap.add_argument('--out',type=Path)
    args=ap.parse_args()
    result=check(read_alignment(args.alignment),args.limit)
    report=json.dumps(result,indent=2)+'\n'
    print(report,end='')
    if args.out:
        args.out.parent.mkdir(parents=True,exist_ok=True)
        args.out.write_text(report,encoding='utf-8')

if __name__=='__main__':main()
