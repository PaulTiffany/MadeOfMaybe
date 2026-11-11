"""Tiny local native check, not CI: 6 adjacent words share one four-row stream.
Demonstrate that directly evolved B3/S23 agrees with the exact traveling
LWSS orbit. This is only a bounded spot check; the general noninterference
condition is geometric and verified by the compiler across all 10,366 ships.
"""
from compile_karaoke import compile_score,LWSS,evolve
words,ships,_=compile_score()
right=words[5]['rightmost_ship_g0']
part=[(x,y) for x,y in ships if x<=right]
assert len(part)==sum(w['glyph_ship_count'] for w in words[:6])
world={(x+dx,y+dy) for x,y in part for dx,dy in LWSS}
for g in range(65):
    if g%4==0:
        expected={(x-g//2+dx,y+dy) for x,y in part for dx,dy in LWSS}
        assert world==expected,('actual B3/S23 diverged',g,len(world),len(expected))
    if g<64:world=evolve(world)
print(f'NATIVE: first 6 consecutive words, {len(part)} ships, 65 generations, exact 4-phase B3/S23 flight PASS')
