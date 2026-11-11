"""Export initial B3/S23 board for glider-written WE at a faster audio clock.

Only the physical lyric word is exported; the bubble is deliberately omitted.
The singer is not included until its control gliders are separately rescored.

    python -m life.export_clocked_text --gps 192 --pitch 160 > highspeed_we.rle
"""
import argparse
import json
from pathlib import Path
from .lyric_clock import plan_we,physical_initial
from .export_operational import compact_rle


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--gps',type=int,default=192)
    parser.add_argument('--pitch',type=int,default=160)
    parser.add_argument('--line-clear',type=float,default=13.42)
    parser.add_argument('--manifest',type=Path)
    args=parser.parse_args()
    p=plan_we(args.gps,line_clear_s=args.line_clear)
    if args.manifest:
        args.manifest.parent.mkdir(parents=True,exist_ok=True)
        args.manifest.write_text(json.dumps({**p.as_dict(),'physical_pitch':args.pitch,
         'note':'This plan is physically qualified only at rate/pitch combinations in test_lyric_clock.py',
         'bubble':'omitted','singer':'requires independent glider rescore'},indent=2)+'\n')
    print(compact_rle(physical_initial(p,args.pitch),(
        f'MadeOfMaybe REAL glider-written WE at {args.gps} Life gens per audio second',
        f'Physical target pitch {args.pitch}; build by g{p.make_at} ({p.make_at/p.gps:.3f}s)',
        f'Word holds to line clear by g{p.erase_by} ({p.erase_by/p.gps:.3f}s)',
        'All 105 input gliders present at generation zero; no cell injections',
        'Isolated lyric stage: no speech bubble and no singer (not retimed yet).',
    )),end='')

if __name__=='__main__':main()
