"""Research tool: greedy high-clearance router for glider-written lyric words.

Run from repo root: python research/route_native_word.py --word WE --on 268
  --first 200 --erase 442 --erase-floor 326 --pitch 20
  --output /tmp/we_routes.json

Uses only genuine block synthesis/erasure, strong per-generation Moore-2
separation, and deterministic search order. It may FAIL on denser layouts.
The source file under data/ is the vetted output; CI validates it by
actually running B3/S23, not by trusting this router's prediction.

To reproduce the WE layout in minutes or explore other fonts use --seed and
--pitch. The erase-stage search checkpoints itself after each block so
crashed or manually interrupted runs can resume. The algorithm is greedy;
there is NO completeness or optimality guarantee.
"""
from __future__ import annotations
import argparse
from functools import lru_cache
import json
from pathlib import Path
import random
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from life.core import evolve
from life.glider_controlled_mouth import BLOCK,block_make_at,block_erase_at,rotate
from life.lyric_font import GLYPHS


def target_origins(word:str,pitch:int):
    return [((i*6+x)*pitch,y*pitch)
            for i,ch in enumerate(word)
            for y,row in enumerate(GLYPHS[ch])
            for x,bit in enumerate(row) if bit=='1']


def shadow_update(world,states,x,y):
    for gen,cells in enumerate(states):
        world[gen].update((i+x+dx,j+y+dy) for i,j in cells
                          for dx in (-2,-1,0,1,2)
                          for dy in (-2,-1,0,1,2))


def fits(world,states,x,y):
    return all(not any((i+x,j+y) in world[g] for i,j in cells)
               for g,cells in enumerate(states))


def trace(seed,end):
    out=[];cells=seed
    for g in range(end+1):
        out.append(cells)
        if g<end:cells=evolve(cells)
    return out


def plan(word:str,on:int,first:int,erase:int,erase_floor:int,pitch:int,seed:int,output:Path):
    if not word or any(ch not in GLYPHS for ch in word.upper()):
        raise ValueError('Use only letters in the existing 5x7 Life font')
    if on%4 or first%4 or erase%4!=2 or erase_floor%4!=2:
        raise ValueError('make ticks must be 0 mod4; erase ticks must be 2 mod4')
    if first<4 or on<first or erase<=on+22 or erase_floor<=on+22 or erase_floor>erase:
        raise ValueError('Invalid generation range')
    if pitch<8:raise ValueError('Pixel pitch below eight not qualified for router')
    duration=erase+38
    word=word.upper()
    rng=random.Random(seed)
    targets=target_origins(word,pitch)
    rng.shuffle(targets)
    @lru_cache(maxsize=256)
    def make_trace(t,d):
        p=trace(rotate(block_make_at(t),d),duration)
        if p[t]!=BLOCK:raise RuntimeError('Unverified make reaction')
        return p
    @lru_cache(maxsize=256)
    def combo_trace(t,d,off,erase_d):
        live=rotate(block_make_at(t),d)|rotate(block_erase_at(off),erase_d)
        p=trace(live,duration)
        if not BLOCK<=p[t] or p[off]:return None
        return p
    make_world=[set() for _ in range(duration+1)]
    makes=[]
    for i,(x,y) in enumerate(targets):
        options=[(t,d) for t in range(on,first-1,-4) for d in range(8)]
        options.sort(key=lambda a:(-a[0],rng.random()))
        for t,d in options:
            q=make_trace(t,d)
            if fits(make_world,q,x,y):
                shadow_update(make_world,q,x,y)
                makes.append([x,y,t,d,None,None]);break
        else:
            raise RuntimeError(f'MAKE routing failed at pixel {i+1}/{len(targets)}; try larger pitch or seed')
    # Persist after each erase circuit so a long greedy search is recoverable.
    if output.exists():
        loaded=json.loads(output.read_text())
        if len(loaded)==len(makes) and [p[:4] for p in loaded]==[p[:4] for p in makes]:
            makes=loaded
        else:
            raise RuntimeError('Existing checkpoint does not match generated make routes; choose a new output file')
    for i,(x,y,t,d,off0,erase_d0) in enumerate(makes):
        if off0 is not None:continue
        world=[set() for _ in range(duration+1)]
        for j,(xx,yy,tt,dd,off,ed) in enumerate(makes):
            if i==j:continue
            q=make_trace(tt,dd) if off is None else combo_trace(tt,dd,off,ed)
            shadow_update(world,q,xx,yy)
        for off in range(erase,erase_floor-1,-4):
            found=False
            for ed in range(8):
                q=combo_trace(t,d,off,ed)
                if q is not None and fits(world,q,x,y):
                    makes[i]=[x,y,t,d,off,ed]
                    output.parent.mkdir(parents=True,exist_ok=True)
                    output.write_text(json.dumps(makes,indent=2)+'\n')
                    print(f'Routed pixel {i+1}/{len(makes)}',flush=True)
                    found=True
                    break
            if found:break
        else:
            raise RuntimeError(f'ERASE routing failed at pixel {i+1}/{len(targets)}; try larger pitch, later erase, or new seed')
    return makes

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--word',default='WE')
    p.add_argument('--on',type=int,default=268)
    p.add_argument('--first',type=int,default=200)
    p.add_argument('--erase',type=int,default=442)
    p.add_argument('--erase-floor',type=int,default=326)
    p.add_argument('--pitch',type=int,default=20)
    p.add_argument('--seed',type=int,default=0)
    p.add_argument('--output',type=Path,default=Path('/tmp/we_glider_routes.json'))
    args=p.parse_args()
    result=plan(args.word,args.on,args.first,args.erase,args.erase_floor,args.pitch,args.seed,args.output)
    print(f'Completed {len(result)} independently routed glyph pixels in {args.output}')
